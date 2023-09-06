from util.chain import Chain

NFT_NAME = 'Holograph x LayerZero'
NFT_CONTRACT = '0x2c4BD4e25D83285f417E26a44069F41d1a8aD0e7'

# Select mode to work: 'minter' | 'bridger'
MODE = 'bridger'

# Amount for mint nft: 
# AMOUNT_OF_NFTS = 1 - it will be ONLY this number for each account 
# AMOUNT_OF_NFTS = (1, 3) - it will select RANDOM number of NFTs from this range of numbers for each account and mint the NFT
AMOUNT_OF_NFTS = (1, 3)

# Do u need to shuffle? - 'Yes' - 1, 'No' - 0
IS_SHUFFLE_KEYS = 1

'''
    Settings
    Chains where we will mint nft and to which chains or one chain we will bridge
    If u need one chain for mint and some chains for bridge, please comment or uncomment the needed chains
    For example:

    BRIDGE_FROM_CHAINS = [ - the script will be minting from Avalanche only and bridge to BSC (for example)
        Chain.AVALANCHE, 
        # Chain.POLYGON, 
        # Chain.BSC, 
        # Chain.ARBITRUM
    ]

    BRIDGE_TO_CHAINS = [
        # Chain.AVALANCHE, 
        # Chain.POLYGON, 
        Chain.BSC, 
        # Chain.ARBITRUM
    ] 
'''

BRIDGE_FROM_CHAINS = [
    Chain.AVALANCHE, 
    Chain.POLYGON, 
    Chain.BSC, 
    Chain.ARBITRUM
]

BRIDGE_TO_CHAINS = [
    Chain.AVALANCHE, 
    Chain.POLYGON, 
    Chain.BSC, 
    Chain.ARBITRUM
] 

FEE_MULTIPLICATOR = 1.8

# break between activities
DELAY = (100, 700)

# moralis api key - https://admin.moralis.io/login go here and get the api key, DEFAULT KEY IS NEEDED!, needed to find the nft id
MORALIS_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjEwNzg2NDU4LWEyMWUtNDU3Mi1hNTU2LWI0OWE0ZTJhZTU3YyIsIm9yZ0lkIjoiMzQ0MTM2IiwidXNlcklkIjoiMzUzNzY3IiwidHlwZUlkIjoiNjY4MDVjNTQtMzlmYS00OGQ1LTgyMDItY2EwMjkzNmJiNzQ2IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE2ODcxMDk4MTUsImV4cCI6NDg0Mjg2OTgxNX0.6Sgw7i3Fl_5JRYV6_2Sz2SFDLp-i26xK4nPWzmcEWaQ'

# how many seconds the script will wait for transaction confirmation
MAX_WAIT_TIME = 150