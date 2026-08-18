import os
import cv2
import numpy as np
from PIL import Image
from datasets import load_from_disk

def preprocessing(image:np.ndarray)->np.ndarray:
    """
    이미지를 입력받아 크기 조정, 노이즈 제거, 데이터 증강, 흑백 변환, 정규화를 수행

    Args:
        image(np.ndarray): OpenCV BGR 이미지 객체 (uint8)

    Returns:
        normalized(np.ndarray): 전처리 및 정규화가 완료된 흑백 이미지 (float32, 0.0 ~ 1.0)
    """

    # 1. 이미지 크기 조정 (224x224)
    resized = cv2.resize(image, (224, 224))

    # 2. 가우시안 필터를 이용한 노이즈 제거
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)

    # 3. 0.5의 확률로 좌우 반전
    if np.random.rand() > 0.5:
        blurred = cv2.flip(blurred, 1)

    # 4. 무작위 회전 (-15도 ~ +15도)
    angle = np.random.uniform(-15.0, 15.0)
    h, w = blurred.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    blurred = cv2.warpAffine(blurred, rotation_matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

    # 5. 밝기 및 대비 무작위 조절
    alpha = np.random.uniform(0.8, 1.2)
    beta = np.random.randint(-30, 30)
    blurred = cv2.convertScaleAbs(blurred, alpha=alpha, beta=beta)

    # 6. 흑백(GrayScale)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

    # 7. 정규화 (0.0 ~ 1.0)
    normalized = gray.astype(np.float32) / 255.0

    return normalized

# 데이터 가져오기
ds = load_from_disk("./my_food101")

# 출력할 폴더 생성
output_dir = "./preprocessed_samples"
os.makedirs(output_dir, exist_ok=True)

for i, item in enumerate(ds["train"]):
    if i >= 5: # 5번만 반복
        break
    
    image = item["image"]
    image.save(f"{output_dir}/original_image_{i}.jpg") # 원본 이미지 저장

    # numpy형태로 전달한 뒤 다시 pillow로 변경
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    result = preprocessing(image_bgr)
    img_uint8 = (result * 255).astype(np.uint8)
    pil_image = Image.fromarray(img_uint8)

    # 전처리된 이미지 저장
    pil_image.save(f"{output_dir}/preprocessed_image_{i}.jpg")

print(f"이미지가 '{output_dir}' 폴더에 저장되었습니다!")