import pytest
from core.decoder import MorseDecoder

class MockClock:
    """테스트를 위해 수동으로 시간을 흐르게 하는 가상 시계"""
    def __init__(self, initial_time=100.0):
        self._time = initial_time

    def time(self):
        return self._time

    def advance(self, seconds: float):
        self._time += seconds


@pytest.fixture
def mock_clock():
    return MockClock(initial_time=100.0)


@pytest.fixture
def decoder(mock_clock):
    return MorseDecoder(
        min_blink=0.25,
        dot_max=0.70,
        dash_max=2.00,
        char_timeout=1.50,
        time_fn=mock_clock.time
    )


def test_ignore_physiological_blink(decoder, mock_clock):
    """0.25초 미만의 깜빡임은 무시되어야 함 (0.15초 폐안)"""
    decoder.update(is_closed=True)
    mock_clock.advance(0.15)
    res = decoder.update(is_closed=False)

    assert res["current_morse"] == ""
    assert res["event"] is None


def test_dot_detection(decoder, mock_clock):
    """0.25초 ~ 0.7초 사이 폐안은 Dot(.)이어야 함 (0.4초 폐안)"""
    decoder.update(is_closed=True)
    mock_clock.advance(0.40)
    res = decoder.update(is_closed=False)

    assert res["current_morse"] == "."
    assert res["event"] == "DOT"


def test_dash_detection(decoder, mock_clock):
    """0.7초 ~ 2.0초 사이 폐안은 Dash(-)이어야 함 (1.0초 폐안)"""
    decoder.update(is_closed=True)
    mock_clock.advance(1.00)
    res = decoder.update(is_closed=False)

    assert res["current_morse"] == "-"
    assert res["event"] == "DASH"


def test_ignore_too_long_blink(decoder, mock_clock):
    """2.0초 초과 폐안은 무시되어야 함 (2.5초 폐안)"""
    decoder.update(is_closed=True)
    mock_clock.advance(2.50)
    res = decoder.update(is_closed=False)

    assert res["current_morse"] == ""
    assert res["event"] is None


def test_character_conversion_sos(decoder, mock_clock):
    """연속 신호 입력 후 1.5초 대기 시 'S' (...) 문자로 변환되어야 함"""
    # 3번의 Dot 입력 (각 0.4초 감고 0.3초 대기)
    for _ in range(3):
        decoder.update(is_closed=True)
        mock_clock.advance(0.40)
        decoder.update(is_closed=False)
        mock_clock.advance(0.30)

    # 3번째 Dot 직후: 버퍼에 '...'가 있어야 하고, 텍스트 변환은 아직 안 됨
    assert decoder.current_morse == "..."
    assert decoder.decoded_text == ""

    # 1.5초 타임아웃 경과 (0.3초 이미 지났으므로 1.3초 추가 전진)
    mock_clock.advance(1.30)
    res = decoder.update(is_closed=False)

    assert res["event"] == "CHAR_S"
    assert res["current_morse"] == ""
    assert res["decoded_text"] == "S"

def test_unknown_morse_code_fallback(decoder, mock_clock):
    """사전에 정의되지 않은 부호는 '?'로 변환되어야 함"""
    # 임의로 정의되지 않은 부호 '...-' 대신 길게 조합
    decoder.current_morse = ".......-"
    mock_clock.advance(1.6)
    res = decoder.update(is_closed=False)

    assert res["decoded_text"] == "?"
    assert res["current_morse"] == ""


def test_multi_character_word(decoder, mock_clock):
    """연속 입력으로 여러 글자(예: 'HI')가 차례대로 결합되는지 검증"""
    def input_blink(duration):
        decoder.update(is_closed=True)
        mock_clock.advance(duration)
        decoder.update(is_closed=False)
        mock_clock.advance(0.2)  # 심볼 간 짧은 쉼

    # 'H' (....)
    for _ in range(4):
        input_blink(0.4)
    mock_clock.advance(1.5)  # 글자 완성 타임아웃
    decoder.update(is_closed=False)
    assert decoder.decoded_text == "H"

    # 이어서 'I' (..)
    for _ in range(2):
        input_blink(0.4)
    mock_clock.advance(1.5)  # 글자 완성 타임아웃
    decoder.update(is_closed=False)
    assert decoder.decoded_text == "HI"


def test_no_duplicate_signal_on_continuous_closed_frames(decoder, mock_clock):
    """눈을 감고 있는 동안 수십 프레임 연속 update(True)가 들어와도 부호는 1개만 찍혀야 함"""
    # 0.5초 동안 30프레임 들어온 상황 모사
    for _ in range(15):
        decoder.update(is_closed=True)
        mock_clock.advance(0.033)

    # 감고 있는 도중에는 아직 부호가 추가되지 않아야 함
    assert decoder.current_morse == ""

    # 눈을 뜸
    res = decoder.update(is_closed=False)
    assert res["current_morse"] == "."
    assert len(res["current_morse"]) == 1


def test_exact_boundaries(decoder, mock_clock):
    """경계값 테스트: 0.25초(최소 Dot), 0.70초(최대 Dot / 최소 Dash)"""
    # 0.25초 (Dot 진입점)
    decoder.update(is_closed=True)
    mock_clock.advance(0.25)
    res = decoder.update(is_closed=False)
    assert res["current_morse"] == "."

    # 1.5초 대기해서 버퍼 비우기
    mock_clock.advance(1.6)
    decoder.update(is_closed=False)

    # 0.70초 (Dash 진입점)
    decoder.update(is_closed=True)
    mock_clock.advance(0.70)
    res = decoder.update(is_closed=False)
    assert res["current_morse"] == "-"