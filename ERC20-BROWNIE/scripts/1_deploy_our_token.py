from brownie import OurToken
from scripts.helpers import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")


def deploy_our_token():
    account = get_account()
    our_token = OurToken.deploy(initial_supply, {"from": account})
    print(
        f"{our_token.name()} has been deployed with {our_token.balanceOf(account) / (10**18)} tokens minited"
    )
    return our_token


def main():
    deploy_our_token()
