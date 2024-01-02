import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = "Resources/coffee_final_try.csv"

# Load data using the cache
def load_data():
    data = pd.read_csv(DATA_PATH)
    lowercase = lambda x: str(x).lower()
    return data 

# Load data
data = load_data()


# Coffee Recommender
def coffee_recommender(aroma, flavor, acid, body, aftertaste, data):
    input_data = pd.DataFrame({
        'aroma': [aroma], 
        'flavor': [flavor], 
        'acid': [acid], 
        'body': [body], 
        'aftertaste': [aftertaste]
        })
    
    input_array = input_data.to_numpy().reshape(1, -1)
    
    # We will store similarity for each row of the dataset.
    sim = []
    
    for idx, row in data.iterrows():
        num_array2 = row[['aroma', 'flavor', 'acid', 'body', 'aftertaste']].to_numpy().reshape(1, -1)
        num_sim = cosine_similarity(input_array, num_array2)[0][0]
        sim.append(num_sim)
    
    return sim

# Coffee Recommender Streamlit App
def recommend_coffees(data):
    
    # Get user input for coffee preference of user 
    aroma = st.sidebar.slider("Select Aroma level", 0, 10, 5)
    flavor = st.sidebar.slider("Select Flavor level", 0, 10, 5)
    acid = st.sidebar.slider("Select Acid level", 0, 10,5)
    body = st.sidebar.slider("Select Body level", 0, 10, 5)
    aftertaste = st.sidebar.slider("Select Aftertaste level", 0, 10, 5) 
    
    # Create a DataFrame with user input
    input_data = pd.DataFrame({'aroma': [aroma], 'flavor': [flavor], 'acid': [acid], 'body': [body], 'aftertaste': [aftertaste]}, index=[0])
    input_features = input_data.to_numpy()


    data['similarity_factor'] = coffee_recommender(aroma, flavor, acid, body, aftertaste, data)
    data.sort_values(by=['similarity_factor'], ascending=False, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data.index = data.index + 1
    
    recommendation = (data.head())
    
 
    return recommendation 