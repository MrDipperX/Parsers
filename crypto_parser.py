import requests
from bs4 import BeautifulSoup
import os

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'crypto')
os.remove(path)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
}

numb = 1
for i in range(1, 92):
    url = f"https://coinmarketcap.com/?page={i}"

    resp = requests.get(url, headers=headers).text
    soup = BeautifulSoup(resp, "lxml")
    coins = soup.find("tbody").find_all("tr")

    for coin in coins:
        name = coin.find(class_="cmc-link").get("href").replace("/currencies/", "")[:-1]
        price = coin.find(class_="sc-131di3y-0 cLgOOr")

        if price:
            with open("crypto", "a") as file:
                file.write(f"{numb}.{name} : {price.text}\n")
        else:
            price = coin.find_all("td")[-2].find("span").text
            with open("crypto", "a") as file:
                file.write(f"{numb}.{name} : {price}\n")
        numb += 1