This folder contains the following notebooks:

1. [Data Engineering](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/1_DataEngineering.ipynb):
   - Collection of images: download from the web, validate URLs, download Images, evaluate if all of the files downloaded are images
   - Exploratory data analysis: explora metadata (e.g. product categories) and images (e.g. image size in pixeles, width/height, number of colors)

2. [Data Annotation](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/3_Data_Annotation.ipynb): I manually crop each image to focus solely on the makeup area—for instance, isolating just the lipstick in an image. Then I,
   - Read cropped images 
   - Identify `ground truth` CIELab value
   - Save the value as part of the Metadata
  
3. [Method A for Identifying CIELab Color: Clustering](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/2_Model_A_for_color_identification.ipynb):
  - Test Cases 1 & 2: I used test cases images to apply and improve a k-means algorithm to cluster images and then extract the mean CIELab color of each cluster. I wrote functions to allow for a number of image types (e.g. `.png`) to be read and analyzed, this was needed because different image types have different number of color channels.
  - Scaling to other images: Reading the images, splitting into training/validation/test sets
  - Round 1: Applying the algorithm and validating the results
  - Round 2: Improving the algorithm based on the round 1 results, mainly enhancing the accuracy of the makeup color detection by identifying background color of the image (white or black), and removing it.
  - Round 3: Improving the algorithing based on the round 2 results, focusing on improving handling of `.png` images and conversion to CIELab color scale.
  - Assessing the final algorithm with the test set: The model shows strong generalization for blush and reasonable stability for lipgloss and lipstick, further refinement may be needed for lipliner to reduce variability and improve color accuracy.

4. [Method B for Identifying CIELab Color: Multimodal Large Language Model `Claude`](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/2_Model_B_for_color_identification_LLM_.ipynb):
  - Test of individual image
  - Prompt Engineering
  - Round 1: Scaling up and validation of results
  - Round 2: Based on the results of round 1, I refine the prompt and new results show considerable improvement.
  - Assessing the final algorithm with the test set: almost 70% of the cases have a Delta E below 20, and 50% have a Delta E below 15, indicating a substantial improvement in the model's precision. 
  
5. [Comparison of Methods A & B](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/4_Comparison_of_Approaches_A_and_B_.ipynb): The analysis reveals that the LLM consistently outperformed the clustering technique, particularly for the lipstick category. Both methods showed improved accuracy with larger image sizes, likely due to the increased availability of color information and detail. 

7. [Makeup App in Streamlit](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/6_Makeup_App_in_Streamlit.ipynb):  I development a makeup color search application using Streamlit. This app allows users to filter and find makeup products, offering a more nuanced and extensive color selection process compared to major retailers like Sephora and Ulta.
  - Makeup predicted color is grouped in multiple color categories using a clustering algorithm so that filtering makeup by similar shade was user-friendly (see second half of this [notebook](https://github.com/ConstanzaSchibber/capstone_colors/blob/main/notebooks/4_Comparison_of_Approaches_A_and_B_.ipynb))
  - Create color swatches so that users can pick colors by seeing the color, rather than reading the color name.
  - Streamlit and python code for the app
