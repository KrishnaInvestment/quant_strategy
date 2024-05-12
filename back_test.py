# Importing Indicator Calculation Modules
import pandas as pd
import math
from strategy.ma_rsi_strategy import MAStrategy

import constants as cn

def create_signal(file_name):
    rsi_ma_columns = [f'close_trans_rsi_{cn.SHORT_RSI_PERIOD}_ma_{i}' for i in cn.SHORT_RSI_MA_PERIOD]

    trend_calculation_ = MAStrategy().generate_signal(*rsi_ma_columns)
    trend_calculation_.to_csv(file_name, index=False)

if __name__ == "__main__":
    print("Backtest started")
    file_name = "processed_data_20_23.csv"
    create_signal(file_name)