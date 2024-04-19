# Refer Examples for more details

import multiprocessing
from untrade.client import Client

def backtest_18_22():
    client = Client()

    # Perform backtest using the provided CSV file path
    backtest_result = client.backtest(
        jupyter_id="krishnainvestment",  # the one you use to login to jupyter.untrade.io
        file_path='processed_data_18_22.csv',
        leverage=1,  # Adjust leverage as needed
    )
    print("2018-2022 Backtest Result") 
    for value in backtest_result:
        print(value)

def backtest_23():
    client = Client()

    # Perform backtest using the provided CSV file path
    backtest_result = client.backtest(
        jupyter_id="krishnainvestment",  # the one you use to login to jupyter.untrade.io
        file_path='processed_data_2023.csv',
        leverage=1,  # Adjust leverage as needed
    )
    print("2023 Backtest Result") 
    for value in backtest_result:
        print(value)


if __name__ == "__main__":
    backtest_process_18_22 = multiprocessing.Process(target=backtest_18_22)
    backtest_process_23 = multiprocessing.Process(target=backtest_23)

    backtest_process_18_22.start()
    backtest_process_23.start()
    
    backtest_process_18_22.join()
    backtest_process_23.join()
    # Note: The fronttest process will keep running.
