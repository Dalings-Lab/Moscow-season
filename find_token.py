import requests
from bs4 import BeautifulSoup
from itertools import groupby


# Парсер страницы
def url_parser(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


# Ссылка на страницу с регистрацией
def link_of_register(soup=url_parser('https://moscowseasons.com/event/katki-moskvy-2021-2022/')):
    return [a['href'] for a in soup.find_all('a', href=True, text=True)][33]


# Поиск place_id
def place_id(url=link_of_register()):
    return [i for i in url.split('/mc/')][1]


# Поиск TOKEN
def token(soup=url_parser(link_of_register())):
    my_token = str([a for a in soup.find_all('script', id="__NEXT_DATA__", type=True, text=True)])
    return my_token.split('"')[31]


# Поиск расписания сеансов
def get_time_link(place_id_active=place_id(), token_active=token()):
    headers_dict = {"Sec-Ch-Ua": '"Chromium";v="97", " Not;A Brand";v="99"',
                    "Accept": "application/json, text/plain, */*",
                    "X-App-Token": token_active}

    response = requests.get('http://mf.technolab.com.ru/v1/place/dates-list?place_id=' + place_id_active,
                            headers=headers_dict)
    soup = BeautifulSoup(response.text, 'html.parser')

    link_time_slots = [link.split('"')[1] for link in
                       ((str(soup).split('"time_slots":{')[1]).split('}}]}]')[0]).split(',')]
    return link_time_slots


# Получение читабельного расписания в виде "Дата 30.01 Время 13:45" например
def get_time_info(link_time_slots=get_time_link()):
    # Поик дат и сортировка в формате ДД.ММ
    day_info = [(day.split('T')[0]).split('-')[-1] + '.' + (day.split('T')[0]).split('-')[-2] for day in
                link_time_slots]
    sorted_day_info = [day for day, _ in groupby(day_info)]

    time_info = [(info.split('T')[1])[0:5] for info in link_time_slots]

    # Индексы времени
    main_mass = []
    for day in sorted_day_info:
        second_str = []
        day = day.split('.')
        day = day[1] + '-' + day[0]
        for link in link_time_slots:
            if day in link:
                second_str.append(time_info[link_time_slots.index(link)])
        main_mass.append(second_str)

    for index in range(len(sorted_day_info)):
        dict_date_to_time = dict.fromkeys(sorted_day_info, main_mass[index])

    return dict_date_to_time


# Ссылка на регистрацию на определенное время
# Под бота надо переписывать
def choose_day_and_time(time_info=get_time_info(), links=get_time_link()):
    print('Выберите день:')
    for day in time_info.keys():
        print(day)

    day = str(input('Введите день: '))

    print('Выберите время')
    for time in time_info[day]:
        new_time = str((int(time[0:2]))+3)+time[2:5]
        print(new_time)

    time = str(input('Введите время: '))
    new_time = str((int(time[0:2]))-3)+time[2:5]

    return [final_link for final_link in links if
            ((((day.split('.')[1]) + '-' + day.split('.')[0]) in final_link) and ('T' + new_time in final_link))]


print(choose_day_and_time())
