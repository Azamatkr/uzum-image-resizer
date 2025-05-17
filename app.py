import streamlit as st
from PIL import Image, ImageOps
import io

# Target size for Uzum requirements
TARGET_SIZE = (1080, 1440)

st.title("📦 Uzum Image Resizer")
st.markdown("Upload your image and we'll resize it to 1080x1440 with white padding to meet Uzum requirements.")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    # Resize with padding
    resized_image = ImageOps.pad(image, TARGET_SIZE, color="white", centering=(0.5, 0.5))
    st.image(resized_image, caption="Resized for Uzum (1080x1440)", use_column_width=True)

    # Prepare for download
    img_bytes = io.BytesIO()
    resized_image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    st.download_button(
        label="📥 Download Resized Image",
        data=img_bytes,
        file_name="resized_uzum_1080x1440.jpg",
        mime="image/jpeg"
    )
