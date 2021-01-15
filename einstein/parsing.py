import requests
from database import *
from fomat import remove_spaces

data = {
    'params[rows]': 0,
    'params[type]': 0,
    'params[season]': 'all',
    'params[direction]': 'desc',
    'params[order]': 'points_sum',
}


def get_html(url, arg):
    response = requests.post(url, arg)
    response.encoding = "utf8"
    return response.json()


def parsing(resp):
    for row in resp['data']['table']:
        if row.get('team') is None:
            return False
        # проверка есть ли такая команда
        elif session.query(Data).filter(Data.name == row.get('team')).count():
            session.query(Data).filter(Data.name == row.get('team')).update(
                {Data.number_game: row.get('count'), Data.points: row.get('sum')},
                synchronize_session=False)
            # Добавление записи
        else:
            team_name = remove_spaces(row.get('team'))
            session.add(Data(team_name, row.get('count'), row.get('sum')))

        print(f"команда {row.get('team')} кол-во игр: {row.get('count')} сумма очков {row.get('sum')}")
        session.commit()
    return True


while True:
    response = get_html('https://albertparty.ru/api/get_new_rows', data)
    if not parsing(response):
        break
    else:
        data['params[rows]'] += 10
