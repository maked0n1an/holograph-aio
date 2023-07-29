import time
import asyncio
import random
from loguru import logger
from input_data.config import MAX_WAIT_TIME, DELAY
from util.data import DATA
from util.chain import Chain

class BlockchainTxChecker:

    def check_tx_status(self, wallet_name, address, chain, tx_hash):
        scan = DATA[chain]['scan']

        logger.info(
            f'{wallet_name} | {address} | {chain} - жду подтверждения транзакции {scan}{self.w3.to_hex(tx_hash)}...')
        
        start_time = int(time.time())
        while True:
            current_time = int(time.time())
            
            if current_time >= start_time + MAX_WAIT_TIME:
                logger.info(
                    f'{wallet_name} | {address} | {chain} - транзакция не подтвердилась за {MAX_WAIT_TIME} cекунд, начинаю повторную отправку...'
                )
                return 0
            try:
                time.sleep(4)
                status = self.w3.eth.get_transaction_receipt(tx_hash)['status']
                if status == 1:
                    return status
            except Exception as e:
                error = str(e)
                logger.info(
                    f'{wallet_name} | {address} | {chain} - произошла ошибка, {error}'
                )
                time.sleep(1)
    
    def sleep_indicator(self, wallet_name, address, chain):
        secs = random.randint(DELAY[0], DELAY[1])
        logger.info(f'{wallet_name} | {address} | {chain} - жду {secs} секунд...')
        time.sleep(secs)

    def set_gas_price_for_bsc(self, tx):
        if self.chain == Chain.BSC:
            del tx['maxFeePerGas']
            del tx['maxPriorityFeePerGas']
            tx['gasPrice'] = self.w3.to_wei(1, 'gwei')

        return tx