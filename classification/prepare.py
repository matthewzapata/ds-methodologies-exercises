from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd

def drop_columns(df):
    df.drop(['measurement_id', 'species_id'], axis=1, inplace=True)
    return df
    
def iris_rename(df):
    df.rename(columns={'species_name':'species'}, inplace=True)
    return df
    
def iris_label_encoder(df):
    species = LabelEncoder()
    species.fit(df.species)
    df['species_encode'] = species.transform(df.species)
    return species
    
def prep_iris(df):
    drop_columns(df)
    iris_rename(df)
    iris_label_encoder(df)
    return df

# ---------------------------------------------------------

def titanic_fillna(df):
    df.embark_town.fillna('Other', inplace=True)
    df.embarked.fillna('O', inplace=True)
    print('fill')
    return df

def titanic_drop_deck(df):
    df.drop(['deck'], axis=1, inplace=True)
    print('drop')
    return df

def titanic_encode_embarked(df):
    embarked_t = LabelEncoder()
    embarked_t.fit(df.embarked)
    df['embarked_encode'] = embarked_t.transform(df.embarked)
    print('encode')
    return df

def split_it(df, training_size=.7, random=123, strat=None):
    """Train test split. Returns train_df and test_df."""
    train, test = train_test_split(df, train_size=training_size, random_state=random, stratify=strat)
    print('Parameters are df, train_size, random_state, and stratify')
    print('Returns train, test')
    return train, test

def min_max(train, list_of_what_to_standardize):
    """Min-max normalization that returns a train_df and the scaler used"""
    scaler = MinMaxScaler()
    scaler.fit(train[list_of_what_to_standardize])
    train[list_of_what_to_standardize] = scaler.transform(train[list_of_what_to_standardize])
    print('Parameters are a training df and a list of what columns to standardize.')
    print('Returns the normalized training df and the scaler for scaling the test set.')
    return train, scaler
    
    
def prep_titanic(df):
    titanic_fillna(df)
    titanic_drop_deck(df)
    titanic_encode_embarked(df)
    # titanic_split(df)
    # titanic_min_max_age_fare(train)
    # global train, test, X_train, X_test, y_train, y_test, X, y
    # X = df.drop(['passenger_id', 'survived'], axis=1)
    # y = df[['survived']]
    # X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.80, random_state=10)
    # train = pd.concat((X_train, y_train), axis=1)
    # test = pd.concat((X_test, y_test), axis=1)
    # print('split')
    # scaler = MinMaxScaler()
    # scaler.fit(train[['fare', 'age']])
    # train[['fare', 'age']] = scaler.transform(train[['fare', 'age']])
    # print('standard')
    return df