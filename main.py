import requests
from bs4 import BeautifulSoup
import re


############ Get data from Mercari ##################

URL = "https://www.mercari.com/jp/search/?keyword=%E6%9D%BE%E4%B8%8B%E5%B9%B8%E4%B9%8B%E5%8A%A9"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7"

}

response = requests.get(URL, headers=headers)
response.raise_for_status()

if 'json' in response.headers.get('content-type'):
    result = response.json()
else:
    result = response.text

soup = BeautifulSoup(result, "html.parser")

items_box = soup.select(".items-box")
item_name_tag = soup.select(".items-box-name")
item_price_tag = soup.select(".items-box-price")
sold_out = soup.select(".items-box-photo")

####### あるキーワードで検索したメルカリの結果の品名・価格・soldかどうかをCSVファイルに書き出す　##################

with open("product.csv", mode="w", encoding="utf8")as file:
    for i in range(len(items_box)):
        item_name = item_name_tag[i].getText()
        item_price = item_price_tag[i].getText()
        new_elems_photo = re.search('figcaption', str(sold_out[i].__str__))
        if new_elems_photo:
            file.write(f"{item_name} ,{item_price},{new_elems_photo.group(0)}\n")
        else:
            file.write(f"{item_name},{item_price}\n")







#
#
# price_tags = soup.find_all(name="div", class_="items-box-price")
# product_price = []
# for n in price_tags:
#     price = n.getText()
#     price_number = price.replace("¥", "")
#     price = price_number.replace(",", "")
#     price = int(price)
#     product_price.append(price)
#
# lowest_price = min(product_price)
# # print(lowest_price)
