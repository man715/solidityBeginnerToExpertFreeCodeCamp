from scripts.helpfulScripts import getAccount, LOCALBLOCKCHAINENVIRONMENTS
from scripts.deploy import deployFundMe
from brownie import network, accounts, exceptions
import pytest

def testCanFundAndWithdraw():
    account = getAccount()
    fundMe = deployFundMe()
    entranceFee = fundMe.getEntranceFee() + 100
    tx = fundMe.fund({"from": account, "value": entranceFee})
    tx.wait(1)
    assert fundMe.addressToAmountFunded(account.address) == entranceFee
    tx2 = fundMe.withdraw({"from": account,})
    tx2.wait(1)
    assert fundMe.addressToAmountFunded(account.address) == 0

def testOnlyOwnerCanWithdraw():
    if network.show_active() not in LOCALBLOCKCHAINENVIRONMENTS:
        pytest.skip("only for local testing")
    fundMe = deployFundMe()
    badActor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError): 
            fundMe.withdraw({"from": badActor})
            
