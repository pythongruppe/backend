import json
import csv
import pandas as pd
import os

database = "memory.csv"
key_part1 = "address"
key_part2 = "zip"
header = ["address","rooms","area_estate","area_property","monthly_payment","cash_price","zip","city","sq_meter_price","property_type","down_payment"]


def input_to_database(input):
    data = json.loads(input)
    # write_tester(data)

    key = data[key_part1]+data[key_part2]
    df = pd.read_csv(database)
    has_entity = exists_in_databse(df, key)

    if has_entity:
        return "adress+zipcode already exists in database"

    write_to_database(df, data)
    return "added entity to database"

def write_to_database(df, data):
    df_new = pd.DataFrame(columns=df.columns)
    df_new = df_new.append(data, sort=True, ignore_index=True)
    df_new.to_csv(database, mode='a', header=False, index=False)


def exists_in_databse(df, key):
    has_entity = False
    df_key_parts = df.filter(items=[key_part1, key_part2])
    for index, row in df_key_parts.iterrows():
        row_key = row[key_part1] + str(row[key_part2])
        if key == row_key:
            has_entity = True
    return has_entity

# def write_tester(data):
#     file_db = open(database, "w")
#     csv_file = csv.writer(file_db)
#     values = dict_tester.values()
#     #if empty list
#     if os.stat(database).st_size == 0:
#         csv_file.writerow(header)
#         csv_file.writerow(values)

#test
dict_tester = {
    "address": "coolstreet3A",
    "rooms": "10",
    "area_estate": "estate1",
    "area_property": "property1",
    "monthly_payment": "4000",
    "cash_price": "1000000",
    "zip": "2130",
    "city": "copenhagen",
    "sq_meter_price": "500",
    "property_type": "wood",
    "down_payment": "100000"
}