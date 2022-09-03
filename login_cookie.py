import requests
import fake_useragent
from bs4 import BeautifulSoup

link = "https://ru.stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fru.stackoverflow.com%2f"

user = fake_useragent.UserAgent().random

session = requests.Session()

header = {
    'user-agent': user
}

data = {
    'email': 'aki.animeking.562@gmail.com',
    'password': 'Naruhina'
}

response = session.post(link, data=data, headers=header)


profile_url = "https://ru.stackoverflow.com/users/481654"
profile_resp = session.get(profile_url, headers=header).text

soup = BeautifulSoup(profile_resp, "lxml")
username = soup.find("div", class_="fs-headline2").text

cookies_dict = [
    {"domain": key.domain, "name": key.name, "path": key.path, "value": key.value}
    for key in session.cookies
]

session2 = requests.Session()

for cookies in cookies_dict:
    session2.cookies.set(**cookies)

resp = session2.get(profile_url, headers=header)
print(resp)



