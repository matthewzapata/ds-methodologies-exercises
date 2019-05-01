import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import prepare

sales = pd.read_csv('sales.csv', sep='\t', index_col=0)
items = pd.read_csv('items.csv', sep='\t', index_col=0)
stores = pd.read_csv('stores.csv', sep='\t', index_col=0)

items_sales = pd.merge(items, sales, left_on='item_id', right_on='item')
heb = pd.merge(items_sales, stores, left_on='store', right_on='store_id')
heb.drop(['item', 'store'], axis=1, inplace=True)

heb.sale_date = pd.to_datetime(heb.sale_date, format=%a, %d %b %Y %H:%M:%S %Z)
heb.set_index('sale_date', inplace=True)

heb['sale_total'] = heb.item_price * heb.sale_amount
heb.head()

plt.figure(figsize=(15, 7))
heb.groupby(heb.index.date, 'store_id')

plt.figure(figsize=(15,6))
for i in range(1, 11):
    sns.lineplot(data=heb.groupby('store_id').resample('D').sale_total.sum().loc[i], label=f'Store {i}')
plt.ylabel('Dollars')
plt.xlabel('Date')
plt.title('Daily total sales by store over time')
plt.legend()
plt.show()

plt.figure(figsize=(15,6))
for i in range(1, 11):
    sns.lineplot(data=heb.groupby('store_id').resample('W').sale_total.sum().loc[i], label=f'Store {i}')
plt.ylabel('Dollars')
plt.xlabel('Date')
plt.title('Weekly total sales by store over time')
plt.legend()
plt.show()

plt.figure(figsize=(15,6))
for i in range(1, 11):
    sns.lineplot(data=heb.groupby('store_id').resample('M').sale_total.sum().loc[i], label=f'Store {i}')
plt.ylabel('Dollars')
plt.xlabel('Date')
plt.title('Monthly total sales by store over time')
plt.legend()
plt.show()