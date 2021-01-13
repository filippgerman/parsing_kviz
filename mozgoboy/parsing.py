import requests
from bs4 import BeautifulSoup
from database import *


def get_html(url):
    """
    :param url: str ссылка на сайт (Иозгобой)
    :return: str html в ввиде текста
    """
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    response = requests.request("GET", url, headers=headers)
    return response.text


def format_name(name):
    """
    :param name: str имя команды, для парсинга
    :return: str форматированное имя команды (без цифр и пунктиров)
    """
    name = name.split(" ")
    return ' '.join(name[2::])


def insert_in_database(url):
    """
    :param url: str ссылка на сайт (Иозгобой)
    Заприсывает в Бд информацию с сайта
    """
    response = get_html(url)
    soup = BeautifulSoup(response, 'lxml')

    for tr in soup.find_all('tr', class_='command_row'):
        name = format_name(tr.find('td').get_text())
        games = int(tr.find('td', class_='games').get_text())
        points = float(tr.find('td', class_='points').get_text())

        if session.query(Data).filter(Data.name == name).count():
            session.query(Data).filter(Data.name == name).update(
                {Data.number_game: games, Data.points: points},
                synchronize_session=False)
            # Добавление записи
        else:
            session.add(Data(name, games, points))

        print(f"команда {name} кол-во игр: {games} сумма очков {points}")
        session.commit()


def parsing(url):
    """
    :param url: str ссылка на сайт (Иозгобой)
    просиходит (пагинация)
    """
    offset = 0
    while get_html(url):
        insert_in_database(url)
        offset += 20
        url = f"http://mozgoboy.ru/ajax?action=get/rating&city=5&offset={offset}&season=all&league=1&search_team_name=&_=1610204052611"


parsing(f"http://mozgoboy.ru/ajax?action=get/rating&city=5&offset=0&season=all&league=1&search_team_name=&_=1610204052611")
