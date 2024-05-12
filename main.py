# Refer Examples for more details

import multiprocessing
from untrade.client import Client
import constants as cn

def backtest(file_name):
    client = Client()

    # Perform backtest using the provided CSV file path
    backtest_result = client.backtest(
        jupyter_id=cn.JUPYTER_ID,  # the one you use to login to jupyter.untrade.io
        file_path=file_name,
        leverage=cn.LEVERAGE,  # Adjust leverage as needed
        # result_type="Y",
    )
    last_value = None
    for value in backtest_result:
        last_value = value
    print(last_value)


if __name__ == "__main__":
    backtest_process = multiprocessing.Process(target=backtest('processed_data_20_23.csv'))
    backtest_process.start()
    
    backtest_process.join()
