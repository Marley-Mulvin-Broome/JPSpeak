import curses

ENTER_KEYS = [
    curses.KEY_ENTER,
    ord("\n"),
    100
]


class OptionData:
    def __init__(self, text, data, x, y, target):
        self.text = text
        self.data = data
        self.x = x
        self.y = y
        self.target = target

    def draw(self, selected):
        if selected:
            self.target.addstr(self.y, self.x, ">" + self.text + "<")
        else:
            self.target.addstr(self.y, self.x, "  " + self.text + " ")


class OptionList:
    def __init__(self, window, options):
        self.window = window
        self.options = options

        self.selected = 0

    def draw(self):
        for i, option in enumerate(self.options):
            option.draw(self.selected == i)

    def select(self, index):
        self.selected = index

        if self.selected < 0:
            self.selected = len(self.options) - 1
        elif self.selected >= len(self.options):
            self.selected = 0

    def listen(self) -> OptionData:
        input_key = self.window.screen.getch()

        self.window.write_line(0, 20, str(input_key))

        if input_key in ENTER_KEYS:
            return self.options[self.selected]

        if input_key == curses.KEY_LEFT:
            self.select(self.selected - 1)
        elif input_key == curses.KEY_RIGHT:
            self.select(self.selected + 1)

        return None
