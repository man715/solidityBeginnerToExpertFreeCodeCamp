from brownie import SimpleStorage, accounts, config

def readContract():
    simpleStroage = SimpleStorage[-1]
    print(simpleStroage.retrieve())

def main():
    readContract()
