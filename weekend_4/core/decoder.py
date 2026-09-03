import time

MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z',
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'
}

class MorseDecoder:
    def __init__(self, min_blink=0.25, dot_max=0.7, dash_max=2.0, char_timeout=1.5):
        self.min_blink = min_blink
        self.dot_max = dot_max
        self.dash_max = dash_max
        self.char_timeout = char_timeout

        self.current_morse = ""
        self.decoded_text = ""
        
        self.is_eye_closed = False
        self.close_start_time = 0.0
        self.open_start_time = time.time()

    def update(self, is_closed: bool) -> dict:
        """
        매 프레임 호출되어 상태를 갱신하고 현재 상태 정보를 dict로 반환.
        """
        now = time.time()
        event = None

        # 상태 전이: OPEN -> CLOSED (눈을 감기 시작함)
        if is_closed and not self.is_eye_closed:
            self.is_eye_closed = True
            self.close_start_time = now

        # 상태 전이: CLOSED -> OPEN (눈을 감았다가 뜸)
        elif not is_closed and self.is_eye_closed:
            self.is_eye_closed = False
            self.open_start_time = now
            duration = now - self.close_start_time

            # 부호 판정
            if self.min_blink <= duration < self.dot_max:
                self.current_morse += "."
                event = "DOT"
            elif self.dot_max <= duration <= self.dash_max:
                self.current_morse += "-"
                event = "DASH"
            # 0.25s 미만은 생리적 깜빡임으로 자동 무시됨

        # 눈을 계속 뜨고 있는 상태: Timeout 체크
        elif not is_closed and not self.is_eye_closed:
            if self.current_morse and (now - self.open_start_time >= self.char_timeout):
                # 글자 변환
                char = MORSE_CODE_DICT.get(self.current_morse, "?")
                self.decoded_text += char
                event = f"CHAR_{char}"
                self.current_morse = ""  # 버퍼 비우기

        return {
            "current_morse": self.current_morse,
            "decoded_text": self.decoded_text,
            "event": event
        }