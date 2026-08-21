#pytest를 활용한 기본 Unit Test
import numpy as np
import pytest
from generate_2D_to_3D import generate_2D_to_3D

# 테스트 코드
def test_depth_map_shape():
    h, w = 60, 80
    image = np.zeros((h, w, 3), dtype=np.uint8)
    depth_map, _ = generate_2D_to_3D(image)

    assert depth_map.shape == image.shape, "출력 크기가 입력 크기와 다릅니다."

def test_depth_map_dtype():
    h, w = 60, 80
    image = np.zeros((h, w, 3), dtype=np.uint8)
    depth_map, _ = generate_2D_to_3D(image)

    assert isinstance(depth_map, np.ndarray), "출력 데이터 타입이 ndarray가 아닙니다."

def test_depth_map_no_nan_or_inf():
    h, w = 60, 80
    image = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
    depth_map, _ = generate_2D_to_3D(image)

    assert not np.isnan(depth_map).any(), "depth_map에 NaN(결측값)이 존재합니다."
    assert not np.isinf(depth_map).any(), "depth_map에 Inf(무한대)가 존재합니다."

def test_points_3d_shape():
    h, w = 60, 80
    image = np.zeros((h, w, 3), dtype=np.uint8)
    _, points_3d = generate_2D_to_3D(image)

    assert points_3d.shape == (h, w, 3), f"출력 Shape가 ({h}, {w}, 3)이 아닙니다."

def test_points_3d_dtype():
    h, w = 60, 80
    image = np.zeros((h, w, 3), dtype=np.uint8)
    _, points_3d = generate_2D_to_3D(image)

    assert isinstance(points_3d, np.ndarray), "points_3d가 ndarray가 아닙니다."

def test_points_3d_no_nan_or_inf():
    h, w = 60, 80
    image = np.random.randint(0, 256, (h, w, 3), dtype=np.uint8)
    _, points_3d = generate_2D_to_3D(image)

    assert not np.isnan(points_3d).any(), "points_3d에 NaN(결측값)이 존재합니다."
    assert not np.isinf(points_3d).any(), "points_3d에 Inf(무한대)가 존재합니다."

def test_points_3d_non_square_coordinate_bounds():
    h, w = 60, 80
    image = np.zeros((h, w, 3), dtype=np.uint8)
    _, points_3d = generate_2D_to_3D(image)

    # X좌표는 0 ~ w-1, Y좌표는 0 ~ h-1 범위여야 함
    x_coords = points_3d[:, :, 0]
    y_coords = points_3d[:, :, 1]

    assert x_coords.max() == w - 1, f"X축 최댓값이 {w - 1}가 아닙니다. 입력 차원: [{h}, {w}, 3]"
    assert y_coords.max() == h - 1, f"Y축 최댓값이 {h - 1}가 아닙니다. 입력 차원: [{h}, {w}, 3]"

def test_generate_2D_to_3D_none_input():
    with pytest.raises(ValueError, match="입력된 이미지가 없습니다."):
        generate_2D_to_3D(None)
    
# pytest 실행
if __name__ == "__main__":
    pytest.main()