import os
import random
from flask import Flask, jsonify
from typing import List
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import Block
import http.client as status
import requests
from backend.pubsub import PubSub

app = Flask(__name__)

blockchain = Blockchain()
pubsub  = PubSub(blockchain)


@app.route('/')
def route_default():
    return "Tests server"


@app.route('/blockchain')
def route_blockchain() -> List['Block']:
    print(blockchain)
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json()), status.CREATED


# SETTING RANDOM PORTS BETWEEN 5001-5999. BELOW IS THE COMMAND FOR RUNNING ANOTHER INSTANCE 
# export PEER=True && python3 -m backend.app

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    results = requests.get(f'http://127.0.0.1:{ROOT_PORT}/blockchain')
    print(f'Results JSON => {results.json()}')
    result_blockchain: 'Blockchain' = Blockchain.from_json(results.json())

    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('In -- Successfully synchronized the local chain')
    except Exception as e:
        print(f'Couldn\'t Successfully Synchronized Chain, {str(e)}')


app.run(port=PORT)
# if __name__ == '__main_-':
#     app.run(debug=True, port=5000)
