import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, Table, MetaData
from flask import Flask, jsonify
from flask_cors import CORS
import joblib
import folium
from streamlit_folium import folium_static

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

# Load Standard Scaler and PCA model
loaded_scaler = joblib.load("models/scaler.joblib")
loaded_pca = joblib.load("models/pca_model.joblib")

# Coffee Recommender
def coffee_recommender(coffee_data_df, loaded_scaler, loaded_pca, aroma, flavor, acid, body, aftertaste, top_n=5):
    input_data = pd.DataFrame({'aroma': [aroma], 'flavour': [flavor], 'acid': [acid], 'body': [body], 'aftertaste': [aftertaste]})  # Apply loaded scaler 
    scaled_input_data = loaded_scaler.transform(input_data)  # Apply scaler transformation
    input_pca = loaded_pca.transform(scaled_input_data)  # Apply PCA transformation

    # Transform the entire dataset using PCA
    coffee_data_pca = loaded_pca.transform(coffee_data_df[['aroma', 'flavor', 'acid', 'body', 'aftertaste']])

    # Calculate cosine similarity using the transformed features
    similarity_scores = cosine_similarity(input_pca, coffee_data_pca)

    # Get the indices of the top N similar items
    top_indices = similarity_scores.argsort(axis=1)[:, -top_n:].flatten()

    return coffee_data_df.loc[top_indices]

# Function to create a Folium map
def create_map(recommended_coffees):
    # Create a map centered at a specific location (you can customize the coordinates)
    map_center = [0, 0]
    coffee_map = folium.Map(location=map_center, zoom_start=2)

    # Add markers for each recommended coffee
    for i, (_, row) in enumerate(recommended_coffees.iterrows(), 1):
        # Customize the content of the popup for each marker
        popup_content = f"<strong>Recommendation #{i}</strong><br><strong>Country of Origin:</strong> {row['country_of_origin']}<br><strong>Rating:</strong> {row['rating']}"

        marker_location = [row['latitude'], row['longitude']]  # Add latitude and longitude columns to your DataFrame

        folium.Marker(location=marker_location, popup=popup_content).add_to(coffee_map)

    return coffee_map

# Set the page configuration with the desired tab name
st.set_page_config(page_title="Coffee Recommender", page_icon="☕️", layout="wide")

# Coffee Recommender Title and Intro
st.markdown(
    """
    <div style='text-align: center; border: 1.5px solid #FFFFFF; padding: 50px;'>
        <div style='display: flex; align-items: center; justify-content: center;'>
            <span style='font-size: 42px;'>&#9749;</span>
            <h1 style='color: #d29c6c; margin: 0 10px;'>Coffee Recommender</h1>
            <span style='font-size: 42px;'>&#9749;</span>
        </div>
        <br> <!-- Line break -->
        <h3>Welcome to the Coffee Recommender app!</h3>
        <p>Discover your next favorite coffee based on your preferences.</p>
        <p>Adjust the sliders to the left to select your preferred aroma, flavor, acidity, body, and aftertaste levels, and we'll recommend the best coffees for you.</p>
        <hr style="border-top: 1px solid #d29c6c;"> <!-- Visual line -->
        <p><strong><span style='color: #d29c6c; font-size: 14pt;'>Aroma:</span></strong> The intensity of the coffee's fragrance. <br>
            0: No noticeable aroma → 10: Extremely strong and aromatic</p>
        <p><strong><span style='color: #d29c6c; font-size: 14pt;'>Flavour:</span></strong> The overall taste profile of the coffee. <br>
            0: No flavour → 10: Intensely rich and complex flavour</p>
        <p><strong><span style='color: #d29c6c; font-size: 14pt;'>Acidity:</span></strong> The perceived brightness or sharpness of the coffee. <br>
            0: Low acidity → 10: Very high acidity</p>
        <p><strong><span style='color: #d29c6c; font-size: 14pt;'>Body:</span></strong> The weight or thickness of the coffee on your palate. <br>
            0: Light-bodied → 10: Full-bodied and robust</p>
        <p><strong><span style='color: #d29c6c; font-size: 14pt;'>Aftertaste:</span></strong> The lingering taste after swallowing. <br>
            0: No aftertaste → 10: Long-lasting and pleasant aftertaste</p>
        <hr style="border-top: 1px solid #d29c6c;"> <!-- Visual line -->
    </div>
    """,
    unsafe_allow_html=True
)

# Create an empty container for the recommendations
result_container = st.empty()

# Sidebar with horizontally aligned sliders and buttons
with st.sidebar:
    st.markdown("<div style='text-align: center; font-weight: bold;'>Adjust Your Coffee Preferences Here</div><hr style='border-top: 1px solid #FFFFFF;'>", unsafe_allow_html=True)

    aroma = st.slider(":brown[Select Aroma level]", 0, 10, step=1, key="aroma_slider")
    flavor = st.slider(":brown[Select Flavour level]", 0, 10, step=1, key="flavor_slider")
    acid = st.slider(":brown[Select Acidity level]", 0, 10, step=1, key="acid_slider")
    body = st.slider(":brown[Select Body level]", 0, 10, step=1, key="body_slider")
    aftertaste = st.slider(":brown[Select Aftertaste level]", 0, 10, step=1, key="aftertaste_slider")


    col1, col2 = st.columns(2)  # Create two columns for the buttons to sit in

    # Button 1: Show me my results
    if col1.button("Show Me The Coffee!"):
        # Get recommended coffees
        recommended_coffees = coffee_recommender(coffee_data_df, loaded_scaler, loaded_pca, aroma, flavor, acid, body, aftertaste, top_n=5)
        
        # Display recommended coffees on a map
        coffee_map = create_map(recommended_coffees)
        folium_static(coffee_map)

        # Display recommended coffees with centered text
        recommendations_html = ""
        for i, (_, row) in enumerate(recommended_coffees[['rating', 'name', 'roaster', 'roast', 'country_of_origin', 'desc_1', 'desc_2']].head(6).iterrows(), 1):
            recommendations_html += f"""
            <div style="font-family: 'Open Sans', sans-serif; 
                        border: 2px solid #a6a6a6; 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin: 10px; 
                        background-color: #271b12; 
                        color: #FFFFFF;
                        max-height: 300px; 
                        overflow-y: auto;
                        text-align: center;">  <!-- Centering text -->
                <h2 style="color: #d29c6c;">Recommendation #{i}</h2>
                <p style="color: #d29c6c;"><strong>Name:</strong> {row['name']}</p> 
                <p><strong>Rating:</strong> {row['rating']}</p>
                <p><strong>Roaster:</strong> {row['roaster']}</p>
                <p><strong>Roast Level:</strong> {row['roast']}</p>
                <p><strong>Country of Origin:</strong> {row['country_of_origin']}</p>
                <p style="color: #d29c6c;"><strong>Information About The Coffee</strong></p>
                <p>{row['desc_1']}</p>
                <p style="color: #d29c6c;"><strong>Information About The Coffee's Origins</strong></p>
                <p>{row['desc_2']}</p>
            </div>
            """
        
        # Update the content of the container with the recommendations
        result_container.markdown(recommendations_html, unsafe_allow_html=True)

    # Button 2: Reset
    if col2.button("Reset My Results"):
        # Logic for resetting goes here
        st.warning("Reset") 
        # Clear