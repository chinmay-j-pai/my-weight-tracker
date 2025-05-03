
import streamlit as st
from PIL import Image
from ocr_utils import process_image
from firebase_utils import store_result

st.set_page_config(page_title="Weight OCR", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧮 Digital Weighing OCR</h1>", unsafe_allow_html=True)
st.markdown("### 📷 Capture the weight display:")

image_data = st.camera_input("Align the display within the box below 👇")

if image_data:
    with st.spinner("Reading..."):
        # ocr_value, cropped_img = process_image(Image.open(image_data))
        ocr_value, cropped_img, morph_img, sharpened_img, boxed = process_image(Image.open(image_data))

        st.image(cropped_img, caption="Cropped Region", use_container_width=True)
        st.image(morph_img, caption="Morphological Close", use_container_width=True)
        st.image(sharpened_img, caption="Sharpened Morph", use_container_width=True)
        # st.image(thresh_img, caption="Thesholded image", use_container_width=True)
        st.image(boxed, caption="OCR with Bounding Boxes", use_container_width=True)
        st.write("**OCR Result:**", ocr_value)

        st.image(cropped_img, caption="Cropped OCR Area", use_container_width=True)

    st.markdown("### ✍️ Edit & Confirm")
    edited = st.text_input("Predicted Weight:", value=ocr_value)

    if st.button("✅ Store Result"):
        store_result(edited)
        st.success(f"Stored: {edited} kg")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Built with ❤️ using Streamlit + EasyOCR + Firebase</p>", unsafe_allow_html=True)
