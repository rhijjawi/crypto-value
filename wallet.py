#Wallet Value
from plyer import notification
from sqlite3 import Error
from datetime import datetime
import requests 
import json
import sqlite3
import re

now = datetime.now()
t_string = now.strftime("%H:%M")	
time = re.sub(":","",str(t_string))
time = int(time)
coins = {"MATIC":249.9, "ADA": 179.38}
wallet = "" 
tvalue = 0
for key, value in coins.items():
    conn = None
    price =  requests.get(f"https://api.coinbase.com/v2/exchange-rates?currency={key}")
    price = price.json()
    price = float(price["data"]["rates"]["USD"])
    val = round(price * value, 2)
    wallet += f"Value of {value} {key} = ${val}.\n"
    tvalue += round(val, 3)
    conn = sqlite3.connect(r"pricehistory.db")
    cur = conn.cursor()
    #cur.execute(f"INSERT INTO {key} VALUES ({price})")
    try:
        for row in cur.execute(f'SELECT * FROM {key}'):
            old = float(row[0])
    except Error as e:
        print(e)
        print(":(")
    if 800 < time < 810:
        try:     
            cur.execute(f"UPDATE {key} SET price={price}") 
            conn.commit()
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
    wallet += f"{key} 24 Price Change = {round(((price-old)/old)*100,2)}%\n"
    print(key)
    print(price)
    print(f"Old: {old}")
    del price
    del old

notification.notify(
    title=f"Total asset value = ${tvalue}",
    message=wallet,
    app_icon='app.ico',  # e.g. 'C:\\icon_32x32.ico'
    timeout=10,  # seconds
)