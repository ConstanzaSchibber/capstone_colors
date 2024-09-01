
import streamlit as st
from st_clickable_images import clickable_images
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
from PIL import Image
import base64


# Set page config
st.set_page_config(
    page_title="Makeup Filter App",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>

    /* Change background color */
    .main {
        background-color: #f5f5f5; /* Light grey background */
    }

    /* Change font color and style */
    h1, h2, h3, h4, h5, h6, p, li {
        color: #333333; /* Dark grey font color */
        font-family: 'Arial', sans-serif;
    }

    /* Target the entire sidebar */
    [data-testid="stSidebar"] {
        background-color: #210340;
    }

    /* Target all text elements within the sidebar */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Specific selectors for different text elements */
    [data-testid="stSidebar"] .stMarkdown p {
        color: white !important;
    }

    [data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
    }

    [data-testid="stSidebar"] .stMultiSelect label {
        color: white !important;
    }

    /* Style for sidebar header */
    [data-testid="stSidebarNav"] {
        color: white !important;
    }

    /* Style for dropdown menus in sidebar */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div {
    background-color: #87034e !important;
      }

    /* Style for dropdown options */
    [data-testid="stSidebar"] ul[data-baseweb="menu"] {
    background-color: white !important;
    }

    /* Style for dropdown text */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] span,
    [data-testid="stSidebar"] ul[data-baseweb="menu"] li {
    color: #87034e !important;
    }

    /* Table styles */
    .dataframe {
        color: #333333 !important;
    }
    .dataframe th {
        background-color: #210340;
        color: white !important;
    }
    .dataframe td {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    "## Filter Makeup Options!"
# Title and Introduction
st.title("Makeup Filter App 💄")
st.markdown("""
Welcome to the Makeup Filter App! This tool allows you to filter a makeup by color shade, product category, and brand. Use the filters in the sidebar to narrow down the table and explore the data.
""")

# Instructions
st.header("Instructions")
st.markdown("""
1. **Select Filters:** Use the filters in the sidebar to filter the table by color shade, product category, and brand.
2. **View the Table:** The filtered table will be displayed below the filters.
3. **Explore:** You can experiment with different combinations of filters to explore the dataset.

This app is designed to help you easily navigate through the makeup options by providing dynamic filtering options.
""")

## DATA

# Read and sample data

df = pd.read_csv('/content/drive/My Drive/df_for_streamlit.csv')
df = df[df.ground_truth == 1]
df = df[['category', 'brand', 'median_hex_circle', 'Circle', 'img_url']]


# Filter Sidebar

dynamic_filters = DynamicFilters(df=df, filters=['category', 'brand'])
#dynamic_filters.display_filters(location='sidebar')

# save filtered df as new variable
new_df = dynamic_filters.filter_df()

# Color pick

list_images = ['c13744.png',
 'f3a3a7.png',
 '8c251e.png',
 'ffd9d5.png',
 'dd4b7a.png',
 '5e1920.png',
 'da7670.png',
 'f9c2b5.png',
 'e5817c.png',
 'aa1642.png']

images = []
for file in list_images:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/jpeg;base64,{encoded}")

### Create color bar
clicked = clickable_images(
    images,
    titles=[f"Image #{str(i)}" for i in range(10)],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "50px"},
)

## Filter by color
if clicked == 0:
  cat = df.median_hex_circle.unique()[0]
  new_df = new_df[new_df.median_hex_circle == cat]
  dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 1:
  cat = df.median_hex_circle.unique()[1]
  new_df = new_df[new_df.median_hex_circle == cat]
  dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 2:
  cat = df.median_hex_circle.unique()[2]
  new_df = new_df[new_df.median_hex_circle == cat]
  #dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 3:
  cat = df.median_hex_circle.unique()[3]
  new_df = new_df[new_df.median_hex_circle == cat]
  #dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 4:
  cat = df.median_hex_circle.unique()[4]
  new_df = new_df[new_df.median_hex_circle == cat]
  #dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 5:
  cat = df.median_hex_circle.unique()[5]
  new_df = new_df[new_df.median_hex_circle == cat]
  #dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 6:
  cat = df.median_hex_circle.unique()[6]
  new_df = new_df[new_df.median_hex_circle == cat]
  #dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 7:
  cat = df.median_hex_circle.unique()[7]
  new_df = new_df[new_df.median_hex_circle == cat]
  #dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 8:
  cat = df.median_hex_circle.unique()[8]
  new_df = new_df[new_df.median_hex_circle == cat]
  #dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

elif clicked == 9:
  cat = df.median_hex_circle.unique()[9]
  new_df = new_df[new_df.median_hex_circle == cat]
  #dynamic_filters = DynamicFilters(df=new_df, filters=['category', 'brand'])

dynamic_filters.display_filters(location='sidebar')

# Converting links to html tags
def path_to_image_html(path):
    return '<img src="' + path + '" height="60" >'


if len(new_df) < len(df):
    # Apply the color_square function to the 'District' column
    #new_df['District'] = new_df['District'].apply(color_square)
    new_df = new_df.sort_values(by = ['category','brand'])
    # Display the dataframe with HTML
    #st.write(new_df.to_html(escape=False, index=False), formatters=dict(img_url=path_to_image_html), unsafe_allow_html=True)

    def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return input_df.to_html(escape=False, formatters=dict(img_url=path_to_image_html))

    html = convert_df(new_df)

    st.markdown(
    html,
    unsafe_allow_html=True
    )

else:
    st.write("Please select at least one filter to display the data.")


