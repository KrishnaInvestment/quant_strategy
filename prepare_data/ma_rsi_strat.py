import pandas as pd
import logging

import constants as cn
from calculation.ta import TACalculator
from signal_generation.ta_signal import TASignal
from data_trans.trans import Transformation

from prepare_data.base import Prepare

from utils import configure_logging

configure_logging()

logger = logging.getLogger(__name__)


class PrepareMAData(Prepare):
    def __init__(self) -> None:
        self.df_short = pd.read_csv(cn.SHORT_PERIOD_DATA_PATH_18_22)
        self.df_long = pd.read_csv(cn.LONG_PERIOD_DATA_PATH_18_22)

    def apply_transformation(self, df, trans_name, **kwargs):
        trans = Transformation()
        if trans_name == "square_root":
            df = trans.square_root(df, **kwargs)
        elif trans_name == "ha_aiken":
            df = trans.heikin_ashi(df, **kwargs)
        return df

    def prepare_shorter_period_data(self, df_short, columns):
        logger.info("Starting to Prepare shorter period data")

        df_short["datetime"] = pd.to_datetime(df_short["datetime"])
        TACalculator.calculate_rsi(df_short, columns, cn.SHORT_RSI_PERIOD)

        TACalculator.calculate_ma(
            df_short, f"{columns}_rsi_{cn.SHORT_RSI_PERIOD}", cn.SHORT_RSI_MA_PERIOD
        )
        rsi_ma_columns = [
            f"{columns}_rsi_{cn.SHORT_RSI_PERIOD}_ma_{i}"
            for i in cn.SHORT_RSI_MA_PERIOD
        ]
        TASignal.detect_cross_signals(df_short, *rsi_ma_columns)
        logger.info(
            f"Completed data with rsi and ma periods {cn.SHORT_RSI_PERIOD} and {cn.SHORT_RSI_MA_PERIOD}"
        )
        TACalculator.calculate_adx(df_short, 9)
        TACalculator.calculate_macd(df_short, "ha_close")
        return df_short

    def prepare_longer_period_data(self, df_long, columns):
        logger.info("Starting to Prepare Longer period data")
        df_long["datetime"] = pd.to_datetime(df_long["datetime"])
        df_long.close = df_long.close.shift(1)
        TACalculator.calculate_ma(df_long, columns, cn.LONG_MA_PERIOD)
        ma_columns = [f"{columns}_ma_{i}" for i in cn.LONG_MA_PERIOD]
        TASignal.detect_cross_signals(df_long, *ma_columns)
        logger.info(f"Completed data with ma periods {cn.LONG_MA_PERIOD}")
        return df_long

    def get_data(self):
        df_long = self.apply_transformation(
            self.df_long,
            "square_root",
            periods=1,
            columns=["open", "close", "high", "low"],
        )

        long_data = self.prepare_longer_period_data(df_long, "sq_close")

        df_short = self.apply_transformation(
            self.df_short,
            "square_root",
            periods=1,
            columns=["open", "close", "high", "low"],
        )
        df_short = self.apply_transformation(
            df_short,
            "ha_aiken",
            columns=["sq_open", "sq_close", "sq_high", "sq_low"],
        )

        short_data = self.prepare_shorter_period_data(df_short, "sq_close")

        return long_data, short_data
