import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup



headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
url ="https://minfin.com.ua/ua/currency/crypto/"


async def refresh_data():
    async with aiohttp.ClientSession() as session:
        response = await session.get(url= url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml") 
        coins_in_page=185
        last_page = int(soup.footer.text.split(" ")[-1]) // (coins_in_page*2)
        coin_info_usd = []
        coin_info_eur = []
        coin_info_uah = []
        
        for page in range(0,last_page):
            async with session.get(url= f'https://minfin.com.ua/api/currency/crypto/list/?cpp={coins_in_page}&page={page}',headers=headers) as response:
                data = dict(await response.json())['data']
                for coin in data:
                    coin_info_usd.append({
                            'name_long': coin['name'],
                            'name_short': coin['code'],
                            'price': coin['price']['usd'],
                            'capitalized': coin['market_cap']['usd'],
                            'trend': coin['trend']
                        })
                    coin_info_eur.append({
                            'name_long': coin['name'],
                            'name_short': coin['code'],
                            'price': coin['price']['eur'],
                            'capitalized': coin['market_cap']['eur'],
                            'trend': coin['trend']
                        })
                    coin_info_uah.append({
                            'name_long': coin['name'],
                            'name_short': coin['code'],
                            'price': coin['price']['uah'],
                            'capitalized': coin['market_cap']['uah'],
                            'trend': coin['trend']
                        })
                   
                   
    with open('tgbot/models/exchange_rates_usd.json',"w", encoding="utf-8") as file:
        json.dump(coin_info_usd, file, indent=4, ensure_ascii=False)
    
    with open('tgbot/models/exchange_rates_eur.json',"w", encoding="utf-8") as file:
        json.dump(coin_info_eur, file, indent=4, ensure_ascii=False)
    
    with open('tgbot/models/exchange_rates_uah.json',"w", encoding="utf-8") as file:
        json.dump(coin_info_uah, file, indent=4, ensure_ascii=False)
        
                

asyncio.run(refresh_data())