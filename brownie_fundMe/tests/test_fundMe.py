from brownie import fundMe, network, accounts, exceptions
from scripts._functions import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fundMe
import pytest

def test_canFund_andWithdraw():
    account = get_account()
    fund_me = deploy_fundMe()
    entranceFee = fund_me.getEntranceFee() + 100

    txn = fund_me.fund({"from": account, "value": entranceFee})
    txn.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entranceFee

    txn2 = fund_me.withdraw({"from": account})
    txn2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0

def test_onlyOwnerWithdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for Local Network")

    fund_me = deploy_fundMe()
    unauthAcc = accounts.add()

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": unauthAcc})    
"""
Fork Command: (Make New dApp/project in Alchemy/infura) // This needs debugging + Try out on differe
brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127:0:0:1 fork=https://mainnet.infura.io/v3/ec53e33a23aa4ccb83b313fbf6fe1d9e accounts=10 mnemonic=brownie port=8545
"""