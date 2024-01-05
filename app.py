import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, Table, MetaData
from flask import Flask, jsonify
from flask_cors import CORS

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

# Create an API route for coffee data
@app.route("/api/v1.0/coffee_data")
def get_coffee_data_api():
    conn = engine.connect()
    result = conn.execute(coffee_data.select()).fetchall()
    conn.close()

    # Convert each row to a dictionary
    data = [dict(row._asdict()) for row in result]
    return jsonify(data)

# Coffee Recommender
def coffee_recommender(aroma, flavor, acid, body, aftertaste, coffee_data, top_n=5):
    input_data = pd.DataFrame({'aroma': [aroma], 'flavor': [flavor], 'acid': [acid], 'body': [body], 'aftertaste': [aftertaste]})
    input_array = input_data.to_numpy().reshape(1, -1)

    # Calculate cosine similarity for each row
    coffee_data['similarity_factor'] = coffee_data.apply(lambda row: cosine_similarity(input_array, row[['aroma', 'flavor', 'acid', 'body', 'aftertaste']].values.reshape(1, -1))[0][0], axis=1)

    # Get the indices of the top N similar items
    top_indices = coffee_data['similarity_factor'].nlargest(top_n).index.tolist()

    return coffee_data.loc[top_indices]

# Coffee Recommender Streamlit App
def recommend_coffees(coffee_data_df):
    # Get user input for coffee factors
    aroma = st.sidebar.slider("Select Aroma level", 0.0, 10.0, 5.0)
    flavor = st.sidebar.slider("Select Flavor level", 0.0, 10.0, 5.0)
    acid = st.sidebar.slider("Select Acidity level", 0.0, 10.0, 5.0)
    body = st.sidebar.slider("Select Body level", 0.0, 10.0, 5.0)
    aftertaste = st.sidebar.slider("Select Aftertaste level", 0.0, 10.0, 5.0)

    # Get recommended coffees
    recommended_coffees = coffee_recommender(aroma, flavor, acid, body, aftertaste, coffee_data_df)

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

# Streamlit App
st.title("Coffee Recommender")
recommend_coffees(coffee_data_df)

