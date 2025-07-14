from web3 import Web3
import requests
import os


API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETH_PUBLIC_NODE = "https://eth-mainnet.public.blastapi.io"


def get_abi_from_contract(address: str) -> str:
    url = f"https://api.etherscan.io/v2/api?chainid=1&module=contract&action=getabi&address={address}&apikey={API_KEY}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data["result"]
    return []


def decode_contract_input_data(address: str, input: str) -> dict:
    w3 = Web3(Web3.HTTPProvider(ETH_PUBLIC_NODE))
    abi = get_abi_from_contract(address=address)
    contract = w3.eth.contract(abi=abi)

    try:
        func_obj, func_params = contract.decode_function_input(input)
        return {
            "functionName": str(func_obj.fn_name),
            "decodedInputs": func_params
        }
    except Exception as e:
        return {
            "functionName": "Unknown",
            "decodedInputs": [],
            "error": str(e)
        }