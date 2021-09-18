"""pyTest Docs"""
from brownie import simpleStorage, accounts

def test_deploy():
    """Arrange"""
    account = accounts[0]
    
    """Act"""
    simple_storage = simpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    expected = 0

    """Assert"""
    assert stored_value == expected

def test_updateStore():
    account = accounts[0]
    simple_storage = simpleStorage.deploy({"from": account})

    expected = 32
    simple_storage.store(expected, {"from": account})

    assert expected == simple_storage.retrieve()