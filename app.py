import streamlit as st
from PIL import Image, ImageOps
import io

# Target size for Uzum requirements
TARGET_SIZE = (1080, 1440)

st.title("📦 Uzum Image Resizer")
st.markdown("Upload one or more images. They will be resized to 1080x1440 with white padding to meet Uzum requirements.")

uploaded_files = st.file_uploader(
    "Choose one or more images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Original: {uploaded_file.name}", use_column_width=True)

        # Resize with padding
        resized_image = ImageOps.pad(image, TARGET_SIZE, color="white", centering=(0.5, 0.5))
        st.image(resized_image, caption="Resized (1080x1440)", use_column_width=True)

        # Prepare for download
        img_bytes = io.BytesIO()
        resized_image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        st.download_button(
            label=f"📥 Download: {uploaded_file.name}_1080x1440.jpg",
            data=img_bytes,
            file_name=f"{uploaded_file.name}_1080x1440.jpg",
            mime="image/jpeg"
        )
