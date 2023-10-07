class CursorCore:
    def __init__(self, min_cursor, max_cursor, callback_down=None, callback_up=None):
        self.min_cursor = min_cursor
        self.max_cursor = max_cursor
        self.callback_down = callback_down
        self.callback_up = callback_up
        self.cursor_position = 0

    def default_cursor(self):
        for i in range(self.max_cursor, self.min_cursor, -1):
            self.cursor_position = i
            if not self.callback_down is None:
                self.callback_down(self.cursor_position)

    def set_cursor_position(self, new_cursor_position):
        new_cursor_position = max(self.min_cursor, min(self.max_cursor, new_cursor_position))
        if new_cursor_position > self.cursor_position:
            for i in range(self.cursor_position, new_cursor_position, 1):
                if not self.callback_up is None:
                    self.callback_up(self.cursor_position)
        elif new_cursor_position < self.cursor_position:
            for i in range(self.cursor_position, new_cursor_position, -1):
                if not self.callback_down is None:
                    self.callback_down(self.cursor_position)
        self.cursor_position = new_cursor_position
