import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-d2dd6e84-ba65-4664-868d-b0130aa5f5a1'
pnconfig.publish_key = 'pub-c-cd5b0701-3d60-43fa-b3c8-cd8afb8d68a3'

pubnub = PubNub(pnconfig)

# creating a channel and subscribing to it 
TEST_CHANNEL = 'TEST_CHANNEL'

# adding a listener to the channel by inheriting from the subscribe callback class
class Listener(SubscribeCallback):
    # overriding the message method in the base class
    def message(self, pubnub, message_object):
        print (f'\n-- Message Channel: {message_object.channel}, Message: {message_object.message}')
        # return super().message(pubnub, message)


class PubSub():
    """ 
    Handles the publish/subscribe layer of the application 
    Provides communication between the nodes of the blockchain network.
    """
    def __init__(self) -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
         sync() enables message to be sent over the network
        """
        self.pubnub.publish().channel(channel).message(message).sync() 


def main():
    pubsub = PubSub()
    time.sleep(1) 
    pubsub.publish(TEST_CHANNEL, {'foo': 'Bar'})

if __name__ == '__main__':
    main()
    
