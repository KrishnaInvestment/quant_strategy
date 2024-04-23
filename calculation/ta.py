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
            column_name = f'{column}_ma_{period}'
            if column_name in df.columns:
                raise ValueError('Duplicate Error: Column already exists')
            df[column_name] = df[column].rolling(period).mean()

    @staticmethod
    def calculate_rsi(df, column, period):
        """
        This function make changes to orginal dataframe
        df : Pandas dataframe
        column (str) : column name that we want to calculate ma
        periods (list in int) : Periods that we like to calculate ma
        """
        column_name = f'{column}_rsi_{period}'
        if column_name in df.columns:
                raise ValueError('Duplicate Error')
        df[column_name] = talib.RSI(df[column].values, timeperiod=period)
        
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
        cross_signal[(current_difference > 0) & (last_difference < 0)] = 1  # Golden cross signal
        cross_signal[(current_difference < 0) & (last_difference > 0)] = -1  # Dead cross signal
        
        # Assign the signal column to the DataFrame
        df['cross_signal'] = cross_signal
        
        return df
    
    @staticmethod
    def calculate_atr(df, periods, columns):
        df['atr_value'] = talib.ATR(df[columns[0]], df[columns[1]], df[columns[2]], timeperiod=periods)
        return df
    
    @staticmethod
    def calculate_bollinger_bands(df, periods, columns, num_std):
        sma = df[columns].rolling(window=periods).mean()
        std = df[columns].rolling(window=periods).std()

        # Calculate upper and lower bands
        df['upper_band'] = sma + (std * num_std)
        df['lower_band'] = sma - (std * num_std)
        return df