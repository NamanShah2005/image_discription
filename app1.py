from pathlib import Path
import hashlib
import google.generativeai as genai
import streamlit as st
import dotenv
import os

dotenv.load_dotenv()
# Set your API key here
API_KEY = os.getenv("API_KEY")
# Configure with your API key
genai.configure(api_key=API_KEY)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 32,
  "max_output_tokens": 1024,
}

css = """
<style>
body {
    background-image: linear-gradient(to left, rgb(10, 0, 73), rgb(0, 0, 0));
    color: white; /* Text color */
}

/* Style for file uploader */
div.stFileUploader {
    background-color: white; /* White background for file uploader */
    color: black; /* Text color */
    border-color: white; /* Border color */
}
</style>
"""

# Display CSS
st.markdown(css, unsafe_allow_html=True)

st.header("Image Chatbot")
st.markdown('<div class="header-text">Image Chatbot</div>', unsafe_allow_html=True)

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config)

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    st.image(uploaded_image, use_column_width=True)
    # st.markdown('<div class="input-section">Input Section</div>', unsafe_allow_html=True)
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
            st.markdown('<div class="output-text">Output Section</div>', unsafe_allow_html=True)
            st.write(response.text)
        else:
            st.write("Sorry, the model could not generate a valid response.")
