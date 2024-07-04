import aiohttp


async def geocode_address(address: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://geocode-maps.yandex.ru/1.x/?apikey=YOUR_API_KEY&format=json&geocode={address}'
        ) as response:
            data = await response.json()
            coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            return coordinates
