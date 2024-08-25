# Project: Identifying Makeup Color from Images

**tl;dr:**
- Goal: Identify the color of makeup on the CIELab color space in order to compare shades on a standardized scale rather than by creative names each brand decides. 
- Data: Table of makeup products along with an image of each product collected from makeup retailers by scraping their website or using their API. 
- Methosd: (1) color segmentation, (2) Multimodal Large Language Model (Claude)
- Tech stack: Python, Google Colab, React Streamlit

## Goals

I aim to identify the color of makeup from images to organize makeup by shade. Makeup products often have fanciful and inconsistent names, making it difficult for consumers to find the desired shade. These names can complicate organizing makeup by color. For example, the following makeup shades are all labeled as "mauve," even though they are clearly different shades. Some are not even mauve (as defined by Pantone) but brown.

[image](https://github.com/ConstanzaSchibber/capstone_colors/blob/5be3cc59ebc4906092fa95ccbdc54b890ca8827e/img/Screen%20Shot%202024-08-24%20at%208.52.52%20PM.png)


