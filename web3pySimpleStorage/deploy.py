import json
import os
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_standard

load_dotenv('./.env')

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard( {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            }
        },
        solc_version="0.6.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get the bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connect to the ganache blockchain
blockProvider = "http://localhost:8545"
w3 = Web3(Web3.HTTPProvider(blockProvider))

chain_id = 1337

my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
# Get private key for os env variable
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction count
nonce = w3.eth.getTransactionCount(my_address)

# Make a transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from": my_address, "nonce": nonce})
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying Contract")
# send signed tx
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract is Deployed")

# Working with the contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Intial value of favoriteNumber
print(simple_storage.functions.retrieve().call())

print("Updaing the favorite number")
store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1
    })

signed_stored_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_stored_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("New Number: ", end="")
print(simple_storage.functions.retrieve().call())
