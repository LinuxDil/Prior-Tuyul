from web3 import Web3
from eth_abi import encode
import requests, time, json, random
from colorama import Fore, Style, init
from requests.exceptions import RequestException

init(autoreset=True)

web3 = Web3(Web3.HTTPProvider('https://base-sepolia-rpc.publicnode.com'))
chainId = web3.eth.chain_id

if web3.is_connected():
    print(Fore.GREEN + "🔗 Web3 Connected...\n")
else:
    print(Fore.RED + "❌ Web3 Connection Failed. Please Try Again.")
    exit()

def retry(max_retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except RequestException as e:
                    print(Fore.YELLOW + f"⚠️ Request Error in {func.__name__}: {e} (Retry {attempt}/{max_retries})")
                except Exception as e:
                    print(Fore.YELLOW + f"⚠️ Error in {func.__name__}: {e} (Retry {attempt}/{max_retries})")
                time.sleep(delay)
            print(Fore.RED + f"⛔ Max retries reached for {func.__name__}")
            return None
        return wrapper
    return decorator

apiurl = "https://priortestnet.xyz"

@retry()
def users(addr, proxy=None):
    url = f"{apiurl}/api/users/{addr}"
    headers = {
        'authorization': None,
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0',
        'origin': 'https://priortestnet.xyz',
        'referer': 'https://priortestnet.xyz/swap'
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(Fore.RED + f"❌ Request failed: {e}")
        return {}

@retry()
def verif_swap(addr, amount, txhash, proxy=None):
    url = f"{apiurl}/api/swap"
    data = {
        "address": addr,
        "amount": str(amount),
        "tokenFrom": "PRIOR",
        "tokenTo": "USDC",
        "txHash": txhash
    }
    headers = {
        'authorization': None,
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0',
        'origin': 'https://priortestnet.xyz',
        'referer': 'https://priortestnet.xyz/swap'
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = requests.post(url, headers=headers, json=data, proxies=proxies, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(Fore.RED + f"❌ Request failed: {e}")
        return {}

tokenabi = json.loads('[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
 
def approveTokens(tokenaddr, targetaddr, sender, senderkey):
    try:
        print(Fore.CYAN + f"🔒 Approving PRIOR from {sender} to {targetaddr}...")
        token = web3.eth.contract(address=tokenaddr, abi=tokenabi)
        nonce = web3.eth.get_transaction_count(sender)
        gas_price = web3.eth.gas_price
        max_amount = 2**256 - 1
        gas = token.functions.approve(targetaddr, max_amount).estimate_gas({'from': sender})
        tx = token.functions.approve(targetaddr, max_amount).build_transaction({
            'chainId': chainId,
            'from': sender,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce
        })
        signed_tx = web3.eth.account.sign_transaction(tx, senderkey)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(Fore.GREEN + f"✅ Approve success! TX: {web3.to_hex(tx_hash)}")
    except Exception as e:
        print(Fore.RED + f"❌ Approve error: {e}")

def apprvCheck(tokenaddr, sender, targetaddr):
    token = web3.eth.contract(address=tokenaddr, abi=tokenabi)
    return int(token.functions.allowance(sender, targetaddr).call())

def checkBal(tokenaddr, sender):
    token = web3.eth.contract(address=tokenaddr, abi=tokenabi)
    return int(token.functions.balanceOf(sender).call())

def balUser(sender):
    eth = web3.from_wei(web3.eth.get_balance(sender), 'ether')
    prior = checkBal('0xeFC91C5a51E8533282486FA2601dFfe0a0b16EDb', sender) / 10**18
    usdc = checkBal('0xdB07b0b4E88D9D5A79A08E91fEE20Bb41f9989a2', sender) / 10**6
    user_data = users(sender)
    print(Fore.BLUE + f"\n📊 Wallet: {sender}")
    print(f"💰 ETH: {eth} | 🟡 PRIOR: {prior} | 💵 USDC: {usdc}")
    print(f"🏅 Daily: {user_data.get('dailyPoints')} | Total: {user_data.get('totalPoints')}, Swaps: {user_data.get('dailySwaps')}")

def swapPriorUSDC(targetaddr, sender, senderkey, amount):
    try:
        print(Fore.MAGENTA + f"🔁 Swapping {amount:.5f} PRIOR to USDC...")
        nonce = web3.eth.get_transaction_count(sender)
        data = web3.to_hex(bytes.fromhex('8ec7baf1') + encode(['uint256'], [web3.to_wei(amount, 'ether')]))

        tx = {
            'chainId': chainId,
            'from': sender,
            'to': targetaddr,
            'data': data,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'gas': web3.eth.estimate_gas({'from': sender, 'to': targetaddr, 'data': data})
        }

        signed_tx = web3.eth.account.sign_transaction(tx, senderkey)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(Fore.GREEN + f"✅ Swap Success! TX: {web3.to_hex(tx_hash)}")
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(Fore.RED + f"❌ Swap Error: {e}")

print(Style.BRIGHT + Fore.YELLOW + "\n=== Auto Swap PRIOR Testnet by ADFMIDN Team ===\n")

amountmin = float(input('🔢 Min Swap Amount PRIOR [ex 0.01] : '))
amountmax = float(input('🔢 Max Swap Amount PRIOR [ex 0.02] : '))
totals = int(input('🔁 Total Loops : '))
print()

while True:
    for i in range(totals):
        with open('pkevm.txt', 'r') as file:
            wallets = file.read().splitlines()
            for pvkey in wallets:
                try:
                    acct = web3.eth.account.from_key(pvkey)
                    PRIORaddr = web3.to_checksum_address('0xeFC91C5a51E8533282486FA2601dFfe0a0b16EDb')
                    SWAPaddr = web3.to_checksum_address('0x8957e1988905311EE249e679a29fc9deCEd4D910')
                    amount = random.uniform(amountmin, amountmax)
                    amount_wei = web3.to_wei(amount, 'ether')

                    if apprvCheck(PRIORaddr, acct.address, SWAPaddr) >= amount_wei:
                        print(Fore.CYAN + f"✅ Already Approved")
                    else:
                        approveTokens(PRIORaddr, SWAPaddr, acct.address, acct.key)

                    txhash = swapPriorUSDC(SWAPaddr, acct.address, acct.key, amount)
                    print(Fore.YELLOW + f"🔍 Verifying TX: {txhash}")
                    verify = verif_swap(acct.address, amount, txhash)

                    if verify and verify.get("transaction", {}).get("status") == "completed":
                        print(Fore.GREEN + f"🎯 Verified! Points: {verify.get('pointsEarned')}")
                    else:
                        print(Fore.RED + "❌ Verification Failed")

                    balUser(acct.address)
                    print("-" * 40)

                except Exception as e:
                    print(Fore.RED + f"❌ Error on wallet loop: {e}")
    
    print(Fore.YELLOW + "\n⏳ Semua akun telah selesai. Menunggu 24 jam untuk loop berikutnya...\n")
    time.sleep(86400)  
