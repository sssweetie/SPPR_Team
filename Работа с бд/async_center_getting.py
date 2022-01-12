import csv
import pathlib
from time import time
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import os

node_coords = []
node_ids = []
way_ids = []


async def get_node_coordinates(session, node_pos, node_id: int, semaphore: asyncio.Semaphore) -> [int]:
    global node_coords
    url = f'https://www.openstreetmap.org/api/0.6/node/{node_id}'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.77 Safari/537.36'
    }

    async with semaphore:
        async with session.get(url=url, headers=headers) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')

            cs = soup.find('node')
            if cs:
                node_coords.append([float(cs['lat']), float(cs['lon'])])

    print(f"[INFO] Обработал  {node_pos}")


async def gather_data():
    global node_ids
    s = asyncio.Semaphore(value=50000)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(force_close=True)) as session:
        tasks = []

        for node_pos, node_id in enumerate(node_ids):
            task = asyncio.create_task(get_node_coordinates(session, node_pos, node_id, semaphore=s))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    global node_coords, node_ids
    dir_path = pathlib.Path.cwd()  # Получить путь к папке
    csv_path = fr'{str(dir_path)}/ways_with_nodes'

    content = os.listdir(csv_path)
    for i, filename in enumerate(content, 1):
        print(f' {i}. {filename}')
    csv_file = content[int(input('csv: '))-1]

    with open(fr'{csv_path}/{csv_file}', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        for row in reader:
            way_ids.append(row[0])
            node_ids.append(row[1])

    start_time = time()
    asyncio.run(gather_data())
    print(f'End time: {round(time() - start_time, 2)} sec')
    print(len(node_coords))

    csv_path = fr'{str(dir_path)}/ways_with_center'
    with open(fr'{csv_path}/{csv_file}', mode='w') as file:
        file.write('way_id,node_lat,node_lon\n')

    with open(fr'{csv_path}/{csv_file}', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        for node_pos, node in enumerate(node_coords):
            writer.writerow([way_ids[node_pos], node[0], node[1]])
    print('Write success')


if __name__ == '__main__':
    main()
