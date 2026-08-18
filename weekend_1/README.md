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