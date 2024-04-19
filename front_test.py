# Importing Indicator Calculation Modules
import pandas as pd
from untrade.client import Client
import logging
import datetime
import time

from ta_strategy import (
    calculate_ma,
    calculate_rsi,
    detect_cross_signals,
    TradingStrategy,
)

import multiprocessing
import constants as cn

from prepare_data import get_latest_short_prepared_data, get_latest_long_prepared_data

# Call the configure_logging function to set up logging
logger = logging.getLogger(__name__)


def get_latest_signal():
    df_hour = get_latest_short_prepared_data(symbol="BTCUSDT", interval="1h", limit=11)
    df_daily = get_latest_long_prepared_data(symbol="BTCUSDT", interval="1d", limit=8)
    daily_signal = df_daily.cross_signal.iloc[-1]

    rsi_ma_columns1, rsi_ma_columns2 = [
        f"close_rsi_{cn.SHORT_RSI_PERIOD}_ma_{i}" for i in cn.SHORT_RSI_MA_PERIOD
    ]
    df_hour["cross_signal"] = df_hour[rsi_ma_columns1] - df_hour[rsi_ma_columns2]
    current_value = df_hour.cross_signal.iloc[-1]
    previous_value = df_hour.cross_signal.iloc[-2]
    signal = TradingStrategy.get_cross_over_info(current_value, previous_value)
    print(daily_signal, signal)
    if daily_signal != signal:
        current_price = df_hour.close.iloc[-1]
        stop_loss = current_price * abs(daily_signal - 0.035)
        target = current_price * abs(daily_signal + 0.04)
        return signal, current_price, target, stop_loss
    return (0) * 4


def close_trades():
    # Get existing open positions
    # Check if the open time and current time is greater
    # than 8 hours then close it
    pass


def existing_open_order():
    "It will return the time of entry of order"
    current_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
    return current_time


def get_account_info():
    # get account info
    # for dynamically calculating the quantity
    return 1000


def execute_trades():
    signal, current_price, target, stop_loss = get_latest_signal()
    quantity = get_account_info()
    client = Client()
    if signal == 1:
        # Executing Long Trade
        client.create_order(
            symbol="BTCUSDT",
            side="BUY",
            type="MARKET",
            market="COIN-M",
            quantity=quantity,
            leverage=cn.LEVERAGE,
            target=target,
            stop_loss=stop_loss,
        )
        logger.info(
            f"Executed Long trade for BTCUSDT at price {current_price} with sl {stop_loss}, tr {target} and quantity {quantity}"
        )
    elif signal == -1:
        # Executing short trades
        client.create_order(
            symbol="BTCUSDT",
            side="SELL",
            type="MARKET",
            market="COIN-M",
            quantity=quantity,
            leverage=cn.LEVERAGE,
            target=target,
            stop_loss=stop_loss,
        )
        logger.info(
            f"Executed Short trade for BTCUSDT at price {current_price} with sl {stop_loss}, tr {target} and quantity {quantity}"
        )
    else:
        logger.info(f"Nither long or short trades executed at price {current_price}")


def front_test_strategy():
    logger.info(f"Current Time {datetime.datetime.now(datetime.timezone.utc)}, Executing now") 
    order_entry_time = existing_open_order()
    if order_entry_time:
        current_date = datetime.datetime.now(datetime.timezone.utc)
        order_difference = (current_date - order_entry_time).total_seconds() / (60 * 60)
        logger.info(f"Time between entry time and now {order_difference}")
        if order_difference >= 8:
            logger.info("Starting to close open_order")
            try:
                close_trades()
                logger.info("Successfully closed a trade")
            except Exception as e:
                logger.error(f"Failed closing a trade {e}", exc_info=True)
                # Inform developer right way with notification
    else:
        try:
            logger.info("Starting to generate live signal")
            execute_trades()
        except Exception as e:
            logger.error(f"Failed opening a trade {e}", exc_info=True)
            # Inform developer right way with notification


def sleep_until_next_hour():
    # Get the current time
    current_time = datetime.datetime.now(datetime.timezone.utc)
    
    # Calculate the number of seconds until the next whole hour
    seconds_until_next_hour = 3600 - (current_time.timestamp() % 3600)
    
    # Sleep until the next whole hour
    logger.info(f"Next running time after {round(seconds_until_next_hour/60, 2)} Minutes Current Time {current_time}") 
    time.sleep(seconds_until_next_hour)

def fronttest():
    # User should write their fronttest logic here.
    # This function should be designed to run continuously.
    while True:
        # Sleep until the next whole hour
        sleep_until_next_hour()
        
        # Run the command at the top of the hour
        front_test_strategy()


if __name__ == "__main__":
    fronttest_process = multiprocessing.Process(target=fronttest)
    fronttest_process.start()
