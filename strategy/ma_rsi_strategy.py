from strategy.base import Strategy
from prepare_data.ma_rsi_strat import PrepareMAData
from strategy.limit_strategy import LimitStrategy
import constants as cn

class MAStrategy(Strategy, LimitStrategy):
    
    def entry_signal(self, df_short, df_long, column1, column2, ind):
        signal_date = df_short['datetime'].iloc[ind].date()
        long_period_signal = df_long[df_long['datetime'].dt.date==signal_date].cross_signal.iloc[0]
        short_period_signals = df_short.cross_signal.iloc[ind]
        
        if long_period_signal and short_period_signals and long_period_signal==short_period_signals:
            return abs(long_period_signal)
        
    def exit_signal(self, df_short, signal, ind, trade_period=cn.TRADE_PERIOD):
        entry_price = df_short.close.iloc[ind]
        stop_loss = entry_price*abs(signal-cn.STOP_LOSS)
        target = entry_price*abs(signal+cn.TARGET)
        
        exit_params = {
            "df":df_short[ind+1:ind + trade_period],
            "stop_loss":stop_loss, 
            "target": target, 
            "signal_value": signal,
        }
        
        value_index, price = self.get_exit(exit_strategy='stop_loss_target',**exit_params)
        return value_index, price, stop_loss, target
    
    def generate_signal(self, column1, column2):
        """
        Generate signals for entry and exit based on short-term and long-term dataframes.

        Parameters:
        - df_short (DataFrame): DataFrame containing short-term data.
        - df_long (DataFrame): DataFrame containing long-term data.
        - column1 (str): Name of the column representing the first data series.
        - column2 (str): Name of the column representing the second data series.

        Returns:
        - DataFrame: DataFrame with signals added.
        """
        df_long, df_short = PrepareMAData().get_data()
        
        signals = [0] * len(df_short)
        close_price = list(df_short.close)
        stop_loss_list = [0] * len(df_short)
        target_list = [0] * len(df_short)
        i = 1
        while i < len(df_short) - 1:
            entry_signal_value = self.entry_signal(df_short, df_long, column1, column2, i)
            if entry_signal_value:
                signals[i] = entry_signal_value
                exit_index, price, stop_loss, target = self.exit_signal(df_short, entry_signal_value, i)
                stop_loss_list[i] = stop_loss
                target_list[i] = target
                close_price[exit_index] = price
                signals[exit_index] = -entry_signal_value
                i = exit_index + 1
            else:
                i += 1
            if i >= len(df_short) - 1:
                    break
        df_short['signals'] = signals
        
        # Assign zero to 'sl' and 'tp' columns where the 'signals' column is zero
        df_short['sl'] = stop_loss_list
        df_short['tp'] = target_list
        
        df_short.rename(columns={'close':'org_close'}, inplace=True)
        df_short['close'] = close_price
        return df_short
