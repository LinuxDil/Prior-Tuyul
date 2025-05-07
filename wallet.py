from eth_account import Account
from mnemonic import Mnemonic

Account.enable_unaudited_hdwallet_features()

def generate_wallet():
    mnemo = Mnemonic("english")
    mnemonic = mnemo.generate(strength=128)  
    acct = Account.from_mnemonic(mnemonic)
    private_key = acct.key.hex()
    address = acct.address
    return mnemonic, private_key, address

def main():
    try:
        jumlah = int(input("📥 Masukkan jumlah wallet yang ingin dibuat: "))
    except ValueError:
        print("❌ Input tidak valid. Masukkan angka.")
        return

    with open("mnemonic.txt", "w") as f_mnemonic, \
         open("pkevm.txt", "w") as f_privkey, \
         open("addressevm.txt", "w") as f_address:

        for i in range(jumlah):
            mnemonic, privkey, address = generate_wallet()

            print("=================================")
            print(f"🔐 ADFMIDN | Wallet #{i+1}")
            print("---------------------------------")
            print(f"🧠 Mnemonic      : {mnemonic}")
            print(f"🔑 PrivateKey EVM: {privkey}")
            print(f"🏦 Address EVM   : {address}")
            print("=================================\n")

            f_mnemonic.write(f"{mnemonic}\n")
            f_privkey.write(f"{privkey}\n")
            f_address.write(f"{address}\n")

    print("✅ Semua wallet berhasil dibuat dan disimpan ke file!")

if __name__ == "__main__":
    main()
