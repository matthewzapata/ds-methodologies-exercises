import pandas as pd
import pytz, datetime


# Write a function to convert a date to a datetime data type.
def date_to_datetime(date, format_of_date=None):
    """Returns a series converted to datetime."""
    return pd.to_datetime(date, format=format_of_date)

# Write a function to change a datetime to UTC.
def datetime_to_UTC(dates, format_of_date, timezone="CST6CDT"):
    """Changes date string to UTC datetime. Returns a series."""
    new_datetime = []
    for date in dates:
        date = str(date)
        local = pytz.timezone(timezone)
        naive = datetime.datetime.strptime(date, format_of_date)
        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        utc_dt.strftime(format_of_date)
        new_datetime.append(utc_dt)
    
    return new_datetime

# Write a function to parse a date column into 6 additional columns (while keeping the original date): 
# year, quarter, month, day of month, day of week, weekend vs. weekday
def parse_date_into_columns(df, dates, format_of_date):
    """Creates new columns derived from the dates inputted."""
    years = []
    quarter_list = []
    months_list = []
    day_of_month = []
    day_of_week = []
    weekend_or_weekday = []
    for date in dates:
        date = str(date)
        parsed_date = datetime.datetime.strptime(date, format_of_date)
        weekday_num = parsed_date.weekday()
        day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_of_week.append(day_list[weekday_num])
        if '%y' in format_of_date:
            year = parsed_date.strftime('%y')
            years.append(year)
        if '%Y' in format_of_date:
            year = parsed_date.strftime('%Y')
            years.append(year)
        if '%m' in format_of_date:
            month = parsed_date.strftime('%m')
            months_list.append(month)
        if '%b' in format_of_date:
            month = parsed_date.strftime('%b')
            months_list.append(month)
        if '%B' in format_of_date:
            month = parsed_date.strftime('%B')
            months_list.append(month)
        if '%d' in format_of_date:
            day = parsed_date.strftime('%d')
            day_of_month.append(day)
        if '%e' in format_of_date:
            day = parsed_date.strftime('%e')
            day_of_month.append(day)
        if parsed_date.weekday() < 5:
            weekend_or_weekday.append('weekday')
        if parsed_date.weekday() >= 5:
            weekend_or_weekday.append('weekend')
        quarter_dict = {'1': [1, 2, 3], 
                        '2': [4, 5, 6], 
                        '3': [7, 8, 9], 
                        '4': [10, 11, 12]}
        for quarter, months in quarter_dict.items():
            if int(month) in months:
                quarter_list.append(quarter)
        

    df['year'] = years
    df['year'] = df['year'].astype('int')
    df['quarter'] = quarter_list
    df['quarter'] = df['quarter'].astype('int')
    df['month'] = months_list
    df['month'] = df['month'].astype('int')
    df['day_of_month'] = day_of_month
    df['day_of_month'] = df['day_of_month'].astype('int')
    df['day_of_week'] = day_of_week
    df['weekend_or_weekday'] = weekend_or_weekday


# Write a function to set the index to be the datetime variable.
def index_setter(df, column):
    df.set_index(column, inplace=True)