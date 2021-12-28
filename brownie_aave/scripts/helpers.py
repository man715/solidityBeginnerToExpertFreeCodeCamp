from brownie import accounts, network, config

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-infura"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork"]


def get_account(index=None, id=None):
    # brownie accounts
    # account from environment variables

    # use brownie account based on index given
    if index:
        return accounts[index]

    # use a custom account added to brownie
    if id:
        accounts.load(id)

    # use account 0 if no account was given and in a locla environment
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    # default account
    return accounts.add(config["wallets"]["from_key"])
