# client.py
import requests
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import os
import json
import time
import plotly.express as px

#general font
st.markdown(
        """
        <style>
@font-face {
  font-family: Monserrat;
  font-style: semibold;
}
    html, body, [class*="css"]  {
    font-family: Monserrat;
    font-style: semibold;
    }
    </style>

    """, unsafe_allow_html=True)

# background
bg = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://www.cfp.energy/img/Admin/blog_image/20231220_BLOG_1703066789.png");
    background-size: 100vw 100vh;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(bg, unsafe_allow_html=True)

# title
original_title = '''
<h1 style="text-align: center;
box-shadow: rgba(0, 0, 0, 0.56) 0px 22px 70px 4px;
font-family: Montserrat, semibold; color:white; font-size: 56px;
">CARBON CALCULATOR</h1>
'''
st.markdown(original_title, unsafe_allow_html=True)

# Sub title
sub_title = '''
<h1 style="text-align: center;
padding: 1rem;
box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
font-family: Montserrat, semibold; color:white; font-size: 20px;
">Consume better - Reduce your carbon footprint</h1>
'''
st.markdown(sub_title, unsafe_allow_html=True)

st.divider()

#Server URL
SERVER_BASE_URL = 'https://carbon-calculator-mk1-klerphlnqq-ew.a.run.app'

#DRY Func
def show_carb_det(txt):
    sub_title = f'''
    <h1 style="text-align: left;
    padding: 1rem;
    box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
    font-family: Montserrat, semibold; color:white; font-size: 16px;
    ">{txt}</h1>
    '''
    st.markdown(sub_title, unsafe_allow_html=True)

def dec_to_t(decimal):
    time = decimal
    hours = int(time)
    minutes = int((time*60) % 60)
    tv = f'{hours}h{minutes}'
    return tv

def show_subheader(txt):
    subhea = f"<p style='box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px; background:#b9c2bd; text-align: center; border-radius: 8px; font-family: Montserrat, semibold; color:#24744d; font-size: 24px;'>{txt}</p>"
    st.markdown(subhea, unsafe_allow_html=True)

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
            st.stop()
    except Exception as e:
        show_subheader('Upload error - Try again')
        st.stop()

def display_cropped_img(content):
    new_image = Image.fromarray(np.array(json.loads(content['image_cropped']), dtype='uint8'))
    return new_image

def more_info():
    st.divider()
    sub_title = '''
    <h1 style="
    box-shadow: rgb(0 0 0 / 20%) 0px 2px 1px -1px, rgb(0 0 0 / 14%) 0px 1px 1px 0px, rgb(0 0 0 / 12%) 0px 1px 3px 0px;
    font-family: Montserrat, semibold; color:white; font-size: 24px;
    ">About the project</h1>
    '''
    st.markdown(sub_title, unsafe_allow_html=True)

    txt = 'The Carbon Calculator project aims to raise awareness about carbon emissions and help estimate carbon footprint of vegetables and fruits. By analysing live stream footage, the system can identify fruits and vegetables, providing valuable insights into environmental impact.'
    subhea = f"<p style='text-align: center; width: 720px; height: 112px; background:#1c1c1c; padding: 1rem; border-radius: 8px; font-family: Montserrat, semibold; color:white; font-size: 16px;'>{txt}</p>"

    st.markdown(subhea, unsafe_allow_html=True)

# Optionals
def devTeam(name,pic,link):
    a = pic
    st.header(name)
    st.image("logo.png",width=240)
    st.link_button('Linkedin',link)

def team():
    on = st.toggle('Meet our team')

    if on:
        col1, col2, col3 = st.columns(3)

        with col1:
            devTeam('mat','a','http://www.google.com')
            devTeam('mat','a','http://www.google.com')

        with col2:
            devTeam('mat','a','http://www.google.com')
            devTeam('mat','a','http://www.google.com')

        with col3:
            devTeam('mat','a','http://www.google.com')
            st.divider()
            st.divider()
            st.divider()
            show_subheader('Thank you')

# MAIN MAIN
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
        #loading bar

        with st.empty():
            bar = st.progress(0.2)
            num = 2
            for i in range(num+1):
                bar.progress((100//num)*i)
                time.sleep(1)

        key = list(content_json['message'].keys())[0]
        fruit = key.capitalize()

        value = content_json['message'][key]
        value = float(round(value, 1))*1000

        #description = 'Oranges coming from Spain blablabla'
        col1, col2 = st.columns(2)

        with col1:
            show_subheader('Image Uploaded')
            st.image(uploaded_file)

        with col2:
            txt_to_show = 'Fruit Detected: ' + fruit
            show_subheader(txt_to_show)

            st.image(cropped_image, width=200)
            txt_to_show2 = f"CO2: {value} grams/kilo of {fruit}"
            show_subheader(txt_to_show2)

        # SHOW GRAPH

        miles_driven = float(round(value/400, 1))
        chatgpt = value/140
        tv_watch = value/90

        nme = ["Miles", "ChatGPT", "TV"]
        scr = [miles_driven, chatgpt, tv_watch]
        df = pd.DataFrame({'name': nme, 'CO2': scr})

        fig = px.bar(df, x="CO2", y="name", orientation='h',title='Comparison')
        st.write(fig)

        # container = st.container(border=True)
        # container.write(f'{miles_driven} miles by car')
        # container.write(f'ChatGPT usage : {dec_to_t(chatgpt)}')
        # container.write(f'TV watch time : {dec_to_t(tv_watch)}')

        show_carb_det(f'{miles_driven} miles by car')
        show_carb_det(f'ChatGPT usage : {dec_to_t(chatgpt)}')
        show_carb_det(f'TV watch time : {dec_to_t(tv_watch)}')



if __name__ == "__main__":
    main()
    more_info()
    # team()
