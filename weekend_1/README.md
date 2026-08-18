# 이미지 전처리 및 증강 파이프라인

## 주요 전처리 과정 (Pipeline steps)

| 단계 | Process | Details |
| --- | --- | --- |
| 1 | 크기 조정 | `(224, 224)`크기로 이미지 변경 |
| 2 | 노이즈 제거 | 가우시안 필터(`Kernal: 5x5`) 적용 |
| 3 | 좌우 반전 | 50% 확률로 수평 반전 |
| 4 | 무작위 회전 | -15 ~ +15 범위 내 회전(`BORDER_REFLECT` 처리) |
| 5 | 색상/밝기 변환 | 대비($\alpha$ : 0.8 ~ 1.2), 밝기($\beta$ : -30 ~ 30) 무작위 조절 |
| 6 | 흑백 변환 | BGR채널을 단일 채널(Grayscale)로 변환 |
| 7 | 정규화 | `float32` 형변환 후 `0.0 ~ 1.0` 범위로 스케일링 |

## 입출력 데이터 명세 (Input / Output Specs)
- Input: `numpy.ndarray` (Shape: `(H, W, 3)`, dtype: `uint8`, BGR Color)

- Output: `numpy.ndarray` (Shape: `(224, 224)`, dtype: `float32`, Value range: `0.0 ~ 1.0`)

## 전처리 결과 (Result)

| 원본 | 결과 |
| --- | --- |
| <img width="384" height="512" alt="original_image_0" src="https://github.com/user-attachments/assets/34774318-ed10-4ff7-b927-56d38254e05c" /> | <img width="224" height="224" alt="preprocessed_image_0" src="https://github.com/user-attachments/assets/76d7f518-3598-4a68-8c34-156c20059915" /> |
| <img width="512" height="512" alt="original_image_1" src="https://github.com/user-attachments/assets/42a85d29-8940-4706-9395-45d9477ec8d3" /> | <img width="224" height="224" alt="preprocessed_image_1" src="https://github.com/user-attachments/assets/cac47e9e-85f0-46bf-af58-19837cff2d41" /> |
| <img width="512" height="383" alt="original_image_2" src="https://github.com/user-attachments/assets/105ef0bd-6798-469a-b898-9c449aa73c62" /> | <img width="224" height="224" alt="preprocessed_image_2" src="https://github.com/user-attachments/assets/b60f1e9d-427e-475c-b8fd-cf77113b4a04" /> |
| <img width="512" height="348" alt="original_image_3" src="https://github.com/user-attachments/assets/2c9931d5-bcc4-4238-9642-ab4490f52945" /> | <img width="224" height="224" alt="preprocessed_image_3" src="https://github.com/user-attachments/assets/44ae299c-a5a5-401e-8132-753be57cf1f3" /> |
| <img width="512" height="512" alt="original_image_4" src="https://github.com/user-attachments/assets/ab6532f1-fdb3-4daa-8b3c-dc0803935ec6" /> | <img width="224" height="224" alt="preprocessed_image_4" src="https://github.com/user-attachments/assets/f5df294f-0526-4892-94af-b127a5c3646d" /> |