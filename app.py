### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(customized_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([customized_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)



goal = st.radio("Select your goal:", ("Weight Loss", "Weight Gain"))
age = st.number_input("Enter your Age",min_value=6)
submit=st.button("Detail Description")
input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of 
               every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

        you can also mention wether the food is healthy or not and also 
        mention the percentage split in carbohydrates,fats,sugar,protein,fiber and other important macro and micro nutrients
        reqiure in our diet Analyze my food or diet image to assess its suitability for acheiving {GOAL}, 
        and suggest the best alternatives or adjustments if the current food or dishes 
        are not optimal for {GOAL} and if it is optimal then provide positive feedback.
        These all result should be personalized according to user age and gender. The User's age is {AGE} year old.
        



"""
customized_prompt = input_prompt.format(GOAL=goal,AGE=age)


## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(customized_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)



