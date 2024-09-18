import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# Configure Gemini API
genai.configure(api_key=" ")

# Streamlit Interface Setup
st.set_page_config(page_title="Gemini Application")

# Header
st.header("Gemini Application - Analyze an Image")

# Text input for user prompt
input_text = st.text_input("Enter your prompt:")

# Image uploader for uploading an image (jpg, jpeg, png)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Function to load and convert the image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Convert image to byte array to pass to the Gemini model
        byte_array = BytesIO()
        
        # Save the image in its original format (remove hardcoded JPEG)
        image_format = uploaded_file.type.split("/")[-1].upper()  # Get the format (e.g., PNG, JPEG)
        image.save(byte_array, format=image_format)
        
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
            You are an expert in analyzing invoices.
            You will receive images of invoices, and your task is to extract relevant information such as:
            - Invoice Number
            - Date of Issue
            - Due Date
            - Billing and Shipping Addresses
            - Total Amount Due
            - Tax Details
            - Itemized List of Products/Services with their respective quantities and prices.

            Please extract and provide the relevant data from the invoice image and answer any specific questions based on the input image.
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
