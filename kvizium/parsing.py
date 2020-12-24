import requests
from database import *


def get_html(url):
    response = requests.get(url)
    response.encoding = "utf8"
    return response.json()


number = 0
while True:
    url = f'https://quizium.ru/ajaxrating?search_team=&season=all&city=7&json=1&offset={number}'

    if get_html(url).get('rows'):
        for row in get_html(url).get('rows'):

            # проверка есть ли такая команда
            if session.query(Data).filter(Data.name == row.get('team_name')).count():
                session.query(Data).filter(Data.name == row.get('team_name')).update(
                    {Data.number_game: row.get('all_games'), Data.points: row.get('points_alltime')},
                    synchronize_session=False)
                # Добавление записи
            else:
                session.add(Data(row.get('team_name'), row.get('all_games'), row.get('points_alltime')))

            print(
                f"Название: {row.get('team_name')} Все мигры:{row.get('all_games')} Очков в игре {row.get('points_alltime')}")

        session.commit()
        number += 10
    else:
        break
