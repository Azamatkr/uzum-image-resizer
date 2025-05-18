import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile

# Настройки
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1440
SCALE_FACTOR = 0.9

st.set_page_config(page_title="Uzum Image Resizer", layout="centered")
st.title("🖼️ Uzum Image Resizer")
st.caption("Изображения уменьшаются и центрируются на белом фоне 1080×1440. Все файлы сохраняются в корень ZIP.")

uploaded_files = st.file_uploader(
    "📤 Загрузите изображения разных наборов (JPG, PNG, WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def resize_and_pad(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    max_w = int(TARGET_WIDTH * SCALE_FACTOR)
    max_h = int(TARGET_HEIGHT * SCALE_FACTOR)
    image.thumbnail((max_w, max_h), Image.LANCZOS)
    background = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), "white")
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

            clean_name = uploaded_file.name.rsplit(".", 1)[0]
            zip_path = f"{clean_name}_1080x1440.jpg"
            zip_file.writestr(zip_path, img_bytes.read())

            st.image(processed, caption=zip_path, use_container_width=True)

    zip_buffer.seek(0)
    st.download_button(
        label="📦 Скачать всё (без папок)",
        data=zip_buffer.getvalue(),
        file_name="uzum_flat.zip",
        mime="application/zip"
    )
