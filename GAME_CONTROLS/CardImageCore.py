from CORES.JSONController import JSONController
from CORES.WebsiteController import RequestController
from PIL import Image
import os

class CardImageCore:
    def __init__(self):
        self.JSONController = JSONController()
        self.card_data = self.JSONController.return_page_as_json("https://db.ygoprodeck.com/api/v7/cardinfo.php")['data']

    def return_card_image(self, our_card):
        if our_card is None: return Image.open("IMAGES/CardBack.png")
        if os.path.exists(f"IMAGES/{our_card['CardName']}.png"): return Image.open(f"IMAGES/{our_card['CardName']}.png")
        for card in self.card_data:
            if our_card['CardName'] == card['name']:
                RequestController().download_image(
                    image_url=card['card_images'][0]['image_url'],
                    save_path=f"IMAGES/{our_card['CardName']}.png"
                )
                return Image.open(f"IMAGES/{our_card['CardName']}.png")
        return Image.open("IMAGES/CardBasck.png")


