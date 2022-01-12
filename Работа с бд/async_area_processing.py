import csv
import pathlib
from utils import calculate_polygon_area, Node
from time import time
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import os

ways_data = []
node_data = []


async def get_node_coordinates(session, way_pos, node_pos, node, semaphore: asyncio.Semaphore) -> [int]:
    global node_data
    url = f'https://www.openstreetmap.org/api/0.6/node/{node.id}'
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
                node_data[way_pos][node_pos].set_coords(float(cs['lat']), float(cs['lon']))

    print(f"[INFO] Обработал  {node_pos}/{way_pos}")


async def gather_data():
    global node_data
    s = asyncio.Semaphore(value=40000)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(force_close=True)) as session:
        tasks = []

        for way_pos, nodes in enumerate(node_data):
            for node_pos, node in enumerate(nodes):
                task = asyncio.create_task(get_node_coordinates(session, way_pos, node_pos, node, semaphore=s))
                tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    global ways_data, node_data
    dir_path = pathlib.Path.cwd()  # Получить путь к папке
    csv_path = fr'{str(dir_path)}/ways_with_nodes'

    content = os.listdir(csv_path)
    for i, filename in enumerate(content, 1):
        print(f' {i}. {filename}')
    csv_file = content[int(input('csv: ')) - 1]

    with open(fr'{csv_path}/{csv_file}', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        rows = [row for row in reader]
        for row in rows:
            ways_data.append([row[0]])
            # append without way_id and duplicating last node_id
            node_data.append([Node(node_id) for node_id in row[1:-1]])

    start_time = time()
    asyncio.run(gather_data())
    print(f'End time: {round(time() - start_time, 2)} sec')
    print(len(ways_data))

    errors = []
    for way_pos, nodes in enumerate(node_data):
        nodes.append(nodes[0])
        try:
            area = calculate_polygon_area(nodes)
            ways_data[way_pos].append(area)
        except Exception as e:
            print(ways_data[way_pos], nodes)
            errors.append([way_pos] + nodes)
    for error in errors:
        print('* ---', [node.i() for node in error[1:]])

    csv_path = fr'{str(dir_path)}/ways_with_area'
    with open(fr'{csv_path}/{csv_file}', mode='w') as file:
        file.write('way_id,area\n')

    with open(fr'{csv_path}/{csv_file}', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        for data in ways_data:
            writer.writerow(data)
    print('Write success')


if __name__ == '__main__':
    main()
