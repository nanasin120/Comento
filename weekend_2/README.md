# 2D to 3D Depth Map & Point Cloud 변환

## 주요 처리 과정 (Pipeline Steps)

해당과정은 Dummy depth map과 3D Point Cloud생성 과정입니다.

| 단계 | Process | Details |
| --- | --- | --- |
| 1 | 입력 검증 | 이미지 `None` 여부 확인 및 예외 처리(`ValueError`) |
| 2 | 흑백 변환 | BGR 컬러 이미지를 단일 채널 Grayscale로 변환 (`cv2.COLOR_BGR2GRAY`) |
| 3 | Depth Map 생성 | Grayscale 이미지에 JET 컬러맵 적용 (`cv2.applyColorMap`) |
| 4 | 2D 좌표 그리드 생성 | 너비($W$) 및 높이($H$) 기준 $X, Y$ 좌표 Meshgrid 생성 |
| 5 | Depth(Z축) 매핑 | Grayscale 밝기값을 `float32` 형태의 $Z$ 축 깊이 데이터로 변환 |
| 6 | 3D Point Cloud 결합 | $X, Y, Z$ 배열을 3차원 깊이 방향으로 결합 (`np.dstack`) |

## 입출력 데이터 명세 (Input / Output Specs)

- **Input**: `numpy.ndarray` (Shape: `(H, W, 3)`, dtype: `uint8`, BGR Color)
- **Output 1 (`depth_map`)**: `numpy.ndarray` (Shape: `(H, W, 3)`, dtype: `uint8`)
- **Output 2 (`points_3d`)**: `numpy.ndarray` (Shape: `(H, W, 3)`, dtype: `float32`, Values: `[X, Y, Z]`)

## 검증 및 단위 테스트 (Unit Tests)

`pytest`를 통해 파이프라인의 데이터 정합성을 검증합니다.

| 테스트 항목 | 검증 내용 |
| --- | --- |
| `test_depth_map_shape` | Depth Map 출력 크기와 입력 이미지 크기 일치 여부 |
| `test_depth_map_dtype` | Depth Map의 `np.ndarray` 타입 검증 |
| `test_depth_map_no_nan_or_inf` | Depth Map 내 결측값(`NaN`) 및 무한대(`Inf`) 포함 여부 |
| `test_points_3d_shape` | 3D Point Cloud의 형상 `(H, W, 3)` 일치 여부 |
| `test_points_3d_dtype` | 3D Point Cloud의 `np.ndarray` 타입 검증 |
| `test_points_3d_no_nan_or_inf` | 3D 좌표 내 결측값(`NaN`) 및 무한대(`Inf`) 포함 여부 |
| `test_points_3d_non_square_coordinate_bounds` | 비정방형 이미지에 대한 $X$($0 \sim W-1$), $Y$($0 \sim H-1$) 좌표 범위 유효성 |
| `test_generate_2D_to_3D_none_input` | `None` 입력 시 `ValueError` 정상 발생 여부 |

## 변환 결과 예시 (Result)

| 원본 이미지 (Input) | Depth Map 결과 (Output 1) | 3D Point Cloud (Output 2) |
| :---: | :---: | :---: |
