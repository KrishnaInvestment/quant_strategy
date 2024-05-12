import pandas as pd
import logging

from utils import configure_logging
import constants as cn

# Call the configure_logging function to set up logging
configure_logging()

logger = logging.getLogger(__name__)

class TATrans:
    def heikin_ashi(self, df, columns=["open", "close", "high", "low"]):
        """
        Calculate Heikin-Ashi candlestick values from OHLC data.

        Parameters:
        - df (DataFrame): DataFrame containing OHLC data with columns 'open', 'high', 'low', 'close', and 'datetime'.

        Returns:
        - DataFrame: DataFrame containing Heikin-Ashi candlestick values with columns 'datetime', 'ha_open', 'ha_high', 'ha_low', and 'ha_close'.
        """
        logger.info("Starting to Heikin Ashi Transformation")
        # Convert 'datetime' column to datetime type if it's not already
        df["datetime"] = pd.to_datetime(df["datetime"])

        # Calculate Heikin-Ashi close values
        df["ha_close"] = (
            df[columns[0]] + df[columns[1]] + df[columns[2]] + df[columns[3]]
        ) / 4
        return df

    def ichimoku_cloud(self, df, columns=["high", "low"]):
        df["ic_close"] = (
            df[columns[0]].rolling(window=cn.ICHIMOKU_CLOUD_PERIOD).max()
            + df[columns[1]].rolling(window=cn.ICHIMOKU_CLOUD_PERIOD).max()
        ) / 2
        return df