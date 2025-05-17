import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

TARGET_SIZE = (1080, 1440)

st.title("📦 Uzum Image Resizer")
st.markdown("This tool resizes all uploaded images to 1080x1440 for Uzum with white background. The full image will be preserved, and padding will be added as needed.")

uploaded_files = st.file_uploader(
    "Choose one or more images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def force_pad_no_crop(image, target_size, fill_color="white"):
    image.thumbnail(target_size, Image.LANCZOS)
    background = Image.new("RGB", target_size, fill_color)
    offset = ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2)
    background.paste(image, offset)
    return background

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Original: {uploaded_file.name}", use_column_width=True)

            resized_image = force_pad_no_crop(image, TARGET_SIZE)

            st.image(resized_image, caption="Processed (1080x1440, no crop)", use_column_width=True)

            img_bytes = io.BytesIO()
            resized_image.save(img_bytes, format="JPEG")
            img_bytes.seek(0)

            filename = f"{uploaded_file.name.rsplit('.', 1)[0]}_1080x1440.jpg"
            zip_file.writestr(filename, img_bytes.read())

    zip_buffer.seek(0)
    st.download_button(
        label="📥 Download All as ZIP",
        data=zip_buffer,
        file_name="resized_images.zip",
        mime="application/zip"
    )
