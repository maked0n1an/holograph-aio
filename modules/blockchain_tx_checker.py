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
            f'{wallet_name} | {address} | {chain} - waiting for tx approve {scan}{self.w3.to_hex(tx_hash)}...')
        
        start_time = time.time()
        while True:
            current_time = int(time.time())
            
            if current_time >= start_time + MAX_WAIT_TIME:
                logger.warning(
                    f'{wallet_name} | {address} | {chain} - tx is not approved for {MAX_WAIT_TIME} secs, start resending...'
                )
                return 0
            try:
                status = self.w3.eth.get_transaction_receipt(tx_hash)['status']
                if status == 1:
                    return status
                time.sleep(1)
            except Exception as e:
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