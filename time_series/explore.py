import pandas as pd

sales = pd.read_csv('sales.csv', sep='\t', index_col=0)
items = pd.read_csv('items.csv', sep='\t', index_col=0)
stores = pd.read_csv('stores.csv', sep='\t', index_col=0)

items_sales = pd.merge(items, sales, left_on='item_id', right_on='item')
heb = pd.merge(items_sales, stores, left_on='store', right_on='store_id')
heb.drop(['item', 'store'], axis=1, inplace=True)

