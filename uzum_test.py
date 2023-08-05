# import csv
# import datetime
# import requests
# # from fake_useragent import UserAgent
# from selenium import webdriver
# import time
# from bs4 import BeautifulSoup
# import pathlib
#
#
# def get_all_product_urls(start_url, mode):
#     domain = "https://uzum.uz"
#     options = webdriver.ChromeOptions()
#     user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
#                  "(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
#     options.add_argument("user-agent=%s" % user_agent)
#     options.add_argument("--headless")
#     browser = webdriver.Chrome(options=options)
#     result = list()
#     page = 1
#     check = True
#     try:
#         while check:
#             if mode == "query":
#                 url = f"{start_url}&currentPage={page}"
#             else:
#                 url = f"{start_url}?currentPage={page}"
#             browser.get(url)
#             time.sleep(2)
#             response = browser.page_source
#             bs_object = BeautifulSoup(response, "lxml")
#             cards_on_page = bs_object.find_all(name="div", class_="col-mbs-12 col-mbm-6 col-xs-4 col-md-3")
#             card_urls_on_page = [domain + card.a["href"].split("?")[0] for card in cards_on_page]
#             result.extend(card_urls_on_page)
#             navigation_button = bs_object.find(name="div", class_="pagination-wrapper")
#             if "style" in navigation_button.attrs:
#                 check = False
#             else:
#                 page += 1
#     finally:
#         browser.close()
#         browser.quit()
#         result = set(result)
#         return result
#
# category_url = "https://uzum.uz/category/Elektronika-10020"
# # product_urls = list(get_all_product_urls(start_url=category_url, mode="category"))
#
# user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
#              "(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
# # options.add_argument("user-agent=%s" % user_agent)
# headers = {"user-agent": user_agent}
#
# product_id = "https://uzum.uz/product/Kovrik-dlya-myshki-R-Silver-G-2-33-256687".split("-")[-1]
# api_url = f"https://api.umarket.uz/api/v2/product/{product_id}"
# response = requests.get(url=api_url, headers=headers)
# json_object = response.json()["payload"]["data"]
#
# print(json_object)
#
# name = json_object["title"]

# category = json_object["category"]["title"]
# sub_category = json_object["category"]
# parent = json_object["category"]["parent"]
# # description = BeautifulSoup(json_object["description"], "lxml").text
# print(json_object["description"])
# print(description)

with open("uzum_categ_links", 'r') as f:
    categ_links = f.read().split()

print(categ_links)