from backend.blockchain.block import Block, GENESIS_DATA
import time 
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_binary
import pytest

def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block=last_block, data=data)

    # asserting the instance on the created block 
    assert isinstance(block, Block)
    # asserting the data of the block is the same as the data parsed in creation it
    assert block.data == data
    # asserting block's last hashed equals the last_block's hash
    assert block.last_hash == last_block.hash

    assert hex_to_binary(block.hash)[: block.difficulty] == '0' * block.difficulty

def test_quickly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')
    assert mined_block.difficulty == last_block.difficulty + 1

def test_slowly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, 'bar')
    assert mined_block.difficulty == last_block.difficulty - 1

def test_mined_block_difficulty_limits_at_1():
    last_block = Block(time.time_ns(),'test_last_hash', 'test_hash', 'test_data', 1, 0)
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')
    assert mined_block.difficulty == 1

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)

    # testing the data in the generated block , shorthand below with the for loop 
    assert genesis.timestamp == GENESIS_DATA['timestamp']
    assert genesis.last_hash == GENESIS_DATA['last_hash']
    assert genesis.hash == GENESIS_DATA['hash']
    assert genesis.data == GENESIS_DATA['data']

    # Better way of testing the data in the generated block 
    for key, value in GENESIS_DATA.items () :
        getattr(genesis, key) == value

@pytest.fixture
def last_block() -> 'Block':
    return Block.genesis()

@pytest.fixture
def block(last_block)-> 'Block':
    return Block.mine_block(last_block, 'test_data')

def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)

# TODO CORRECT THIS TESTS IMPLEMENTATION IN THE MAIN CODE
def test_is_valid_block_with_bad_last_hash(last_block: 'Block', block: 'Block'):
    block.last_hash = 'bad_hash'

    with pytest.raises(Exception, match='The block last_hash must be correct') as e:
        Block.is_valid_block(last_block, block)
       
def test_is_valid_block_bad_proof_of_work(last_block, block: 'Block'):
    block.hash = 'fff'
    with pytest.raises(Exception, match='Proof of work requirement not met') as e:
        Block.is_valid_block(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block: 'Block', block: 'Block'):
    jumped_difficulty = 10
    block.difficulty = jumped_difficulty
    block.hash = f'{"0" * jumped_difficulty}111abc'
    with pytest.raises(Exception, match='Block difficulty must only adjust by 1') as e:
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_block_hash(last_block, block: 'Block'):
    block.hash = '00000000000000abbbbabc'
    with pytest.raises(Exception, match='The block hash must be correct') as e:
        Block.is_valid_block(last_block, block)