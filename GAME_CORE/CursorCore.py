class CursorCore:
    def __init__(self, min_cursor, max_cursor, callback_down=None, callback_up=None):
        self.min_cursor = min_cursor
        self.max_cursor = max_cursor
        self.callback_down = callback_down
        self.callback_up = callback_up
        self.current_cursor = self.min_cursor

    def set_cursor_position(self, new_cursor):
        new_cursor = max(self.min_cursor, min(self.max_cursor, new_cursor))
        if new_cursor > self.current_cursor:
            for i in range(self.current_cursor, new_cursor, 1):
                if not self.callback_up is None: self.callback_up(self.current_cursor)
                self.current_cursor = i
        elif new_cursor < self.current_cursor:
            for i in range(self.current_cursor, new_cursor, -1):
                if not self.callback_down is None: self.callback_down(self.current_cursor)
                self.current_cursor = i