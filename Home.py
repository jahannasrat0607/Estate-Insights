# import streamlit as st
#
# st.set_page_config(
#     page_title="Real Estate Analytics App",
#     page_icon='👋🏻'
# )
#
# st.header('Welcome to Streamlit! 👋🏻')
# st.sidebar.success('Select a demo above.')
import streamlit as st
from PIL import Image

# Set the page config
st.set_page_config(
    page_title="Real Estate Analytics App",
    page_icon='🏠',
    layout="centered"  # Center the layout
)

# Add a header with a welcoming message
st.title("🏡 Real Estate Analytics App")
st.markdown("""
    ## Welcome to the Real Estate Analytics App!  
    Explore property data, predict prices, and analyze trends in the real estate market with ease.
""")

# Add an introductory paragraph
st.markdown("""
    This app allows you to gain insights into the real estate market by:
    - **Predicting property prices**
    - **Visualizing key trends**
    - **Recommending apartments**

    Let's get started and make informed decisions!
""")

image = Image.open('real_estate.jpg')  # Make sure the image is available in your directory
st.image(image, caption="Your Real Estate Assistant", use_column_width=True)

# Adding a button to encourage exploration
if st.button('Explore the App'):
    st.sidebar.success('Now you can explore different sections!')


st.sidebar.header("Navigate")
st.sidebar.text("Explore different features and demos available on the left.")
