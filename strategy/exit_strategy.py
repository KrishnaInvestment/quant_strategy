import constants as cn
from calculation.ta import TACalculator
class ExitStrategy:
    def stop_loss_target(self, df, stop_loss, target, signal_value):
        
        if signal_value>0:
            stop_loss_df = df[df['close'] <= stop_loss].sort_values('datetime')
        else:
            stop_loss_df = df[df['close'] >= stop_loss].sort_values('datetime')
            
            
        if signal_value>0:
            target_df = df[df['close'] >= target].sort_values('datetime')
        else:
            target_df = df[df['close'] <= target].sort_values('datetime')
            

        if stop_loss_df.empty and target_df.empty:
            return df.index[-1]
        elif not stop_loss_df.empty and not target_df.empty:
            if stop_loss_df.datetime.iloc[0] < target_df.datetime.iloc[0]:
                return df[df['datetime'] == stop_loss_df.datetime.iloc[0]].index[0]
            else:
                return df[df['datetime'] == target_df.datetime.iloc[0]].index[0]

        elif not stop_loss_df.empty:
            return df[df['datetime'] == stop_loss_df.datetime.iloc[0]].index[0]

        else:
            return df[df['datetime'] == target_df.datetime.iloc[0]].index[0]
    
    def within_period(self, periods, ind):
        value = periods + ind
        return value
    
    def atr_exit(self, df, columns=["high", "low", "close"]):
        # df = df[ind+1: ind+cn.TRADE_PERIOD]
        atr = TACalculator.calculate_atr(df, periods=cn.ATR_EXIT_PERIOD, columns=columns)
        atr_values = atr.iloc[-1]
        exit_condition = df[df['close'] - df['close'].shift(1)  <  0.02 * atr_values]
        return exit_condition.index[0]
    
    def bb_exit(self, df, columns="close"):
        filter_condition = (df[columns] > df['upper_band'])
        # Apply the filter to the DataFrame
        filtered_df = df[filter_condition]
        if filtered_df.empty:
            return df.index[-1]
        return filtered_df.index[0]
        
    def get_exit(self, exit_strategy, **kwargs):
        if exit_strategy=='within_periods':
            return self.within_period(**kwargs)
        elif exit_strategy=='stop_loss_target':
            return self.stop_loss_target(**kwargs)