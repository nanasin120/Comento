import time

# 모스부호 Dictionary
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
    """모스 부호가 들어오면 알파벳으로 변환해주는 디코더"""
    def __init__(self, min_blink=0.25, dot_max=0.7, dash_max=2.0, char_timeout=1.5, time_fn=None):
        self.min_blink = min_blink
        self.dot_max = dot_max
        self.dash_max = dash_max
        self.char_timeout = char_timeout
        self.time_fn = time_fn if time_fn else time.time

        self.current_morse = ""
        self.decoded_text = ""
        
        self.is_eye_closed = False
        self.close_start_time = 0.0
        self.open_start_time = self.time_fn()

    def update(self, is_closed: bool) -> dict:
        now = self.time_fn()
        event = None

        # 지금 눈 감음 + 이전에 눈 감지 않음 = 눈 감기 시작
        if is_closed and not self.is_eye_closed:
            self.is_eye_closed = True
            self.close_start_time = now

        # 지금 눈 감지 않음 + 이전에 눈 감음 = 눈 뜸
        elif not is_closed and self.is_eye_closed:
            self.is_eye_closed = False
            self.open_start_time = now
            duration = now - self.close_start_time

            if self.min_blink <= duration < self.dot_max:
                self.current_morse += "."
                event = "DOT"
            elif self.dot_max <= duration <= self.dash_max:
                self.current_morse += "-"
                event = "DASH"

        # 지금 눈 감지 않음 + 이전에 눈 감지 않음 = 눈 계속 뜨고 있는 상태
        elif not is_closed and not self.is_eye_closed:
            if self.current_morse and (now - self.open_start_time >= self.char_timeout):
                char = MORSE_CODE_DICT.get(self.current_morse, "?")
                self.decoded_text += char
                event = f"CHAR_{char}"
                self.current_morse = ""

        return {
            "current_morse": self.current_morse,
            "decoded_text": self.decoded_text,
            "event": event
        }