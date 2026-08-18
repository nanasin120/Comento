from datasets import load_from_disk
import os

ds = load_from_disk("./my_food101")

output_dir = "./food101_images"
os.makedirs(output_dir, exist_ok=True)

# 3. 데이터셋에서 이미지 추출해서 저장 (예: 처음 20개 저장)
for i, item in enumerate(ds["train"]):
    if i >= 20:  # 원하시는 개수만큼 조절 가능합니다.
        break
    
    image = item["image"]  # PIL Image 객체
    label = item["label"]  # 클래스 번호
    
    # jpg 파일로 저장
    image.save(f"{output_dir}/image_{i}_label_{label}.jpg")

print(f"이미지가 '{output_dir}' 폴더에 저장되었습니다!")