import pandas as pd

def get_titanic_data():
    from env import user, password, host, get_connection
    dbc = get_connection('titanic_db')
    print('Don\'t forget to assign to a df')
    return pd.read_sql('SELECT * FROM passengers', dbc)


def get_iris_data():
    from env import user, password, host, get_connection
    dbc = get_connection('iris_db')
    measurements = pd.read_sql('SELECT * FROM measurements', dbc)
    names = pd.read_sql('SELECT * FROM species', dbc)
    iris_df = measurements.merge(names, on='species_id')
    print('Don\'t forget to assign to a df')
    return iris_df
