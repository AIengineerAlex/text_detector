import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import anthropic
import os 

def get_images_base64(image):
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


client = anthropic.Anthropic(api_key='YOUR API')

st.title('文字起こし')
st.write("画像をアップロードしてください、アップロードしにかいてあるものを読みます")
uploaded_image = st.file_uploader("画像を選択...",type=["png","jpg","jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption= 'アップロードされた画像',use_column_width=True)
    image_base64 = get_images_base64(image)

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="アップロードされた画像の文字起こしをしてください",
        messages=[
            {
                "role":"user",
                "content":[
                    {
                        "type":"image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data":image_base64
                        }
                    }
                ]
            }
        ]

    )

    st.write(message.content[0].text)
                        
