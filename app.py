import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

TARGET_SIZE = (1080, 1440)

st.title("📦 Uzum Image Resizer")
st.markdown("Resize images to 1080x1440 for Uzum. Choose one of the resize modes below:")

fit_mode = st.radio("Choose resize mode:", [
    "Smart Fit (less padding)",
    "Full Fit (white padding)",
    "Force Pad (always white sides if needed)"
])

uploaded_files = st.file_uploader(
    "Choose one or more images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def force_pad_to_target(image, target_size, fill_color="white"):
    img_ratio = image.width / image.height
    target_ratio = target_size[0] / target_size[1]

    if img_ratio > target_ratio:
        # Image is too wide — fit height and pad left/right
        new_height = target_size[1]
        new_width = round(new_height * img_ratio)
    else:
        # Image is too tall — fit width and pad top/bottom
        new_width = target_size[0]
        new_height = round(new_width / img_ratio)

    image_resized = image.resize((new_width, new_height), Image.LANCZOS)
    background = Image.new("RGB", target_size, fill_color)
    offset = ((target_size[0] - new_width) // 2, (target_size[1] - new_height) // 2)
    background.paste(image_resized, offset)
    return background

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Original: {uploaded_file.name}", use_column_width=True)

            if fit_mode == "Full Fit (white padding)":
                resized_image = ImageOps.pad(image, TARGET_SIZE, color="white", centering=(0.5, 0.5))
            elif fit_mode == "Smart Fit (less padding)":
                resized_image = ImageOps.fit(image, TARGET_SIZE, centering=(0.5, 0.5))
            else:  # Force Pad Mode
                resized_image = force_pad_to_target(image, TARGET_SIZE)

            st.image(resized_image, caption=f"Processed ({fit_mode})", use_column_width=True)

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
