from brownie import draw, accounts, network, config
from web3 import Web3

def test_EntranceFee():
    account = accounts[0]
    _draw = draw.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    
    assert _draw.getEntranceFee() > Web3.toWei(0.015, "ether")
    assert _draw.getEntranceFee() < Web3.toWei(0.020, "ether")
