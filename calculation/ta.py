import talib
import pandas as pd
import constants as cn


class TACalculator:
    @staticmethod
    def calculate_ma(df, column, periods):
        """
        This function make changes to orginal dataframe
        df : Pandas dataframe
        column (str) : column name that we want to calculate ma
        periods (list in int) : Periods that we like to calculate ma
        """
        for period in periods:
            column_name = f"{column}_ma_{period}"
            if column_name in df.columns:
                raise ValueError("Duplicate Error: Column already exists")
            df[column_name] = df[column].rolling(period).mean()

    @staticmethod
    def calculate_rsi(df, column, period):
        """
        This function make changes to orginal dataframe
        df : Pandas dataframe
        column (str) : column name that we want to calculate ma
        periods (list in int) : Periods that we like to calculate ma
        """
        column_name = f"{column}_rsi_{period}"
        if column_name in df.columns:
            raise ValueError("Duplicate Error")
        df[column_name] = talib.RSI(df[column].values, timeperiod=period)

    @staticmethod
    def calculate_atr(df, periods, columns):
        df["atr_value"] = talib.ATR(
            df[columns[0]], df[columns[1]], df[columns[2]], timeperiod=periods
        )
        return df

    @staticmethod
    def calculate_bollinger_bands(df, periods, columns, num_std):
        sma = df[columns].rolling(window=periods).mean()
        std = df[columns].rolling(window=periods).std()

        # Calculate upper and lower bands
        df["upper_band"] = sma + (std * num_std)
        df["lower_band"] = sma - (std * num_std)
        return df

    @staticmethod
    def calculate_adx(df, periods, columns=["high", "low", "close"]):
        df["adx_close"] = talib.ADX(
            df[columns[0]], df[columns[1]], df[columns[2]], timeperiod=periods
        )
        return df

    @staticmethod
    def calculate_macd(df, columns="close"):
        df["macd"], df["macdsignal"], _ = talib.MACD(
            df[columns],
            fastperiod=cn.MACD_FAST_PERIOD,
            slowperiod=cn.MACD_SLOW_PERIOD,
            signalperiod=cn.MACD_SIGNAL_PERIOD,
        )
        return df
