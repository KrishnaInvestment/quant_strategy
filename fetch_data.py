import pandas as pd
import pandas as pd
import requests
import datetime
import pytz
from typing import Union
from untrade.client import Client

def fetch_historical_data(
    symbol: str,
    interval: str,
    timezone: Union[None, str] = None,
    startTime: Union[None, str] = None,
    endTime: Union[None, str] = None,
    limit: str = 1000,
    futures: bool = False,
) -> pd.DataFrame:
    """
    Fetch historical price data from Binance API.

    Parameters:
    - symbol (str): Cryptocurrency symbol (e.g., BTCUSDT).
    - interval (str): Time interval for data (e.g., '1h', '4h', '1d').
    - timezone (str): Timezone to convert timestamps to (optional).
    - startTime (str): Start time for data retrieval (optional).
    - endTime (str): End time for data retrieval (optional).
    - limit (int): Limit the number of data points fetched.
    - futures (bool): Whether to fetch futures data.
    - cm (bool): Not used.

    Returns:
    - data (DataFrame): Historical price data.
    """
    if not futures:
        URL = (
            f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
        )
    else:
        URL = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}"

    if startTime:
        startTime = str(
            int(
                datetime.datetime.timestamp(
                    datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
                )
            )
            * 1000
        )
        URL += f"&startTime={startTime}"
        URL += f"&limit={limit}"
    elif startTime and endTime:
        startTime = str(
            int(
                datetime.datetime.timestamp(
                    datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
                )
            )
            * 1000
        )
        endTime = str(
            int(
                datetime.datetime.timestamp(
                    datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")
                )
            )
            * 1000
        )
        URL += f"&startTime={startTime}&endTime={endTime}"
    else:
        URL += f"&limit={limit}"
    response = requests.get(URL, timeout=10)
    data = response.json()

    # Organizing the data
    data_dict = {
        "datetime": [],
        "open": [],
        "high": [],
        "low": [],
        "close": [],
        "volume": [],
    }

    for candle in data:
        timestamp = candle[0] / 1000.0
        dt = datetime.datetime.fromtimestamp(timestamp)
        if timezone:
            dt = dt.astimezone(pytz.timezone(timezone))  # Convert to specified timezone

        # Extract OHLCV data from the request data
        O, H, L, C, V = map(float, candle[1:6])

        # Append data to data_dict
        data_dict["datetime"].append(dt)
        data_dict["open"].append(O)
        data_dict["high"].append(H)
        data_dict["low"].append(L)
        data_dict["close"].append(C)
        data_dict["volume"].append(V)

    df = pd.DataFrame(data_dict)
    return df