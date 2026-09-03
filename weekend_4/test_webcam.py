import cv2
from ultralytics import YOLO
from core.decoder import MorseDecoder

def main():
    # 모델 로드
    model = YOLO(r"weekend_4\yolo\weights\best.pt")

    # 0번 기본 웹캠 열기
    cap = cv2.VideoCapture(0)

    # 카메라 연결 확인
    if not cap.isOpened():
        print("에러: 웹캠을 열 수 없습니다. 카메라 연결 상태를 확인하세요.")
        return

    # 해상도 설정 (640x480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    decoder = MorseDecoder()

    print("웹캠이 실행되었습니다. 종료하려면 'q' 키를 누르세요.")

    while True:
        # 프레임 단위로 읽기
        ret, frame = cap.read()
        if not ret:
            print("프레임을 가져올 수 없습니다. 스트림을 종료합니다.")
            break

        # 좌우 반전
        frame = cv2.flip(frame, 1)

        results = model(frame, imgsz=640, conf=0.35, verbose=False)[0]

        max_closed_conf = 0.0
        max_open_conf = 0.0

        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[cls_id]

            if cls_id == 0:  # closed_eye
                max_closed_conf = max(max_closed_conf, conf)
                box_color = (0, 0, 255)  # 빨강
            elif cls_id == 1:  # open_eye
                max_open_conf = max(max_open_conf, conf)
                box_color = (0, 255, 0)  # 초록
            else:
                box_color = (255, 0, 0)  # 파랑

            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

        # 최댓값 비교 and 0.55 이상인지 확인
        is_closed = (max_closed_conf > max_open_conf) and (max_closed_conf >= 0.55)

        state = decoder.update(is_closed)
        if state["event"]:
            print(f"[EVENT] {state['event']} | Current: {state['current_morse']} | Text: {state['decoded_text']}")

        status_text = "STATE: CLOSED" if is_closed else "STATE: OPEN"
        status_color = (0, 0, 255) if is_closed else (0, 255, 0)

        cv2.putText(frame, status_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        cv2.putText(frame, f"Morse Buffer: [ {state['current_morse']} ]", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, f"Text: {state['decoded_text']}", (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

        cv2.imshow("Eye Morse - Detection & Score Comparison", frame)

        # q 누르면 루프 탈출
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 자원 해제 및 윈도우 닫기
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()