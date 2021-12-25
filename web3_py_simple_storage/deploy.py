from dotenv import load_dotenv
from solcx import compile_standard
from web3 import Web3
import json
import os

load_dotenv()

# Open a file and run code inside the code block then close the file
with open("./SimpleStorage.sol", "r") as file:
    print("Compiling Contract...")
    simple_storage_file = file.read()
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.6.0",
    )

    print("Compiled... ")

    # Write a file that contains the compiled contract
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    # get the byte code
    bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

    # get the abi
    abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

    # connect to ganache
    provider = "https://rinkeby.infura.io/v3/11bdacc6a759421a9bdd30dbb5335855"
    chain_id = 4
    my_address = "0x66957B5AE28ECB9d54C0565804Ac0a7dA0287c50"
    private_key = os.getenv("PRIVATE_KEY")

    # create a Web3 instance
    w3 = Web3(Web3.HTTPProvider(provider))

    # create a contract instance in python
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

    # building a transaction
    # get the latest transaction
    nonce = w3.eth.getTransactionCount(my_address)

    print("Deploying contract...")

    # crate a transaction object
    transaction = SimpleStorage.constructor().buildTransaction(
        {"chainId": chain_id, "from": my_address, "nonce": nonce})
    # sign the transaction
    signed_txn = w3.eth.account.sign_transaction(
        transaction, private_key=private_key)

    # send the signed transaction to the blockchain
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # wait for block confirmation
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Deployed at {tx_receipt.contractAddress}")

    # working with the contract
    # you will need: Contract Address and Contract ABI
    simple_storage = w3.eth.contract(
        address=tx_receipt.contractAddress, abi=abi)
    print(
        f'Before running store: {simple_storage.functions.retrieve().call()}')

    # create the transaction
    store_transaction = simple_storage.functions.store(15).buildTransaction({
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1
    })
    signed_store_tx = w3.eth.account.sign_transaction(
        store_transaction, private_key=private_key)

    send_store_tx = w3.eth.send_raw_transaction(
        signed_store_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
    print(f'After running store: {simple_storage.functions.retrieve().call()}')
