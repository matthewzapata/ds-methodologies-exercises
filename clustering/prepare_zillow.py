import pandas as pd
from sklearn.linear_model import LinearRegression

# include only single unit properties (e.g. no duplexes, no land/lot, ...) 
    # For some properties, you will need to use multiple fields to estimate whether it is a single unit property.
    # What will be considered single_unit properties are those with '1' for unitcnt and with a 
    # property land use description that makes sense for a single unit.
def only_singles(df):
    """Returns a DF with only single unit properties."""
    return df[(df['unitcnt'] == 1) & ((df['bathroomcnt'] > 0) | (df['bedroomcnt'] > 0)) & 
        ((df['propertylandusedesc'] == 'Single Family Residential') |
     (df['propertylandusedesc'] == 'Condominium') |
      (df['propertylandusedesc'] == 'Mobile Home') |
       (df['propertylandusedesc'] == 'Townhouse') |
        (df['propertylandusedesc'] == 'Residential General') |
         (df['propertylandusedesc'] == 'Commercial/Office/Residential Mixed Used'))]
          

# only include properties that include a latitude and longitude value.
def lat_lon(df):
    """Returns a DF with properties that have both latitude and longitude values."""
    return df[(df['latitude'].notna()) & (df['longitude'].notna())]


# takes in a dataframe and a list of columns names and returns the dataframe with the datatypes of those columns 
# changed to a non-numeric type
    # use this function to appropriately transform any numeric columns that should not be treated as numbers
def num_to_string_cols(df, list_of_columns):
    """Returns a DF that has changed the listed columns to an object data type."""
    for col in list_of_columns:
        df[col] = df[col].astype('object')
    return df


# accepts the unprepared zillow data frame and applies all the transformations above.
def single_lat_lon_objects(df, list_of_columns):
    """Returns a DF with transformed dtypes, latitude and longitude aren't missing, and only includes single unit homes."""
    return lat_lon(only_singles(num_to_string_cols(df, list_of_columns)))


# Write or use a previously written function to return the total missing values and the percent missing values by column.
def missing_vals_cols(df):
    """Prints the number of null values and the percent of null values for each column."""
    columns = df.columns
    for col in columns:
        n_missing_values = df[col].isna().sum()
        percent_missing = (n_missing_values/len(df[col]))*100
        if n_missing_values > 0:
            print(f'{col} has {n_missing_values} missing values, accounting for {percent_missing:.2f}% of that column.')

# Write or use a previously written function to return the total missing values and the percent missing values by row.
def missing_vals_rows(df):
    """Prints the number of null values and the percent of null values for each column."""
    n_rows = df.shape[0]
    ans = input('Do you need to reset the index? ')
    if ans == 'yes':
        df.reset_index(drop=True, inplace=True)
    for i in range(n_rows):
        n_missing_values = df.loc[i].isna().sum()
        percent_missing = (n_missing_values/len(df.loc[i]))*100
        if n_missing_values > 0:
            print(f'Row {(i + 1)} has {n_missing_values} missing values, accounting for {percent_missing:.2f}% of that row.')
        
# Write a function that will take a dataframe and list of column names as input and return the dataframe 
# with the null values in those columns replaced by 0. Explore the data and decide which columns it makes 
# sense to apply this transformation to.
def replace_nulls_with_zeros(df, list_of_columns):
    """Returns a DF where null values in listed columns are now zeros."""
    for col in list_of_columns:
        df[col] = df[col].fillna(0)
    return df

# Impute the values in land square feet.
    # For land square feet, the goal is to impute the missing values by creating a linear model where 
    # landtaxvaluedollarcnt is the x variable and the output/y-variable is the estimated land square feet. 
    # We'll then use this model to make predictions and fill in the missing values.
    # Write a function that accepts the zillow data frame and returns the data frame with the missing values filled in.
def impute_based_on_linear_model(df, x_variable, y_variable):
    model = LinearRegression()
    model.fit(df[[x_variable]].notna(), df[[y_variable]].notna())
    m = model.coef_
    b = model.intercept_
    print(f'y = {m}x + {b}')

# Run the first function that returns missing value totals by column: 
# Does the attribute have enough information (i.e. enough non-null values) to be useful? 
# Choose your cutoff and remove columns where there is not enough information available. 
# Document your cutoff and your reasoning.
def drop_col_if_too_many_nulls(df, threshold=.70):
    """Drops columns that have null percentage over the threshold."""
    cols = df.columns
    for col in cols:
        n_missing_values = df[col].isna().sum()
        percent_missing = (n_missing_values/len(df[col]))
        if percent_missing > threshold:
            df.drop([col], axis=1, inplace=True)


# Run the function that returns missing values by row: 
# Does the observation have enough information to use in our sample? 
# Choose your cutoff and remove rows where there is not enough information available. 
# Document your cutoff and your reasoning.
def drop_row_if_too_many_nulls(df, threshold=.30):
    """Drops rows that have null percentage over the threshold."""
    n_rows = df.shape[0]
    ans = input('Do you need to reset the index? ')
    if ans == 'yes':
        df.reset_index(drop=True, inplace=True)
    for i in range(n_rows):
        n_missing_values = df.loc[i].isna().sum()
        percent_missing = (n_missing_values/len(df.loc[i]))
        if percent_missing > threshold:
            df.drop(df.index[[i]], inplace=True)

# Of the remaining missing values, can they be imputed or otherwise estimated?
    # Impute those that can be imputed with the method you feel best fits the attribute.
    # Decide whether to remove the rows or columns of any that cannot be reasonably imputed.
    # Document your reasons for the decisions on how to handle each of those.


# Write a function that accepts a series (i.e. one column from a data frame) and summarizes how many 
# outliers are in the series. This function should accept a second parameter that determines how outliers 
# are detected, with the ability to detect outliers in 3 ways:
    # Using the IQR
    # Using standard deviations
    # Based on whether the observation is in the top or bottom 1%.
def how_many_outliers(series, criteria='iqr'):
    """Prints the number of outliers based on the criteria."""
    if criteria == 'iqr':
        print('Outliers are being found using IQR.')
        Q3 = series.quantile(.75)
        Q1 = series.quantile(.25)
        iqr = Q3 - Q1
        out = iqr*1.5
        upper = Q3 + out
        lower = Q1 - out
        n_outliers = 0
        for x in series:
            if x > upper or x < lower:
                n_outliers += 1
        print(f'Number of outliers: {n_outliers}')
    if criteria == 'sd':
        print('Outliers are being found using 2 standard deviations.')
        mean = series.mean()
        standard_deviation = series.std()
        # sd_range = standard_deviation * 2
        upper = mean + (2 * standard_deviation)
        lower = mean - (2 * standard_deviation)
        n_outliers = 0
        for x in series:
            if x > upper or x < lower:
                n_outliers += 1
        print(f'Number of outliers: {n_outliers}')
    if criteria == 'percentage':
        print('Outliers wil be based on top or bottom 1%.')
        sorted_series = series.sort_values()
        n_values_cutoff = round(len(series) * 0.01)
        print(f'Number of outliers: {n_values_cutoff * 2}')

# Use your function defined above to identify columns where you should handle the outliers.

# Write a function that accepts the zillow data frame and removes the outliers. 
# You should make a decision and document how you will remove outliers.

# consider using a describe DF to capture the upper and lower limits at the 
# beginning of the function instead of having the limits change.
def detect_and_remove_outliers(df):
    """Identifies any outliers in a DataFrame (IQR) and gives option to remove them."""
    cols = df.select_dtypes('number')
    ans = input('Do you need to reset the index? ')
    if ans == 'yes':
        df.reset_index(drop=True, inplace=True)
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
            print('\n')
            print(f'{col} has {n_outliers} outliers.')
            print(f'Upper limit: {upper}')
            print(f'Lower limit: {lower}')
            ans = input('Would you like to see the outliers? ')
            if ans == 'yes':
                print(outliers)
            answer = input('Would you like to delete these outliers? ')
            if answer == 'yes':
                df.reset_index(drop=True, inplace=True)
                for i, x in enumerate(df[col]):
                    if x > upper or x < lower:
                        df.drop([i], inplace=True)
            if answer == 'no':
                continue
    return df

# Is there erroneous data you have found that you need to remove or repair? If so, take action.

# Are there outliers you want to "squeeze in" to a max value? 
# (e.g. all bathrooms > 6 => bathrooms = 6). If so, make those changes.

