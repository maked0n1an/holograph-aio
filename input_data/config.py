from util.chain import Chain

NFT_NAME = 'Holograph x LayerZero'
NFT_CONTRACT = '0x2c4BD4e25D83285f417E26a44069F41d1a8aD0e7'

MODE = 'minter'

AMOUNT_OF_NFTS = 1

IS_SHUFFLE_KEYS = 1

CHAINS_FOR_BRIDGE = [Chain.AVALANCHE, Chain.POLYGON, Chain.BSC, Chain.ARBITRUM] #Chain.OPTIMISM,
FEE_MULTIPLICATOR = 1.8

# перерыв между действиями
DELAY = (50, 500)

# moralis api key - https://admin.moralis.io/login идем сюда и получаем апи ключ, НУЖЕН DEFAULT KEY!, нужно для нахождения id нфт
MORALIS_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjEwNzg2NDU4LWEyMWUtNDU3Mi1hNTU2LWI0OWE0ZTJhZTU3YyIsIm9yZ0lkIjoiMzQ0MTM2IiwidXNlcklkIjoiMzUzNzY3IiwidHlwZUlkIjoiNjY4MDVjNTQtMzlmYS00OGQ1LTgyMDItY2EwMjkzNmJiNzQ2IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE2ODcxMDk4MTUsImV4cCI6NDg0Mjg2OTgxNX0.6Sgw7i3Fl_5JRYV6_2Sz2SFDLp-i26xK4nPWzmcEWaQ'

# cколько максимум секунд скрипт будет ждать подтверждения транзакции
MAX_WAIT_TIME = 150