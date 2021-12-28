from brownie import Lottery, config, network
from scripts.helpers import get_account, get_contract, fund_with_link
import time


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator"),
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed Lottery!")

    return lottery


def start_lottery():
    lottery = Lottery[-1]
    account = get_account()
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery has started!")


def enter_lottery():
    lottery = Lottery[-1]
    account = get_account()
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print(f"{account} has entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    count = 0
    while lottery.lotteryState() != 1:
        print(f"Waiting on random number: {count}")
        count += 1
        time.sleep(60)

    winner = lottery.recentWinner()
    print(f"The winner is {winner}")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
