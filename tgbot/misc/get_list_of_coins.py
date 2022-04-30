import json


def get_coins_names_list():
    list_of_coins = []
    with open("tgbot\\models\\exchange_rates.json","r", encoding="utf-8") as file:
            coins = json.load(file)
            for  coin in coins:
                list_of_coins.append(coin.get("name_long"))
                list_of_coins.append(coin.get("name_short"))
                
    return list_of_coins        