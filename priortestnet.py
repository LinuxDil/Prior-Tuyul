import requests
from web3 import Web3
from eth_account import Account
import time, random
from datetime import datetime, timezone
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
TOKEN_ADDRESS = Web3.to_checksum_address("0xeFC91C5a51E8533282486FA2601dFfe0a0b16EDb")
TOKEN_ABI = [{
    "constant": True,
    "inputs": [{"name": "account", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"name": "", "type": "uint256"}],
    "type": "function",
}]
LOGIN_URL = "https://priortestnet.xyz/api/auth"
DETAIL_URL = "https://priortestnet.xyz/api/users/"
HEADERS = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://priortestnet.xyz",
    "referer": "https://priortestnet.xyz/",
    "user-agent": "Mozilla/5.0"
}
LINE = "-" * 60

with open(PRIVATE_KEYS_FILE, 'r', encoding='utf-8') as f:
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

token_contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=TOKEN_ABI)

print(Fore.CYAN + "\n🔍 Mengecek status akun Prior Testnet...\n")
for idx, privkey in enumerate(keys, start=1):
    try:
        acct = Account.from_key(privkey)
        address = acct.address
        payload = {"address": address}

        proxies = None
        if proxy_list:
            proxy = random.choice(proxy_list)
            proxies = {"http": proxy, "https": proxy}

        login_res = requests.post(LOGIN_URL, headers=HEADERS, json=payload, proxies=proxies)
        if login_res.status_code != 200:
            print(Fore.RED + f"❌ Akun {idx} - Gagal login")
            continue

        detail_res = requests.get(f"{DETAIL_URL}{address}", headers=HEADERS, proxies=proxies)
        if detail_res.status_code != 200:
            print(Fore.RED + f"⚠️  Akun {idx} - Gagal ambil data akun")
            continue

        data = detail_res.json()
        balance = token_contract.functions.balanceOf(address).call()
        readable_balance = web3.from_wei(balance, 'ether')
        base_balance = web3.eth.get_balance(address)
        readable_base_balance = web3.from_wei(base_balance, 'ether')

        print(Fore.GREEN + f"🔢 Akun {idx}")
        print(Fore.CYAN + f"🧾 Address          : {address}")
        print(Fore.MAGENTA + f"🏆 Total Points     : {data['totalPoints']}")
        print(Fore.YELLOW + f"💧 Last Faucet      : {data['lastFaucetClaim']}")
        print(Fore.BLUE + f"💰 Balance PRIOR    : {readable_balance} PRIOR")
        print(Fore.BLUE + f"💵 Balance Base Sepolia: {readable_base_balance} ETH")
        print(Fore.YELLOW + LINE + "\n")

    except Exception as e:
        print(Fore.RED + f"⚠️  Error akun {idx}: {e}\n")

    time.sleep(1)

print(Fore.GREEN + "\n✅ Semua proses selesai.")
