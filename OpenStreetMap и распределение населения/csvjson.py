# import pathlib
# import csv
# from dbfread import DBF
# from pathlib import Path
# dir_path = pathlib.Path.cwd()                           # Получить путь к папке
# path = Path(dir_path, "gis_osm_buildings_a_free_1.dbf") # Path - путь к файлу
# csv_fn = str(path)[:-4] + ".csv"                        # Берем наш путь, удаляем 4 символа, добавляем CSV
# db = DBF(path, encoding='utf-8')                        # Декодируем ДБФ файл для чтения
# with open(csv_fn, 'w', newline='') as f:                # create a csv file, fill it with dbf content
#     writer = csv.writer(f, delimiter=',')
#     writer.writerow(db.field_names)                     # write the column name
#     for record in db:                                   # write the rows
#         writer.writerow(list(record.values()))
# print("file is completed")
import json
import pathlib
from dbfread import DBF
from pathlib import Path
dir_path = pathlib.Path.cwd()                           # Получить путь к папке
path = Path(dir_path, "gis_osm_buildings_a_free_1.dbf") # Path - путь к файлу
json_fn = str(path)[:-4] + ".json"                      # Берем наш путь, удаляем 4 символа, добавляем CSV
db = DBF(path, encoding='utf-8')                        # Декодируем ДБФ файл для чтения
with open(json_fn, 'w') as f:                           # создаем JSON file
    for record in db:                                   # write the rows
        records = list(record.values())                 # records - list of values
        dictionary = {
            "id": records[0],
            "code": records[1],
            "class": records[2],
            "name": records[3],
            "type": records[4],
        }
        json_object = json.dumps(dictionary, indent=5)  # make a json object
        f.write(json_object)                            # write a json object
print("file is completed")