import streamlit as st
from PIL import Image
import io
import zipfile

# Константы
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1440
SCALE_FACTOR = 0.9

st.set_page_config(page_title="Uzum Image Resizer", layout="centered")
st.title("🖼️ Uzum Image Resizer")
st.caption("Изображения масштабируются до 90% и всегда центрируются на белом фоне 1080×1440.")

# Загрузчик файлов
uploaded_files = st.file_uploader(
    "📤 Загрузите изображения (JPG, PNG, WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def process_image(img: Image.Image) -> Image.Image:
    """
    Масштабирует изображение до 90% от целевого,
    и помещает его в центр белого холста 1080×1440.
    """
    img = img.convert("RGB")
    max_w = int(TARGET_WIDTH * SCALE_FACTOR)
    max_h = int(TARGET_HEIGHT * SCALE_FACTOR)
    img.thumbnail((max_w, max_h), Image.LANCZOS)
    bg = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), "white")
    offset = ((TARGET_WIDTH - img.width) // 2, (TARGET_HEIGHT - img.height) // 2)
    bg.paste(img, offset)
    return bg

if uploaded_files:
    zip_buffer = io.BytesIO()
    processed = []

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for up in uploaded_files:
            img = Image.open(up)
            out = process_image(img)

            bts = io.BytesIO()
            out.save(bts, format="JPEG", quality=95)
            bts.seek(0)

            name = up.name.rsplit(".", 1)[0]
            zip_path = f"{name}_1080x1440.jpg"
            zip_file.writestr(zip_path, bts.read())

            processed.append((zip_path, out))

    zip_buffer.seek(0)

    # Кнопка скачивания вверху
    st.download_button(
        label="📦 Скачать все изображения (flat)",
        data=zip_buffer.getvalue(),
        file_name="uzum_images.zip",
        mime="application/zip"
    )

    # Превью изображений
    for caption, img in processed:
        st.image(img, caption=caption, use_container_width=True)
