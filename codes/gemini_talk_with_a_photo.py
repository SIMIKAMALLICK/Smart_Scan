import os
import io
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from PIL import Image

# Load environment variables
load_dotenv(find_dotenv())

# Function to convert Streamlit image upload to PIL Image
def st_image_to_pil(st_image):
    image_data = st_image.read()
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image

# Function to send prompt and image to Gemini model and get a response
def ask_and_get_answer(prompt, img):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt, img])
    return response.text

# application entry point
if __name__ == '__main__':
    # configure Gemini
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

    # UI components
    st.markdown("<h3 style='text-align: center;'>Your Image Has Something to Say 🤫</h3>", unsafe_allow_html=True)
    st.image('logo.png', width=500)

    img = st.file_uploader('Select an Image: ', type=['jpg', 'jpeg', 'png', 'gif'])

    if img:
        st.image(img, caption='Talk with this image.')

        prompt = st.text_area('Ask a question about this image :)')

        if prompt:
            pil_image = st_image_to_pil(img)

            with st.spinner('Running...'):
                answer = ask_and_get_answer(prompt, pil_image)
                st.text_area('Gemini Answer:', value=answer)

            st.divider()

            if 'history' not in st.session_state:
                st.session_state.history = ''

            value = f'Q: {prompt} \n\n A: {answer}'
            st.session_state.history = f'{value} \n\n {"-" * 100} \n\n {st.session_state.history}'

            # Show chat history
            h = st.session_state.history
            st.text_area(label='Chat History', value=h, height=480, key='history')
