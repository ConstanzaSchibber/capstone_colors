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

## Data Collection and Cleaning, and Exploratory Data Analysis

The inital data consists of tables with information on makeup products and links to the makeup images. Some key metadata consists of product category (e.g. blush, lipstick, etc.), brand, shade - fancy names from the brand like `sunset`, `peachy`, `raunchy`-, specific product name, among others. 

The [notebook](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/1_DataEngineering.ipynb) for this section develops a number of functions to collect the images: (1) validation of URLs, (2) downloading the images, (3) checking that every file downloaded is an image and if any image is corrupted.

When it comes to the images, 40% correspond to lipsticks and 35% to blush. Moreover, the are over 159 unique brands and 59.12% of the brands have at least two products in the data.

## Human Annotation: Creating Data Labels

## Method 1: Color Segmentation

I developed a method to identify and analyze CIELAB color shades in makeup images using image clustering techniques, with a focus on achieving accurate color matching (see [notebook 2](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/2_Model_A_for_color_identification.ipynb). The goal was to create a robust framework for identifying and categorizing shades that align with human visual perception, crucial for makeup products where precise color matching is key.

Key Steps:
- Initial Exploration: I started by applying k-means clustering to a few test images, extracting dominant colors and determining the most frequent color in each cluster. This helped establish a foundation for scaling up the approach.
- Scaling to the Entire Dataset: I expanded the method to the entire dataset by dividing the images into training, validation, and test sets. I validated the algorithm’s performance by calculating [Delta E (ΔE)](https://en.wikipedia.org/wiki/Color_difference), a metric that quantifies color difference, to compare the identified color with the 'ground truth'.
- Algorithm Refinement: To improve accuracy, especially for lipstick and lipgloss where container colors were confounding results, I refined the algorithm by filtering out clusters with black and white colors. This adjustment led to a significant reduction in Delta E across the dataset, indicating improved color matching.
- Validation and Testing: The final algorithm iteration showed considerable improvements, particularly in reducing Delta E for products like blush, lipgloss, and lipliner, indicating more reliable color identification. The model was then tested on unseen data to ensure it generalized well.

Validation: Delta E ranges from 0 to 100, where  0 indicates that the colors are identical, while values up to 10 suggest that the colors are similar. For color-matching applications, a threshold between 10 and 15 is generally effective. About 62% of the images from the test set had a Delta E below 15. None of the images had a Delta E above 45 and 95% had a Delta E below 30. On average, the Delta E for blush (10.5) and lipgloss (14.02) are lower than for lipliner (17.8) and lipstick (18.3).

For illustration, the set of six figures displays makeup images (blush, lipstick, or lipgloss) from the validation set, each accompanied by a comparison of the predicted and true colors of the makeup. The Delta E values, which range from 0-5, 5-10, 10-15, and beyond, indicate the difference between the predicted and true colors. For lower Delta E values, the predicted color closely matches the true color, reflecting higher accuracy. As Delta E increases, the prediction accuracy decreases, often due to interference from packaging and shadows, which distort the true color and lead to less accurate predictions.

![img](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/img/deltaE.png)







