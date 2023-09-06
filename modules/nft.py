import random
import aiohttp
import copy
import random
import time

from web3 import Web3
from loguru import logger
from moralis import evm_api
from eth_abi import encode
from eth_utils import to_hex

from input_data.config import *
from modules.blockchain_tx_checker import BlockchainTxChecker
from util.file_utils import *
from util.data import *
from util.chain import Chain

class Nft(BlockchainTxChecker):
    def __init__(self, wallet_name, private_key, chain, to_chain, amount_of_nfts):
        self.wallet_name = wallet_name
        self.private_key = private_key
        self.chain = random.choice(chain) if type(chain) == list else chain
        self.to_chain = random.choice(BRIDGE_FROM_CHAINS) if type(to_chain) == list else to_chain
        self.w3 = Web3(Web3.HTTPProvider(DATA[self.chain]['rpc']))
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.address = self.account.address
        self.count = random.randint(amount_of_nfts[0], amount_of_nfts[1]) if isinstance(amount_of_nfts, (list, tuple)) else amount_of_nfts
        self.delay = random.randint(DELAY[0], DELAY[1])
        self.nft_address = Web3.to_checksum_address(NFT_CONTRACT)
        self.holograph_bridge_contract = Web3.to_checksum_address(HOLOGRAPH_BRIDGE_CONTRACT)
        self.layerzero_endpoint_address = Web3.to_checksum_address(LAYERZERO_ENDPOINT)

    def _get_fee(self, nft_amount_to_mint):
        contract = self.w3.eth.contract(self.nft_address, abi=abi)
        fee = contract.functions.getHolographFeeWei(nft_amount_to_mint).call()

        return int(fee * 1.03)

    def get_native_balance(self):
        chains = BRIDGE_FROM_CHAINS.copy()
        random.shuffle(chains) 
        for chain in chains:
            w3 = Web3(Web3.HTTPProvider(DATA[chain]['rpc']))
            account = w3.eth.account.from_key(self.private_key)
            address = account.address
            balance = w3.eth.get_balance(address)
            if balance / 10 ** 18 > min_balances[chain]:
                return chain
        
        return False
    
    def check_nft_in_one_chain(self, chain):
        if chain not in [Chain.OPTIMISM, Chain.MANTLE]:
            params = {
                'chain': chain,
                'format': 'decimal',
                'token_addresses': [
                    self.nft_address
                ],
                'media_items': False,
                'address': self.address
            }

            try:
                result = evm_api.nft.get_wallet_nfts(api_key=MORALIS_API_KEY, params=params)
                token_id = int(result['result'][0]['token_id'])
                if token_id:
                    logger.success(f'{self.wallet_name} | {self.address} | {chain} - NFT "{NFT_NAME}"[{token_id}] successfully found on the wallet')
                    return chain, token_id
                return False
            except Exception as e:
                if 'list index out of range' in str(e):
                    return False
        else:
            contract_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "payable": False,
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "tokensOfOwner",
                    "outputs": [{"name": "tokenIds", "type": "uint256[]"}],
                    "payable": False,
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
            contract = self.w3.eth.contract(address=self.nft_address, abi=contract_abi)
            try:
                bal = contract.functions.balanceOf(self.address).call()
                if bal:
                    token_id = contract.functions.tokensOfOwner(self.address).call()[0]
                    logger.success(f'{self.wallet_name} | {self.address} | {self.chain} - "{NFT_NAME}"[{token_id}] NFT successfully found in the wallet')
                    return chain, token_id
                return False
            except Exception as e:
                logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - error, {e}')
                return False

    def check_nft_in_some_chains_return_some(self):
        result = []
        for chain in BRIDGE_FROM_CHAINS:
            is_have_nft = self.check_nft_in_one_chain(chain)
            if isinstance(is_have_nft, tuple):
                results.append(is_have_nft)
        return results

    def check_any_nft(self):
        for chain in BRIDGE_FROM_CHAINS:
            is_have_nft = self.check_nft_in_one_chain(chain)
            if is_have_nft:
                return is_have_nft
        logger.error(f'{self.wallet_name} | {self.address} | - "{NFT_NAME}" NFT is not found in any chain in the wallet...')
        return None
    
    def mint_nft(self):
        chain = self.get_native_balance()

        if chain:
            self.chain = chain
        else:
            logger.error(f'{self.wallet_name} | {self.address} | - could not get chain for mint NFT')
            return self.private_key, self.address, 'not enough balance'

        self.w3 = Web3(Web3.HTTPProvider(DATA[self.chain]['rpc']))
        self.account = self.w3.eth.account.from_key(self.private_key)
        self.address = self.account.address
        fee = self._get_fee(self.count)

        try:
            nonce = self.w3.eth.get_transaction_count(self.address)
            contract = self.w3.eth.contract(address=self.nft_address, abi=abi)

            tx = contract.functions.purchase(self.count).build_transaction({
                'from': self.address,
                'nonce': nonce,
                'value': fee,
                'maxFeePerGas': 0,
                'maxPriorityFeePerGas': 0
            })
            gas = self.w3.eth.gas_price
            tx['maxFeePerGas'], tx['maxPriorityFeePerGas'] = gas, gas

            tx = self.set_gas_price_for_bsc(tx)

            logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - minting is started...')
            sign = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
            status = self.check_tx_status(self.wallet_name, self.address, self.chain, tx_hash)
            if status == 1:
                scan = DATA[self.chain]['scan']
                logger.success(
                    f'{self.wallet_name} | {self.address} | {self.chain} - successfully minted {self.count} {NFT_NAME} NFT(s): {scan}{self.w3.to_hex(tx_hash)}...')
                self.sleep_indicator(self.wallet_name, self.address, self.chain)
                return self.private_key, self.address, 'success'
        except Exception as e:
            error = str(e)
            if "insufficient funds for gas * price + value" or "error, {'code': -32000, 'message': 'INTERNAL_ERROR: insufficient funds'}" in error:
                logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - not enough native balance')
                return self.private_key, self.address, 'error'
            elif 'nonce too low' in error or 'already known' in error:
                logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - trying one more time...')
                self.mint_nft()
            else:
                logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - error, {e}')
                return self.private_key, self.address, 'error'

    def bridge_nft(self):
        nft_data = self.check_any_nft()

        if nft_data:
            self.chain, nft_id = nft_data
            self.w3 = Web3(Web3.HTTPProvider(DATA[self.chain]['rpc']))
            self.account = self.w3.eth.account.from_key(self.private_key)
            self.address = self.account.address
            if self.chain == self.to_chain:
                chains = BRIDGE_TO_CHAINS.copy()
                chains.remove(self.to_chain)
                self.to_chain = random.choice(chains)
        else:
            logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - NFT is not found in wallet')
            return self.private_key, self.address, 'NFT is not found in wallet'
        
        payload = to_hex(encode(['address', 'address', 'uint256'], [self.address, self.address, nft_id]))
        gas_price = holograph_gas_limit[self.to_chain]
        gas_lim = random.randint(450000, 500000)

        holograph = self.w3.eth.contract(address=self.holograph_bridge_contract, abi=holo_abi)
        lzEndpoint = self.w3.eth.contract(address=self.layerzero_endpoint_address, abi=lzEndpointABI)

        lzFee = lzEndpoint.functions.estimateFees(layerzero_ids[self.to_chain], self.holograph_bridge_contract, '0x', False, '0x').call()[0]
        lzFee = int(lzFee * FEE_MULTIPLICATOR)
        to_chain_id = holograph_ids[self.to_chain]

        while True:
            logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - trying to bridge...')
            try:
                tx = holograph.functions.bridgeOutRequest(to_chain_id, self.nft_address, gas_lim, gas_price,
                                                          payload).build_transaction({
                    'from': self.address,
                    'value': lzFee,
                    'gas': holograph.functions.bridgeOutRequest(to_chain_id, self.nft_address, gas_lim, gas_price,
                                                                payload).estimate_gas(
                        {'from': self.address, 'value': lzFee,
                         'nonce': self.w3.eth.get_transaction_count(self.address)}),
                    'nonce': self.w3.eth.get_transaction_count(self.address),
                    'maxFeePerGas': int(self.w3.eth.gas_price),
                    'maxPriorityFeePerGas': int(self.w3.eth.gas_price * 0.8)
                })
                tx = self.set_gas_price_for_bsc(tx)
                scan = DATA[self.chain]['scan']

                sign = self.account.sign_transaction(tx)
                tx_hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
                status = self.check_tx_status(self.wallet_name, self.address, self.chain, tx_hash)
                if status == 1:
                    logger.success(
                        f'{self.wallet_name} | {self.address} | {self.chain} - successfully bridged "{NFT_NAME}"[{nft_id}] to {self.to_chain} : {scan}{self.w3.to_hex(tx_hash)}...')
                    self.sleep_indicator(self.wallet_name, self.address, self.chain)
                    return self.private_key, self.address, 'success'
                else:
                    logger.warning(f'{self.wallet_name} | {self.address} | {self.chain} - try to mint one more time...')
                    self.mint_nft()
            except Exception as e:
                error = str(e)
                if "insufficient funds for gas * price + value" or "error, {'code': -32000, 'message': 'INTERNAL_ERROR: insufficient funds'}" in error:
                    logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - not enough balance in native token')
                    return self.private_key, self.address, 'error'
                elif 'nonce too low' in error or 'already known' in error:
                    logger.info(f'{self.wallet_name} | {self.address} | {self.chain} - try to mint one more time...')
                    self.bridge_nft()
                else:
                    logger.error(f'{self.wallet_name} | {self.address} | {self.chain} - {e}')
                    return self.private_key, self.address, 'error'