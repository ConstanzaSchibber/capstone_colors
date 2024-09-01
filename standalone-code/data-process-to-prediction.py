import utilities

# read metatadata
df = pd.read_csv(...) 

# validate url in metadata (img_url)

df['validation'] = '0'

for i in range(len(df)):
  url = df.loc[i, 'img_url']
  df.loc[i, 'validation'] = validators.url(url)

# download images and save in destination folder
download(df['img_url'], '/content/drive/My Drive/makeup_img')

# LLM 
key = ['YOUR_API_KEY'] #from Antropic
api_url = "https://api.anthropic.com/v1/messages"

# Headers for the API request
headers = {
    "Content-Type": "application/json",
    "X-API-Key": api_key,
    "anthropic-version": "2023-06-01"  # Add this line

}

# to store results

df['Claude_message'] = pd.Series(dtype='object')

# make API calls for all images

for i in range(len(df)):
    path = '/content/drive/MyDrive/makeup_img/' + str(df.img_name[i])
    prompt3 = prompt_product(df.category[i])
    lab_claude = apply_claude(path, key, prompt3)
    df.at[i, 'Claude_message_2'] = lab_claude

# extract color
df['Claude_CIELAB'] = df['Claude_message_2'].apply(lambda x: x['content'][0]['text'])

# check if all the colors are in list format
df['is_list_LLM'] = df['Claude_CIELAB'].apply(is_list)

