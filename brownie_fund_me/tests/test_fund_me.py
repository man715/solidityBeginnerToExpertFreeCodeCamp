from brownie import network, accounts, exceptions
from scripts.helpers import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    # get account
    account = get_account()
    # deploy the contract(s)
    fund_me = deploy_fund_me()
    # get the minimal amount to be funded
    # added an extra 100 to help with any descrepencies
    entrance_fee = fund_me.getEntranceFee() + 100
    # fund the contract with the minimum
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    # check to make sure we are on a local blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # skip if we are not on a local blockchain
        pytest.skip("only for local testing")

        account = get_account()
        fund_me = deploy_fund_me()

        # crate a random account
        bad_actor = accounts.add()
        # testing for a revert
        with pytest.rases(exceptions.VirtualMachineError):
            # fund using the bad_actor account instead of the owner.
            fund_me.withdraw({"from": bad_actor})
