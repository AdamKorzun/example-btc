from btc import *
from Crypto.PublicKey import RSA
import json
from config_manager import ConfigManager


config = ConfigManager()
config.from_json('config.json')


with open('private_key.pem', 'rb') as file:
    private_key = RSA.import_key(file.read())
with open('public_key.pem', 'rb') as file:
    public_key = RSA.import_key(file.read())

wallet = Wallet()
wallet.retrieve(private_key)

wallet_2 = Wallet()
wallet_2.create()

# transaction = Transaction(str(wallet), str(wallet_2), 1)
# signature = transaction.sign(private_key)
# transaction.send()

transaction = Transaction()
with open('pending_transactions/6117195753517267720.json') as json_file:
    json_dict = json.load(json_file)

transaction.from_json(json_dict)

print(transaction)

block = Block(None)

miner = Miner()
miner.verify_transaction(transaction)
node = Node()
print(node.verify_transaction(transaction))

config = {
    'transaction_dir':'/Desktop/Python/example-btc/pending_transactions',
    'blocks_dir':'/Desktop/Python/example-btc/blocks'

}
