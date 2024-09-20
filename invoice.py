import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')
# Configure Gemini API
genai.configure(api_key=os.getenv('API_KEY'))

# Streamlit Interface Setup
st.set_page_config(page_title="Gemini Application")

# Header
st.header("Insights of Bills and Invoices")

# Text input for user prompt
input_text = st.text_input("Enter your prompt:")

# Image uploader for uploading an image (jpg, jpeg, png)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Function to load and convert the image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # Convert image to RGB if it's not already in a JPEG-compatible mode
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert image to byte array to pass to the Gemini model
        byte_array = BytesIO()
        image.save(byte_array, format="JPEG")
        byte_array = byte_array.getvalue()
        image_data = [{"mime_type": uploaded_file.type, "data": byte_array}]
        return image, image_data
    else:
        return None, None

# Display the uploaded image
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

# Define input prompt for the AI task
input_prompt = """
            Please analyze the information from the invoice in the provided image and extract the following details:

1. Invoice number
2. Invoice date
3. Due date
4. Company name and address
5. Billing address
6. Total amount
7. Tax amount
8. List of purchased items, including quantity, unit price, and total price per item

Summarize this information in a structured format.
"""

# If the submit button is clicked
if st.button("Tell me about the image"):
    if uploaded_file is not None and input_text:
        # Process the image
        image, image_data = input_image_setup(uploaded_file)

        if image_data:
            # Load the Gemini model
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate the response using Gemini model
            response = model.generate_content([input_text, image_data[0], input_prompt])

            # Display the response from the model
            st.subheader("Response:")
            st.write(response.text)
    else:
        st.write("Please upload an image and enter a text prompt.")
