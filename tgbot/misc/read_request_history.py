import json

def get_request_history_info():
        with open("tgbot/models/request_history.json", "r", encoding="utf-8") as file :
                users = json.load(file)
                return users
        
        
