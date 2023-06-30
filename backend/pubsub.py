import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

# publish_key = "pub-c-cd5b0701-3d60-43fa-b3c8-cd8afb8d68a3"
# subscribe_key = "sub-c-d2dd6e84-ba65-4664-868d-b0130aa5f5a1"


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-d2dd6e84-ba65-4664-868d-b0130aa5f5a1'
pnconfig.publish_key = 'pub-c-cd5b0701-3d60-43fa-b3c8-cd8afb8d68a3'

pubnub = PubNub(pnconfig)

"""
Publishers publish messages through a channel and subscribers receive messages through the channel
"""

# creating a channel and subscribing to it 
TEST_CHANNEL = 'TEST_CHANNEL'
pubnub.subscribe().channels([TEST_CHANNEL]).execute()

# adding a listener to the channel by inheriting from the subscribe callback class
class Listener(SubscribeCallback):
    # overriding the message method in the base class
    def message(self, pubnub, message):
        print (f'\n-- Incoming message_object: {message}')
        # return super().message(pubnub, message)

pubnub.add_listener(Listener())

def main():
    # publishing to the channel
    # enables channel subscription before publishing as both are network events and requires some time 
    time.sleep(1) 
    pubnub.publish().channel(TEST_CHANNEL).message({'foo': 'Bar'}).sync() 
    # sync() enables message to be sent over the network

if __name__ == '__main__':
    main()
    
