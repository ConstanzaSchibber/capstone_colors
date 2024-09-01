# Project: Identifying Makeup Color from Images

**tl;dr:**

- **Goal:** Identify the color of makeup on the CIELab color space in order to compare shades on a standardized scale rather than by creative names each brand decides. 
- **Data:** Table of makeup products along with an image of each product collected from makeup retailers by scraping their website or using their API. 
- **Methods:** (1) color segmentation, (2) Multimodal Large Language Model (Claude)
- **App:** web-user interface in which users can filter makeup by color
- **Tech stack:** Python, Google Colab, React Streamlit

*Table of Contents*
- [Problem](https://github.com/ConstanzaSchibber/capstone_colors/tree/main?tab=readme-ov-file#problem)
- [Data Collection, Data Cleaning, and Exploratory Data Analysis](https://github.com/ConstanzaSchibber/capstone_colors/tree/main?tab=readme-ov-file#data-collection-and-cleaning-and-exploratory-data-analysis)
- [Human Annotation: Creating Data Labels](https://github.com/ConstanzaSchibber/capstone_colors/tree/main?tab=readme-ov-file#human-annotation-creating-data-labels)
- [Method 1: Color Segmentation](https://github.com/ConstanzaSchibber/capstone_colors/tree/main?tab=readme-ov-file#method-1-color-segmentation)
- [Method 2: Improving Makeup Color Identification with Multimodal AI](https://github.com/ConstanzaSchibber/capstone_colors/tree/main?tab=readme-ov-file#method-2-improving-makeup-color-identification-with-multimodal-ai)
- [Comparative Analysis of Clustering and Multimodal LLM Approaches for Makeup Color Identification](https://github.com/ConstanzaSchibber/capstone_colors/tree/main?tab=readme-ov-file#comparative-analysis-of-clustering-and-multimodal-llm-approaches-for-makeup-color-identification)
- [Building User-Friendly Streamlit App](https://github.com/ConstanzaSchibber/capstone_colors/tree/main?tab=readme-ov-file#building-user-friendly-streamlit-app)

## Problem

I aim to identify the color of makeup from images to organize makeup by shade. Makeup products often have fanciful and inconsistent names, making it difficult for consumers to find the desired shade. These names can complicate organizing makeup by color. For example, the following makeup shades are all labeled as "mauve," even though they are clearly different shades. Some are not even mauve (as defined by Pantone) but brown.

<img src="https://github.com/ConstanzaSchibber/capstone_colors/blob/5be3cc59ebc4906092fa95ccbdc54b890ca8827e/img/Screen%20Shot%202024-08-24%20at%208.52.52%20PM.png" width=50%>

Moreover, the color shade filters offered by makeup retailers are often limited. For example, below are the lipstick color options available at Sephora and Ulta, compared to the more comprehensive shade palette my app provides which allows users to filter by a lot more shades: 

<img src="https://github.com/ConstanzaSchibber/capstone_colors/blob/main/img/filters_retail.png" width=50%>


By leveraging the [CIELAB color space](https://en.wikipedia.org/wiki/CIELAB_color_space), which provides a standardized and perceptually uniform representation of color, I aim to identify makeup colors from images, and organize them and categorize them by shade. It's designed to be perceptually uniform, meaning that the numerical differences between colors correspond to perceived differences to the human eye.

CIELAB is a color space defined by the International Commission on Illumination (CIE) where colors are represented in three dimensions: 

- L (lightness)
- a (green to red)
- b (blue to yellow)

CIELAB offers a standardized method for describing colors, enabling accurate color comparison and matching across various brands and products. This standardization eliminates the confusion caused by subjective or creative color names, making it easier for consumers to find their desired shades. This is especially important for consumers seeking a specific color or looking for a similar shade from a more affordable brand.

In sum, this approach would enable the creation of a more reliable and user-friendly system for consumers to search and compare makeup by shade.

## Data Collection, Data Cleaning, and Exploratory Data Analysis

The inital data consists of tables with information on makeup products and links to the makeup images. Some key metadata consists of product category (e.g. blush, lipstick, etc.), brand, shade - fancy names from the brand like `sunset`, `peachy`, `raunchy`-, specific product name, among others. 

The [notebook](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/1_DataEngineering.ipynb) for this section develops a number of functions to collect the images: (1) validation of URLs, (2) downloading the images, (3) checking that every file downloaded is an image and if any image is corrupted.

When it comes to the images, 40% correspond to lipsticks and 35% to blush. Moreover, the are over 159 unique brands and 59.12% of the brands have at least two products in the data.

## Human Annotation: Creating Data Labels

In this project, the absence of labeled data necessitated a manual approach to data annotation. Specifically, I manually cropped each image to focus solely on the makeup area, such as isolating the lipstick in an image. This step was crucial to ensure the accuracy of the color analysis, as the cropped section was then analyzed to determine the average CIELAB color, which served as a close approximation to the 'ground truth' color (see [notebook](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/3_Data_Annotation.ipynb)) 

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

In this [notebook](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/2_Model_B_for_color_identification_LLM_.ipynb), I explored the use of `Claude`, a multimodal large language model, to identify and analyze CIELAB color values of makeup products from images. The goal was to create a more accurate and nuanced color identification system than typically found in e-commerce platforms.

Key Steps and Findings:

1. Initial Implementation:
   - Developed a system to process makeup product images and estimate CIELAB colors using Claude.
   - Created a function to resize images and encode them for API compatibility.

2. Prompt Engineering:
   - Refined prompts over multiple rounds to improve color identification accuracy.
   - Tailored prompts for specific makeup categories (lipstick, lipliner, blush, lipgloss).

3. Evaluation:
   - Used Delta E to measure the difference between predicted and ground truth colors.
   - Initial results showed a mean Delta E  of 15.76, with variations across product categories.

4. Improvement:
   - Enhanced prompts led to significant improvements:
     - Mean Delta E decreased from 16.4 to 11.5 (30% improvement).
     - Median Delta E decreased from 12.8 to 10.56 (17% improvement).
   - Substantial improvements across all product categories, particularly for challenging items like lipstick and lipliner.

5. Final Results:
   - 70% of cases now have a Delta E below 20, and 50% below 15.
   - Eliminated cases with very high Delta E (>40), indicating increased reliability.
   - Net gain of 8% in cases with improved color accuracy.

The refined approach using Claude and carefully engineered prompts significantly enhanced the accuracy and reliability of makeup color identification. This method shows promise for improving color matching in e-commerce and cosmetics applications, offering a more nuanced and precise color selection process for consumers.

## Comparative Analysis of Clustering and Multimodal LLM Approaches for Makeup Color Identification

Next, I [compared the two methods](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/4_Comparison_of_Approaches_A_and_B_.ipynb) for identifying CIELAB shades in makeup products. The comparison was based on Delta E values, which measure color difference. If for a specific makeup product the Delta E of method A is higher than for Method B (Method A > Method B), then Method B performs better because the color predicted is closer to the ground truth color. On the other hand, of for a specific makeup product the Delta E of method B is higher than for Method A, then Method A is performing better because of the small Delta E.

Overall, the LLM method (Claude) generally outperformed the clustering method across all makeup categories. More specifically, for blush and lipgloss, the LLM approach showed slightly better performance, with about 58-60% of cases having better color accuracy. For lipliner, both methods performed similarly, with the LLM approach having a slight edge (44.83% vs 41.38%). Finally, for lipstick, the LLM significantly outperformed clustering, providing better color accuracy in 62.83% of cases compared to 28.27% for clustering. 

Table: Delta E comparisons (% of products with higher Delta E)
| Category | LLM > Clustering (%) | Clustering > LLM (%) |
|----------|----------------------|----------------------|
| blush    | 34.15                | 59.76                |
| lipgloss | 36.89                | 57.38                |
| lipliner | 41.38                | 44.83                |
| lipstick | 28.27                | 62.83                |


The LLM's superior performance, especially in the lipstick category, may be attributed to its ability to incorporate contextual information about makeup packaging in its analysis.
The balanced performance in the lipliner category suggests that both methods have their strengths for certain types of products.

In a nutshell, the multimodal LLM approach (Claude) demonstrated overall better performance in identifying CIELAB shades across various makeup categories, particularly excelling with lipsticks. This suggests that leveraging advanced AI models with contextual understanding can significantly improve color identification accuracy.

## Building User-Friendly Streamlit App

In the final [notebook](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/6_Makeup_App_in_Streamlit.ipynb), I developed a makeup color search application using Streamlit. This app allows users to filter and find makeup products, offering a more nuanced and extensive color selection process compared to major retailers like Sephora and Ulta.

In the world of makeup, finding the perfect shade can be a challenge. While many online retailers offer basic color filtering, this app takes it a step further by providing a more granular and visually intuitive color selection process.

Key Features:
- Color Filtering: Users can choose from over 10 color groups, significantly more than typical e-commerce platforms.
- Multiple Filter Options: Products can be filtered by color, brand, and category (lipstick, blush, lipliner, lipgloss).
- Visual Color Selection: Color swatches are provided for users to click and filter by color intuitively.
- AI-Powered Color Prediction: The colors are predicted from product images using advanced methods (detailed previously).

How It Works:
- The app uses Streamlit to create an interactive web interface.
- Color data is pre-processed and grouped by similarity.
- Users interact with color swatches, brand selections, and product categories to filter results.
- The filtered results are displayed in a dynamic, user-friendly table.

### Streamlit - Setup and Styling:

The app uses Streamlit's page configuration to set the layout and sidebar state. Custom CSS is applied to style the page, including the sidebar and table.

- Data Loading and Preparation: The makeup data is loaded from a CSV file and relevant columns are selected.
- Dynamic Filters: The `DynamicFilters` class is used to create filters for category and brand.
- Color Swatch Selection: Color swatches are loaded and displayed as clickable images. When a color is clicked, it filters the dataset by that color.
- Result Display: The filtered results are displayed in a table with product images.

This app leverages Streamlit's interactive features and custom styling to create a user-friendly interface. The color prediction and grouping (done in separate processes) allow for a more refined color selection than typically found in e-commerce platforms.

## Streamlit App

Before selecting filters:

![img](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/img/myapp.jpg)

After filtering by a color shade:

![img](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/img/appl_filter.png)



