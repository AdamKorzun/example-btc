from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import pkcs1_15
import base58
import binascii
import json


class Wallet:
    def __init__(self):
        self.balance = 0
        self.private_key = None
        self.public_key = None

    def create(self):
        key = RSA.generate(2048)
        self.private_key = key
        self.public_key = key.publickey()

    # save public and private keys to files
    def dump(self):
        # add path from config manager / overwrite option
        with open("private_key.pem", "wb") as private_file:
            private_file.write(self.private_key.export_key())
        with open("public_key.pem", "wb") as public_file:
            public_file.write(self.public_key.export_key())

    def retrieve(self, private_key):
        self.private_key = private_key
        self.public_key = self.private_key.publickey()

    def __str__(self):
        if (self.public_key is not None):
            return base58.b58encode(self.public_key.exportKey('DER')).decode('utf8')


class Transaction:
    def __init__(self, sender=None, recipient=None, value=0):
        if value < 0.0 and value is not None:
            raise ValueError()
        if value is not None and recipient is not None and sender is not None:
            self.raw_transaction = {
                'sender':sender,
                'recipient':recipient,
                'value':value
            }

    def send(self):
        # add path from config manager
        if self.signature is None:
            raise Error('Transaction is not signed')
        with open('pending_transactions/' + str(hash(self.signature)) + '.json', 'w') as ts_file:
            ts_file.write(json.dumps(self.to_json(), indent=2))

    # sign raw_transaction using private key
    def sign(self, private_key):
        ts = SHA.new(str(self.raw_transaction).encode('utf8'))
        signed_transaction = pkcs1_15.new(private_key).sign(ts)
        self.signature = binascii.hexlify(signed_transaction).decode('utf8')
        return self.signature

    def to_json(self):
        transaction = {
            'signature':self.signature,
            'raw_transaction':self.raw_transaction
        }
        return transaction

    def from_json(self, dict_object):
        self.signature = dict_object['signature']
        self.raw_transaction = dict_object['raw_transaction']

    def __str__(self):
        return str(self.to_json())


class Block():
    def __init__(self, previous_block_hash):
        self.previous_block_hash = previous_block_hash
        self.transactions = []
        self.markle_root = None
        self.block_id = 0
        self.nonce = 0

    def dump(self):
        # get path from config manager
        with open('blocks/block' + str(self.block_id) + '.json') as file:
            file.write(str(self))

    def to_json(self):
        json_dict = {
            'previous_block_hash':self.previous_block_hash,
            'merkle_root':self.merkle_root,
            'block_id':self.block_id,
            'nonce':self.nonce,
            'transactions':self.transactions
        }
        return json_dict

    def __str__(self):
        return str(self.to_json())


class Node:
    def __init__(self):
        None

    def verify_transaction(self, transaction):
        signature = binascii.unhexlify((transaction.signature).encode('utf8'))
        sender = transaction.raw_transaction['sender']
        recipient = transaction.raw_transaction['recipient']
        value = transaction.raw_transaction['value']
        public_key = RSA.importKey(base58.b58decode(sender.encode('utf8')), 'DEM')
        raw_transaction = SHA.new(str(transaction.raw_transaction).encode('utf8'))
        valid = True
        try:
            pkcs1_15.new(public_key).verify(raw_transaction,signature)
        except Exception():
            valid = False
        return valid


class Miner(Node):
    def mine():
        block = Block(hash(get_last_block()))
    def get_last_block():
        None
