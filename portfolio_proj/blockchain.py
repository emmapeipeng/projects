## Make a Blockchain class
# manages the blockchain and adding new transactions

## Blocks:
# include: index, timestamp (in Unix time), list of transactions,
# proof, and hash of previous Block **important (practically immutable)
# originally used for digital timestamps like a notary; then, used for 
# bitcoin in 2009; point is, blocks are immutable
# super secure because of hashing, proof of work, and that everyone gets full copy(peer-peer network)

## Proof of Work:
# "how new Blocks are created or mined on the blockchain. The goal of PoW 
# is to discover a number which solves a problem. The number must be difficult 
# to find but easy to verify"
# slows down creation of new blocks; takes like 10 min for bitcoin

import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4
from flask import Flask, request, jsonify


class Blockchain(object):
    def __init__(self): # make new Blockchain object
        self.chain = [] # list to store blocks
        self.current_transactions = [] # list of transactions to be added

        self.new_block(proof=100, previous_hash='1') # genesis block

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



## Flask framework to send/get http requests; need API layer to interact with blockchain

app = Flask(__name__) # make flask app, the server

node_identifier = str(uuid4()).replace('-', '') # unique ID for node

blockchain = Blockchain()

## API routes (url paths to interact with app)

@app.route('/mine', methods=['GET']) # get data
def mine(): # the magic: calculate proof, reward miner, add to chain
    # use previous proof to calculate new proof
    last_block = blockchain.last_block 
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
   
    # reward 
    blockchain.new_transaction(sender='0', recipient=node_identifier, amount=1)
    
    # create new block by adding to chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
  

@app.route('/transactions/new', methods=['POST']) # give data
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all (k in values for k in required):
        return 'Missing values'
    

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to block {index}'}
    return jsonify(response), 201
    

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200 # status code for completed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


## Test: 
# curl -X POST -H "Content-Type: application/json" \
     #-d '{"sender":"Alice","recipient":"Bob","amount":5}' \
     #http://127.0.0.1:5000/transactions/new
# curl http://127.0.0.1:5000/mine
# curl http://127.0.0.1:5000/chain
