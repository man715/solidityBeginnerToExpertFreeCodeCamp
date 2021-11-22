from brownie import FundMe
from scripts.helpfulScripts import getAccount

def fund():
    fundMe = FundMe[-1]
    account = getAccount()
    entranceFee = fundMe.getEntranceFee()
    print(f"The current entry fee is {entranceFee}")
    print("Funding")
    fundMe.fund({"from": account, "value": entranceFee})
    print(account)

def withdraw():
    fundMe = FundMe[-1]
    account = getAccount()
    print("Withdrawing")
    fundMe.withdraw({"from": account})
    print(account)

def main():
    fund()
    withdraw()

