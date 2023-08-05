import requests
import fake_useragent
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random

headers = {
    'user-agent': user
}
url = "http://wiki.tgl.net.ru/index.php/%D0%A2%D0%BE%D0%BF_100_%D0%BB%D1%83%D1%87%D1%88%D0%B8%D1%85_%D0%BF%D0%BE%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%86_%D0%B8%D0%B7_%D1%81%D0%B1%D0%BE%D1%80%D0%BD%D0%B8%D0%BA%D0%B0_%D0%92._%D0%98._%D0%94%D0%B0%D0%BB%D1%8F_%22%D0%9F%D0%BE%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%86%D1%8B_%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BD%D0%B0%D1%80%D0%BE%D0%B4%D0%B0%22"

resp = requests.get(url, headers=headers).text
soup = BeautifulSoup(resp, "lxml")
proverbs = soup.find("div", class_="mw-content-ltr").find_all("li")

for proverb, i in zip(proverbs, range(len(proverbs))):
    print(f'{i+1}) {proverb.text}')
