import talib
import pandas as pd

def calculate_ma(df, column, periods):
    for period in periods:
        column_name = f'{column}_ma_{period}'
        if column_name in df.columns:
            raise ValueError('Duplicate Error: Column already exists')
        df[column_name] = df[column].rolling(period).mean()
    return df


def calculate_rsi(df, column, period):
    column_name = f'{column}_rsi_{period}'
    if column_name in df.columns:
            raise ValueError('Duplicate Error')
    df[column_name] = talib.RSI(df[column].values, timeperiod=period)
     
    
def detect_cross_signals(df, column1, column2):
    """
    Detects golden cross and dead cross signals based on the relationship between two columns in a DataFrame.
    
    Args:
        df (DataFrame): Input DataFrame containing the data.
        column1 (str): Name of the first column for comparison.
        column2 (str): Name of the second column for comparison.
    
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


class TradingStrategy:

    @staticmethod
    def get_cross_over_info(current_difference, last_difference):
        if current_difference>0 and last_difference<0:
            return 1
        elif current_difference<0 and last_difference>0:
            return -1
        else:
            return 0
    
    @staticmethod
    def get_stop_loss_target(df, stop_loss, target, signal_value):
        if signal_value>0:
            stop_loss_df = df[df['close'] <= stop_loss].sort_values('datetime')
        else:
            stop_loss_df = df[df['close'] >= stop_loss].sort_values('datetime')
            
        if stop_loss_df.empty:
            stop_loss_date = None
        else:
            stop_loss_date = stop_loss_df.datetime.iloc[0]

        if signal_value>0:
            target_df = df[df['close'] >= target].sort_values('datetime')
        else:
            target_df = df[df['close'] <= target].sort_values('datetime')
            
        if target_df.empty:
            target_date = None
        else:
            target_date = target_df.datetime.iloc[0]

        if not stop_loss_date and not target_date:
            return df.index[-1]
        elif stop_loss_date and target_date:
            if stop_loss_date < target_date:
                return df[df['datetime'] == stop_loss_date].index[0]
            else:
                return df[df['datetime'] == target_date].index[0]

        elif stop_loss_date:
            return df[df['datetime'] == stop_loss_date].index[0]

        else:
            return df[df['datetime'] == target_date].index[0]

    
    @staticmethod
    def get_final_trend(df_short, df_long, column1, column2):
        signal = [0] * len(df_short)
        i = 1
        while True:
            current_difference = df_short[column1].iloc[i] - df_short[column2].iloc[i]
            last_difference = df_short[column1].iloc[i - 1] - df_short[column2].iloc[i - 1]
            signal_date = df_short['datetime'].iloc[i].date()
            long_period_signal = df_long[df_long['datetime'].dt.date==signal_date].cross_signal.iloc[0]
            short_period_signals = TradingStrategy.get_cross_over_info(current_difference, last_difference)
            if long_period_signal and short_period_signals and long_period_signal==short_period_signals:
                signal[i] = short_period_signals
                entry_price = df_short.close.iloc[i]
                stop_loss = entry_price*abs(long_period_signal-0.035)
                target = entry_price*abs(long_period_signal+0.04)
                
                value_index = TradingStrategy.get_stop_loss_target(df_short[i:i + 9], stop_loss, target, short_period_signals)
                signal[value_index] = -(short_period_signals)
                i = value_index + 1
            else:
                i += 1

            if i >= len(df_short) - 1:
                break
        df_short['signals'] = signal
        return df_short