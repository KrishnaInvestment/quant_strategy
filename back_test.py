# Importing Indicator Calculation Modules
import pandas as pd
import math
from strategy.ma_strategy import MAStrategy

import constants as cn

def create_signal_18_22():
    # df_day.ha_close = df_day.ha_close.apply(lambda x: None if not x else math.sqrt(x))
    rsi_ma_columns = [f'close_trans_rsi_{cn.SHORT_RSI_PERIOD}_ma_{i}' for i in cn.SHORT_RSI_MA_PERIOD]

    trend_calculation_ = MAStrategy().generate_signal(*rsi_ma_columns)
    trend_calculation_.to_csv("processed_data_18_22.csv", index=False)
    
    
# def create_signal_2023():
#     df_hour = pd.read_csv(cn.SHORT_PERIOD_DATA_PATH_23)
#     df_hour = prepare_shorter_period_data(df_hour)
    
#     df_day = pd.read_csv(cn.LONG_PERIOD_DATA_PATH_23)
#     df_day = prepare_longer_period_data(df_day)

#     rsi_ma_columns = [f'close_rsi_{cn.SHORT_RSI_PERIOD}_ma_{i}' for i in cn.SHORT_RSI_MA_PERIOD]

#     trend_calculation_ = TradingStrategy.get_final_trend(df_hour, df_day, *rsi_ma_columns)
#     trend_calculation_.to_csv("processed_data_2023.csv", index=False)
    

if __name__ == "__main__":
    print("Backtest started")
    create_signal_18_22()
    # create_signal_2023()