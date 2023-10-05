from CORES.JSONController import JSONController
from CORES.WebsiteController import RequestController
from CORES.SccrenGrabController import SccrenGrabController
from PIL import Image
import os

class GameDataController:
    def __init__(self):
        self.player_hand = []
        self.player_field = []
        self.json_controller = JSONController()
        self.sccren_grab = SccrenGrabController("RetroArch Beetle PSX HW 0.9.44.1 88929ae")
        self.sccren_grab.take_screenshot().save("Test.png")

    def return_array_photos(self, array):
        images = []
        for i in range(0, 5, 1):
            data = array[i]['CardName'] if i < len(array) else None
            images.append(self.return_card_photo_url(data))
        return images

    def return_json_data(self):
        return self.json_controller.return_page_as_json("https://db.ygoprodeck.com/api/v7/cardinfo.php")['data']

    def return_card_photo_url(self, card_name):
        if card_name is None:
            return Image.open("IMAGES/CARDS/CardBack.png")
        if os.path.exists(f"IMAGES/CARDS/{card_name}.png"):
            return Image.open(f"IMAGES/CARDS/{card_name}.png")
        for card in self.return_json_data():
            if card_name == card['name']:
                RequestController().download_image(
                    image_url=card['card_images'][0]['image_url'],
                    save_path=f"IMAGES/CARDS/{card_name}.png"
                )
                return Image.open(f"IMAGES/CARDS/{card_name}.png")
        return Image.open("IMAGES/CARDS/CardBack.png")
