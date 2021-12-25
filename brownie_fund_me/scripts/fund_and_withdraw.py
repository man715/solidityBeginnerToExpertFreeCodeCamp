from brownie import FundMe
from scripts.helpers import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f"The entrance fee: {entrance_fee} Wei")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    print("Withdrawing funds")
    fund_me.withdraw({"from": account})
    print("Funds have been withdrawn!")


def main():
    fund()
    withdraw()
