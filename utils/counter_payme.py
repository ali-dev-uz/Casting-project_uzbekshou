import aiohttp


async def fetch_data():
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            for summa in await response.json():
                if summa['Ccy'] == 'USD':
                    return float(summa['Rate'])


