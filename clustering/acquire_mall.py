import pandas as pd
from env import password, host, user, get_connection

# Create a file named acquire_mall.py that contains a function that returns the data from the 
# customers table in the mall_customers database.
def get_customers():
    dbc = get_connection('mall_customers')
    return pd.read_sql('SELECT * FROM customers', dbc)