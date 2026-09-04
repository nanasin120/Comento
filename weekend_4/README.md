# 눈 깜빡임을 통한 모스부호 인식

웹캠 영상을 실시간으로 분석하여 사용자의 눈 깜빡임 지속 시간을 측정하고, 이를 모스부호로 변환하여 텍스트를 출력하는 컴퓨터 비전 프로젝트입니다.

---

## 프로젝트 소개
- **목적:** 손을 사용하기 어려운 사용자를 위한 보조 입력 수단 및 실시간 비전 기반 인터페이스 프로토타입 구현
- **동작 방식:**
  1. 웹캠 프레임에서 **YOLOv8** 모델을 활용해 실시간 눈 상태(`closed_eye`, `open_eye`) 감지
  2. 눈 감김 지속 시간을 측정하여 점(`.`), 선(`-`) 판정
  3. 터미널 및 화면에 실시간 번역 결과 출력

---

## 기술 스택 (Tech Stack)
- **Language:** Python 3.10+
- **Computer Vision / Deep Learning:** OpenCV, Ultralytics YOLOv8
- **Testing & Quality:** PyTest
- **Version Control:** Git, GitHub

---

## 사용 데이터셋
- **데이터셋명:** Open_closed_eyes_and_yawning_labelled
- **작성자 (Author):** AryanSharma8911
- **링크:** [Kaggle Dataset 바로가기](https://www.kaggle.com/datasets/aryansharma8911/open-closed-eyes-and-yawning-labelled/data)
- **라이선스:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **클래스 구성:** `0: closed_eye`, `1: open_eye`, `2: yawning` (약 33,000장 학습셋 활용)

## 환경 구성
```python
# 1. 가상환경 생성
conda create -n eye-morse python=3.10 -y

# 2. 가상환경 활성화
conda activate eye-morse

# 3. 필수 패키지 설치
pip install ultralytics opencv-python pytest
```

## 실행 방법
```python
# Comento/weekend_4 디렉토리로 이동
cd weekend_4

# test_webcam 실행 방법
python main.py

# unittest 실행 방법
python -m pytest
```

# 실행 영상

![데모 시연](https://raw.githubusercontent.com/nanasin120/Comento/main/weekend_4/play.gif)
