from brownie import fundMe
from scripts._functions import get_account

def fund():
    fund_me = fundMe[-1]
    account = get_account()
    entranceFee = fund_me.getEntranceFee()
    print(f"The current entry fee is {entranceFee}")
    fund_me.fund({"from": account, "value": entranceFee})

def withdraw():
    fund_me = fundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})

def main():
    fund()
    withdraw()