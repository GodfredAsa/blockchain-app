import time
from abc import ABC

from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block, raise_exception
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-d2dd6e84-ba65-4664-868d-b0130aa5f5a1'
pnconfig.publish_key = 'pub-c-cd5b0701-3d60-43fa-b3c8-cd8afb8d68a3'

pubnub = PubNub(pnconfig)

# creating a channel and subscribing to it 
CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


# adding a listener to the channel by inheriting from the subscribe callback class
class Listener(SubscribeCallback, ABC):

    def __init__(self, blockchain: 'Blockchain', transaction_pool: 'TransactionPool') -> None:
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    # overriding the message method in the base class
    def message(self, pubnub, message_object):
        print(f'\n-- Message Channel: {message_object.channel}, Message: {message_object.message}')
        # return super().message(pubnub, message)
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            # making a copy of a chain 
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print('\nChain Replacement Successful')
            except Exception as e:
                print(f'\nChain Replacement Failed: {e}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool')



class PubSub:
    """ 
    Handles the publishing /subscribe layer of the application
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain: 'Blockchain', transaction_pool: 'TransactionPool') -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transaction_pool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
         sync() enables message to be sent over the network
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block: 'Block'):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

    def broadcast_transaction(self, transaction):
        """ Broadcast transaction  to all nodes"""
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())


def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'Bar'})


if __name__ == '__main__':
    main()
