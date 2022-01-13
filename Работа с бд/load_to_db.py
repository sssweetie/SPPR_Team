import csv
import pathlib
import pymongo
import os

ways_data = {}


def main():
    global ways_data
    dir_path = pathlib.Path.cwd()  # Получить путь к папке
    csv_path = fr'{str(dir_path)}/final_csv'

    content = os.listdir(csv_path)
    for i, filename in enumerate(content, 1):
        print(f' {i}. {filename}')
    csv_file = content[int(input('csv: ')) - 1]

    with open(fr'{csv_path}/{csv_file}', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            ways_data[int(row[0])] = {
                'way_id': int(row[0]),
                'lat': float(row[1]),
                'lon': float(row[2]),
                'area': float(row[3])
                'residents': float(row[4])
            }

    # write to mongoDB
    connection = 'mongodb+srv://ScorpionVSTU:VsTuBoY@scorpioncluster.kb9vl.mongodb.net/' \
                 'myFirstDatabase?retryWrites=true&w=majority'

    client = pymongo.MongoClient(connection)
    collection = client.SpprDb[csv_file[:-4]]
    collection.insert_many(ways_data.values())


if __name__ == '__main__':
    main()
