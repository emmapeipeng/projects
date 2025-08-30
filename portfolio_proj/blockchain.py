## Make a Blockchain class
# manages the blockchain and adding new transactions

## Blocks:
# include: index, timestamp (in Unix time), list of transactions,
# proof, and hash of previous Block **important (practically immutable)

## Proof of Work:
# "how new Blocks are created or mined on the blockchain. The goal of PoW 
# is to discover a number which solves a problem. The number must be difficult 
# to find but easy to verify"

import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self): # make new Blockchain object
        self.chain = [] # list to store blocks
        self.current_transactions = [] # list of transactions to be added


    def new_block(self, proof, previous_hash=None): # creates new block & adds to chain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block


    def new_transaction(self, sender, recipient, amount): # adds transaction to current_transactnos
        self.current_transactions.append({ # easier than making new object for transactions
            'sender': sender,
            'recipient': recipient,
            'amount':amount})
        return self.last_block['index'] + 1


    @staticmethod # doesn't need self
    def hash(block):
         block_string = json.dumps(block, sort_keys=True).encode()
         return hashlib.sha256(block_string).hexdigest()

    @property # access like attribute
    def last_block(self):
        return self.chain[-1]


    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
