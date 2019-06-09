import pandas as pd
from src.machine_learning.cost_prediction import get_predictors


def to_int(df):
    return df.iloc[0][0]


def create_cost_predictor(data):
    cash, monthly, down = get_predictors(data)

    def f(user_data):
        df = pd.DataFrame.from_dict({key: [value] for key, value in user_data.items()})
        return {
            'cash_price': to_int(cash(df)),
            'monthly_payment': to_int(monthly(df)),
            'down_payment': to_int(down(df))
        }

    return f
