import pandas as pd
import numpy as np
from collections import defaultdict
import operator

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