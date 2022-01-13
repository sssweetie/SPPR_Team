import csv
import pathlib
from time import time
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import os

way_ids = []
ways_data = []


async def get_way_nodes(session, i, way_id: int, semaphore: asyncio.Semaphore) -> [int]:
    global ways_data
    url = f'https://www.openstreetmap.org/api/0.6/way/{way_id}/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.77 Safari/537.36'
    }

    async with semaphore:
        async with session.get(url=url, headers=headers) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')

            nodes = [int(tag['ref']) for tag in soup.find_all('nd')]
            if nodes:
                ways_data.append([way_id] + nodes)

    print(f"[INFO] Обработал  {i}")


async def gather_data():
    global way_ids
    s = asyncio.Semaphore(value=50000)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(force_close=True)) as session:
        tasks = []

        for i, way_id in enumerate(way_ids, 1):
            task = asyncio.create_task(get_way_nodes(session, i, way_id, semaphore=s))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    global way_ids
    dir_path = pathlib.Path.cwd()  # Получить путь к папке
    csv_path = fr'{str(dir_path)}/raw_csv'

    content = os.listdir(csv_path)
    for i, filename in enumerate(content, 1):
        print(f' {i}. {filename}')
    csv_file = content[int(input('csv: ')) - 1]

    with open(fr'{csv_path}/{csv_file}', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader, None)  # skip the headers
        way_ids += [row[0] for row in reader]

    start_time = time()
    asyncio.run(gather_data())
    print(f'End time: {round(time() - start_time, 2)} sec')
    print(len(ways_data))

    csv_path = fr'{str(dir_path)}/ways_with_nodes'
    with open(fr'{csv_path}/{csv_file}', mode='w') as file:
        file.write('way_id,*nodes_id\n')

    with open(fr'{csv_path}/{csv_file}', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        for node in ways_data:
            writer.writerow(node)
    print('Write success')


if __name__ == '__main__':
    main()
