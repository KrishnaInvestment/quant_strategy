import constants as cn
from calculation.ta import TACalculator


class LimitStrategy:
    def stop_loss_target(self, df, stop_loss, target, signal_value):
        if signal_value > 0:
            stop_loss_df = df[df["low"] <= stop_loss].sort_values("datetime")
        else:
            stop_loss_df = df[df["high"] >= stop_loss].sort_values("datetime")

        if signal_value > 0:
            target_df = df[df["high"] >= target].sort_values("datetime")
        else:
            target_df = df[df["low"] <= target].sort_values("datetime")

        if stop_loss_df.empty and target_df.empty:
            ind = df.index[-1]
            price = df.close.iloc[-1]
        elif not stop_loss_df.empty and not target_df.empty:
            if stop_loss_df.datetime.iloc[0] < target_df.datetime.iloc[0]:
                ind = df[df["datetime"] == stop_loss_df.datetime.iloc[0]].index[0]
                price = stop_loss
            else:
                ind = df[df["datetime"] == target_df.datetime.iloc[0]].index[0]
                price = target

        elif not stop_loss_df.empty:
            ind = df[df["datetime"] == stop_loss_df.datetime.iloc[0]].index[0]
            price = stop_loss

        else:
            ind = df[df["datetime"] == target_df.datetime.iloc[0]].index[0]
            price = target
        return ind, price

    def within_period(self, periods, ind):
        value = periods + ind
        return value

    def atr_exit(self, df, columns=["high", "low", "close"]):
        atr = TACalculator.calculate_atr(
            df, periods=cn.ATR_EXIT_PERIOD, columns=columns
        )
        atr_values = atr.iloc[-1]
        exit_condition = df[
            df["close"] - df["close"].shift(1) < cn.ATR_MULTIPLIER * atr_values
        ]
        return exit_condition.index[0]

    def adx_macd_exit(self, df, signal):
        df_new = df[df["adx_close"] < cn.ADX_FILTER]
        if signal < 0:
            df_new = df_new[
                df_new["macd"] > (1 + cn.MACD_FILTER_PERCENTAGE) * df_new["macdsignal"]
            ]
        else:
            df_new = df_new[
                df_new["macd"] < (1 - cn.MACD_FILTER_PERCENTAGE) * df_new["macdsignal"]
            ]

        if df_new.empty:
            ind = df.index[-1]
            price = df.close.iloc[-1]
        else:
            ind = df_new.index[0]
            price = df_new.close.iloc[0]

        return ind, price

    def adx_exit(self, df):
        df_new = df[df["adx_close"] < cn.ADX_FILTER]
        if df_new.empty:
            ind = df.index[-1]
            price = df.close.iloc[-1]
        else:
            ind = df_new.index[0]
            price = df_new.close.iloc[0]

        return ind, price

    def bb_exit(self, df, columns="close"):
        filter_condition = df[columns] > df["upper_band"]
        filtered_df = df[filter_condition]
        if filtered_df.empty:
            return df.index[-1]
        return filtered_df.index[0]

    def get_exit(self, exit_strategy, **kwargs):
        if exit_strategy == "within_periods":
            return self.within_period(**kwargs)
        elif exit_strategy == "stop_loss_target":
            return self.stop_loss_target(**kwargs)
        elif exit_strategy == "adx_macd_exit":
            return self.adx_macd_exit(**kwargs)
