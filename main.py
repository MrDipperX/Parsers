import requests
from bs4 import BeautifulSoup

url = "https://cryptoprices.com/wp-admin/admin-ajax.php?draw=1&columns[0][data]=rank&columns[0][name]=rank&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=name&columns[1][name]=name&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=price_usd&columns[2][name]=price_usd&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=percent_change_24h&columns[3][name]=percent_change_24h&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=market_cap_usd&columns[4][name]=market_cap_usd&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=volume_usd_24h&columns[5][name]=volume_usd_24h&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=available_supply&columns[6][name]=available_supply&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=weekly&columns[7][name]=weekly&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=actions&columns[8][name]=actions&columns[8][searchable]=true&columns[8][orderable]=false&columns[8][search][value]=&columns[8][search][regex]=false&start=0&length=100&search[value]=&search[regex]=false&action=coinmc_table&id=9&watchlist=false&currency=USD&_=1642185209750"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "X-Requested-With": "XMLHttpRequest"
}

result = requests.get(url, headers=headers).json()

for coin in result["data"]:
    name_soup = BeautifulSoup(coin["name"], "lxml")
    price_soup = BeautifulSoup(coin["price_usd"], "lxml")

    name_soup = name_soup.find("img").get("alt")
    price_soup = price_soup.find_all("span")[-1].text
    print(name_soup + " - " + price_soup)
