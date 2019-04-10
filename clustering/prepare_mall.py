import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Create a file named prepare_mall.py that contains functions that do the following:
    # detects any outliers
def detect_outliers(df):
    """Identifies any outliers in a DataFrame and gives option to remove them."""
    cols = df.select_dtypes('number')
    for col in cols:
        Q3 = df[col].quantile(.75)
        Q1 = df[col].quantile(.25)
        iqr = Q3 - Q1
        out = iqr*1.5
        upper = Q3 + out
        lower = Q1 - out
        n_outliers = 0
        outliers = []
        for x in df[col]:
            if x > upper or x < lower:
                outliers.append(x)
                n_outliers += 1
        if n_outliers > 0:
            print(f'{col} has {n_outliers} outliers. They are: {outliers}')
            answer = input('Would you like to delete these outliers? ')
            if answer == 'yes':
                for i, x in enumerate(df[col]):
                    if x > upper or x < lower:
                        df.drop([i], inplace=True)
            if answer == 'no':
                continue
    return df

    # encodes all the categorical columns, and adds the encoded column (i.e. it doesn't remove the original column)
def encode_cats(df):
    """Identifies 'object' columns and returns a DataFrame with additional encoded columns. Also returns a dict with encoders."""
    cols = df.select_dtypes('object')
    label_encoder_dict = {}
    for col in cols:
        x = LabelEncoder()
        x.fit(df[col])
        df[f'{col}_encoded'] = x.transform(df[col])
        label_encoder_dict[f'{col}'] = x
        return df, label_encoder_dict


    # accepts the unprepared mall customers data frame and applies all the transformations above
def out_outliers_and_encode(df):
    """Returns a DF that has been encoded along with the label encoder."""
    return encode_cats(detect_outliers(df))

# Write or use a previous function you have written that summarizes the data you have just read 
# into a dataframe in the ways we have discussed in previous modules 
# (sample view, datatypes, value counts, summary stats, ...)
def quick_breakdown(df):
    cols = df.columns
    print('Head and Tail')
    print(pd.concat([df.head(), df.tail()]))
    print('\n')
    print('Column Data Types')
    print(df.dtypes)
    for col in cols:
        print('\n')
        print(col)
        print('Most Common Values')
        print(df[col].value_counts().head())
        print('\n')
        print('Describe Table')
        print(df[col].describe(include='all'))

