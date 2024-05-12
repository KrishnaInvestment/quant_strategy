import talib
import pandas as pd
import constants as cn


class TASignal:
    @staticmethod
    def detect_cross_signals(df, column1, column2):
        """
        Detects golden cross and dead cross signals based on the relationship between two columns in a DataFrame.

        Args:
            df (DataFrame): Input DataFrame containing the data.
            column1 (str): Name of the fast column for comparison.
            column2 (str): Name of the slow column for comparison.

        Returns:
            DataFrame: The input DataFrame with an additional column 'Cross_Signal' indicating the signals.
        """
        # Compute the differences between the two columns
        current_difference = df[column1] - df[column2]
        last_difference = current_difference.shift(1)
        # Initialize the signal column with zeros
        cross_signal = pd.Series(0, index=df.index)

        # Detect cross signals
        cross_signal[
            (current_difference > 1) & (last_difference < 0)
        ] = 1  # Golden cross signal
        cross_signal[
            (current_difference < 1) & (last_difference > 0)
        ] = -1  # Dead cross signal

        # Assign the signal column to the DataFrame
        df["cross_signal"] = cross_signal

        return df
    
    @staticmethod
    def adx_signal(df, value=None):
        filter_value  = value or cn.ADX_FILTER
        df.loc[df['adx_close'] <= filter_value, 'adx_signal'] = 1
        return df
    
    @staticmethod
    def macd_signal(df, per_value=None):
        filter_value = per_value or cn.MACD_FILTER_PERCENTAGE
        
        df.loc[df["macd"] > (1 + filter_value) * df["macdsignal"], 'macd_signal'] = 1
        df.loc[df["macd"] < (1 - filter_value) * df["macdsignal"], 'macd_signal'] = -1
        
        return df