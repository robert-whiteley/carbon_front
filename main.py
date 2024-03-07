# client.py
import requests
import streamlit as st
import numpy as np
from PIL import Image
import os
import json
import time

original_title = '<h1 style="text-align: center; font-family: san-serif; color:white; font-size: 44px;">CARBON CALCULATOR</h1>'
st.markdown(original_title, unsafe_allow_html=True)


# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://th-thumbnailer.cdn-si-edu.com/bxv2go30Qu51_mZgT_sYjsb8vCY=/1000x750/filters:no_upscale()/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/06/9c/069cfb16-c46c-4742-85f0-3c7e45fa139d/mar2018_a05_talkingtrees.jpg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;

}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)


#Server URL
#SERVER_BASE_URL = 'http://127.0.0.1:8000'
SERVER_BASE_URL = 'https://carbon-calculator-rw-klerphlnqq-ew.a.run.app/'

col_upl, col_prog = st.columns(2)


def upload_image(file_path):
    #The post endpoint
    url = SERVER_BASE_URL + "/predict"
    #Writing in the files -> image the file in binary
    files = {'image': open(file_path, 'rb')}
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            st.error("No fruit detected")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def display_cropped_img(content):
    new_image = Image.fromarray(np.array(json.loads(content['image_cropped']), dtype='uint8'))
    return new_image

def main():
    #Limiting only to jpg, jpeg and png files
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


    if uploaded_file:
        #Getting the file extension
        file_path = f"temp_image.{uploaded_file.type.split('/')[-1]}"
        #Opens the file in write binary (wb) mode
        with open(file_path, "wb") as f:
            #writes the content of the uploaded file
            f.write(uploaded_file.getvalue())
        content_json = upload_image(file_path)
        os.remove(file_path)
        cropped_image = display_cropped_img(content_json)

        with st.empty():
            bar = st.progress(0.2)
            num = 2
            for i in range(num+1):
                bar.progress((100//num)*i)
                time.sleep(1)

        key = list(content_json['message'].keys())[0]
        value = content_json['message'][key]
        fruit = key.capitalize()
        description = 'Oranges coming from Spain blablabla'
        col1, col2 = st.columns(2)

        col1.subheader('Image Uploaded')
        col1.image(uploaded_file)

        col2.subheader(f'Fruit Detected: {fruit}')
        col2.subheader(f"CO2: {value} kg per 1kg of {fruit}s")
        col2.image(cropped_image, width=120)




if __name__ == "__main__":

    main()
