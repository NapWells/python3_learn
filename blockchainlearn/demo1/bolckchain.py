# {
#     "index": 0,
#     "timestamp": "",
#     "transactions": [
#         {
#             "sender": "",
#             "recipient": "",
#             "amount":0
#         }
#     ],
#     "proof": "",
#     "previous_hash": ""
# }
import hashlib
import json
from time import time
from urllib import parse
from uuid import uuid4
from flask import Flask, jsonify, request
import requests
from argparse import ArgumentParser


class BlockChain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(proof=100, previous_hash=1)
        self.nodes = set()

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount) -> int:
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    def register_node(self, address: str):
        parser_url = parse.urlparse(address)
        self.nodes.add(parser_url.netloc)

    def resolve_conflicts(self) -> bool:
        neighbours = self.nodes
        max_length = len(self.chain)
        new_chain = None
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

                if new_chain:
                    self.chain = new_chain
                    return True
                return False

    def valid_chain(self, chain) -> bool:
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1
        return True

    @staticmethod
    def hash(block):
        block_str = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof: int):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        print("proof is ", proof)
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(guess_hash)
        return guess_hash[0:4] == '0000'


app = Flask(__name__)
block_chain = BlockChain()
node_identifier = str(uuid4()).replace('-', '')


@app.route('/index', methods=['GET'])
def index():
    return 'hello BlockChain'


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    require = ['sender', 'recipient', 'amount']
    if values is None or not all(k in values for k in require):
        return 'Missing values', 400
    block_index = block_chain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block{block_index}'}
    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = block_chain.proof_of_work(last_proof)
    block_chain.new_transaction(sender='0', recipient=node_identifier, amount=1)
    block = block_chain.new_block(proof, None)
    response = {
        'message': 'New block forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': proof,
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain)
    }
    return jsonify(response), 200


@app.route('/register/node', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return 'error: please supply a  valid list of nodes', 400
    for node in nodes:
        block_chain.register_node(node)
    response = {
        'message': 'new nodes has been added',
        'total_nodes': list(block_chain.nodes)
    }
    return jsonify(response), 200


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = block_chain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'our chain was replace',
            'new_chain': block_chain.chain
        }
    else:
        response = {
            'message': 'our chain was authoritative',
            'new_chain': block_chain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    # testPow = BlockChain()
    # testPow.proof_of_work(1000)
    parser = ArgumentParser()
    parser.add_argument('-p','--port', default=5001,type=int,help='port to listen to ')
    args = parser.parse_args()
    port = args.port
    app.run(host='127.0.0.1', port=port)
