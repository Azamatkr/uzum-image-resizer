import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

# Target size for Uzum requirements
TARGET_SIZE = (1080, 1440)

st.title("📦 Uzum Image Resizer")
st.markdown("""Upload one or more images (jpg, png, webp). They will be resized to 1080x1440 with white padding.
After processing, you can download all the results as a ZIP archive.""")

uploaded_files = st.file_uploader(
    "Choose one or more images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Original: {uploaded_file.name}", use_column_width=True)

            # Resize with padding
            resized_image = ImageOps.pad(image, TARGET_SIZE, color="white", centering=(0.5, 0.5))
            st.image(resized_image, caption="Resized (1080x1440)", use_column_width=True)

            # Save to memory
            img_bytes = io.BytesIO()
            resized_image.save(img_bytes, format="JPEG")
            img_bytes.seek(0)

            # Add to ZIP
            filename = f"{uploaded_file.name.rsplit('.', 1)[0]}_1080x1440.jpg"
            zip_file.writestr(filename, img_bytes.read())

    zip_buffer.seek(0)
    st.download_button(
        label="📥 Download All as ZIP",
        data=zip_buffer,
        file_name="resized_images.zip",
        mime="application/zip"
    )
