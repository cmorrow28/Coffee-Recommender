# streamlit_app.py
import streamlit as st
from recommendation_system import recommend_coffees, data

def main():
    st.title("Coffee Recommendation System")

    # Call the recommend_coffees function from recommendation_system.py
    recommendations = recommend_coffees(data)

    # Display recommendations
    st.header("Recommendations:")
    st.table(recommendations)
    
    st.sidebar.button("Recommendation Button")

if __name__ == "__main__":
    main()

# import streamlit as st
# from recommendation_system import recommend_coffees, coffee_recommended, coffee_recommender
# import sqlite3 
# import pandas as pd 

# # Configure your SQLite database connection details
# conn = sqlite3.connect("your_database.db")  # Replace with your SQLite database file path
# query = "SELECT * FROM your_table"  # Replace with your table name

# # Read data with Pandas DataFrame
# data = pd.read_sql(query, conn)

# # Streamlit app
# st.title("Coffee Recommendation App")

# # Sidebar with user preferences
# aroma = st.sidebar.slider("Select Aroma level", 0, 10, 5)
# flavor = st.sidebar.slider("Select Flavor level", 0, 10, 5)
# acid = st.sidebar.slider("Select Acid level", 0, 10, 5)
# body = st.sidebar.slider("Select Body level", 0, 10, 5)
# aftertaste = st.sidebar.slider("Select Aftertaste level", 0, 10, 5)

# # Display user preferences
# st.write("User Preferences:")
# st.write(f"Aroma: {aroma}, Flavor: {flavor}, Acid: {acid}, Body: {body}, Aftertaste: {aftertaste}")

# # Get recommendations based on user preferences
# recommendations = recommend_coffees(data, aroma, flavor, acid, body, aftertaste)

# # Display recommendations
# st.header("Recommendations:")
# st.table(recommendations)
