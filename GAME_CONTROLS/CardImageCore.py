from CORES.JSONController import JSONController
from CORES.WebsiteController import RequestController
from PIL import Image
import os

class CardImageCore:
    def __init__(self):
        self.JSONController = JSONController()
        self.card_data = self.JSONController.return_page_as_json("https://db.ygoprodeck.com/api/v7/cardinfo.php")['data']

    def return_card_image(self, card_name):
        if card_name is None: return Image.open("IMAGES/CardBack.png")
        if os.path.exists(f"IMAGES/CARDS/{card_name}.png"): return Image.open(f"IMAGES/{card_name}.png")
        for card in self.card_data:
            if card_name == card['name']:
                RequestController().download_image(
                    image_url=card['card_images'][0]['image_url'],
                    save_path=f"IMAGES/CARDS/{card_name}.png"
                )
                return Image.open(f"IMAGES/CARDS/{card_name}.png")
        return Image.open("IMAGES/CardBack.png")


