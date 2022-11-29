import asyncio
import time
from aiohttp import ClientSession

import requests

# https://habr.com/ru/post/667630/

async def get_weather(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            print(f'{city}: {weather_json["weather"][0]["main"]}')


async def main(cities_):
    tasks = []
    for city in cities_:
        tasks.append(asyncio.create_task(get_weather(city)))

    for task in tasks:
        await task

def sync_main(cities):
    url = f'http://api.openweathermap.org/data/2.5/weather'

    for city in cities:
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
        response = requests.get(url=url, params=params).json()
        print(f'{city}: {response["weather"][0]["main"]}')


cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
          'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York']

print(time.strftime('%X'))

asyncio.run(main(cities))
# sync_main(cities)

print(time.strftime('%X'))
