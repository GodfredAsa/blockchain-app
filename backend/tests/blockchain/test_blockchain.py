
import pytest
from backend.blockchain.block import GENESIS_DATA
from backend.blockchain.blockchain import Blockchain


def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA ['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)
    assert blockchain.chain[-1].data == data

@pytest.fixture
def blockchain_with_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block(i)
    return blockchain

def test_is_valid_chain_bad_genesis_block(blockchain_with_three_blocks: 'Blockchain'):
    blockchain_with_three_blocks.chain[0].hash = 'bad_hash'
    with pytest.raises(Exception, match='The Genesis Block Must be Valid'):
        Blockchain.is_valid_chain(blockchain_with_three_blocks.chain)

def test_is_valid_chain(blockchain_with_three_blocks: 'Blockchain'):
    Blockchain.is_valid_chain(blockchain_with_three_blocks.chain)

def test_replace_chain(blockchain_with_three_blocks: 'Blockchain'):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_with_three_blocks.chain)
    assert blockchain.chain == blockchain_with_three_blocks.chain


def test_replace_chain_chain_not_longer(blockchain_with_three_blocks: 'Blockchain'):
    blockchain = Blockchain()
    with pytest.raises(Exception, match='Cannot Replace. Incoming chain should be longer'):
        blockchain_with_three_blocks.replace_chain(blockchain.chain)


def test_replace_chain_bad_chain(blockchain_with_three_blocks: Blockchain):
    blockchain = Blockchain()
    blockchain_with_three_blocks.chain[1].hash = 'evil_hash'
    with pytest.raises(Exception, match='Cannot replace. The incoming chain is invalid'):
        blockchain.replace_chain(blockchain_with_three_blocks.chain)