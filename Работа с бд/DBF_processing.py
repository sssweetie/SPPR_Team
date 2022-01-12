import csv
import pathlib
import zipfile
from dbfread import DBF
from pathlib import Path
import os

while True:
    dir_path = pathlib.Path.cwd()  # Получить путь к папке
    dbf_path = str(dir_path) + fr'/Countries'

    print('Choose your continent')
    content = os.listdir(dbf_path)
    for i, filename in enumerate(content):
        print(f'  -> {i}. {filename}')
    pos = int(input('Input: '))
    dbf_path += f'/{content[pos]}'

    print('Choose your country')
    content = os.listdir(dbf_path)
    for i, filename in enumerate(content):
        print(f'  -> {i}. {filename}')
    pos = int(input('Input: '))
    dbf_path += f'/{content[pos]}'

    fantasy_zip = zipfile.ZipFile(dbf_path)
    fantasy_zip.extract('gis_osm_buildings_a_free_1.dbf', dir_path)

    path = Path(dir_path, 'gis_osm_buildings_a_free_1.dbf') # Path - путь к файлу
    db = DBF(path, encoding='utf-8')                        # Декодируем ДБФ файл для чтения

    csv_fn = fr'{dir_path}/raw_csv/{content[pos][:-4]}.csv'                        # Берем наш путь, удаляем 4 символа, добавляем CSV
    with open(csv_fn, 'w', newline='', encoding='utf-8') as f:                # create a csv file, fill it with dbf content
        writer = csv.writer(f, delimiter=',')
        writer.writerow(db.field_names)                     # write the column name
        for record in db:                                   # write the rows
            writer.writerow(list(record.values()))
    print("file is completed")