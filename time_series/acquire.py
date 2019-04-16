import requests
import pandas as pd

def get_items():    
    response = requests.get('https://python.zach.lol/api/v1/items')
    data = response.json()
    items_1 = pd.DataFrame(data['payload']['items'])

    response = requests.get('https://python.zach.lol/api/v1/items?page=2')
    data = response.json()
    items_2 = pd.DataFrame(data['payload']['items'])

    response = requests.get('https://python.zach.lol/api/v1/items?page=3')
    data = response.json()
    items_3 = pd.DataFrame(data['payload']['items'])

    items = pd.concat([items_1, items_2, items_3])
    items.reset_index(inplace=True, drop=True)
    return items


def get_stores():
    response = requests.get('https://python.zach.lol/api/v1/stores')
    data = response.json()
    stores = pd.DataFrame(data['payload']['stores'])
    return stores


def get_sales():
    url = '/api/v1/sales'
response = requests.get('https://python.zach.lol' + url)
data = response.json()
max_pages = data['payload']['max_page']
url = data['payload']['next_page']
all_data = {}
all_data['page_0'] = pd.DataFrame(data['payload']['sales'])
page = data['payload']['page']
print(page)

while data['payload']['page'] < max_pages:
    if url == None:
        break
    response = requests.get('https://python.zach.lol' + url)
    data = response.json()
    page = data['payload']['page']
    print(page)
    url = data['payload']['next_page']
    all_data[f'page {page}'] = pd.DataFrame(data['payload']['sales'])
    if page%10 == 0:
        print(f'page {page}')
    
sales = pd.concat(all_data)
sales.reset_index(inplace=True, drop=True)
return sales

def get_heb_data():
    items = get_items()
    stores = get_stores()
    sales = get_sales()
    items_sales = pd.merge(items, sales, left_on='item_id', right_on='item')
    shopping_df = pd.merge(items_sales, stores, left_on='store', right_on='store_id')
    shopping_df.drop(['item', 'store'], axis=1, inplace=True)
    return heb_df