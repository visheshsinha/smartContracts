from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv
import json, os

load_dotenv()

with open("simpleStorage.sol", "r") as file:
    simpleStorage = file.read()

install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simpleStorage.sol": {"content": simpleStorage}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


bytecode = compiled_sol["contracts"]["simpleStorage.sol"]["simpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["simpleStorage.sol"]["simpleStorage"]["abi"]

""" working on ganache """

w3 = Web3(Web3.HTTPProvider(os.environ.get("HTTP_PROVIDER")))
chain_id = int(os.environ.get("CHAIN_ID"))
myAddress = os.environ.get("MY_ADDRESS")
pvt_key = os.environ.get("PRIVATE_KEY")

simpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

" Latest Transaction"

nonce = w3.eth.getTransactionCount(myAddress)

"""
1. Build a Transaction
2. Sign the Transaction 
3. Send the Transaction
"""

"""Build"""
transaction = simpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": myAddress, "nonce": nonce}
)
print("\nDeploying Contract ...")
"""Sign"""
signed_txn = w3.eth.account.sign_transaction(transaction, private_key = pvt_key)

"""Send"""
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_reciept = w3.eth.wait_for_transaction_receipt(txn_hash)

print("Contract Deployed \n")

"""
Interacting: Contract Address & ABI
Call -> Simulate making the call & get a return value
Transact -> Actually make State Change
"""
simple_storage = w3.eth.contract(address = txn_reciept.contractAddress, abi = abi)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

store_transaction = simple_storage.functions.store(32).buildTransaction(
    {"chainId": chain_id, "from": myAddress, "nonce": nonce + 1}
)

print("\nInitiating Transaction ...")

sign_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key = pvt_key)
store_txn_hash = w3.eth.send_raw_transaction(sign_store_txn.rawTransaction)
store_txn_reciept = w3.eth.wait_for_transaction_receipt(store_txn_hash)

print("Transaction Completed \n")
print(f"Final Stored Value {simple_storage.functions.retrieve().call()}")