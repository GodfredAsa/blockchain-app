import time
from backend.utils.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.utils.hex_to_binary import hex_to_binary

GENESIS_DATA = { 
    'timestamp': 1, 
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash', 
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}



class Block:
    """
    Block: a unit of storage.
    Store transactions in a blockchain that supports a cryptocurrency.
    """
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce) -> None:
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce


    def __repr__(self) -> None:
        return f'<Block timestamp: {self.timestamp}, ast_hash: {self.last_hash}, hash: {self.hash}, data: {self.data}, difficulty: {self.difficulty}, nonce: {self.nonce}>'



    @staticmethod
    def mine_block(last_block: 'Block', data):
        """  Mines a block on the given last block and data, until a block hash is found that meets the leading 0's proof of work requirements"""
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp )
        nonce = 0
        hashed = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hashed)[:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block,timestamp )
            hashed = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp=timestamp, last_hash=last_hash, hash=hashed, data=data, difficulty=difficulty, nonce=nonce)

    @staticmethod
    def genesis():
        """ Generate the Genesis Block """ 
        return Block(**GENESIS_DATA)
    
    @staticmethod
    def adjust_difficulty(last_block: 'Block', new_timestamp) -> int:
        """
        calculates adjusted difficulty according to the MINE_RATE.
        Increase the difficulty for quickly mined blocks
        Decrease the difficult for slowly mined blocks 
        """

        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        return last_block.difficulty - 1 if last_block.difficulty > 1 else 1


def main():

    genesis_block = Block.genesis()
    block = Block.mine_block(genesis_block, 'beautiful')
    print(block)

if __name__=='__main__':
    main()