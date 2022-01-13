import csv
import pathlib
import pymongo
import os

ways_data = {}


def main():
    global ways_data
    dir_path = pathlib.Path.cwd()  # Получить путь к папке
    csv_path = fr'{str(dir_path)}/raw_csv'

    content = os.listdir(csv_path)
    for i, filename in enumerate(content, 1):
        print(f' {i}. {filename}')
    csv_file = content[int(input('csv: ')) - 1]

    csv_path = fr'{str(dir_path)}/ways_with_center'
    with open(fr'{csv_path}/{csv_file}', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            ways_data[int(row[0])] = {
                'way_id': int(row[0]),
                'lat': float(row[1]),
                'lon': float(row[2])
            }

    csv_path = fr'{str(dir_path)}/ways_with_area'
    with open(fr'{csv_path}/{csv_file}', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            ways_data[int(row[0])]['area'] = float(row[1])
            ways_data[int(row[0])]['residents'] = None

    csv_path = fr'{str(dir_path)}/residents'
    with open(fr'{csv_path}/{csv_file}', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        for row in reader:
            ways_data[int(row[0])]['residents'] = float(row[2])

    csv_path = fr'{str(dir_path)}/final_csv'
    with open(fr'{csv_path}/{csv_file}', mode='w') as file:
        file.write('way_id,lat,lon,area,residents\n')

    with open(fr'{csv_path}/{csv_file}', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        for way_id in ways_data:
            writer.writerow(ways_data[way_id].values())
    print('Write success')


if __name__ == '__main__':
    main()
