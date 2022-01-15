import requests
from bs4 import BeautifulSoup
import csv

CSV = 'Guinea-Bissau.csv'
HOST = 'https://en.wikipedia.org/'
URL = 'https://en.wikipedia.org/wiki/List_of_cities_in_Guinea-Bissau'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 OPR/82.0.4227.33'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content_from_table(html, city_num, population_num):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='wikitable')
    t_body = table.find('tbody')
    items = t_body.find_all('tr')
    city_population = []

    count = 0
    for item in items:
        count += 1
        if(count > 3):
            row= item.find_all('td')
            city_population.append(
                {
                    'city': row[city_num].find('a').get_text(),
                    'population': row[population_num].get_text(strip=True)
                }
            )

    return city_population


def get_content_from_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find_all('ol')
    items = ul.find_all('li')

    city_population = []
    count = 0
    for item in items:
        count += 1
        if(count > 0):
            row= item.find_all('td')
            print(item)
            if (item.find('b') != None):
                city_population.append(
                    {
                        'city': row.find('a').get_text(),
                        'population': row.find('b').get_text().replace("Pop. ", "")
                    }
                )

    return city_population


def save_content(items, path):
    with open(path, 'w', newline='', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['City', 'Population'])

        for item in items:
            if (item['population'] != ''):
                writer.writerow([item['city'], item['population']])
                print(item)


def parser():
    html = get_html(URL)
    if (html.status_code == 200):
        city_population = []
        selection = int(input('В какой форме представлены данные: 1 - в виде таблицы, 2 - в виде списка '))

        if(selection == 1):
            city_num = int(input('Номер столбца с названием города: ').strip())
            population_num = int(input('Номер столбца с численностью населения: ').strip())
            city_population.extend(get_content_from_table(html.text, city_num, population_num))
        elif(selection == 2):
            city_population.extend(get_content_from_list(html.text))

        print(city_population)
        CSV = input('Название файла: ') + '.csv'
        print(CSV)
        save_content(city_population, CSV)
    else:
        print('Error')


parser()
