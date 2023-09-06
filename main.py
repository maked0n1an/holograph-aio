import asyncio
import random

from termcolor import colored
from art import text2art
from web3 import Web3
from loguru import logger

from input_data.config import *
from modules.nft import Nft
from modules.blockchain_tx_checker import BlockchainTxChecker
from util.file_utils import *

def main():
    if MORALIS_API_KEY == '':
        logger.error("Don't imported Moralis API key!...")
        return
    if len(PRIVATE_KEYS) == 0:
        logger.error("Don't imported private keys in 'private_keys.txt'!")
        return
    if len(WALLET_NAMES) == 0:
        logger.error("Please insert names into wallet_names.txt")
        return
    if len(PRIVATE_KEYS) != len(WALLET_NAMES):
        logger.error("The wallet names' amount must be equal to private keys' amount")
        return    

    logger.info('The bot has been started')
    logger.info(f'The amount of accs is: {len(PRIVATE_KEYS)}')
    name_key_tuple = list(zip(WALLET_NAMES, PRIVATE_KEYS))
    
    if IS_SHUFFLE_KEYS:
        random.shuffle(name_key_tuple)

    if MODE == 'minter':
        logger.info(f'The minting of {NFT_NAME} NFT has been launched') 
        for wallet_name, private_key in name_key_tuple:
            nft_operations = Nft(wallet_name, private_key, BRIDGE_FROM_CHAINS, Chain.AVALANCHE, AMOUNT_OF_NFTS)
            nft_operations.mint_nft()
            BlockchainTxChecker.sleep_indicator(wallet_name=wallet_name)
            
    elif MODE == 'bridger':
        logger.info(f'The minting and bridging of {NFT_NAME} NFT has been launched')
        for wallet_name, private_key in name_key_tuple:
            nft_operations = Nft(wallet_name, private_key, BRIDGE_FROM_CHAINS, BRIDGE_TO_CHAINS, AMOUNT_OF_NFTS)
            nft_operations.mint_nft()
            main_sleep_indicator(wallet_name=wallet_name)
            nft_operations.bridge_nft()
    else:
        logger.info('Incorrect mode, please check config.py!')
        return

    logger.info("The bot has ended it's work")


if __name__ == '__main__':
    authors = ["@1liochka1", "@maked0n1an"]
    random.shuffle(authors)
    art = text2art(text=NFT_NAME + ' NFT', font="standart")
    print(colored(art, "cyan"))
    print(colored(f"Authors: {authors[0]}, {authors[1]}\n", "cyan"))

    write_to_main_log()

    main()