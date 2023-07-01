from flask import Flask, jsonify
from typing import List
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import Block
import  http.client as status

app = Flask(__name__)

blockchain = Blockchain()


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


app.run()
# if __name__ == '__main_-':
#     app.run(debug=True, port=5000)