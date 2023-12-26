import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
# import plost

DATA_PATH = "Resources/arabica_final.csv"

# add option to open style.css 
# with open("css/style.css") as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ----- Side bar Info -----# 
st.sidebar.header('Coffee Characteristics')

# Load data using the cache
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    return data

# Load data
data = load_data()

# Sidebar sliders
def create_slider(label, default_value=5):
    return st.sidebar.slider(label, 0, 10, default_value)

def coffee_information(coffee_label, default_values=0):
    if slider_values == slider_coffee_values:
        return slider_coffee 

# Slider labels
slider_labels = data.columns[5:12]
slider_coffee = data.iloc[:, [0,1,2,3,4,13,14]]

# Create sliders and store values in a dictionary
slider_values = {label: create_slider(label) for label in slider_labels}
slider_coffee_values = {coffee_label: data['species'] for coffee_label in slider_coffee}

st.title(slider_values)
st.title(slider_coffee_values)

# # Extract coffee information based on slider values
# selected_coffee = data[
#     (data["Species"] == data["species"]) &
#     (data["Aroma"] == data["aroma"]) &
#     (data["Country of Origin"] == data["country_of_origin"]) &
#     (data["Variety"] == data["variety"]) &
#     (data["Process"] == data["processing_method"]) &
#     (data["Altitude"] == data["altitude"]) &
#     (data["Latitude"] == data["latitude"])
# ]

# # Display coffee information
# st.title("Coffee Preference")

# # Display extracted coffee information
# st.subheader("Selected Coffee Information:")
# st.table(selected_coffee[["Species", "Aroma", "Country of Origin", "Variety", "Process", "Altitude", "Latitude"]])


# # Display top 5 similar coffee beans and their characteristics
# st.subheader("Top 5 Similar Coffee Beans:")
# similar_coffees = data.sample(5)
# st.table(similar_coffees[["Species", "Acidity", "Flavor", "Aroma", "Aftertaste", "Body", "Balance", "Clean Cup"]])

# # Plot characteristics of similar coffee beans
# fig, ax = plt.subplots(figsize=(10, 6))
# for index, row in similar_coffees.iterrows():
#     ax.plot(row.index[5:12], row[5:12], label=f"{row['Species']} - {row['Country of Origin']}")
# ax.set_title("Characteristics of Similar Coffee Beans")
# ax.set_xlabel("Characteristic")
# ax.set_ylabel("Value")
# ax.legend()
# st.pyplot(fig)







# import streamlit as st
# import pandas as pd
# from PIL import Image, ImageDraw
# import numpy as np

# DATA_PATH = ("Resources/arabica_final.csv")

# # ------ INFORMATION ------ # 
# st.title("Coffee Preference")

# st.markdown(
# """
# This is an example of a coffee recommendation model. This model will generate the top 5
# recommendation tailored to the choice of the user. 
# Select the the different coffee components to view your taste. 
# """)

# # ------ LOADING OF DATA ------# 

# @st.cache_data
# def load_data():
#     data = pd.read_csv(DATA_PATH)
#     lowercase = lambda x: str(x).lower()
#     return data 

# # Load data using the cache
# data = load_data()

# # ------SIDEBAR SLIDERS ------#

# def create_slider(label, default_value=5):
#     return st.sidebar.slider(label, 0, 10, default_value)

# # Define the slider labels
# slider_labels = data.columns[5:12]

# # Create sliders using the function and store the values in a dictionary
# slider_values = {label: create_slider(label) for label in slider_labels}


# # ------MAIN COFFEE ------#

# coffee_image_labels = data.iloc[:, [0,1, 2, 3, 4, 13, 14]]
# image_path = ""

# def create_image(labels):
#     # Image size
#     image_size = (400, 200)
    
#     # Create a white image
#     image = Image.new("RGB", image_size, "white")
#     draw = ImageDraw.Draw(image)
    
#     # Draw empty boxes based on user input
#     box_width = 40
#     box_height = 20
#     margin = 10
#     x = margin
    
#     for label in labels:
#         draw.rectangle([x, margin, x + box_width, margin + box_height], outline="black", width=2)
#         draw.text((x + box_width // 2 - 10, margin + box_height + 5), label, fill="black", font=None)
#         x += box_width + 2 * margin  # Adjust the spacing by changing this line


#     return np.array(image)

# # Display main coffee image
# st.title("Custom Image with Sliders")
# coffee_image_labels = data.columns[[0, 1, 2, 3, 4, 13, 14]]
# custom_image = create_image(coffee_image_labels)
# st.image(custom_image, caption="Main Coffee Image", use_column_width=True)

# # Create and display the image using the sliders
# custom_image = create_image(slider_labels)
# st.image(custom_image, caption="Custom Image with Sliders", use_column_width=True)

# # ------TOP 5 ------#

# # Add input boxes
# user_input1 = st.text_input("Enter value 1:")
# user_input2 = st.text_input("Enter value 2:")

# # You can use the inputs as needed in your application logic
# result = user_input1 + user_input2
# st.write("Result:", result) 

# # ------MORE INFO ------#


# #-- Etra Loading images --#


# # ------REFERENCES ------#