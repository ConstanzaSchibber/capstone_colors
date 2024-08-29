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

In this project, the absence of labeled data necessitated a manual approach to data annotation. Specifically, I manually cropped each image to focus solely on the makeup area, such as isolating the lipstick in an image. This step was crucial to ensure the accuracy of the color analysis, as the cropped section was then analyzed to determine the average CIELAB color, which served as a close approximation to the 'ground truth' color (see [notebook 3](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/3_Data_Annotation.ipynb)) 

However, not all images could provide this ground truth value. Some images displayed only the container without showing the actual makeup color (e.g., lipstick). As a result, 88.8% of the images in the dataset had a corresponding ground truth value. The fact that not all images have a ground truth color is not a problem, though, because the absense of label is due to factors unrelated to the color itself, such as incomplete data (e.g., images showing packaging without the makeup color). Therefore, missing labels do not introduce any bias related to the color properties being studied.

Finally, for the images with ground truth values, I extracted and stored the average CIELAB color in the metadata, which allowed for precise comparison and evaluation of the color predictions in the subsequent steps.


## Method 1: Color Segmentation

I developed a method to identify and analyze CIELAB color shades in makeup images using image clustering techniques, with a focus on achieving accurate color matching (see [notebook 2](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/2_Model_A_for_color_identification.ipynb). The goal was to create a robust framework for identifying and categorizing shades that align with human visual perception, crucial for makeup products where precise color matching is key.

Key Steps:

1. Initial Exploration: I started by applying k-means clustering to a few test images, extracting dominant colors and determining the most frequent color in each cluster. This helped establish a foundation for scaling up the approach.

2. Scaling to the Entire Dataset: I expanded the method to the entire dataset by dividing the images into training, validation, and test sets. I validated the algorithm’s performance by calculating [Delta E (ΔE)](https://en.wikipedia.org/wiki/Color_difference), a metric that quantifies color difference, to compare the identified color with the 'ground truth'.

3. Algorithm Refinement: To improve accuracy, especially for lipstick and lipgloss where container colors were confounding results, I refined the algorithm by filtering out clusters with black and white colors. This adjustment led to a significant reduction in Delta E across the dataset, indicating improved color matching.

4. Validation and Testing: The final algorithm iteration showed considerable improvements, particularly in reducing Delta E for products like blush, lipgloss, and lipliner, indicating more reliable color identification. The model was then tested on unseen data to ensure it generalized well.

Validation: Delta E ranges from 0 to 100, where  0 indicates that the colors are identical, while values up to 10 suggest that the colors are similar. For color-matching applications, a threshold between 10 and 15 is generally effective. About 62% of the images from the test set had a Delta E below 15. None of the images had a Delta E above 45 and 95% had a Delta E below 30. On average, the Delta E for blush (10.5) and lipgloss (14.02) are lower than for lipliner (17.8) and lipstick (18.3).

For illustration, the set of six figures displays makeup images (blush, lipstick, or lipgloss) from the validation set, each accompanied by a comparison of the predicted and true colors of the makeup. The Delta E values, which range from 0-5, 5-10, 10-15, and beyond, indicate the difference between the predicted and true colors. For lower Delta E values, the predicted color closely matches the true color, reflecting higher accuracy. As Delta E increases, the prediction accuracy decreases, often due to interference from packaging and shadows, which distort the true color and lead to less accurate predictions.

![img](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/img/deltaE.png)

Overall, the refined model demonstrated strong generalization for most makeup products, with notable improvements in color matching accuracy. However, further refinement is suggested for lipliner to reduce variability and enhance precision.

Here's a brief, high-level report of your work:

## Method 2: Improving Makeup Color Identification with Multimodal AI

In this [section](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/2_Model_B_for_color_identification_LLM_.ipynb), I explored the use of `Claude`, a multimodal large language model, to identify and analyze CIELAB color values of makeup products from images. The goal was to create a more accurate and nuanced color identification system than typically found in e-commerce platforms.

Key Steps and Findings:

1. Initial Implementation:
   - Developed a system to process makeup product images and estimate CIELAB colors using Claude.
   - Created a function to resize images and encode them for API compatibility.

2. Prompt Engineering:
   - Refined prompts over multiple rounds to improve color identification accuracy.
   - Tailored prompts for specific makeup categories (lipstick, lipliner, blush, lipgloss).

3. Evaluation:
   - Used Delta E (ΔE) to measure the difference between predicted and ground truth colors.
   - Initial results showed a mean ΔE of 15.76, with variations across product categories.

4. Improvement:
   - Enhanced prompts led to significant improvements:
     - Mean Delta E decreased from 16.4 to 11.5 (30% improvement).
     - Median Delta E decreased from 12.8 to 10.56 (17% improvement).
   - Substantial improvements across all product categories, particularly for challenging items like lipstick and lipliner.

5. Final Results:
   - 70% of cases now have a Delta E below 20, and 50% below 15.
   - Eliminated cases with very high ΔE (>40), indicating increased reliability.
   - Net gain of 8% in cases with improved color accuracy.

The refined approach using Claude and carefully engineered prompts significantly enhanced the accuracy and reliability of makeup color identification. This method shows promise for improving color matching in e-commerce and cosmetics applications, offering a more nuanced and precise color selection process for consumers.










