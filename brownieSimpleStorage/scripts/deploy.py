from brownie import accounts, config, SimpleStorage, network


def deploySimpleStorage():
    account = getAccount()
    # account = accounts.load("MetaMask")
    # account = accounts.add(config["wallets"]["from_key"])
    print("Deploying Simple Storage")
    simpleStorage = SimpleStorage.deploy({"from": account})

    storedValue = simpleStorage.retrieve()
    transaction = simpleStorage.store(15, {"from": account})
    transaction.wait(1)
    updatedStoredValue = simpleStorage.retrieve()

    print(updatedStoredValue)

    pass

def getAccount():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploySimpleStorage()
