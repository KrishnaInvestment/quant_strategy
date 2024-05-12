import logging
import os
import pandas as pd

def configure_logging():
    # Create a logger
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a file handler for the log file
    file_handler = logging.FileHandler('logs/app.log')
    
    # Create a stream handler for the terminal
    stream_handler = logging.StreamHandler()
    
    # Define a custom log message format
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
    file_handler.setFormatter(log_format)
    stream_handler.setFormatter(log_format)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def merge_data(df1, df2):
    df = pd.concat(df1, df2)