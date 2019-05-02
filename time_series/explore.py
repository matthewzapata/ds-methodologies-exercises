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

heb.sale_date = pd.to_datetime(heb.sale_date, format='%a, %d %b %Y %H:%M:%S %Z')
heb.set_index('sale_date', inplace=True)

heb['sale_total'] = heb.item_price * heb.sale_amount
heb.head()


plt.subplot(311)
plt.figure(figsize=(15,6))
for i in range(1, 11):
    sns.lineplot(data=heb.groupby('store_id').resample('D').sale_total.sum().loc[i], label=f'Store {i}')
plt.ylabel('Dollars')
plt.xlabel('Date')
plt.title('Daily total sales by store over time')
plt.legend()
plt.show()

plt.subplot(312)
plt.figure(figsize=(15,6))
for i in range(1, 11):
    sns.lineplot(data=heb.groupby('store_id').resample('W').sale_total.sum().loc[i], label=f'Store {i}')
plt.ylabel('Dollars')
plt.xlabel('Date')
plt.title('Weekly total sales by store over time')
plt.legend()
plt.show()

plt.subplot(313)
plt.figure(figsize=(15,6))
for i in range(1, 11):
    sns.lineplot(data=heb.groupby('store_id').resample('M').sale_total.sum().loc[i], label=f'Store {i}')
plt.ylabel('Dollars')
plt.xlabel('Date')
plt.title('Monthly total sales by store over time')
plt.legend()
plt.show()

for i in heb.store_id.unique():
    df = heb[heb.store_id == i]
    df['item_cat'] = df.item_name
    item_list = ['Suave Naturals Moisturizing Body Wash Creamy Tropical Coconut', 
                 'Guava', 
                 'Scotch Removable Clear Mounting Squares - 35 Ct', 
                 'Garnier Nutritioniste Moisture Rescue Fresh Cleansing Foam', 
                 'Hood Latte Iced Coffee Drink Vanilla Latte', 
                 'Betty Crocker Twin Pack Real Potatoes Scalloped 2 Pouches For 2 Meals - 2 Pk', 
                 'Sundown Naturals Essential Electrolytes Tropical Punch Watermelon And Fruit Punch Gummies - 60 Ct']
    df.loc[~df.item_name.isin(item_list), 'item_cat'] = 'other'
    df = df.groupby(['item_cat']).resample('M').sale_amount.sum().reset_index()
    plt.figure(figsize=(15, 8))
    sns.lineplot(x=df.sale_date, y=df.sale_amount, hue=df.item_cat)
    plt.show()