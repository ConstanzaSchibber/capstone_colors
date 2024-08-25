# Project: Identifying Makeup Color from Images

**tl;dr:**
- Goal: Identify the color of makeup on the CIELab color space in order to compare shades on a standardized scale rather than by creative names each brand decides. 
- Data: Table of makeup products along with an image of each product collected from makeup retailers by scraping their website or using their API. 
- Methods: (1) color segmentation, (2) Multimodal Large Language Model (Claude)
- App: web-user interface in which users can filter makeup by color
- Tech stack: Python, Google Colab, React Streamlit

## Problem

I aim to identify the color of makeup from images to organize makeup by shade. Makeup products often have fanciful and inconsistent names, making it difficult for consumers to find the desired shade. These names can complicate organizing makeup by color. For example, the following makeup shades are all labeled as "mauve," even though they are clearly different shades. Some are not even mauve (as defined by Pantone) but brown.

![image](https://github.com/ConstanzaSchibber/capstone_colors/blob/5be3cc59ebc4906092fa95ccbdc54b890ca8827e/img/Screen%20Shot%202024-08-24%20at%208.52.52%20PM.png)

By leveraging the [CIELAB color space](https://en.wikipedia.org/wiki/CIELAB_color_space), which provides a standardized and perceptually uniform representation of color, I aim to identify makeup colors from images, and organize them and categorize them by shade. It's designed to be perceptually uniform, meaning that the numerical differences between colors correspond to perceived differences to the human eye.

CIELAB is a color space defined by the International Commission on Illumination (CIE) where colors are represented in three dimensions: 

- L (lightness)
- a (green to red)
- b (blue to yellow)

CIELAB offers a standardized method for describing colors, enabling accurate color comparison and matching across various brands and products. This standardization eliminates the confusion caused by subjective or creative color names, making it easier for consumers to find their desired shades. This is especially important for consumers seeking a specific color or looking for a similar shade from a more affordable brand.

In sum, this approach would enable the creation of a more reliable and user-friendly system for consumers to search and compare makeup by shade.

## Data



## Method 1: Color Segmentation







