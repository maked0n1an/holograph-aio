from util.chain import Chain

NFT_NAME = 'Cosmic flower'
NFT_CONTRACT = '0xd4Feff615c0E90f06340Be95d30e1f397779A184'

MODE = 'minter'

AMOUNT_OF_NFTS = (1, 10)

IS_SHUFFLE_KEYS = 1

CHAINS_FOR_BRIDGE = [Chain.AVALANCHE, Chain.POLYGON, Chain.BSC, Chain.OPTIMISM, Chain.ARBITRUM]
FEE_MULTIPLICATOR = 1.8

# перерыв между действиями
DELAY = (200, 700)

# moralis api key - https://admin.moralis.io/login идем сюда и получаем апи ключ, НУЖЕН DEFAULT KEY!, нужно для нахождения id нфт
MORALIS_API_KEY = ''

# cколько максимум секунд скрипт будет ждать подтверждения транзакции
MAX_WAIT_TIME = 150