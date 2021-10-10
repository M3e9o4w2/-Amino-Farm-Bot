import time
import json
import uuid
import requests
from threading import Thread
from binascii import hexlify
from os import urandom
from uuid import UUID
from functools import reduce
from base64 import b85decode, b64decode

def start():
    for i in "Выберите тип фарма.\n\n        По ссылкам >> 1.\n        По uid >> 2.\n        С передачаей монет >> 3.\n\n        Введите цифру >> ":
        print(i, end = "", flush = True)
        time.sleep(0.05)
  
    choice = int(input())

    
    if choice == 1:
        try:
            links = open("links.txt", "r").read().split()
        
        except:
            for i in "\nОшибка.\n    Отсутствует файл links.txt с ссылками.\n":
                print(i, end = "", flush = True)
                time.sleep(0.05)
            
            exit()
            
        for link in links:
            Thread(target = farm, args = (link,)).start()
        
            for i in "\nStart farm on {}.".format(link):
                print(i, end = "", flush = True)
                time.sleep(0.05)


    if choice == 2:
        try:
            uids = open("uid.txt", "r").read().split()
        
        except:
            for i in "\nОшибка.\n    Отсутствует файл uid.txt с uid.\n":
                print(i, end = "", flush = True)
                time.sleep(0.05)
                
            exit()
           
        for uid in uids:
            Thread(target = farm, args = (None, uid,)).start()
        
            for i in "\nStart farm on {}.".format(uid):
                print(i, end = "", flush = True)
                time.sleep(0.05)
    if choice == 3:
        for i in "\nВыберите тип входа.\n\n        Обычный >> 1.\n        sid >> 2.\n\n        Введите цифру >> ":
            print(i, end = "", flush = True)
            time.sleep(0.05)
  
        choice = int(input())
        
        for i in "\n        Введите ссылку на пост >> ":
            print(i, end = "", flush = True)
            time.sleep(0.05)
            
        link = input()
        
        if choice == 1:
            open("sids.txt", "w")
            try:
                emails = open("emails.txt", "r").read().split()
            
            except:
                for i in "\nОшибка.\n    Отсутствует файл emails.txt с почтами.\n":
                    print(i, end = "", flush = True)
                    time.sleep(0.05)
                
                exit()
               
            try:
                passwords = open("passwords.txt", "r").read().split()
            
            except:
                for i in "\nОшибка.\n    Отсутствует файл passwords.txt с паролями.\n":
                    print(i, end = "", flush = True)
                    time.sleep(0.05)
                
                exit()
            
            for email, password in zip(emails, passwords):
               Thread(target = with_login, args = (email, password, None, link)).start()
               
               for i in "\nStart farm on {}.".format(email):
                    print(i, end = "", flush = True)
                    time.sleep(0.05)
                    
        if choice == 2:
            try:
                sids = open("sids.txt", "r").read().split()
            
            except:
                for i in "\nОшибка.\n    Отсутствует файл sids.txt с sid.\n":
                    print(i, end = "", flush = True)
                    time.sleep(0.05)
                
                exit()
                
            for sid in sids:
               Thread(target = with_login, args = (None, None, sid, link)).start()
               
               for i in "\nStart farm on {}.".format(sid[sid.index("=") + 1:]):
                    print(i, end = "", flush = True)
                    time.sleep(0.05)
               
def with_login(email = None, password = None, sid = None, link = None):
    headers = {"NDCDEVICEID": "2270ED6CECADB44285E55C169570C865F3C20FD1DE1A7B8E8743E88AE0124B4E9669D2CE07864B6362"}
    
    if sid:
        headers["NDCAUTH"] = sid
        sid = sid[sid.index("=") + 1:]
        uid = json.loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + "=" * (-len(sid) % 4)).encode())[1:-20].decode())["2"]
        
    
    if email:
        data = json.dumps({
           "email": email,
           "v": 2,
           "secret": f"0 {password}",
           "deviceID": "2270ED6CECADB44285E55C169570C865F3C20FD1DE1A7B8E8743E88AE0124B4E9669D2CE07864B6362",
            "clientType": 100,
            "action": "normal",
            "timestamp": int(time.time() * 1000)
        })

        response = requests.post(f"https://aminoapps.com/api-p/g/s/auth/login", data=data, headers = headers)
    
        headers["NDCAUTH"] = "sid=" + response.json()["sid"]
        open("sids.txt", "a").write(headers["NDCAUTH"] + "\n")
        uid = response.json()["userProfile"]["uid"]
        
    farm(uid = uid)
        
    link_data = requests.get(f"https://aminoapps.com/api-p/g/s/link-resolution?q={link}").json()["linkInfoV2"]["extensions"]["linkInfo"]
        
    blog_id = link_data["objectId"]
    com_id = link_data["ndcId"]
        
    requests.post(url = f"https://aminoapps.com/api-p/x{com_id}/s/community/join", headers = headers)
        
    coins = int(requests.get("https://aminoapps.com/api-p/g/s/wallet", headers = headers).json()["wallet"]["totalCoins"])
        
    while coins != 0:
        if coins >= 500: coins = 500
            
        data = {
            "coins": coins,
            "tippingContext": {"transactionId": str(UUID(hexlify(urandom(16)).decode('ascii')))},
            "timestamp": int(time.time() * 1000)
        }

        url = f"https://aminoapps.com/api-p/x{com_id}/s/blog/{blog_id}/tipping"
    
        data = json.dumps(data)
    
        response = requests.post(url, data=data,headers = headers)
            
        coins = int(requests.get("https://aminoapps.com/api-p/g/s/wallet", headers = headers).json()["wallet"]["totalCoins"])
            
    requests.post(url = f"https://aminoapps.com/api-p/x{com_id}/s/community/leave", headers = headers)

def farm(link = None, uid = None):
    ad_data = {"reward": {"ad_unit_id": "255884441431980_807351306285288", "credentials_type": "publisher", "custom_json": {"hashed_user_id": None}, "demand_type": "sdk_bidding", "event_id": None, "network": "facebook", "placement_tag": "default", "reward_name": "Amino Coin", "reward_valid": "true", "reward_value": 2, "shared_id": "dc042f0c-0c80-4dfd-9fde-87a5979d0d2f", "version_id": "1569147951493", "waterfall_id": "dc042f0c-0c80-4dfd-9fde-87a5979d0d2f"}, "app": {"bundle_id": "com.narvii.amino.master", "current_orientation": "portrait", "release_version": "3.4.33567", "user_agent": "Dalvik\\/2.1.0 (Linux; U; Android 10; G8231 Build\\/41.2.A.0.219; com.narvii.amino.master\\/3.4.33567)"}, "date_created": 1620295485, "session_id": "49374c2c-1aa3-4094-b603-1cf2720dca67", "device_user": {"country": "US", "device": {"architecture": "aarch64", "carrier": {"country_code": 602, "name": "Vodafone", "network_code": 0}, "is_phone": "true", "model": "GT-S5360", "model_type": "Samsung", "operating_system": "android", "operating_system_version": "29", "screen_size": {"height": 2260, "resolution": 2.55, "width": 1080}}, "do_not_track": "false", "idfa": "7495ec00-0490-4d53-8b9a-b5cc31ba885b", "ip_address": "", "locale": "en", "timezone": {"location": "Asia\\/Seoul", "offset": "GMT+09: 00"}, "volume_enabled": "true"}}
  
    ad_headers = {"cookies": "__cfduid=d0c98f07df2594b5f4aad802942cae1f01619569096", "authorization": "Basic NWJiNTM0OWUxYzlkNDQwMDA2NzUwNjgwOmM0ZDJmYmIxLTVlYjItNDM5MC05MDk3LTkxZjlmMjQ5NDI4OA=="}
    
    if link:
        uid = requests.get(f"https://aminoapps.com/api-p/g/s/link-resolution?q={link}").json()["linkInfoV2"]["extensions"]["linkInfo"]["objectId"]

    ad_data["reward"]["custom_json"]["hashed_user_id"] = uid
        
    for i in range(50):
        ad_data["reward"]["event_id"] = str(uuid.uuid4())
        requests.post("https://ads.tapdaq.com/v4/analytics/reward", headers = ad_headers, json = ad_data)

for i in "Created by Ananasik.\n        https://t.me/meow3942.\n\n":
    print(i, end = "", flush = True)
    time.sleep(0.05)
	
start()
print()
