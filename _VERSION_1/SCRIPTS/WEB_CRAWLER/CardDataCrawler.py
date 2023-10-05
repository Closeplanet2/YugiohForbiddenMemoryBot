from CORES.WebsiteController import WebsiteController
from CORES.JSONController import JSONController
from bs4 import BeautifulSoup

class CardDataCrawler:
    def __init__(self):
        self.website_controller = WebsiteController()
        self.urls = []
        self.urls.append("https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_cards")

    def gen_data(self):
        card_data = {}
        card_data['Cards'] = []
        for url in self.urls:
            website = self.website_controller.return_webpage(url)
            wikitable = website.find('table', class_="wikitable")
            tr_elements = wikitable.find_all('tr')
            for i in range(1, len(tr_elements), 1):
                card = {}
                td_elements = tr_elements[i].find_all('td')
                card['CardURL'] = f"https://yugipedia.com{str(td_elements[1].find('a')['href'])}"
                card['CardID'] = str(td_elements[0].contents[0].replace('\n', ''))
                card['CardName'] = str(td_elements[1].contents[0].contents[0]).replace('\n', '')
                card['CardType'] = str(td_elements[2].contents[0].contents[0])
                card['Type'] = str(td_elements[3].contents[0].contents[0]) if len(str(td_elements[3])) > 10 else ""
                card['CardGuardianStars'] = self.return_guardian_stars(td_elements[4])
                card['CardLevel'] = str(td_elements[5].contents[0]).replace('\n', '')
                card['CardATK'] = str(td_elements[6].contents[0]).replace('\n', '')
                card['CardDEF'] = str(td_elements[7].contents[0]).replace('\n', '')
                card['CardPassword'] = str(td_elements[8].contents[0]).replace('\n', '')
                card['SC_Cost'] = str(td_elements[9].contents[0]).replace('\n', '')
                card_data['Cards'].append(card)

        for card in card_data['Cards']:
            website = self.website_controller.return_webpage(card['CardURL'])
            innertable = website.find('table', class_="innertable")
            tr_elements = innertable.find_all('tr')
            card['CardDesc'] = self.combine_description(tr_elements)

        JSONController().dump_dict_to_json(card_data, "DATA/CardData.json", True)
        self.website_controller.chrome_driver.close()

    def return_guardian_stars(self, td_element):
        stars = []
        for x in td_element.contents:
            content = x.replace('\n', '')
            if len(content) > 0: stars.append(content)
        return stars

    def combine_description(self, tr_elements):
        master_string = ""

        if len(tr_elements) > 4 and tr_elements[4].find('p'):
            for tr_element in tr_elements[4].find('p').contents:
                if str(tr_element).startswith('<a') or str(tr_element).startswith('<a '):
                    soup = BeautifulSoup(str(tr_element), 'html.parser')
                    tag_content = soup.get_text()
                    master_string += tag_content
                else:
                    master_string += str(tr_element)

        return master_string




