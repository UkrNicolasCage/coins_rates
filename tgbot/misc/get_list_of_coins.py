import json


def get_coins_names_list(lower_case: bool = False):
    list_of_coins = []
    with open("tgbot\\models\\exchange_rates.json","r", encoding="utf-8") as file:
            coins = json.load(file)
            if lower_case == False:
                for  coin in coins:
                    list_of_coins.append(coin.get("name_long"))
                    list_of_coins.append(coin.get("name_short"))
            else:
                for  coin in coins:
                    list_of_coins.append(coin.get("name_long").lower())
                    list_of_coins.append(coin.get("name_short").lower())
    return list_of_coins        