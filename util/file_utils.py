import copy
import sys
import random
import time

from loguru import logger
from input_data.config import DELAY

out_file = ''

with open(f"{out_file}input_data/private_keys.txt", "r") as f:
    PRIVATE_KEYS = [row.strip() for row in f]

with open(f"{out_file}input_data/wallet_names.txt", "r") as f:
    WALLET_NAMES = [row.strip() for row in f]
    
def setup_logger():
    logger.remove()
    logger.add(
        sys.stderr,
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )
    logger.add(
        "main.log",
        format="<white>{time: MM/DD/YYYY HH:mm:ss}</white> | <level>"
        "{level: <8}</level> | <cyan>"
        "</cyan> <white>{message}</white>",
    )

    logger.level("HAS_NFT", no=26, color="<green>")
    logger.level("NFT_BRIDGED", no=27, color="<green>")
    logger.level("NFT_MINTED", no=28, color="<green>")

    return logger

def main_sleep_indicator(wallet_name):
    secs = random.randint(DELAY[0], DELAY[1])
    logger.info(f'{wallet_name} - waiting for {secs} seconds...')
    time.sleep(secs)