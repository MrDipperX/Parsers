import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
}
url = "https://daryo.uz/"

resp = requests.get(url, headers=headers).text
soup = BeautifulSoup(resp, "lxml")
news = soup.find("div", class_="content").find("main", class_="maincontent").find_all("section", "model")
i = 1

for event in news:
    category = event.find(class_="article__cat").text
    date = event.find(class_="article__meta").find(class_="meta-date").text
    title = event.find(class_="article__link")['title']

    print(f"{i}) Category: {category.strip()} \n DateTime: {date.strip()} \n Title: {title}\n")
    i += 1
