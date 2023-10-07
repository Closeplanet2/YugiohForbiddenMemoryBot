import pygetwindow as gw
from PIL import ImageGrab
import pyautogui

class ScreenGrabController:
    def __init__(self, window_name=None):
        self.window_name = window_name
        if self.window_name is None:
            self.window = None
        else:
            self.window = gw.getWindowsWithTitle(self.window_name)[0]

    def take_screenshot(self, left=0, top=0):
        height, width = pyautogui.size()
        screenshot = ImageGrab.grab()
        left = self.window.left if self.window else left
        top = self.window.top if self.window else top
        width = self.window.right if self.window else width
        height = self.window.bottom if self.window else height
        return screenshot.crop((left, top, width, height))

    def convert_pos(self, pos_x, pos_y):
        if self.window is None:
            return (pos_x, pos_y)
        x = pos_x + self.window.left + pos_x
        y = pos_y + self.window.top + pos_y
        return (x, y)

    def does_image_contain_color_pixel(self, image, color):
        pixel_data = image.load()
        for x in range(image.width):
            for y in range(image.height):
                if pixel_data[x, y] == color: return True;
        return False