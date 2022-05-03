import json
import aiohttp
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
        
        last_page = int(int(soup.find("nav").find_all("a",class_="pagination-button")[-2].text) / 2)
        coin_info = []
        
        for page in range(1,last_page):
            async with session.get(url= f'https://minfin.com.ua/ua/currency/crypto/{page}',headers=headers) as response:
                    soup = BeautifulSoup(await response.text(), "lxml") 
                    coins = soup.find_all(class_="coin js-sort-elem")
                    
                    for coin in coins:
                        name_long = coin.find(class_ = "blue coin-name--long").text
                        name_short = coin.find(class_ = "grey coin-name--short").text
                        price = coin.find(class_="coin-item coin-price row-nocollapsed").get("data-sort-val")
                        capitalized = coin.find(class_="coin-item coin-capital row-collapsed").get("data-sort-val")                        
                        days_change= coin.find(class_="coin-item coin-changes row-collapsed").get("data-sort-val")
                        
                        coin_info.append({
                            'name_long': name_long,
                            'name_short': name_short,
                            'price': price,
                            'capitalized': capitalized,
                            'days_change': days_change
                        })
        
  
        with open('tgbot\\models\\exchange_rates.json',"w", encoding="utf-8") as file:
            json.dump(coin_info, file, indent=4, ensure_ascii=False)
        
    
    