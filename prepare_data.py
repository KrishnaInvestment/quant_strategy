import pandas as pd
import logging

import constants as cn
from ta_strategy import (
    calculate_ma,
    calculate_rsi,
    detect_cross_signals,
)
from fetch_data import fetch_historical_data

from utils import configure_logging

# Call the configure_logging function to set up logging
configure_logging()

logger = logging.getLogger(__name__)


def prepare_shorter_period_data(df_short):
    logger.info('Starting to Prepare shorter period data')
    df_short['datetime'] = pd.to_datetime(df_short['datetime'])
    calculate_rsi(df_short, "close", cn.SHORT_RSI_PERIOD)
    calculate_ma(df_short, f'close_rsi_{cn.SHORT_RSI_PERIOD}', cn.SHORT_RSI_MA_PERIOD)
    logger.info(f'Completed data with rsi periods {cn.SHORT_RSI_PERIOD}')
    logger.info(f'Completed data with rsi_ma periods {cn.SHORT_RSI_MA_PERIOD}')
    return df_short

def prepare_longer_period_data(df_long):
    logger.info('Starting to Prepare Longer period data')
    df_long['datetime'] = pd.to_datetime(df_long['datetime'])
    calculate_ma(df_long, 'close', cn.LONG_MA_PERIOD)
    ma_columns  = [f'close_ma_{i}' for i in cn.LONG_MA_PERIOD]
    df_long = detect_cross_signals(df_long, *ma_columns)
    logger.info(f'Completed data with ma periods {cn.LONG_MA_PERIOD}')
    return df_long


def get_latest_short_prepared_data(symbol, interval, limit):
    df_hour = fetch_historical_data(symbol=symbol, interval=interval, limit=limit)
    df_hour = prepare_shorter_period_data(df_hour)
    return df_hour

def get_latest_long_prepared_data(symbol, interval, limit):
    df_day = fetch_historical_data(symbol=symbol, interval=interval, limit=limit)
    df_day = prepare_longer_period_data(df_day)
    return df_day