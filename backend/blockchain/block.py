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


def raise_exception(message: str) -> Exception :
    raise Exception(message)




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
    
    @staticmethod
    def is_valid_block(last_block: 'Block', block: 'Block'):
       
        """ 
        Validate a block enforcing the following roles 
        - block must have proper last hashed referenced.
        - Block must meet proof of work requirement
        - Difficulty must only adjust by 1
        - the block hash must be a valid combination of the block fields  
        """


        if block.last_hash != last_block.hash:
            raise_exception('The block last_hash must be correct')
            # raise Exception('the block last_hash must be correct')
        if hex_to_binary(block.hash)[: block.difficulty] != '0' * block.difficulty:
           raise_exception('Proof of work requirement not met')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise_exception('Block difficulty must only adjust by 1')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )

        if block.hash != reconstructed_hash:
            raise_exception('The block hash must be correct')
            
    def to_json(self):
        """
        Serialize a block to a dictionary of its attributes.
        """
        return self.__dict__
    
    @staticmethod
    def from_json(block_json):
        """
        Deserialize a block's json representation back into a block instance
        """
        return Block(**block_json)
         

def main():
    genesis_block = Block.genesis()
    bad_block  = Block.mine_block(genesis_block, 'foo')
    bad_block.last_hash = 'evil_data'

    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')


if __name__ == '__main__':
    main()
