from CORES.WebsiteController import WebsiteController
from CORES.JSONController import JSONController

class FusionWebCrawler:
    def __init__(self):
        self.website_controller = WebsiteController()
        self.urls = []
        self.urls.append("https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_Fusions_(001–200)")
        self.urls.append("https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_Fusions_(201–400)")
        self.urls.append("https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_Fusions_(401–600)")
        self.urls.append("https://yugipedia.com/wiki/List_of_Yu-Gi-Oh!_Forbidden_Memories_Fusions_(601–722)")

    def gen_data(self):
        fusion_data = {}
        for url in self.urls:
            website = self.website_controller.return_webpage(url)
            headers = website.find_all('span', class_="mw-headline")
            wikitables = website.find_all('table', class_="wikitable")
            for i in range(0, len(headers), 1):
                card_id = ''.join(str(headers[i].contents)[2:5])
                fusion_data[card_id] = self.gen_data_from_header_and_table(fusion_data, wikitables[i])

        JSONController().dump_dict_to_json(fusion_data, "DATA/FusionData.json", True)
        self.website_controller.chrome_driver.close()


    def gen_data_from_header_and_table(self, fusion_data, table):
        data = {}
        for tr_element in table.find_all('tr'):
            td_elements = tr_element.find_all('td')
            if len(td_elements) <= 0: continue
            for mat1 in td_elements[0].find_all('li'):
                for mat2 in td_elements[1].find_all('li'):
                    mat1_id = self.convert_mat_to_id(str(mat1))
                    mat2_id = self.convert_mat_to_id(str(mat2))
                    if not mat1_id in data: data[mat1_id] = []
                    data[mat1_id].append(mat2_id)
        return data

    def convert_mat_to_id(self, mat):
        return ''.join(mat)[5:8]

