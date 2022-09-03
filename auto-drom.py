import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
}
numb = 1
url = f"https://auto.drom.ru/all/page{numb}/"

resp = requests.get(url, headers=headers).text
soup = BeautifulSoup(resp, "lxml")
autos = soup.find("div", class_="eaczv700").find_all("a", class_="ewrty961")

print(autos)


# for auto in autos:
#     title = auto.find("div",class_="e3f4v4l2").text
#     description = auto.find("div", class_="e162wx9x0").text
#     price = auto.find("div",class_="ef5lgk11").text
#     print(f"\n{title}  Цена:{price}\n{description}")
