import os
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_standard, install_solc

# Ensure standard solc is installed
# You might need to run this once or handle errors appropriately
try:
    install_solc("0.8.0")
except Exception as e:
    print(f"Warning: Failed to install solc implicitly: {e}")

load_dotenv()

# Web3 setup
rpc_url = os.getenv("WEB3_PROVIDER_URI", "")
private_key = os.getenv("PRIVATE_KEY", "")

# We will initialize this gracefully so the server can start without crashing if .env is missing
w3 = Web3(Web3.HTTPProvider(rpc_url)) if rpc_url else None

CONTRACT_ADDRESS_FILE = "contract_address.txt"

def deploy_contract():
    if not w3 or not private_key:
        print("Missing Ethereum credentials in .env")
        return None
        
    with open("contracts/VotingLedger.sol", "r") as f:
        contract_source = f.read()

    # Compile contract
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "VotingLedger.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    }, solc_version="0.8.0")

    bytecode = compiled_sol["contracts"]["VotingLedger.sol"]["VotingLedger"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["VotingLedger.sol"]["VotingLedger"]["abi"]

    account = w3.eth.account.from_key(private_key)
    VotingLedger = w3.eth.contract(abi=abi, bytecode=bytecode)

    print("Deploying contract...")
    transaction = VotingLedger.constructor().build_transaction({
        "chainId": w3.eth.chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print("Waiting for transaction receipt...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    contract_address = tx_receipt.contractAddress
    print(f"Contract deployed at: {contract_address}")
    
    # Save the address to file
    with open(CONTRACT_ADDRESS_FILE, "w") as f:
        f.write(contract_address)

    # We also need to save ABI locally for `app.py` to use, but we can recompile on block push if needed,
    # or just return it here and cache it. Let's just write to a json file to be clean.
    import json
    with open("contract_abi.json", "w") as f:
        json.dump(abi, f)
        
    return contract_address

def load_contract():
    if not w3 or not os.path.exists(CONTRACT_ADDRESS_FILE) or not os.path.exists("contract_abi.json"):
        return None
        
    with open(CONTRACT_ADDRESS_FILE, "r") as f:
        address = f.read().strip()
        
    import json
    with open("contract_abi.json", "r") as f:
        abi = json.load(f)
        
    return w3.eth.contract(address=address, abi=abi)

def submit_hash_to_ethereum(block_hash):
    if not w3 or not private_key:
        return "N/A - Ethereum not configured"
        
    contract = load_contract()
    if not contract:
        return "N/A - Contract not deployed"

    account = w3.eth.account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)
    
    try:
        transaction = contract.functions.recordVoteHash(block_hash).build_transaction({
            "chainId": w3.eth.chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": account.address,
            "nonce": nonce,
        })
        
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # Don't wait for receipt as this breaks web server async flow, just return hex hash
        return w3.to_hex(tx_hash)
    except Exception as e:
        print(f"Error submitting to Ethereum: {e}")
        return f"Error: {str(e)}"

if __name__ == '__main__':
    deploy_contract()
