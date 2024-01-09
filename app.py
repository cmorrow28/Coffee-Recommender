import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, Table, MetaData
from flask import Flask, jsonify
from flask_cors import CORS
# import folium
# from streamlit_folium import folium_static
import joblib 

# Flask setup
app = Flask(__name__)
CORS(app)

# Database Setup
engine = create_engine("sqlite:///Coding/Data_Engineering.db")

# Reflect the tables
metadata = MetaData()
metadata.reflect(bind=engine)
coffee_data = metadata.tables['coffee_data']

# Fetch data from the database
conn = engine.connect()
result = conn.execute(coffee_data.select()).fetchall()
conn.close()

# Convert each row to a dictionary
data = [dict(row._asdict()) for row in result]

# Create a DataFrame
coffee_data_df = pd.DataFrame(data)

# Load models
loaded_model = joblib.load("models/kmeans_model.joblib")
loaded_pca = joblib.load("models/pca_model.joblib")

# Coffee Recommender
def coffee_recommender(aroma, flavor, acid, body, aftertaste, loaded_model, loaded_pca, coffee_data_df, top_n=5):
    # Transform user input using PCA
    input_data = loaded_pca.transform([[aroma, flavor, acid, body, aftertaste]])
    input_array = input_data.reshape(1, -1)

    # Make predictions using the loaded KMeans model
    cluster_label = loaded_model.predict(input_data)[0]

    # Assign the cluster label to a new column
    coffee_data_df['coffee_segments'] = loaded_model.predict(loaded_pca.transform(coffee_data_df[['aroma', 'flavor', 'acid', 'body', 'aftertaste']]))

    # Filter coffee_data_df for the predicted cluster
    recommended_coffees = coffee_data_df[coffee_data_df['coffee_segments'] == cluster_label]

    # Calculate cosine similarity for each row
    input_array = input_data.reshape(1, -1)
    recommended_coffees['similarity_factor'] = recommended_coffees.apply(lambda row: cosine_similarity(input_array, row[['aroma', 'flavor', 'acid', 'body', 'aftertaste']].values.reshape(1, -1))[0][0], axis=1)

    # Get the indices of the top N similar items
    top_indices = recommended_coffees['similarity_factor'].nlargest(top_n).index.tolist()

    return recommended_coffees.loc[top_indices]

# def show_map(latitude, longitude):
#     # Create a Folium map centered at the specified location
#     coffee_map = folium.Map(location=[latitude, longitude], zoom_start=12)

#     # Add a marker to the map
#     folium.Marker(location=[latitude, longitude], popup="Recommended Coffee Location").add_to(coffee_map)

#     # Display the map using st.map
#     st.markdown(folium_static(coffee_map))

# Coffee Recommender Streamlit App
def recommend_coffees(coffee_data_df, loaded_model, loaded_pca):
    # Get user input for coffee factors
    aroma = st.sidebar.slider("Select Aroma level", 0.0, 10.0, 5.0)
    flavor = st.sidebar.slider("Select Flavor level", 0.0, 10.0, 5.0)
    acid = st.sidebar.slider("Select Acidity level", 0.0, 10.0, 5.0)
    body = st.sidebar.slider("Select Body level", 0.0, 10.0, 5.0)
    aftertaste = st.sidebar.slider("Select Aftertaste level", 0.0, 10.0, 5.0)

    # Get recommended coffees
    recommended_coffees = coffee_recommender(aroma, flavor, acid, body, aftertaste, loaded_model, loaded_pca, coffee_data_df)

    # Display recommended coffees with a rectangle appearance and Open Sans font
    for i, (_, row) in enumerate(recommended_coffees[['name', 'roaster', 'roast', 'country_of_origin', 'desc_1', 'desc_2']].head(6).iterrows(), 1):
        st.markdown(
            f"""
            <div style="font-family: 'Open Sans', sans-serif; 
                        border: 2px solid #a6a6a6; 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin: 10px; 
                        background-color: #271001; 
                        color: #FFFFFF;
                        max-height: 230px; 
                        overflow-y: auto;">
                <h2 style="color: #d29c6c;">Recommendation #{i}</h2>
                <p><strong>Name:</strong> {row['name']}</p>
                <p><strong>Roaster:</strong> {row['roaster']}</p>
                <p><strong>Roast Level:</strong> {row['roast']}</p>
                <p><strong>Country of Origin:</strong> {row['country_of_origin']}</p>
                <p style="color: #d29c6c;"><strong>Information About The Coffee</strong></p>
                <p>{row['desc_1']}</p>
                <p style="color: #d29c6c;"><strong>Information About The Coffee's Origins</strong></p>
                <p>{row['desc_2']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # # Add a map to display the location of the recommended coffee
        # st.markdown("<h2 style='color: #d29c6c;'>Location on Map</h2>", unsafe_allow_html=True)
        # show_map(row['latitude'], row['longitude'])

# if __name__ == "__main__":
#     recommend_coffees(coffee_data_df, loaded_model, loaded_pca)

# Streamlit App
st.title("Coffee Recommender")
recommend_coffees(coffee_data_df, loaded_model, loaded_pca)
