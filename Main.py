import matplotlib.pylab as plt
import streamlit as st
import os
from API import transfer_style

st.set_page_config(page_title="ArtAdapt - Neural Style Transfer", layout="wide")

st.title("Neural Style Transfer")
st.write("Upload a content image and a style image to generate a new piece of art.")

# 1. Setup paths for the cloud environment
# The model path should be relative to your GitHub root
model_path = "model" 

# Create a temporary directory for uploaded files
if not os.path.exists("temp"):
    os.makedirs("temp")

# 2. Streamlit UI for file uploads
col1, col2 = st.columns(2)

with col1:
    content_file = st.file_uploader("Choose Content Image (e.g., Einstein)", type=["jpg", "png", "jpeg"])
with col2:
    style_file = st.file_uploader("Choose Style Image (e.g., Starry Night)", type=["jpg", "png", "jpeg"])

# 3. Process the images
if content_file and style_file:
    # Save uploaded bytes to temp files so transfer_style can read them
    content_path = os.path.join("temp", "content.jpg")
    style_path = os.path.join("temp", "style.jpg")
    
    with open(content_path, "wb") as f:
        f.write(content_file.getbuffer())
    with open(style_path, "wb") as f:
        f.write(style_file.getbuffer())

    if st.button("Generate Stylized Image"):
        with st.spinner("Applying style... this may take a moment."):
            try:
                # Call your original function
                img = transfer_style(content_path, style_path, model_path)
                
                # Display the result
                st.image(img, caption="Generated Image", use_container_width=True)
                
                # Allow user to download the result
                plt.imsave('stylized_image.jpeg', img)
                with open("stylized_image.jpeg", "rb") as file:
                    st.download_button(
                        label="Download Image",
                        data=file,
                        file_name="stylized_image.jpg",
                        mime="image/jpeg"
                    )
            except Exception as e:
                st.error(f"An error occurred: {e}")
