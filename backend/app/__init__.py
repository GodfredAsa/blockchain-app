import os
import random
from flask import Flask, jsonify
from typing import List
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import Block
import  http.client as status

from backend.pubsub import PubSub

app = Flask(__name__)

blockchain = Blockchain()
pubsub  = PubSub()


@app.route('/')
def route_default():
    return "Tests server"


@app.route('/blockchain')
def route_blockchain() -> List['Block']:
    print(blockchain)
    return jsonify(blockchain.to_json()), status.OK


@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'
    blockchain.add_block(transaction_data)
    return jsonify(blockchain.chain[-1].to_json()), status.CREATED


# SETTING RANDOM PORTS BETWEEN 5001-5999. BELOW IS THE COMMAND FOR RUNNING ANOTHER INSTANCE 
# export PEER=True && python3 -m backend.app

PORT = 5000
if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

app.run(port=PORT)
# if __name__ == '__main_-':
#     app.run(debug=True, port=5000)