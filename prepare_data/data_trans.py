import pandas as pd
import math
import logging

from utils import configure_logging

# Call the configure_logging function to set up logging
configure_logging()

logger = logging.getLogger(__name__)


class Transformation:
    def heikin_ashi(self, df, columns=['open', 'close', 'high', 'low'], **kwargs):
        """
        Calculate Heikin-Ashi candlestick values from OHLC data.

        Parameters:
        - df (DataFrame): DataFrame containing OHLC data with columns 'open', 'high', 'low', 'close', and 'datetime'.

        Returns:
        - DataFrame: DataFrame containing Heikin-Ashi candlestick values with columns 'datetime', 'ha_open', 'ha_high', 'ha_low', and 'ha_close'.
        """
        logger.info('Starting to Heikin Ashi Transformation')
        # Convert 'datetime' column to datetime type if it's not already
        df["datetime"] = pd.to_datetime(df["datetime"])

        # Calculate Heikin-Ashi close values
        df["trans_close"] = (df[columns[0]] + df[columns[1]] + df[columns[2]] + df[columns[3]]) / 4
        return df

    def root_function(self, df, periods, power, aggregation, **kwargs):
        if aggregation == "mean":
            df["trans_close"] = (
                df['close']
                .rolling(periods)
                .mean()
                .apply(lambda x: None if not x else (x**1/power))
            )
        elif aggregation == "sum":
            df["trans_close"] = (
                df['close']
                .rolling(periods)
                .sum()
                .apply(lambda x: None if not x else (x**1/power))
            )
        return df
    
    def cube_root(self, df, periods,  aggregation="mean", **kwargs):
        logger.info('Starting to Cube Root Transformation')
        df = self.root_function(df, periods, 3,  aggregation, **kwargs)
        return df
        
    def square_root(self, df, periods,  aggregation="mean", **kwargs):
        logger.info('Starting to Square Root Transformation')
        df = self.root_function(df, periods, 2,  aggregation, **kwargs)
        return df
            
    def natural_log(self, df, periods, aggregation="sum"):
        logger.info('Starting to Natural Log Transformation')
        if aggregation == "mean":
            df["trans_close"] = (
                df['close']
                .rolling(periods)
                .mean()
                .apply(lambda x: None if not x else (math.log(x)))
            )
        elif aggregation == "sum":
            df["trans_close"] = (
                df['close']
                .rolling(periods)
                .sum()
                .apply(lambda x: None if not x else (math.log(x)))
            )
        return df

    def square_root_ha(self, df, **kwargs):
        logger.info('Starting to square_root_ha Transformation')
        df['sq_open'] = df['open'].apply(lambda x: math.sqrt(x))
        df['sq_close'] = df['close'].apply(lambda x: math.sqrt(x))
        df['sq_high'] = df['high'].apply(lambda x: math.sqrt(x))
        df['sq_low'] = df['high'].apply(lambda x: math.sqrt(x))
        df = self.heikin_ashi(df, ['sq_open','sq_close', 'sq_high', 'sq_low'])
        return df
    
    def cube_root_ha(self, df, **kwargs):
        logger.info('Starting to cube_root_ha Transformation')
        df['sq_open'] = df['open'].apply(lambda x: x**1/3)
        df['sq_close'] = df['close'].apply(lambda x: x**1/3)
        df['sq_high'] = df['high'].apply(lambda x: x**1/3)
        df['sq_low'] = df['high'].apply(lambda x: x**1/3)
        df = self.heikin_ashi(df, ['sq_open','sq_close', 'sq_high', 'sq_low'])
        return df
    
    def natural_log_ha(self, df, **kwargs):
        logger.info('Starting to natural_log_ha Transformation')
        df['sq_open'] = df['open'].apply(lambda x: math.log(x))
        df['sq_close'] = df['close'].apply(lambda x: math.log(x))
        df['sq_high'] = df['high'].apply(lambda x: math.log(x))
        df['sq_low'] = df['high'].apply(lambda x: math.log(x))
        df = self.heikin_ashi(df, ['sq_open','sq_close', 'sq_high', 'sq_low'])
        return df
    
    
    def ha_square_root(self, df, **kwargs):
        logger.info('Starting to ha_square_root Transformation')
        df = self.heikin_ashi(df)
        df['trans_close'] = df['trans_close'].apply(lambda x: math.sqrt(x))
        return df
    
    def ha_cube_root(self, df, **kwargs):
        logger.info('Starting to ha_cube_root Transformation')
        df = self.heikin_ashi(df)
        df['trans_close'] = df['trans_close'].apply(lambda x: x**1/3)
        return df