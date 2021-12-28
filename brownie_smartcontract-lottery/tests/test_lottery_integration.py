from scripts.deploy import deploy_lottery
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS


from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, fund_with_link
from scripts.deploy import deploy_lottery
from brownie import network
import pytest
import time


def test_can_pick_winner():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    print(lottery.address)
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    previous_random_number = lottery.recentRandomNumber()
    fund_with_link(lottery)
    # Act
    tx = lottery.endLottery({"from": account})
    tx.wait(1)
    # Wait for the randomness Oracle to return a random number
    count = 0
    while lottery.lotteryState() != 1:
        print(f"Waiting on random number: {count}")
        time.sleep(60)
        count += 1
    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
