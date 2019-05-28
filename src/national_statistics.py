import pandas as pd
import numpy as np
from collections import defaultdict
import operator

def get_avg_area_basement(df):
    return get_avg_key(df, 'area_basement', dropna=True, drop0=True)

def get_avg_area_estate(df):
    return get_avg_key(df, 'area_estate')

def get_avg_area_property(df):
    return get_avg_key(df, 'area_property', drop0=True)

def get_avg_cash_price(df):
    return get_avg_key(df, 'cash_price')

def get_avg_down_payment(df):
    return get_avg_key(df, 'down_payment', dropna=True)

def get_avg_monthly_payment(df):
    return get_avg_key(df, 'monthly_payment')

def get_avg_rooms(df):
    return get_avg_key(df, 'rooms')

def get_avg_key(df, key, dropna=False, drop0=False):
    values = df[key]
    if dropna:
        values = values.dropna()
    if drop0:
        values = values[values != 0.0]

    return values.sum() / len(values)
    

def order_zip_by_cash_price(df, min_count=10):
    return order_x_by_y(df, 'zip', 'cash_price', min_count)

def order_year_by_cash_price(df, min_count=10):
    filtered = df.iloc[df['year'].dropna().index.values]
    return order_x_by_y(filtered, 'year', 'cash_price', min_count)

def order_property_type_by_cash_price(df, min_count=10):
    return order_x_by_y(df, 'property_type', 'cash_price', min_count)

def order_x_by_y(df, x, y, min_count=10):
    key_count = defaultdict(int)
    y_sum = defaultdict(int)

    for i, row in df.iterrows():
        key = row[x]
        value = row[y]
        key_count[key] = key_count[key] + 1
        y_sum[key] = y_sum[key] + value

    y_mean = defaultdict(int)
    for key, y_sum in y_sum.items():
        count = key_count[key]
        if count >= min_count:
            y_mean[key] = y_sum / count
    
    return dict(sorted(y_mean.items(), key=operator.itemgetter(1), reverse=True))

if __name__ == '__main__':
    data = pd.read_csv('new_data.csv')
    print(f'get_avg_area_basement={get_avg_area_basement(data)}')
    print(f'get_avg_area_estate={get_avg_area_estate(data)}')
    print(f'get_avg_area_property={get_avg_area_property(data)}')
    print(f'get_avg_cash_price={get_avg_cash_price(data)}')
    print(f'get_avg_down_payment={get_avg_down_payment(data)}')
    print(f'get_avg_monthly_payment={get_avg_monthly_payment(data)}')
    print(f'get_avg_rooms={get_avg_rooms(data)}')