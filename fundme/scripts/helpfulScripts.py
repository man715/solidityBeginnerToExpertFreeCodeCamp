from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTINGPRICE = 200000000000
LOCALBLOCKCHAINENVIRONMENTS = ["development", "ganache-local"]
FORKEDLOCALENVIRONMENTS = ["mainnet-forked", "mainnet-forked-dev"]

def getAccount():
    if (
            network.show_active() in LOCALBLOCKCHAINENVIRONMENTS 
            or network.show_active() in FORKEDLOCALENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deployMocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        mockAggregator = MockV3Aggregator.deploy(DECIMALS, STARTINGPRICE, {"from": getAccount()})
    print("Mocks Deployed")
