from web3 import Web3
from eth_account import Account
from hexbytes import HexBytes
import time
from colorama import init, Fore

init(autoreset=True)

web3 = Web3(Web3.HTTPProvider('https://base-sepolia-rpc.publicnode.com'))
assert web3.is_connected(), "Gagal konek ke jaringan Base Sepolia!"
chainId = web3.eth.chain_id

PRIVATE_KEYS_FILE = 'pkutama.txt'
TARGET_ADDRESSES_FILE = 'addressevm.txt'

while True:
    try:
        eth_input = input(Fore.CYAN + "💰 Masukkan jumlah ETH yang ingin dikirim per address (misal: 0.001): ").strip()
        AMOUNT_TO_SEND = float(eth_input)
        if AMOUNT_TO_SEND <= 0:
            raise ValueError
        break
    except ValueError:
        print(Fore.RED + "❌ Masukan tidak valid. Harus angka lebih dari 0.")

GAS_LIMIT = 21000
GAS_PRICE = web3.eth.gas_price

with open(PRIVATE_KEYS_FILE, 'r') as f:
    private_keys = [line.strip() for line in f if line.strip()]

with open(TARGET_ADDRESSES_FILE, 'r') as f:
    target_addresses = [line.strip() for line in f if line.strip()]

print(Fore.CYAN + f"\n🚀 Mengirim {AMOUNT_TO_SEND} ETH ke {len(target_addresses)} address...\n")

for pk_index, private_key in enumerate(private_keys, start=1):
    try:
        sender_account = Account.from_key(private_key)
        sender_address = sender_account.address
        balance = web3.eth.get_balance(sender_address)

        print(Fore.YELLOW + f"🔑 PK#{pk_index} - {sender_address}")
        print(Fore.BLUE + f"💼 Balance: {web3.from_wei(balance, 'ether')} ETH")

        total_send = Web3.to_wei(AMOUNT_TO_SEND * len(target_addresses), 'ether')
        est_gas = GAS_LIMIT * GAS_PRICE * len(target_addresses)

        if balance < (total_send + est_gas):
            print(Fore.RED + "❌ Saldo tidak cukup untuk kirim ke semua address.\n")
            continue

        nonce = web3.eth.get_transaction_count(sender_address)

        for idx, target in enumerate(target_addresses, start=1):
            tx = {
                'to': target,
                'value': Web3.to_wei(AMOUNT_TO_SEND, 'ether'),
                'gas': GAS_LIMIT,
                'gasPrice': GAS_PRICE,
                'nonce': nonce,
                'chainId': chainId
            }

            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(Fore.GREEN + f"✅ TX#{idx} dikirim ke {target} | TX Hash: {tx_hash.hex()}")

            nonce += 1
            time.sleep(2)  

        print(Fore.CYAN + f"✅ Semua transaksi dari {sender_address} selesai.\n")

    except Exception as e:
        print(Fore.RED + f"⚠️  Error pada PK#{pk_index}: {e}\n")

print(Fore.GREEN + "\n✅ Semua pengiriman selesai.")
