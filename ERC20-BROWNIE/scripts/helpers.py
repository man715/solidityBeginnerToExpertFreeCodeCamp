from brownie import accounts, network, config

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-infura"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account(index=None, id=None):
    # if there is an index given, use the account in accounts at that index
    if index:
        return accounts[index]
    # if id is given, get the account with that ID stored in the brownie database
    if id:
        return accounts.load(id)
    # if on a local development chain and account index not given, use accounts[0]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    # default account from brownie-config.yaml
    return accounts.add(config["wallets"]["from_key"])
