from backend.blockchain.block import Block

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


def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    
    print(blockchain)

if __name__=='__main__':
    main()