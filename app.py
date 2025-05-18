import streamlit as st
from PIL import Image
import io
import zipfile

# Настройки
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1440
SCALE_FACTOR = 0.9
WHITE_THRESHOLD = 250  # порог для определения белого фона

st.set_page_config(page_title="Uzum Image Resizer", layout="centered")
st.title("🖼️ Uzum Image Resizer")
st.caption("Добавляет белый фон только если фон не белый, сохраняет все изображения в один ZIP без папок.")

uploaded_files = st.file_uploader(
    "📤 Загрузите изображения (JPG, PNG, WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def has_white_corners(img: Image.Image) -> bool:
    rgb = img.convert("RGB")
    w, h = rgb.size
    for x, y in ((0,0), (w-1,0), (0,h-1), (w-1,h-1)):
        r, g, b = rgb.getpixel((x, y))
        if r < WHITE_THRESHOLD or g < WHITE_THRESHOLD or b < WHITE_THRESHOLD:
            return False
    return True

def process_image(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    need_padding = not has_white_corners(img)
    max_w = int(TARGET_WIDTH * SCALE_FACTOR)
    max_h = int(TARGET_HEIGHT * SCALE_FACTOR)
    img.thumbnail((max_w, max_h), Image.LANCZOS)
    if need_padding:
        bg = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), "white")
        offset = ((TARGET_WIDTH - img.width) // 2, (TARGET_HEIGHT - img.height) // 2)
        bg.paste(img, offset)
        return bg
    else:
        return img

if uploaded_files:
    # Сначала обрабатываем и сохраняем в ZIP в памяти
    zip_buffer = io.BytesIO()
    processed_images = []  # для показа
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded in uploaded_files:
            img = Image.open(uploaded)
            proc = process_image(img)

            img_bytes = io.BytesIO()
            proc.save(img_bytes, format="JPEG", quality=95)
            img_bytes.seek(0)

            name = uploaded.name.rsplit(".", 1)[0]
            zip_path = f"{name}_1080x1440.jpg"
            zip_file.writestr(zip_path, img_bytes.read())

            processed_images.append((zip_path, proc))

    zip_buffer.seek(0)

    # Кнопка скачивания — теперь сверху
    st.download_button(
        label="📦 Скачать все изображения (без папок)",
        data=zip_buffer.getvalue(),
        file_name="uzum_flat.zip",
        mime="application/zip"
    )

    # После кнопки показываем миниатюры
    for zip_path, proc in processed_images:
        st.image(proc, caption=zip_path, use_container_width=True)
