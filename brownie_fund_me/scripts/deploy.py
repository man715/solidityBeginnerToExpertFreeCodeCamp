from brownie import FundMe, MockV3Aggregator, network, config
from scripts.fund_and_withdraw import fund
from scripts.helpers import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    # pass the price feed address to the constructor
    # if on a persistent network, use the associated address
    # otherwise, use mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]

    else:
        deploy_mocks()
        # use the most recently deployed MockV3Aggregator
        price_feed_address = MockV3Aggregator[-1]

    # the publish_source=True will verify the smart contract with etherscan.io
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # pull verify from config (the get will help avoiding errors if verify does not exist)
    )

    print(f"Contract deployed to: {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
