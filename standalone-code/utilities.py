import os
from getpass import getpass
import urllib
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
from PIL import Image
import cv2
import numpy as np
import validators
import base64
from io import BytesIO
from getpass import getpass
import cv2
from skimage.color import rgb2lab, lab2rgb
from skimage import color
import binascii
import struct
import scipy
import scipy.misc
import scipy.cluster
from warnings import simplefilter
import ast


def download(dest_folder: str):
  '''
  This function takes the images from the URL and saves them
  The file saved uses the filename from the URL because files have
  different extensions. The exception is ULTA urls, because they
  did not provide a file name so I created a file name.
  I save the name of the image in a column in the original table
  for linking image and data of the product. If an URL was broken,
  I save that error code in the table to identify products with a broken
  URL.
  '''

  # create folder if it does not exist
  #if not os.path.exists(dest_folder):
   #     os.makedirs(dest_folder)

  df['img_name'] = '0'

  for i in range(len(df)):
    url = df.loc[i, 'img_url']
    # request
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    r = requests.get(url, headers = headers)

    # Ulta has no name attached
    source =  url.split('//')[1].split('/')[0].split('.')[1]

    if r.ok:

      if source != 'ulta':
        # create file name and extension
        file_name = url.split('/')[-1].split('.')[0]
        file_type = url.split('/')[-1].split('.')[-1][0:3]
        # where the file will be saved
        file_path = dest_folder + '/' + file_name + '.' + file_type
        # save file name to row
        df.loc[i, 'img_name'] = file_name + '.' + file_type
        # save image
        print("saving to", file_path)
        open(file_path, 'wb').write(r.content)

      elif source == 'ulta':
        # create file name and extension
        file_name = 'ulta' + str(i)
        file_type = 'jpg'
        # where the file will be saved
        file_path = dest_folder + '/' + file_name + '.' + file_type
        # save file name to row
        df.loc[i, 'img_name'] = file_name + '.' + file_type
        # save image
        print("saving to", file_path)
        open(file_path, 'wb').write(r.content)

    else:  # HTTP status code 4XX/5XX
      print("Download failed: status code {}\n{}".format(r.status_code, r.text))
      df.loc[i, 'img_name'] = r.status_code


def check_img(filename):
    '''
    This function checks if a file is an image or not, and if it is corrupted
    '''
    try:
        im = Image.open(filename)
        im.verify()
        im.close()
        im = Image.open(filename)
        im.transpose(Image.FLIP_LEFT_RIGHT)
        im.close()
        return True
    except:
        print(filename,'corrupted')
        return False


def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

def resize_image(image_path, max_size=(150, 150)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)

        # Convert for png
        if img.mode != "RGB":
          img = img.convert("RGB")

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return buffered.getvalue()
    
def apply_claude(image_path, key, prompt_round):
    # wait
    time.sleep(12)
    # Resize and encode the image
    resized_image = resize_image(image_path)
    base64_image = encode_image(resized_image)



    # Your API key and the API endpoint
    api_key = key
    api_url = "https://api.anthropic.com/v1/messages"

    # Headers for the API request
    headers = {
      "Content-Type": "application/json",
      "X-API-Key": api_key,
      "anthropic-version": "2023-06-01"  # Add this line
      }

    # Prompt
    prompt = prompt_round

    # Data for the API request
    data = {
      "model": "claude-3-opus-20240229",
      "max_tokens": 1000,
      "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": base64_image
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
          }
        ]
      }
    # Sending the request to the API
    response = requests.post(api_url, json=data, headers=headers)

    # Return response, list
    return response.json()

def prompt_product(category):
  if category == 'lipstick':
    return 'Your task is to identify the CIELAB color (or the closest approximation) of the lipstick in the image. Lipsticks are in a container, but focus solely on the color of the lipstick itself. Respond only with the CIELAB color in a Python list format. For CIELAB color, L is between 0 and 100, a and b are between -128 and 128.'
  if category == 'lipliner':
    return 'Your task is to identify the CIELAB color (or the closest approximation) of the pencil in the image. I need the color of the pencil which will be in the tip of the pencil. Respond only with the CIELAB color in a Python list format. For CIELAB color, L is between 0 and 100, a and b are between -128 and 128.'
  if category == 'blush':
    return 'Your task is to identify the CIELAB color (or the closest approximation) of the blush or foundation in the image. Makeup sometimes comes in containers, but focus solely on the color of the makeup itself. Respond only with the CIELAB color in a Python list format. For CIELAB color, L is between 0 and 100, a and b are between -128 and 128.'
  if category == 'lipgloss':
    return 'Your task is to identify the CIELAB color (or the closest approximation) of the lipgloss in the image. I need the color of the lipgloss, not the container. Respond only with the CIELAB color in a Python list format. For CIELAB color, L is between 0 and 100, a and b are between -128 and 128.'


def analyze_image_colors(image_path, num_clusters=4):
    """
    Analyzes the colors in an image using k-means clustering and converts the dominant color
    to CIELAB color space.

    Parameters:
    - image_path (str): Path to the image file.
    - num_clusters (int): Number of clusters for k-means.

    Returns:
    - tuple: Average color and most frequent color in CIELAB color space.
    """

    # Read the image
    im = Image.open(image_path)

    # Optionally resize the image to reduce processing time
    im = im.resize((150, 150))

    # Convert the image to a numpy array
    ar = np.asarray(im)

    # Variance in color values
    sd_color = np.sqrt(np.var(ar))

    # Store the shape of the array
    shape = ar.shape

    # Check the number of channels in the image
    if len(shape) == 2:
    # No need to convert to RGB; use grayscale values directly
      num_channels = 1
    elif len(shape) == 3 and shape[2] in [3, 4]:
      # RGB or RGBA image
      if shape[2] == 4:
      # Remove the alpha channel
        ar = ar[:, :, :3]
      num_channels = 3
    else:
      raise ValueError("Unsupported image format")

    shape = ar.shape

    # Reshape the array for clustering
    ar = ar.reshape(np.prod(shape[:2]), num_channels).astype(float)

    # Perform k-means clustering to find color clusters
    codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)

    # Assign each pixel to a cluster and count occurrences
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = np.histogram(vecs, len(codes))

    # Find the index of the most frequent cluster
    index_max = np.argmax(counts)
    peak = codes[index_max]

    # Convert the average color from RGB or grayscale to CIELAB
    if num_channels == 1:
      peak_rgb = np.array([peak[0], 0, 0]) / 255
      peak_xyz = color.rgb2xyz(peak_rgb)  # Convert to XYZ
      peak_lab = color.xyz2lab(peak_xyz)  # Convert to CIELAB

      # Calculate difference between peak & white
      diff_peak_white = deltaE_ciede2000(peak_lab, [100,0,0])

      # Calculate difference between peak & black
      diff_peak_black = deltaE_ciede2000(peak_lab, [0,0,0])

      # Filter out clusters with black or white if Delta E < 5
      if diff_peak_white < 5:
        codes = np.delete(codes, index_max, axis=0)
      if diff_peak_black < 5:
        codes = np.delete(codes, index_max, axis=0)

      # Average over the color of the clusters after dropping peak
      columns_average = codes.mean(axis=0)
      mean_rgb = np.array([columns_average[0], 0, 0]) / 255 # Normalize RGB values to [0, 1]
      mean_xyz = color.rgb2xyz(mean_rgb)  # Convert to XYZ
      mean_lab = color.xyz2lab(mean_xyz)  # Convert to CIELAB

    else:
      peak_rgb = np.array(peak).reshape(1, 1, num_channels) / 255  # Normalize RGB values to [0, 1]
      peak_xyz = color.rgb2xyz(peak_rgb)  # Convert to XYZ
      peak_lab = color.xyz2lab(peak_xyz)  # Convert to CIELAB

      # Calculate difference between peak & white
      diff_peak_white = deltaE_ciede2000(peak_lab[0][0], [100,0,0])

      # Calculate difference between peak & black
      diff_peak_black = deltaE_ciede2000(peak_lab[0][0], [0,0,0])

      # Filter out clusters with black or white if Delta E < 5
      if diff_peak_white < 5:
        codes = np.delete(codes, index_max, axis=0)
      if diff_peak_black < 5:
        codes = np.delete(codes, index_max, axis=0)

      # Average over the color of the clusters after dropping peak
      columns_average = codes.mean(axis=0)
      mean_rgb = np.array(columns_average).reshape(1, 1, num_channels) / 255  # Normalize RGB values to [0, 1]
      mean_xyz = color.rgb2xyz(mean_rgb)  # Convert to XYZ
      mean_lab = color.xyz2lab(mean_xyz)  # Convert to CIELAB

    if num_channels == 1:
      return mean_lab, peak_lab
    else:
      return mean_lab[0][0], peak_lab[0][0]
    
def generate_color_square(hex_color, size=100, output_path=None):
    # Create an image with the given color
    img = Image.new('RGB', (size, size), hex_color)

    # Save the image
    if output_path:
        img.save(output_path)
    return img

def is_list(cell):
    try:
        ast.literal_eval(cell)
    except (SyntaxError, ValueError):
        return False
    return isinstance(ast.literal_eval(cell), list)