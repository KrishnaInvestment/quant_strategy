class StrategyUtils:
    def get_stop_loss_target(self, df, stop_loss, target, signal_value):
        # Define filter conditions based on signal_value
        if signal_value > 0:
            stop_loss_condition = df['close'] <= stop_loss
            target_condition = df['close'] >= target
        else:
            stop_loss_condition = df['close'] >= stop_loss
            target_condition = df['close'] <= target

        # Filter DataFrame based on conditions
        stop_loss_df = df[stop_loss_condition].sort_values('datetime')
        target_df = df[target_condition].sort_values('datetime')

        # Extract stop loss and target dates
        stop_loss_date = stop_loss_df.iloc[0]['datetime'] if not stop_loss_df.empty else None
        target_date = target_df.iloc[0]['datetime'] if not target_df.empty else None

        # Determine final date based on stop loss and target dates
        if not stop_loss_date and not target_date:
            return df.index[-1]
        elif stop_loss_date and target_date:
            exit_date =  min(stop_loss_date, target_date)
        elif stop_loss_date:
            exit_date =  stop_loss_date
        else:
            exit_date =  target_date
            
        return df[df['datetime']==exit_date].index[0]