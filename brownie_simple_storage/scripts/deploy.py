from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})

    # run the retrieve function on SimpleStorage instance
    stored_value = simple_storage.retrieve()
    print(f"Before running store: {stored_value}")

    # run the store function on SimpleStorage
    simple_storage.store(15, {"from": account})

    # retrieve the stored value again
    stored_value = simple_storage.retrieve()
    print(f"After running store: {stored_value}")


# if we are on a dev network use accounts[0]
# if not on a dev network use another key
def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
