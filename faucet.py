import time
from web3 import Web3
from eth_account import Account
from colorama import init, Fore
from web3.middleware import geth_poa_middleware

init(autoreset=True)

web3 = Web3(Web3.HTTPProvider("https://base-sepolia-rpc.publicnode.com"))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

if web3.is_connected():
    print(Fore.GREEN + "🔗 Web3 Connected...\n")
else:
    print(Fore.RED + "❌ Gagal konek ke RPC")
    exit()

PRIVATE_KEYS_FILE = 'pkevm.txt'
PROXY_FILE = 'proxy.txt'
FAUCET_CONTRACT = Web3.to_checksum_address("0x0c2363273543fb186b3aa570d6ad2b80cd75521d")
FAUCET_ABI = [{
    "inputs": [
        {"internalType": "uint256", "name": "total", "type": "uint256"},
        {"internalType": "address", "name": "recipient", "type": "address"}
    ],
    "name": "Claims",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
}]
CLAIM_AMOUNT = 1
CHAIN_ID = 84532
GAS_PRICE_GWEI = 0.1
DELAY_SECONDS = 10
SLEEP_AFTER_CLAIM = 86400  

with open(PRIVATE_KEYS_FILE, 'r') as f:
    keys = [line.strip() for line in f if line.strip()]

use_proxy = input("🔧 Gunakan proxy? (y/n): ").strip().lower()
proxy_list = []
if use_proxy == "y":
    try:
        with open(PROXY_FILE, 'r') as pf:
            proxy_list = [line.strip() for line in pf if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + "❌ File proxy.txt tidak ditemukan.")
        exit()

contract = web3.eth.contract(address=FAUCET_CONTRACT, abi=FAUCET_ABI)

while True:
    print(Fore.CYAN + f"\n🔍 Menjalankan klaim faucet untuk {len(keys)} wallet...\n")
    
    for i, priv in enumerate(keys, start=1):
        try:
            account = Account.from_key(priv)
            address = account.address

            nonce = web3.eth.get_transaction_count(address)

            tx = contract.functions.Claims(CLAIM_AMOUNT, address).build_transaction({
                'chainId': CHAIN_ID,
                'gasPrice': web3.to_wei(GAS_PRICE_GWEI, 'gwei'),
                'nonce': nonce,
            })
            estimated_gas = web3.eth.estimate_gas({
                'from': address,
                'to': FAUCET_CONTRACT,
                'data': tx['data']
            })
            tx['gas'] = int(estimated_gas * 1.1)

            signed_tx = web3.eth.account.sign_transaction(tx, priv)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hex = web3.to_hex(tx_hash)

            print(Fore.GREEN + f"✅ [{i}] TX sent for {address} → {tx_hex}")

        except Exception as e:
            print(Fore.RED + f"❌ [{i}] Error wallet {address}: {e}")

        time.sleep(DELAY_SECONDS)

    print(Fore.GREEN + "\n✅ Semua proses klaim selesai. Menunggu 24 jam untuk siklus berikutnya...\n")
    time.sleep(SLEEP_AFTER_CLAIM)
