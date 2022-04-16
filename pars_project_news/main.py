#aiogram - библиотека бота

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json


ua = UserAgent()

def get_first_news():
    headers = {
        'UserAgent': ua.random
    }

    url = "https://stopgame.ru/news?"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all('div', class_='item article-summary')


    news_dict = {}
    for article in articles_cards:
        article_title = article.find('div', class_='caption caption-bold').text.strip()
        article_url = f"https://stopgame.ru{article.a.get('href')}"
        article_date_time = article.find('span', class_='info-item timestamp').text.strip()

        article_id = article_url.split("/")[4]
        # article_id = article_id[:-4] Обрезка ID

        # print(f'{article_title} | {article_url} | {article_date_time} | {article_id}')

        news_dict[article_id] = {
            'article_title': article_title,
            'article_url': article_url,
            'article_date_time': article_date_time
        }

        with open('news_dict.json', "w", encoding='utf-8') as file:
            json.dump(news_dict, file, indent=4, ensure_ascii=False)


def chake_news_update():
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    headers = {
        'UserAgent': ua.random
    }

    url = "https://stopgame.ru/news?"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all('div', class_='item article-summary')

    fresh_news = {}
    for article in articles_cards:
        article_url = f"https://stopgame.ru{article.a.get('href')}"
        article_id = article_url.split("/")[4]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find('div', class_='caption caption-bold').text.strip()
            article_date_time = article.find('span', class_='info-item timestamp').text.strip()

            news_dict[article_id] = {
                'article_title': article_title,
                'article_url': article_url,
                'article_date_time': article_date_time
            }

            fresh_news[article_id] = {
                'article_title': article_title,
                'article_url': article_url,
                'article_date_time': article_date_time
            }
    with open('news_dict.json', "w", encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news

def main():
    # get_first_news()
    print(chake_news_update())

if __name__ == '__main__':
    main()



