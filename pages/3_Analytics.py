# Analytics module
"""
1. geo map
2. word cloud amenities
3. scatter plot -> area vs. price
4. pie chart bhk filter by sector
5. side by side boxplot bedroom price
6. distplot of price of flat and house
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Set Streamlit app configuration
st.set_page_config(
    page_title="Real Estate Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add HTML/CSS for styling
st.markdown("""
    <style>
        .main-header {
            font-size: 36px;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
        }
        .section-header {
            font-size: 28px;
            font-weight: bold;
            color: #2ECC71;
            margin-top: 20px;
        }
        .subsection-header {
            font-size: 20px;
            font-weight: bold;
            color: #F39C12;
        }
        .footer {
            font-size: 12px;
            color: gray;
            text-align: center;
            margin-top: 50px;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown('<div class="main-header">Real Estate Insights Dashboard</div>', unsafe_allow_html=True)

# Load dataset and files
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))
with open("datasets/sector_features.json", "r") as f:
    sector_features = json.load(f)

group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()

# Geo Map Section
st.markdown('<div class="section-header">Geo Map</div>', unsafe_allow_html=True)
fig = px.scatter_mapbox(
    group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
    color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
    mapbox_style="open-street-map", width=1200, height=700,
    title="Average Price Per Sq. Ft. by Sector"
)
st.plotly_chart(fig, use_container_width=True)

# Word Cloud Section
st.markdown('<div class="section-header">Sector-wise Word Cloud</div>', unsafe_allow_html=True)
sectors = list(sector_features.keys())
selected_sector = st.selectbox("Select a sector to view its word cloud:", sectors)

if selected_sector:
    feature_text = sector_features[selected_sector]
    wordcloud = WordCloud(
        width=800, height=800, background_color='white',
        stopwords=set(['s']), min_font_size=10
    ).generate(feature_text)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig)  # Pass the figure explicitly here
# Area vs. Price
st.markdown('<div class="section-header">Area vs. Price</div>', unsafe_allow_html=True)
property_type = st.selectbox('Select property type:', ['flat', 'house'])
fig1 = px.scatter(
    new_df[new_df['property_type'] == property_type],
    x="built_up_area", y="price", color="bedRoom",
    title=f"Area vs. Price for {property_type.capitalize()}",
    labels={"built_up_area": "Built-up Area (sq. ft.)", "price": "Price"}
)
st.plotly_chart(fig1, use_container_width=True)

# BHK Pie Chart
st.markdown('<div class="section-header">BHK Pie Chart</div>', unsafe_allow_html=True)
sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')
selected_sector = st.selectbox('Select Sector:', sector_options, key='pie_chart')
if selected_sector == 'overall':
    fig2 = px.pie(new_df, names='bedRoom', title="Overall BHK Distribution")
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom', title=f"BHK Distribution in {selected_sector}")
st.plotly_chart(fig2, use_container_width=True)

# Side-by-side Boxplot
st.markdown('<div class="section-header">BHK Price Comparison</div>', unsafe_allow_html=True)
temp_df = new_df[new_df['bedRoom'] <= 5]
fig3 = px.box(
    temp_df, x='bedRoom', y='price',
    title='Price Range by BHK',
    labels={"bedRoom": "BHK", "price": "Price"}
)
st.plotly_chart(fig3, use_container_width=True)

# Flat vs. House Price Distribution
st.markdown('<div class="section-header">Flat vs. House Price Distribution</div>', unsafe_allow_html=True)
fig4 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='House',kde=True, color="blue")
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='Flat', kde=True, color="green")
plt.legend()
st.pyplot(fig4)

# Bar Chart for Sector-Wise Average Price
st.markdown('<div class="section-header">Sector-Wise Average Price per Sq. Ft.</div>', unsafe_allow_html=True)
fig5 = px.bar(
    group_df, x=group_df.index, y="price_per_sqft",
    title="Average Price per Sq. Ft. by Sector",
    labels={"x": "Sector", "price_per_sqft": "Price Per Sq. Ft."}
)
st.plotly_chart(fig5, use_container_width=True)

# Sunburst Chart
st.markdown('<div class="section-header">Hierarchical Property Distribution</div>', unsafe_allow_html=True)
fig9 = px.sunburst(
    new_df, path=['sector', 'property_type', 'bedRoom'], values='price',
    title="Sector-Property-BHK Hierarchy"
)
st.plotly_chart(fig9, use_container_width=True)

# Footer
st.markdown('<div class="footer">Developed by Nasrat Jahan | Real Estate Insights Dashboard</div>', unsafe_allow_html=True)