import win32api
import win32con
import time
from pynput.keyboard import Key, Controller
controller = Controller()

class InputController:
    def click_pos(self, posx=77, posy=188, delay=0.5):
        win32api.SetCursorPos((posx, posy))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, posx, posy, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, posx, posy, 0, 0)
        time.sleep(delay)

    def click_button(self, key, delay=0.5):
        controller.press(key)
        time.sleep(0.1)
        controller.release(key)
        time.sleep(delay)

    def left_click_button(self, new_cursor_position=0, delay=0.5):
        controller.press(Key.left)
        time.sleep(0.1)
        controller.release(Key.left)
        time.sleep(delay)

    def right_click_button(self, new_cursor_position=0, delay=0.5):
        controller.press(Key.right)
        time.sleep(0.1)
        controller.release(Key.right)
        time.sleep(delay)

    def up_click_button(self, delay=0.5):
        controller.press(Key.up)
        time.sleep(0.1)
        controller.release(Key.up)
        time.sleep(delay)

    def enter_click_button(self, delay=0.5):
        controller.press(Key.enter)
        time.sleep(0.1)
        controller.release(Key.enter)
        time.sleep(delay)