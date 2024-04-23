import pandas as pd
import logging

import constants as cn
from calculation.ta import TACalculator
from prepare_data.data_trans import Transformation

from utils import configure_logging

# Call the configure_logging function to set up logging
configure_logging()

logger = logging.getLogger(__name__)


class PrepareMAData:
    def __init__(self) -> None:
        self.df_short = pd.read_csv(cn.SHORT_PERIOD_DATA_PATH_18_22)
        self.df_long = pd.read_csv(cn.LONG_PERIOD_DATA_PATH_18_22)
    @staticmethod
    def apply_transformation(func):
        def wrapper(self, df, columns, transformation=None, **kwargs):
            if transformation:
                trans = Transformation()
                df = getattr(trans, transformation)(df, **kwargs)
                columns = 'trans_close'
            return func(self, df, columns)
        return wrapper
    
    @apply_transformation
    def prepare_shorter_period_data(self, df_short,  columns, transformation=None, **kwargs):
        logger.info('Starting to Prepare shorter period data')
        df_short['datetime'] = pd.to_datetime(df_short['datetime'])
        TACalculator.calculate_rsi(df_short, columns, cn.SHORT_RSI_PERIOD)
        TACalculator.calculate_ma(df_short, f'{columns}_rsi_{cn.SHORT_RSI_PERIOD}', cn.SHORT_RSI_MA_PERIOD)
        rsi_ma_columns = [f'{columns}_rsi_{cn.SHORT_RSI_PERIOD}_ma_{i}' for i in cn.SHORT_RSI_MA_PERIOD]
        TACalculator.detect_cross_signals(df_short, *rsi_ma_columns)
        TACalculator.calculate_bollinger_bands(df_short, cn.BB_PERIOD, columns, cn.BB_STD_DEV)
        logger.info(f'Completed data with rsi and ma periods {cn.SHORT_RSI_PERIOD} and {cn.SHORT_RSI_MA_PERIOD}')
        return df_short

    @apply_transformation
    def prepare_longer_period_data(self, df_long, columns, transformation=None, **kwargs):
        logger.info('Starting to Prepare Longer period data')
        df_long['datetime'] = pd.to_datetime(df_long['datetime'])
        TACalculator.calculate_ma(df_long, columns, cn.LONG_MA_PERIOD)
        ma_columns  = [f'{columns}_ma_{i}' for i in cn.LONG_MA_PERIOD]
        TACalculator.detect_cross_signals(df_long, *ma_columns)
        logger.info(f'Completed data with ma periods {cn.LONG_MA_PERIOD}')
        return df_long
    
    
    def get_data(self, long_trans=None, short_trans=None, **kwargs):
        long_data = self.prepare_longer_period_data(self.df_long, 'close', long_trans, **kwargs)
        short_data = self.prepare_shorter_period_data(self.df_short, 'close', short_trans, **kwargs)
        # long_data.dropna(inplace=True)
        # short_data.dropna(inplace=True)
        return long_data, short_data