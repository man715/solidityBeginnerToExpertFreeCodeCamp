from scripts.helpers import get_account
from brownie import interface, network, config


def main():
    get_weth()


def get_weth():
    """
    Mints WETH by depositying ETH
    """
    account = get_account()
    # We will need the WETH ABI and contract address.
    # For the ABI, we created an interface in the interface directory
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10 ** 18})
    tx.wait(1)
    print(f"Received 0.1 WETH")
    return tx
