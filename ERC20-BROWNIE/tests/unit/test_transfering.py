from brownie import OurToken
from scripts.helpers import get_account
from web3 import Web3


def test_transfering():
    initial_supply = Web3.toWei(1000, "ether")
    transfer_amount = Web3.toWei(1, "ether")
    account = get_account()
    user = get_account(index=1)
    our_token = OurToken.deploy(initial_supply, {"from": account})
    our_token.transfer(user, transfer_amount, {"from": account})

    assert our_token.balanceOf(user) == transfer_amount
    contract_balance_after = initial_supply - transfer_amount
    assert our_token.balanceOf(account) == contract_balance_after
