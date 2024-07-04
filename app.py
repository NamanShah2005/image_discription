from pathlib import Path
import hashlib
import google.generativeai as genai
import streamlit as st

# Set your API key here
API_KEY = "AIzaSyBsJVn3VYMKmuHX0bie7Qt_Sfur0JDX_h8"

# Configure with your API key
genai.configure(api_key=API_KEY)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 32,
  "max_output_tokens": 1024,
}

st.header("Image Chatbot")

model = genai.GenerativeModel(model_name="gemini-1.0-pro-vision-latest",
                              generation_config=generation_config)

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


if uploaded_image is not None:
    st.image(uploaded_image, use_column_width=True)
    input_text = st.text_input("Enter your query here")

    if input_text:
        # Save the uploaded image as a file
        image_path = "uploaded_image.png"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())
        
        # Pass the image file path to the API
        response = model.generate_content(["You are given an image, you will be asked a question, answer it, if multiple questions are asked, answer it in a form of a list, the question is : " + input_text, genai.upload_file(image_path)])
        
        # Check if the response contains a valid Part
        if response.parts:
            st.write(response.text)
        else:
            st.write("Sorry, the model could not generate a valid response.")