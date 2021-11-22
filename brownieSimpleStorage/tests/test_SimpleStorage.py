from brownie import SimpleStorage, accounts, network

def testDeploy():
    # Arrange, Act, Assert

    # Arrange
    account = getAccount()
    # Act
    simpleStorage = SimpleStorage.deploy({"from": account})
    startingValue = simpleStorage.retrieve()
    expected = 0
    # Assert
    assert startingValue == expected

def getAccount():
    if(network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def testUpdatingStorage():
    # Arrange
    account = accounts[0]
    simpleStorage = SimpleStorage.deploy({"from": account})
    # Act
    expected = 15
    simpleStorage.store(expected, {"from": account})

    # Assert
    assert expected == simpleStorage.retrieve()
