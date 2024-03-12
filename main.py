# client.py
import requests
import streamlit as st
import numpy as np
from PIL import Image
import os
import json
import time

# background
bg = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1528200575999-1853e416cf07?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(bg, unsafe_allow_html=True)

# title
original_title = '<h1 style="text-align: center; background:#b9c2bd; border-radius: 20px; font-family: Helvetica; color:#24744d; font-size: 44px;">CARBON CALCULATOR</h1>'
st.markdown(original_title, unsafe_allow_html=True)
st.divider()

#Server URL
#SERVER_BASE_URL = 'http://127.0.0.1:8000'
SERVER_BASE_URL = 'https://carbon-calculator-mk1-klerphlnqq-ew.a.run.app'

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
            # st.error("No fruit detected")
            subhea = f"<p style='font-family: Arial; background:#b9c2bd; text-align: center; border-radius: 12px; font-family: Helvetica; color:#24744d; font-size: 25px;'>Upload error - Try again</p>"
            st.markdown(subhea, unsafe_allow_html=True)
            st.stop()
    except Exception as e:
        subhea = f"<p style='font-family: Arial; background:#b9c2bd; text-align: center; border-radius: 12px; font-family: Helvetica; color:#24744d; font-size: 25px;'>Upload error - Try again</p>"
        st.markdown(subhea, unsafe_allow_html=True)
        # st.error(f"Error: {str(e)}")
        st.stop()



def display_cropped_img(content):
    new_image = Image.fromarray(np.array(json.loads(content['image_cropped']), dtype='uint8'))
    return new_image

def main():
    #Limiting only to jpg, jpeg and png files
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], label_visibility='collapsed')

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
        #description = 'Oranges coming from Spain blablabla'
        col1, col2 = st.columns(2)

        with col1:
            subhea = "<p style='font-family: Arial; background:#b9c2bd; text-align: center; border-radius: 12px; font-family: Helvetica; color:#24744d; font-size: 25px;'>Image Uploaded</p>"
            st.markdown(subhea, unsafe_allow_html=True)
            st.image(uploaded_file)

        with col2:
            txt_to_show = 'Fruit Detected: ' + fruit
            subhea = f"<p style='font-family: Arial; background:#b9c2bd; text-align: center; border-radius: 12px; font-family: Helvetica; color:#24744d; font-size: 25px;'>{txt_to_show}</p>"
            st.markdown(subhea, unsafe_allow_html=True)

            st.image(cropped_image, width=200)

            txt_to_show2 = f"CO2: {value} kg per 1kg of {fruit}"
            subhea2 = f"<p style='font-family: Arial; background:#b9c2bd; text-align: center; border-radius: 12px; font-family: Helvetica; color:#24744d; font-size: 25px;'>{txt_to_show2}</p>"
            st.markdown(subhea2, unsafe_allow_html=True)

            # st.subheader(f"CO2: {value} kg per 1kg of {fruit}s")



        st.divider()




if __name__ == "__main__":

    main()
