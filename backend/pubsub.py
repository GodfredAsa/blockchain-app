import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block, raise_exception
from backend.blockchain.blockchain import Blockchain

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-d2dd6e84-ba65-4664-868d-b0130aa5f5a1'
pnconfig.publish_key = 'pub-c-cd5b0701-3d60-43fa-b3c8-cd8afb8d68a3'

pubnub = PubNub(pnconfig)

# creating a channel and subscribing to it 
CHANNELS = {'TEST': 'TEST', 'BLOCK': 'BLOCK'}


# adding a listener to the channel by inheriting from the subscribe callback class
class Listener(SubscribeCallback):
    
    def __init__(self, blockchain: 'Blockchain') -> None:
        self.blockchain = blockchain

    # overriding the message method in the base class
    def message(self, pubnub, message_object):
        print (f'\n-- Message Channel: {message_object.channel}, Message: {message_object.message}')
        # return super().message(pubnub, message)
        if message_object.channel == CHANNELS ['BLOCK']:
            block = Block.from_json(message_object.message)
            # making a copy of a chain 
            potential_chain = self. blockchain.chain [:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print('\nChain Replacement Successful')
            except Exception as e:
                 print(f'\nChain Replacement Failed: {e}')


class PubSub():
    """ 
    Handles the publish/subscribe layer of the application 
    Provides communication between the nodes of the blockchain network.
    """
    def __init__(self, blockchain: 'Blockchain') -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

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
        self.publish (CHANNELS['BLOCK'], block.to_json())

def main():
    pubsub = PubSub()
    time.sleep(1) 
    pubsub.publish(CHANNELS['TEST'], {'foo': 'Bar'})

if __name__ == '__main__':
    main()
    
