# 건설 현장 안전 장비 객체 탐지

## 모델 및 학습 파라미터 (Model & Training Configuration)

| 항목 (Parameter) | 세부 사양 (Details) |
| --- | --- |
| **기반 모델 (Model)** | `YOLOv8n, YOLOv8s` (Ultralytics v8.4.132) |
| **데이터셋 (Dataset)** | Kaggle `construction-site-safety-image-dataset-roboflow` (v3) |
| **입력 크기 (Image Size)** | `800 x 800` |
| **배치 크기 (Batch Size)** | `16` |
| **에폭 (Epochs)** | `50` |

---

## 데이터셋 및 클래스 명세 (Dataset & Classes)

- **데이터 분할 (Split)**: Train `2,605`장 / Validation `114`장 / Test 이미지
- **탐지 클래스 (10 Classes)**:
  - `0: Hardhat` (안전모)
  - `1: Mask` (마스크)
  - `2: NO-Hardhat` (안전모 미착용)
  - `3: NO-Mask` (마스크 미착용)
  - `4: NO-Safety Vest` (안전조끼 미착용)
  - `5: Person` (사람/작업자)
  - `6: Safety Cone` (안전 삼각뿔)
  - `7: Safety Vest` (안전조끼)
  - `8: machinery` (건설 기계)
  - `9: vehicle` (차량)

---

## 추론 결과 (Inference Result)

### yolo8n
<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/e5beebfd-81b2-4660-a27d-18426d88c9c6" />

### yolo8n + Augumentation
<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/ebd7109b-9546-4bda-a3c4-079e9e5f5d4b" />

### yolo8s
<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/9fa3d122-e293-4325-985f-88f83eeab50a" />

### yolo8s + Augumentation
<img width="1189" height="590" alt="image" src="https://github.com/user-attachments/assets/f5a8dad4-7a2e-4f7d-9799-9a681b80a8c8" />
