from curses import initscr, noecho, echo, cbreak, endwin, curs_set, beep
from option_list import OptionList, OptionData
from googlegtts import GoogleTTS
from pyclip import copy as copy_to_clipboard
from os.path import isdir
from os import mkdir as make_dir

MAX_INPUT_LENGTH = 1024


class Window:
    def __init__(self):
        self.screen = initscr()
        noecho()
        cbreak()
        self.screen.keypad(True)

        x_block = 27
        center = self.get_center(x_block + 7)

        self.options = [
            OptionData("Execute", None, center, 3, self.screen),
            OptionData("Engine", None, 30 + center, 3, self.screen),
            OptionData("Exit", None, center, 4, self.screen),
        ]

        self.option_list = OptionList(self, self.options)

        curs_set(0)

        self.engine = self.create_engine_options()[0].data

        self.bottom_text = ""
        self.set_bottom_text(f"Engine: {self.engine}")

        if not isdir("output"):
            make_dir("output")

    def __del__(self):
        self.screen.keypad(False)
        cbreak()
        noecho()
        self.screen.clear()
        self.screen.refresh()
        endwin()

    def set_bottom_text(self, text):
        self.bottom_text = f"{text}"

    def get_dimensions(self):
        return self.screen.getmaxyx()

    def get_height(self):
        return self.get_dimensions()[0]

    def get_width(self):
        return self.get_dimensions()[1]

    def get_center(self, width):
        return (self.get_width() - width) // 2

    def write_middle(self, y, text, target=None):
        if target is None:
            target = self.screen

        target.addstr(y, self.get_center(len(text)), text)

    def draw_line(self, y, char="-", target=None):
        if target is None:
            target = self.screen

        target.addstr(y, 0, char * self.get_width())

    def clear_line(self, y):
        self.draw_line(y, " ")

    def write_line(self, x, y, text, target=None):
        if target is None:
            target = self.screen

        target.addstr(y, x, text)

    def create_engine_options(self):
        return [
            OptionData("Google", GoogleTTS(), self.get_center(6) - 1, 3, self.screen),
            OptionData("Cancel", None, self.get_center(6) - 1, 4, self.screen),
        ]

    def draw_bottom_text(self):
        self.write_line(0, self.get_height() - 1, self.bottom_text)

    def get_string(self, y, x, length):
        echo()
        curs_set(1)

        string = self.screen.getstr(y, x, length).decode("utf-8")

        noecho()
        curs_set(0)

        return string

    def pick_engine(self):
        engine_options = self.create_engine_options()
        engine_option_list = OptionList(self, engine_options)

        while True:
            self.screen.clear()

            self.print_title()

            self.write_middle(2, "Set Engine")

            engine_option_list.draw()

            self.screen.refresh()

            result = engine_option_list.listen()

            if result is None:
                continue

            if result.text == "Cancel":
                return self.engine

            return result.data

    def execute(self):
        if self.engine is None:
            beep()
            self.set_bottom_text("Error: No engine selected")
            return

        while True:
            self.screen.clear()
            self.print_title()

            self.set_bottom_text("Enter text to speak")
            self.draw_bottom_text()
            self.screen.refresh()

            input_string = self.get_string(2, 4, MAX_INPUT_LENGTH)

            if not input_string:
                break

            self.set_bottom_text("Loading...")
            self.draw_bottom_text()
            self.screen.refresh()

            stream = self.engine.speak(input_string)
            full_text = b""

            with open(f"output/{input_string}.mp3", "wb") as f:
                for chunk in stream:
                    full_text += chunk
                    f.write(chunk)

            # copy bytes to clipboard
            copy_to_clipboard(full_text)

            beep()

    def print_title(self):
        self.write_middle(0, "JPSpeak")
        self.draw_line(1)

    def run(self):

        while True:
            self.screen.clear()

            self.print_title()

            self.option_list.draw()

            self.draw_bottom_text()

            self.screen.refresh()

            result = self.option_list.listen()

            if result is None:
                continue

            if result.text == "Exit":
                break

            if result.text == "Engine":
                self.engine = self.pick_engine()
                self.set_bottom_text("Engine: " + repr(self.engine))

            if result.text == "Execute":
                self.execute()
