import json
from tgbot.misc.change_history import change

from tgbot.misc.read_request_history import get_request_history_info


async def create_answer(id,data,currency):
    # data = coin
    # id = user_id
    # currency = code of currency that will be used by user (usd, eur, uah)
    with open(f"tgbot/models/exchange_rates_{currency}.json","r", encoding="utf-8") as file:
        coins = json.load(file)
        for coin in coins:
            if coin.get('name_long').lower() == data.lower() or coin.get("name_short").lower() == data.lower():
                name_long = coin.get("name_long")
                name_short = coin.get("name_short")
                price = str(coin.get("price"))
                capitalized = str(coin.get("capitalized"))
                trend = coin.get("trend")
                change_coins_all = [
                    str(trend.get("day")).strip(),
                    str(trend.get("week")).strip(),
                    str(trend.get("month")).strip(),
                    str(trend.get("year")).strip(), 
                ]
                
                # some prettier
                
                for i in range(len(change_coins_all)):
    
                    if change_coins_all[i][0] == "-":
                        change_coins_all[i] = change_coins_all[i] + "%📉"
                    else:
                        change_coins_all[i] = change_coins_all[i] + "%📈"
                
                if currency == "usd":
                    price = price + " USD"
                    capitalized = capitalized + " USD"
                elif currency == "eur":
                    price = price + " EUR"
                    capitalized = capitalized + " EUR"
                else:
                    price = price + " UAH"
                    capitalized = capitalized + " UAH"
                
                # end of prettier part
                break      
                       
    users = get_request_history_info()               
    with open("tgbot/models/request_history.json", "w") as file :   
        
        for user in users:
            if user.get("id") == id:
                user["history"] = change(user.get("history"), data)
            
        json.dump(users, file, indent=4, ensure_ascii=False)
        
    
    answer = str(f"{name_long}({name_short})\n"
                        f"Price:  {price}\n"
                        f"Capitalized:  {capitalized}\n"
                        f"Change:\n"
                        f"        Day: {change_coins_all[0]}\n"
                        f"        Week: {change_coins_all[1]}\n"
                        f"        Month: {change_coins_all[2]}\n"
                        f"        Year:  {change_coins_all[3]}"
                )
    return answer