import csv
import datetime
import math

import requests
from fake_useragent import UserAgent
from selenium import webdriver
from multiprocessing import Process, Manager
import time
from bs4 import BeautifulSoup
import pathlib


def get_all_product_urls(start_url, mode):
    domain = "https://uzum.uz"
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    options.add_argument("user-agent=%s" % user_agent)
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    result = list()
    page = 1
    check = True
    try:
        while check:
            if mode == "query":
                url = f"{start_url}&currentPage={page}"
            else:
                url = f"{start_url}?currentPage={page}"
            browser.get(url)
            time.sleep(2)
            response = browser.page_source
            bs_object = BeautifulSoup(response, "lxml")
            cards_on_page = bs_object.find_all(name="div", class_="col-mbs-12 col-mbm-6 col-xs-4 col-md-3")
            card_urls_on_page = [domain + card.a["href"].split("?")[0] for card in cards_on_page]
            result.extend(card_urls_on_page)
            navigation_button = bs_object.find(name="div", class_="pagination-wrapper")
            if "style" in navigation_button.attrs:
                check = False
            else:
                page += 1
    finally:
        browser.close()
        browser.quit()
        result = set(result)
        return result


def get_basic_info_about_shop(shop_url):
    shop = shop_url.split("/")[3]
    headers = {"user-agent": UserAgent().chrome}
    url = f"https://api.umarket.uz/api/shop/{shop}/"
    response = requests.get(url=url, headers=headers)
    json_object = response.json()
    shop_id = json_object["payload"]["id"]
    shop_name = json_object["payload"]["title"]
    shop_description = json_object["payload"]["description"]
    shop_registration_date = int(str(json_object["payload"]["registrationDate"])[:10])
    shop_registration_date = datetime.datetime.utcfromtimestamp(shop_registration_date).strftime('%Y-%m-%d %H:%M:%S')
    shop_rating = json_object["payload"]["rating"]
    amount_shop_reviews = json_object["payload"]["reviews"]
    amount_shop_orders = json_object["payload"]["orders"]
    shop_account_name = json_object["payload"]["info"]["accountName"]
    if "ogrnip" in json_object["payload"]["info"].keys():
        shop_account_ogrn = json_object['payload']['info']['ogrnip']
    else:
        shop_account_ogrn = json_object['payload']['info']['ogrn']
    return {"id": shop_id, "name": shop_name, "description": shop_description,
            "registration_date": shop_registration_date, "rating": shop_rating, "reviews": amount_shop_reviews,
            "orders": amount_shop_orders, "account": shop_account_name,
            "ogrn": shop_account_ogrn}


def get_products_info(urls, mode):
    result = list()
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    # options.add_argument("user-agent=%s" % user_agent)
    headers = {"user-agent": user_agent}

    for url in urls:
        try:
            product_id = url.split("-")[-1]
            api_url = f"https://api.umarket.uz/api/v2/product/{product_id}"
            response = requests.get(url=api_url, headers=headers)
            json_object = response.json()["payload"]["data"]
            name = json_object["title"]

            category = json_object["category"]["title"]
            sub_category = json_object["category"]
            parent = json_object["category"]["parent"]
            while parent is not None:
                sub_category = sub_category["parent"]
                parent = sub_category["parent"]
                category = f"{sub_category['title']} - {category}"

            rating = json_object["rating"]
            amount_reviews = json_object["reviewsAmount"]
            amount_orders = json_object["ordersAmount"]
            amount_products = json_object['totalAvailableAmount']
            if json_object["description"] is not None:
                description = BeautifulSoup(json_object["description"], "lxml").text
            else:
                description = json_object["description"]
            additional_info = "; ".join(json_object["attributes"])
            images = json_object["photos"]
            images = [image["photo"]["720"]["high"] for image in images]
            images = "; ".join(images)

            comment_objects = json_object["comments"]
            comments = dict()
            for comment_object in comment_objects:
                comments[comment_object["commentType"]] = BeautifulSoup(comment_object["comment"], "lxml").text

            characteristic_objects = json_object["characteristics"]
            characteristics = dict()
            for characteristic_object in characteristic_objects:
                values = characteristic_object["values"]
                characteristics[characteristic_object["title"]] = [value["title"] for value in values]
            characteristics_list = list(characteristics.keys())

            if len(characteristics) > 0:
                prices = dict()
                price_objects = json_object["skuList"]
                for price_object in price_objects:
                    index = price_object["characteristics"][0]["charIndex"]
                    value_index = price_object["characteristics"][0]["valueIndex"]
                    prices[characteristics[characteristics_list[index]][value_index]] = dict()
                    full_price = price_object["fullPrice"]
                    purchase_price = price_object["purchasePrice"]
                    prices[characteristics[characteristics_list[index]][value_index]]["full_price"] = full_price
                    prices[characteristics[characteristics_list[index]][value_index]]["purchase_price"] = purchase_price
            else:
                prices = {"full_price": json_object["skuList"][0]["fullPrice"],
                          "purchase_price": json_object["skuList"][0]["purchasePrice"]}
            if mode == "store":
                result.append({"name": name, "characteristics": characteristics, "description": description,
                               "category": category, "additional_info": additional_info, "prices": prices,
                               "amount_orders": amount_orders, "amount_reviews": amount_reviews, "rating": rating,
                               "amount_products": amount_products, "url": url, "images": images})
            else:
                domain = "https://uzum.uz/"
                seller_name = json_object["seller"]["title"]
                seller_url = domain + json_object["seller"]["link"]
                result.append({"name": name, "characteristics": characteristics, "description": description,
                               "category": category, "additional_info": additional_info, "prices": prices,
                               "amount_orders": amount_orders, "amount_reviews": amount_reviews, "rating": rating,
                               "amount_products": amount_products, "images": images, "url": url, "seller": seller_name,
                               "seller_url": seller_url})
        except Exception as e:
            print(e, url)

    return result


def create_store_basic_info_csv():
    path = pathlib.Path("result_uzum", f"store_basic_info.csv")
    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Store ID", "Name of shop", "Description", "Registration date", "Rating",
                         "Reviews", "Orders", "Company", "OGRN",
                         "File with a complete list of store products"])


def write_into_file(products, mode, basic_info=None, file_name=None):
    if mode == "store":
        path = pathlib.Path("result_uzum", "store_basic_info.csv")
        with open(path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([basic_info['id'], basic_info['name'], basic_info['description'],
                             basic_info['registration_date'], basic_info['rating'], basic_info['reviews'],
                             basic_info['orders'], basic_info['account'], basic_info['ogrn'],
                             f"{basic_info['name']}_products.csv"])
        path = pathlib.Path("result_uzum", f"{basic_info['name']}_products.csv")
        with open(path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name of product", "Characteristics", "Description", "Category",
                             "Additional information", "Full Price", "Purchase Price", "Orders",
                             "Reviews", "Rating", "In stock", "Link to product", "Images"])
    else:
        path = pathlib.Path("result_uzum", f"{file_name}.csv")
        with open(path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name of product", "Characteristics", "Description", "Category",
                             "Additional information", "Full price", "Purchase Price", "Orders",
                             "Reviews", "Rating", "In stock", "Link to product", "Images",
                             "Store", "Link to store"])

    for product in products:
        name = product["name"]
        description = product["description"]
        category = product["category"]
        additional_info = product["additional_info"]
        amount_orders = product["amount_orders"]
        amount_reviews = product["amount_reviews"]
        rating = product["rating"]
        amount_products = product["amount_products"]
        url = product["url"]
        images = product["images"]

        if "full_price" in product["prices"].keys() and "purchase_price" in product["prices"].keys():
            characteristic_list = list()
            for key in product["characteristics"].keys():
                values = "; ".join(product["characteristics"][key])
                characteristic = f'{key}: {values}'
                characteristic_list.append(characteristic)
            characteristics = " || ".join(characteristic_list)
            full_price = product["prices"]["full_price"]
            purchase_price = product["prices"]["purchase_price"]
            if mode == "store":
                with open(path, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([name, characteristics, description, category, additional_info,
                                     full_price, purchase_price, amount_orders, amount_reviews, rating,
                                     amount_products, url, images])
            else:
                seller_name = product["seller"]
                seller_url = product["seller_url"]
                with open(path, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([name, characteristics, description, category, additional_info,
                                     full_price, purchase_price, amount_orders, amount_reviews,
                                     rating, amount_products, url, images, seller_name, seller_url])
        else:
            for key in product["prices"].keys():
                main_key = str()
                characteristic_list = list()
                full_price = product["prices"][key]["full_price"]
                purchase_price = product["prices"][key]["purchase_price"]
                for characteristic_key in product["characteristics"].keys():
                    if key not in product["characteristics"][characteristic_key]:
                        values = "; ".join(product["characteristics"][characteristic_key])
                        characteristic = f"{characteristic_key}: {values}"
                        characteristic_list.append(characteristic)
                    else:
                        main_key = characteristic_key
                characteristics = " || ".join(characteristic_list)
                if characteristics == "":
                    characteristics = f"{main_key}: {key}"
                else:
                    characteristics = f"{main_key}: {key} || {characteristics}"
                if mode == "store":
                    with open(path, "a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow([name, characteristics, description, category, additional_info,
                                         full_price, purchase_price, amount_orders, amount_reviews,
                                         rating, amount_products, url, images])
                else:
                    seller_name = product["seller"]
                    seller_url = product["seller_url"]
                    with open(path, "a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow([name, characteristics, description, category, additional_info,
                                         full_price, purchase_price, amount_orders, amount_reviews,
                                         rating, amount_products, url, images, seller_name, seller_url])


def main():
    mode_text = "store - store analysis, query - search query analysis, category - category analysis"
    input_text = f"Select program mode ({mode_text}): "
    program_mode = input(input_text)
    if program_mode == "store":
        store_urls = input("Enter links to store (https://uzum.uz/store_name) separated by commas: ").split(",")
        store_urls = [store_url.strip() for store_url in store_urls]
        store_urls_string = "\n       ".join(store_urls)
        print(f"[INFO] Program is running. Analysis of : \n       {store_urls_string}")
        create_store_basic_info_csv()
        for store_url in store_urls:
            start_time = time.time()
            basic_seller_info = get_basic_info_about_shop(shop_url=store_url)
            product_urls = get_all_product_urls(start_url=store_url, mode="store")
            products_info = get_products_info(urls=product_urls, mode="store")
            write_into_file(basic_info=basic_seller_info, products=products_info, mode="store")
            stop_time = time.time()
            print(f"[INFO] Scraping of the {store_url} is finished")
            print(f"[INFO] Scraping took {stop_time - start_time} seconds")
    elif program_mode == "query":
        queries = input("Enter queries (phone, airpods, iphone 14) separated by commas: ").split(",")
        queries = [query_url.strip() for query_url in queries]
        queries_string = "\n       ".join(queries)
        print(f"[INFO] Program is running. Analysis of : \n       {queries_string}")
        for query in queries:
            start_time = time.time()
            query_in_url = "%20".join(query.split(" "))
            query_url = f"https://uzum.uz/search?query={query_in_url}"
            product_urls = get_all_product_urls(start_url=query_url, mode="query")
            products_info = get_products_info(urls=product_urls, mode="query")
            write_into_file(products=products_info, mode="query", file_name=query)
            stop_time = time.time()
            print(f"[INFO] Scraping of the {query} is finished")
            print(f"[INFO] Scraping took {stop_time - start_time} seconds")
    else:
        input_text = "Enter category urls (https://uzum.uz/category/Elektronika-10020) separated by commas: "
        # category_urls = input(input_text).split(",")
        with open("uzum_categ_links", 'r') as f:
            category_urls = f.read().split()

        category_urls = [category_url.strip() for category_url in category_urls[17:]]
        # print(category_urls)
        # time.sleep(100)
        category_urls_string = "\n       ".join(category_urls)
        print(f"[INFO] Program is running. Analysis of : \n       {category_urls_string}")
        for category_url in category_urls:
            start_time = time.time()
            category = category_url.split("/")[-1]
            product_urls = get_all_product_urls(start_url=category_url, mode="category")
            products_info = get_products_info(urls=product_urls, mode="category")
            write_into_file(products=products_info, mode="category", file_name=category)
            stop_time = time.time()
            print(f"[INFO] Scraping of the {category} is finished")
            print(f"[INFO] Scraping took {stop_time - start_time} seconds")


if __name__ == "__main__":
    main()
    # with open("uzum_categ_links", 'r') as f:
    #     category_urls = f.read().split()
    # print(category_urls)
    #
    # for i in range(math.ceil(len(category_urls[5:]) / 5)):
    #     processes = []
    #     for j in range(5):
    #         if not i * 5 + j < len(category_urls[5:]):
    #             break
    #         p = Process(target=main, args=(category_urls[5:][i * 5 + j], ))
    #
    #         p.start()
    #         processes.append(p)
    #     for process in processes:
    #         process.join()