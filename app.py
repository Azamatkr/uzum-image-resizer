import streamlit as st
from PIL import Image
import io
import zipfile

# Настройки
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1440
SCALE_FACTOR = 0.9
WHITE_THRESHOLD = 250  # порог для определения "достаточно белого" фона

st.set_page_config(page_title="Uzum Image Resizer", layout="centered")
st.title("🖼️ Uzum Image Resizer")
st.caption("Добавляет белый фон только к изображением без белого фона, все файлы сохраняются в корень ZIP.")

uploaded_files = st.file_uploader(
    "📤 Загрузите изображения (JPG, PNG, WEBP)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True
)

def has_white_corners(img: Image.Image) -> bool:
    """Проверяет, все ли четыре угла изображения достаточно близки к белому."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    for x, y in ((0,0), (w-1,0), (0,h-1), (w-1,h-1)):
        r, g, b = rgb.getpixel((x, y))
        # если хотя бы один канал ниже порога, считаем фон не белым
        if r < WHITE_THRESHOLD or g < WHITE_THRESHOLD or b < WHITE_THRESHOLD:
            return False
    return True

def process_image(img: Image.Image) -> Image.Image:
    """Масштабирует, а при отсутствии белого фона — добавляет паддинг."""
    # Конвертируем в RGB (на случай PNG с альфа)
    img = img.convert("RGB")
    # Определяем, нужен ли паддинг
    need_padding = not has_white_corners(img)

    # Сначала масштабируем
    max_w = int(TARGET_WIDTH * SCALE_FACTOR)
    max_h = int(TARGET_HEIGHT * SCALE_FACTOR)
    img.thumbnail((max_w, max_h), Image.LANCZOS)

    if need_padding:
        # Создаём белый фон нужного размера
        background = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), "white")
        # Центрируем
        offset = ((TARGET_WIDTH - img.width) // 2, (TARGET_HEIGHT - img.height) // 2)
        background.paste(img, offset)
        return background
    else:
        # Без паддинга — возвращаем просто масштабированное изображение
        return img

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            original = Image.open(uploaded_file)
            processed = process_image(original)

            # Сохраняем в байты
            img_bytes = io.BytesIO()
            processed.save(img_bytes, format="JPEG", quality=95)
            img_bytes.seek(0)

            # Формируем имя в ZIP
            clean_name = uploaded_file.name.rsplit(".", 1)[0]
            zip_path = f"{clean_name}_1080x1440.jpg"
            zip_file.writestr(zip_path, img_bytes.read())

            # Показываем в интерфейсе
            st.image(processed, caption=zip_path, use_container_width=True)

    zip_buffer.seek(0)
    st.download_button(
        label="📦 Скачать (без подпапок)",
        data=zip_buffer.getvalue(),
        file_name="uzum_flat.zip",
        mime="application/zip"
    )
