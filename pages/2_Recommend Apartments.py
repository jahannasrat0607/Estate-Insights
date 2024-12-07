import streamlit as st
import pickle
import pandas as pd
import numpy as np
st.set_page_config(page_title='Recommend Apartments')

location_df = pickle.load(open('datasets/location_distance.pkl', 'rb'))
# st.dataframe(location_df)

cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))

df = pd.read_csv('datasets/appartments.csv')
def recommend_properties_with_scores(property_name, top_n=5):

    cosine_sim_matrix = 0.5*cosine_sim1 + 0.8*cosine_sim2 + 1*cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'Link': df['Link'].iloc[top_indices],
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df

st.header('Apartment Recommendation System')
task = st.radio("What would you like to do?",
                options=["Filter by Location and Radius", "Recommend by Apartment"])

if task == "Filter by Location and Radius":
    selected_location = st.selectbox('Location', sorted(location_df.columns.tolist()))
    radius = st.number_input('Radius in kilometers')

    if st.button('Search'):
        # Filter apartments based on radius
        result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values().to_dict()
        if not result_ser:  # Check if no results
            st.warning('No nearby location found.')
        else:
            st.write("Apartments within the specified radius:")
            for key, value in result_ser.items():
                # Find the corresponding apartment in the main dataframe
                apartment_row = df[df['PropertyName'] == key]
                if not apartment_row.empty:
                    # Get the link for the apartment
                    link = apartment_row['Link'].iloc[0]
                    st.markdown(f"- **{key}** ({round(value / 1000, 2)} km): [Link]({link})")
                else:
                    st.markdown(f"- **{key}** ({round(value / 1000, 2)} km): No link available.")

elif task == "Recommend by Apartment":
    # st.header('Recommend Apartments')
    selected_apartment = st.selectbox('Select an Apartment',sorted(location_df.index.tolist()))

    if st.button('Recommend'):
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        # st.dataframe(recommendation_df[['PropertyName', 'Link']])
        if not recommendation_df.empty:
            # Create a new column with Markdown formatted links
            recommendation_df['Link'] = recommendation_df['Link'].apply(lambda x: f"[Link]({x})")

            # st.markdown to display the table with clickable links
            for _, row in recommendation_df.iterrows():
                st.markdown(f"- **{row['PropertyName']}**: {row['Link']}")
        else:
            st.warning("No recommendations found.")