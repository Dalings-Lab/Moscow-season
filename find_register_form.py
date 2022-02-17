import requests


def find_place_id():
    # Тело страницы с регистрацией
    url = requests.get('https://moscowseasons.com/event/katki-moskvy-2021-2022/')
    resp_check = url.text

    # Разбивка тела на куски по 300 символов
    chunks = [resp_check[i:i + 300] for i in range(0, len(resp_check), 300)]
    refer = list()


    # Поиск ссылки на регистрацию
    for row in chunks:
        if "Коптево" in row:
            refer = [i for i in row.split() if 'href' in i]
            refer = refer[0].split('mc/')
            refer = refer[1]
            break
    return refer[:-1]


def find_token(place_id=find_place_id()):
    page = requests.get('https://mftickets.technolab.com.ru/mc/' + place_id).text.split(',"')
    token = ''

    for list_token in page:
        if 'TOKEN' in list_token:
            token = list_token.split('"')
    return token[2]


def get_time_info(place_id=find_place_id(), token=find_token()):
    # Get place_date_id
    headers_dict = {"Sec-Ch-Ua": '"Chromium";v="97", " Not;A Brand";v="99"',
                    "Accept": "application/json, text/plain, */*",
                    "X-App-Token": token}
    page = (requests.get('http://mf.technolab.com.ru/v1/place/dates-list?place_id=' + place_id,
                         headers=headers_dict)).text.split(',')

    place_date_id = (str([i for i in page if 'place_date_id' in i]).split('"'))[5]

    # Выбор времени
    time_date = page[4:-4]
    time_date[0] = (time_date[0].split('{'))[1]
    time_date[-1] = (time_date[-1].split('}'))[0]

    day = str(input('Введите день: '))
    days_with_zero = ('1', '2', '3', '4', '5', '6', '7', '8', '9')

    if day in days_with_zero:
        day = '0' + day

    time_date_with_day = [i for i in time_date if day in i[9:11]]
    only_time = list()
    print('Есть следующее время для записи: ')

    for i in time_date_with_day:
        only_time.append((i[12:17]))

    final_time = list()

    for i in only_time:
        if i[0] == '0':
            i = str(int(i[1]) + 3) + i[2:5]

        else:
            i = str(int(i[0:2]) + 3) + i[2:5]

        final_time.append(i)

    [print(i) for i in final_time]
    my_time = str(input('Введите время, например 11:00: '))
    my_index = final_time.index(my_time)
    time_slot = (time_date[my_index])[1:-4]

    register_page = requests.get('https://mftickets.technolab.com.ru/mc/' + place_id + '/registration?timeSlot=' + time_slot + '&placeDateId=' + place_date_id, headers=headers_dict)
    return print(register_page.text)


get_time_info()
