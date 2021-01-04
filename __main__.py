import requests
from bs4 import BeautifulSoup
import time

sleep_seconds = 300  # 300 sec entspricht 5 min
r = requests.get("https://img.yugioh-card.com/uk/news/")
soup = BeautifulSoup(r.content, features="html.parser")


class NewsChecker():
    def __init__(self):
        self.latest_news = ""
        self.check_news = ""

    def load_check_news(self):
        self.check_news = open("news.txt", "r").read().strip()

    def write_latest_news(self):
        self.latest_news = self.get_latest_news()
        text_file = open("news.txt", "w")
        text_file.write(self.latest_news)
        text_file.close()

    def get_latest_news(self):
        return soup.tr.text.strip()


    def alert_telegramm(self):
        bot_message = "Neue Yugioh News!!: "+ str(self.check_news)
        bot_token = ""
        bot_chat_id = ""
        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?chat_id=' \
            + bot_chat_id \
            + '&parse_mode=Markdown&text=' \
            + bot_message
        response = requests.get(send_text)
   

newsChecker = NewsChecker()
newsChecker.load_check_news()

if len(newsChecker.check_news) == 0:
    newsChecker.write_latest_news()
    newsChecker.check_news = newsChecker.latest_news

while (True):
    if not newsChecker.get_latest_news() == newsChecker.check_news:
        newsChecker.write_latest_news()
        newsChecker.check_news = newsChecker.get_latest_news()
        newsChecker.alert()

    time.sleep(sleep_seconds)
