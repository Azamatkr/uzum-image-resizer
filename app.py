import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

# Константы
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1440
TARGET_SIZE = (TARGET_WIDTH, TARGET_HEIGHT)
SCALE_FACTOR = 0.9  # Отдаление (90% от холста)

st.set_page_config(page_title="Uzum Image Resizer", layout="centered")
st.title("🖼️ Uzum Image Resizer (1080x1440 with padding)")
st.caption("Загрузите изображения. Мы отдалим их и поместим на белый фон 1080×1440 (соотношение 3:4) — так, как требует Uzum.")

uploaded_files = st.file_uploader(
    "📤 Загрузите одно или несколько изображений (JPG, PNG, WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def resize_and_pad(image):
    image = image.convert("RGB")
    target_inner_width = int(TARGET_WIDTH * SCALE_FACTOR)
    target_inner_height = int(TARGET_HEIGHT * SCALE_FACTOR)
    image.thumbnail((target_inner_width, target_inner_height), Image.LANCZOS)

    background = Image.new("RGB", TARGET_SIZE, "white")
    offset = ((TARGET_WIDTH - image.width) // 2, (TARGET_HEIGHT - image.height) // 2)
    background.paste(image, offset)
    return background

if uploaded_files:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            processed = resize_and_pad(image)

            img_bytes = io.BytesIO()
            processed.save(img_bytes, format="JPEG", quality=95)
            img_bytes.seek(0)

            filename = f"{uploaded_file.name.rsplit('.', 1)[0]}_1080x1440.jpg"
            zip_file.writestr(filename, img_bytes.read())

            st.image(processed, caption=filename, use_container_width=True)

    zip_buffer.seek(0)
    st.download_button(
        label="📥 Скачать все изображения (ZIP)",
        data=zip_buffer,
        file_name="uzum_images.zip",
        mime="application/zip"
    )
