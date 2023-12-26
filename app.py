import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = "Resources/arabica_final.csv"

# Load data using the cache
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    lowercase = lambda x: str(x).lower()
    return data 

# Load data
data = load_data()

# Sidebar sliders

# Create sliders and store values in a dictionary
slider_labels = data.columns[5:12]
slider_values = {label: label for label in slider_labels}

# Coffee Recommender
def coffee_recommender(aroma, flavor, acidity, body, balance, data):
    input_data = pd.DataFrame({'aroma': [aroma], 'flavor': [flavor], 'acidity': [acidity], 'body': [body], 'balance': [balance]})
    input_array = input_data.to_numpy().reshape(1, -1)
    
    # We will store similarity for each row of the dataset.
    sim = []
    
    for idx, row in data.iterrows():
        num_array2 = row[['aroma', 'flavor', 'acidity', 'body', 'balance']].to_numpy().reshape(1, -1)
        num_sim = cosine_similarity(input_array, num_array2)[0][0]
        sim.append(num_sim)
    
    return sim

# Coffee Recommender Streamlit App
def recommend_coffees(data):
    # Get user input for coffee factors
    aroma = st.sidebar.slider("Select Aroma level", 0.0, 10.0, 5.0)
    flavor = st.sidebar.slider("Select Flavor level", 0.0, 10.0, 5.0)
    acidity = st.sidebar.slider("Select Acidity level", 0.0, 10.0,5.0)
    body = st.sidebar.slider("Select Body level", 0.0, 10.0, 5.0)
    balance = st.sidebar.slider("Select Balance level", 0.0, 10.0, 5.0)

    # Create a DataFrame with user input
    input_data = pd.DataFrame({'aroma': [aroma], 'flavor': [flavor], 'acidity': [acidity], 'body': [body], 'balance': [balance]}, index=[0])
    input_features = input_data.to_numpy()

    data['similarity_factor'] = coffee_recommender(aroma, flavor, acidity, body, balance, data)
    data.sort_values(by=['similarity_factor'], ascending=False, inplace=True)

    # Display recommended coffees
    st.table(data[['species', 'country_of_origin','region','variety','processing_method','altitude_low_meters','altitude_high_meters']].head(5))

# Streamlit App
st.title("Coffee Recommender")
recommend_coffees(data)


