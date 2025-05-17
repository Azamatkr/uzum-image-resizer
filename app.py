from PIL import Image
import os

TARGET_SIZE = (1080, 1440)
SCALE_RATIO = 0.9

def process_and_save_image(input_path, output_path):
    with Image.open(input_path) as img:
        scaled_size = (int(TARGET_SIZE[0] * SCALE_RATIO), int(TARGET_SIZE[1] * SCALE_RATIO))
        img.thumbnail(scaled_size, Image.LANCZOS)

        background = Image.new("RGB", TARGET_SIZE, "white")
        offset = ((TARGET_SIZE[0] - img.size[0]) // 2, (TARGET_SIZE[1] - img.size[1]) // 2)
        background.paste(img, offset)

        background.save(output_path, format="JPEG", quality=95)

if __name__ == "__main__":
    import sys
    from pathlib import Path

    input_folder = Path("input")
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)

    for file in input_folder.glob("*.*"):
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            out_path = output_folder / f"{file.stem}_1080x1440.jpg"
            process_and_save_image(file, out_path)
            print(f"✅ {file.name} -> {out_path.name}")
