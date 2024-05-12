import math
import logging

from utils import configure_logging

# Call the configure_logging function to set up logging
configure_logging()

logger = logging.getLogger(__name__)


class MathsTrans:
    def root_function(self, df, periods, power, aggregation, columns=['close']):
        if aggregation == "mean":
            for column in columns:
                df[f"sq_{column}"] = (
                    df[column]
                    .rolling(periods)
                    .mean()
                    .apply(lambda x: None if not x else (x**(1 / power)))
                )
        elif aggregation == "sum":
            for column in columns:
                df[f"sq_{column}"] = (
                    df[column]
                    .rolling(periods)
                    .sum()
                    .apply(lambda x: None if not x else (x**(1 / power)))
                )
        return df

    def cube_root(self, df, periods, columns, aggregation="mean"):
        logger.info("Starting to Cube Root Transformation")
        df = self.root_function(df, periods, 3, aggregation, columns)
        return df

    def square_root(self, df, periods, columns, aggregation="mean"):
        logger.info("Starting to Square Root Transformation")
        df = self.root_function(df, periods, 2, aggregation, columns)
        return df

    def natural_log(self, df, periods, columns=['close'], aggregation="sum"):
        logger.info("Starting to Natural Log Transformation")
        if aggregation == "mean":
            for column in columns:
                df["nl_{column}"] = (
                    df[column]
                    .rolling(periods)
                    .mean()
                    .apply(lambda x: None if not x else (math.log(x)))
                )
        elif aggregation == "sum":
            for column in columns:
                df["nl_{column}"] = (
                df[column]
                .rolling(periods)
                .sum()
                .apply(lambda x: None if not x else (math.log(x)))
            )
        return df
