import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
}

url = "https://gravityfalls.fandom.com/ru/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%8D%D0%BF%D0%B8%D0%B7%D0%BE%D0%B" \
      "4%D0%BE%D0%B2"

resp = requests.get(url, headers=headers).text
soup = BeautifulSoup(resp, "lxml")
series = soup.find("table", class_="sortable").find_all("tr")

for episod in series[1:]:
    number = episod.find("td").text
    name = episod.find_all("td")[2].find("a").text
    print("Серия №"+number.replace("\n", "")+": "+name)

