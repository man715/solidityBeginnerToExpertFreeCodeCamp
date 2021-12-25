from brownie import SimpleStorage, accounts, config


def read_contract():
    # the SimpleStorage that is imported from brownie
    # is an array of deployed contracts
    # access the latest deployed contract with -1
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())


def main():
    read_contract()
