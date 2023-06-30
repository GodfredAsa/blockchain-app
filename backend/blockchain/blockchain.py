from backend.blockchain.block import Block, raise_exception
from collections import OrderedDict
class Blockchain:
    """Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """

    def __init__(self) -> None:
        self.chain =[Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(last_block=self.chain[-1], data=data))

    def __repr__(self) -> None:
       return f'Blockchain: {self.chain}'
    
    def __eq__(self, other):
       block = OrderedDict(**self)
       last_block = OrderedDict(**other)
       return block == last_block
    
    @staticmethod
    def is_valid_chain(chain):
        """ 
        Validate incoming chain
        Enforce the following rules of a blockchain 
        - the chain must start with genesis block
        - blocks must be formatted correctly
        """

        if chain[0].hash != Block.genesis().hash:
            raise_exception('The Genesis Block Must be Valid')
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

    def replace_chain(self, chain): 
        """ 
        Replace the local chain with the incoming one if the following applies:
        - The incoming chain is longer than the local one.
        - The incoming chain is formatted properly.
        """

        if len(chain) <= len(self.chain):
            raise_exception('Cannot Replace. Incoming chain should be longer')
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise_exception(f'Cannot replace. The incoming chain is invalid: {e}')

        self.chain = chain


    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return [block.to_json() for block in self.chain ]

def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    
    print(blockchain)

if __name__=='__main__':
    main()