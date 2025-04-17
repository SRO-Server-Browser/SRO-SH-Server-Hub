import colorama
colorama.init(autoreset=False)

class Style:
	ResetAll = "\033[0m"
    

class color(Style):
	Default      = "\033[39m"
	Black        = "\033[30m"
	Red          = "\033[31m"
	Green        = "\033[32m"
	Yellow       = "\033[33m"
	Blue         = "\033[34m"
	Magenta      = "\033[35m"
	Cyan         = "\033[36m"
	LightGray    = "\033[37m"
	DarkGray     = "\033[90m"
	LightRed     = "\033[91m"
	LightGreen   = "\033[92m"
	LightYellow  = "\033[93m"
	LightBlue    = "\033[94m"
	LightMagenta = "\033[95m"
	LightCyan    = "\033[96m"
	White        = "\033[97m"
    
class text(Style):
	Bold       = "\033[1m"
	Dim        = "\033[2m"
	Underlined = "\033[4m"
	Blink      = "\033[5m"
	Reverse    = "\033[7m"
	Hidden     = "\033[8m"
	ResetBold       = "\033[21m"
	ResetDim        = "\033[22m"
	ResetUnderlined = "\033[24m"
	ResetBlink      = "\033[25m"
	ResetReverse    = "\033[27m"
	ResetHidden     = "\033[28m"

class bg(Style):
	Default      = "\033[49m"
	Black        = "\033[40m"
	Red          = "\033[41m"
	Green        = "\033[42m"
	Yellow       = "\033[43m"
	Blue         = "\033[44m"
	Magenta      = "\033[45m"
	Cyan         = "\033[46m"
	LightGray    = "\033[47m"
	DarkGray     = "\033[100m"
	LightRed     = "\033[101m"
	LightGreen   = "\033[102m"
	LightYellow  = "\033[103m"
	LightBlue    = "\033[104m"
	LightMagenta = "\033[105m"
	LightCyan    = "\033[106m"
	White        = "\033[107m"

class box:
    TOP_LEFT = "+"
    TOP_RIGHT = "+"
    BOTTOM_LEFT = "+"
    BOTTOM_RIGHT = "+"
    HORIZONTAL = "-"
    VERTICAL = "|"

    @staticmethod
    def draw(*lines, color_code=color.Default, padding=1, margin=0):
        pad = " " * padding
        processed_lines = [pad + str(line) + pad for line in lines]
        max_width = max(len(line) for line in processed_lines)
        top = f"{box.TOP_LEFT}{box.HORIZONTAL * (max_width)}{box.TOP_RIGHT}"
        bottom = f"{box.BOTTOM_LEFT}{box.HORIZONTAL * (max_width)}{box.BOTTOM_RIGHT}"
        side = box.VERTICAL

        margin_str = "\n" * margin
        result = [margin_str + color_code + top]
        for line in processed_lines:
            result.append(f"{side}{line.ljust(max_width)}{side}")
        result.append(bottom + color.ResetAll + margin_str)
        return "\n".join(result)

    @staticmethod
    def print(*lines, **kwargs):
        print(box.draw(*lines, **kwargs))


import sys
import time
import threading
"""
"|/-\\"
".oO0Oo."
"<^>v"
["", ".", "..", "..."]
"""


class Loader:
    rotating_bar = "|/-\\"
    bouncing_dot = ".oO0⁰Oo."
    scrolling_arrows = "<^>v"
    horizontal_bounce = "←─→"
    progress_dots = ["", ".", "..", "..."]
    ascii_bar = ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[ ===]", "[  ==]", "[   =]"]
    zipper = "=-~"
    grow_shrink = "_-‾-"
    minimal = ".:*"
    flip_flop = "><"
    ping_pong = ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[ == ]", "[  = ]", "[    ]"]
    side_scroll = ["<    >", "<=   >", "<==  >", "<=== >", "< ===>", "<  ==>", "<   =>", "<    >"]
    slanty_wave = "/|\\|"
    def __init__(self, text="Loading", delay=0.1, chars="|/-\\", color_code=color.Default):
        if isinstance(chars, str):
            chars = list(chars)
        self.text = text
        self.delay = delay
        self.chars = chars
        self.color = color_code
        self.stop_running = threading.Event()
        self.thread = threading.Thread(target=self._animate, daemon=True)

    def _animate(self):
        idx = 0
        while not self.stop_running.is_set():
            spinner_char = self.chars[idx % len(self.chars)]
            sys.stdout.write(f"\r{self.color}{spinner_char} {self.text}{color.ResetAll}")
            sys.stdout.flush()
            time.sleep(self.delay)
            idx += 1
        sys.stdout.write("\r")
        sys.stdout.flush()

    def start(self):
        self.stop_running.clear()
        self.thread.start()

    def stop(self):
        self.stop_running.set()
        self.thread.join()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def print_success(*msg, **kwargs):
    print(bg.Green, "=", bg.Default, color.Green, "Success:", color.Default, *msg, **kwargs)

def print_fail(*msg, **kwargs):
    print(bg.Red, "X", bg.Default, color.Red, "Fail:", color.Default, *msg, **kwargs)

def print_debug(*msg, **kwargs):
    print(bg.Blue,">",bg.Default,color.Blue,"Debug:",color.Default, *msg, **kwargs)

def print_warning(*msg, **kwargs):
    print(bg.Yellow,"!",bg.Default,color.Yellow,"Warning:",color.Default, *msg, **kwargs)


