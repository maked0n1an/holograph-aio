from util.chain import Chain

NFT_NAME = 'Green Skull'
NFT_CONTRACT = '0x61B2d56645d697Ac3a27c2fa1e5B26B45429d1A9'

MODE = 'minter'

AMOUNT_OF_NFTS = 1

IS_SHUFFLE_KEYS = 1

CHAINS_FOR_BRIDGE = [Chain.AVALANCHE, Chain.POLYGON, Chain.BSC]

# перерыв между действиями
DELAY = (30, 100)

# moralis api key - https://admin.moralis.io/login идем сюда и получаем апи ключ, НУЖЕН DEFAULT KEY!, нужно для нахождения id нфт
MORALIS_API_KEY = ''
# cколько максимум секунд скрипт будет ждать подтверждения транзакции
MAX_WAIT_TIME = 150