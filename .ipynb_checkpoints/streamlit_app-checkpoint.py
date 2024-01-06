# streamlit_app.py
import streamlit as st
from recommendation_system import recommend_coffees, data
import sqlite3 

# # Configure your SQLite database connection details
# conn = sqlite3.connect("your_database.db")  # Replace with your SQLite database file path
# query = "SELECT * FROM your_table"  # Replace with your table name

# # Read data with Pandas DataFrame
# data = pd.read_sql(query, conn)

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