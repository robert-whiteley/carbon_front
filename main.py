# client.py
import requests
import streamlit as st
import os

#Server URL
SERVER_BASE_URL = 'http://localhost:8000'

def upload_image(file_path):
    #The post endpoint
    url = SERVER_BASE_URL + "/upload"
    #Writing in the files -> image the file in binary
    files = {'image': open(file_path, 'rb')}
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            st.success("Image uploaded successfully")
        else:
            st.error("Failed to upload image")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def main():
    st.title("Image Uploader")
    #Limiting only to jpg, jpeg and png files
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        #Getting the file extension
        file_path = f"temp_image.{uploaded_file.type.split('/')[-1]}"
        #Opens the file in write binary (wb) mode
        with open(file_path, "wb") as f:
            #writes the content of the uploaded file
            f.write(uploaded_file.getvalue())
        upload_image(file_path)
        os.remove(file_path)

if __name__ == "__main__":
    main()
