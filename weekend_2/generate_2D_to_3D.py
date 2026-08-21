#### 기본적인 Depth Map 생성 코드 (OpenCV 활용)
import cv2
import numpy as np

# 샘플 함수: 가짜 깊이 맵 생성
def generate_2D_to_3D(image):
    if image is None:
        raise ValueError("입력된 이미지가 없습니다.")

    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Depth Map 생성
    depth_map = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

    # 3D 포인트 클라우드 변환
    h, w = depth_map.shape[:2]
    X, Y = np.meshgrid(np.arange(w), np.arange(h))
    Z = gray.astype(np.float32) # Depth 값을 Z 축으로 사용

    # 3D 좌표 생성
    # OpenCV로는 출력 불가능, matplotlib or Open3D로 가능
    points_3d = np.dstack((X, Y, Z))

    return depth_map, points_3d

if __name__ == "__main__":
    image = cv2.imread('sample.jpg')
    depth_map, points_3d = generate_2D_to_3D(image)

    # 결과 출력
    cv2.imshow('Depth Map', depth_map)
    cv2.imshow('Points 3D', points_3d)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()