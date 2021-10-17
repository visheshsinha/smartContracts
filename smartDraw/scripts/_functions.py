from brownie import network, config, accounts

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# DECIMALS = 8
# STARTING_PRICE = 200000000000


def get_account(_index=None, _id=None):
    if _index:
        return accounts[_index]

    if _id:
        return accounts.load(_id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


def get_contract():
    pass
