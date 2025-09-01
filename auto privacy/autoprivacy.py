
from PIL import Image, ImageDraw, ImageFilter
import pytesseract

# 민감한 단어 리스트
sensitive_keywords = ["jazzin", "quarts", "MacBookAir", "@gmail.com"]

# 이미지 로딩
try:
    img = Image.open("screenshot.png")
    print("✅ 이미지 불러오기 성공")
except FileNotFoundError:
    print("❌ 이미지 파일을 찾을 수 없습니다. 경로를 확인하세요.")
    exit()

draw = ImageDraw.Draw(img)

# OCR로 텍스트 추출 및 위치 파악
try:
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    print("✅ OCR 데이터 추출 성공")
except Exception as e:
    print("❌ OCR 실패:", e)
    exit()

count = 0
for i in range(len(data['text'])):
    word = data['text'][i]
    if any(s in word for s in sensitive_keywords):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        print(f"🔍 민감 단어 '{word}' 발견 → 위치: ({x}, {y}, {w}, {h})")
        region = img.crop((x, y, x + w, y + h))
        blurred = region.filter(ImageFilter.GaussianBlur(radius=5))
        img.paste(blurred, (x, y))
        count += 1

print(f"🎉 총 {count}개의 민감 단어가 블러 처리되었습니다.")

img.save("screenshot_blurred.png")
print("💾 블러 처리된 이미지가 'screenshot_blurred.png'로 저장되었습니다.")