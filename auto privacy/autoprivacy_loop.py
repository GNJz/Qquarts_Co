import os
import glob
import time
from PIL import Image, ImageDraw, ImageFilter
import pytesseract

sensitive_keywords = ["jazzin", "quarts", "MacBookAir", "@gmail.com"]

def blur_sensitive_info(image_path, output_path):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    blurred_count = 0

    for i in range(len(data['text'])):
        word = data['text'][i]
        if any(s in word for s in sensitive_keywords):
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            region = img.crop((x, y, x + w, y + h))
            blurred = region.filter(ImageFilter.GaussianBlur(radius=5))
            img.paste(blurred, (x, y))
            blurred_count += 1

    img.save(output_path)
    print(f"\n✅ 총 {blurred_count}개의 민감 단어가 블러 처리되었습니다.")
    print(f"💾 결과 이미지: {output_path}")


def get_latest_screenshot(folder_path):
    list_of_files = glob.glob(os.path.join(folder_path, "*.png"))
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


def run_loop():
    desktop_path = os.path.expanduser("~/Desktop")
    counter = 1

    while True:
        input(f"\n📸 스크린샷 찍고 Enter 눌러줘...")

        latest_image = get_latest_screenshot(desktop_path)

        if latest_image is None:
            print("❌ PNG 이미지가 바탕화면에 없어. 다시 확인해줘!")
            continue

        output_file = os.path.join(desktop_path, f"screenshot_{counter}_blurred.png")

        try:
            blur_sensitive_info(latest_image, output_file)
        except Exception as e:
            print(f"⚠️ 흐림 처리 중 오류: {e}")

        counter += 1


if __name__ == "__main__":
    run_loop()