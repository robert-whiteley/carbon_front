# client.py
import requests
import streamlit as st
import numpy as np
from PIL import Image
import os
import json


#Server URL
SERVER_BASE_URL = 'https://carbon-calculator-rw-klerphlnqq-ew.a.run.app'

def upload_image(file_path):
    #The post endpoint
    url = SERVER_BASE_URL + "/predict"
    #Writing in the files -> image the file in binary
    files = {'image': open(file_path, 'rb')}
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            st.success("Image uploaded successfully")
            content_json = json.loads(response.content.decode('utf-8'))
            cropped_image = display_cropped_img(content_json)
            st.image(cropped_image, width=250)
            content_json['message']
        else:
            st.error("Failed to upload image")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def display_cropped_img(content):
    new_image = Image.fromarray(np.array(json.loads(content['image_cropped']), dtype='uint8'))
    return new_image

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
