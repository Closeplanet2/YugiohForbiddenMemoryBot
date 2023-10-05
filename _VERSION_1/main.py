from SCRIPTS.GUI.MainGUI import MainGUI
from SCRIPTS.WEB_CRAWLER.FusionWebCrawler import FusionWebCrawler
from SCRIPTS.WEB_CRAWLER.CardDataCrawler import CardDataCrawler

# if bool(input("Do you want to download data? ")):
#     # web_crawler = FusionWebCrawler()
#     # web_crawler.gen_data()
#     card_crawler = CardDataCrawler()
#     card_crawler.gen_data()

main_gui = MainGUI(h=900, w=800, title="Yu-gi-oh Forbidden Memories", s_w=False, s_h=False, bg="#211717")
main_gui.mainloop()