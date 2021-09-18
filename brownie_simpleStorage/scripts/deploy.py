from brownie import accounts, config, simpleStorage, network

def deploy_simpleStorage():
    account = get_account()
    simple_storage = simpleStorage.deploy({"from": account})
    print(f"Initial Stored Value: {simple_storage.retrieve()}")

    txn = simple_storage.store(32, {"from": account})
    txn.wait(1)
    print(f"Updated Stored Value: {simple_storage.retrieve()}")
    
def get_account():
    if(network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_simpleStorage()