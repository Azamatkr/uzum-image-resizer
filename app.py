import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

TARGET_SIZE = (1080, 1440)

def resize_and_pad(img):
    return ImageOps.pad(img, TARGET_SIZE, color="white", centering=(0.5, 0.5))

st.title("Uzum Image Resizer (1080x1440)")

uploaded_files = st.file_uploader(
    "Загрузите одно или несколько изображений (JPG, PNG, WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

if uploaded_files:
    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for uploaded_file in uploaded_files:
                img = Image.open(uploaded_file).convert("RGB")
                processed_img = resize_and_pad(img)

                output_filename = f"{uploaded_file.name.rsplit('.', 1)[0]}_1080x1440.jpg"
                img_byte_arr = io.BytesIO()
                processed_img.save(img_byte_arr, format='JPEG', quality=95)
                zip_file.writestr(output_filename, img_byte_arr.getvalue())

        st.success("✅ Изображения обработаны!")
        st.download_button(
            label="📦 Скачать все как ZIP",
            data=zip_buffer.getvalue(),
            file_name="processed_images.zip",
            mime="application/zip"
        )
