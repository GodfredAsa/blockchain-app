import uuid
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from backend.config import STARTING_BALANCE


# ec means elliptic cryptography

class Wallet:
    """ 
    An individual wallet for a miner
    Keeps track of the miner's balance 
    .
    Allows miner to authorize transactions 
    """

    def __init__(self) -> None:
        self.address = str(uuid.uuid4())[:8]
        self.balance = STARTING_BALANCE
        # bitcoin uses the ec.SECP256k1() SECP => STANDARD EFFICIENT CRYPTOGRAPHY PRIME 256 BITS
        # Uses a prime number to generate the curb. The prime number will be represented btn 256 binary Bits
        # K is a name of a mathematician and the 1 is the 1st implementation
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        # public key is generated from the private key
        self.public_key = self.private_key.public_key()

    def generate_signature(self, data):
        """
        Generate a signature based on the data using the local private key.
        """
        return self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify_signature(public_key, data, signature):
        """
        Verify signature based on the original public key and data
        """
        try:
            public_key.verify(signature, json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False


def main():
    wallet = Wallet()
    print(f'Wallet__dict__: {wallet.__dict__}')

    # SIGN DATA
    data = {'foo': 'bar'}
    signature = wallet.generate_signature(data)
    print(f'Signature : {signature}')

    # VERIFY SIGNED DATA
    should_be_valid = Wallet.verify_signature(wallet.public_key, data, signature)
    print(f"should_be_valid: {should_be_valid}")

    # VERIFY INVALID DATA
    should_be_invalid = Wallet.verify_signature(Wallet().public_key, data, signature)
    print(f"should_be_invalid: {should_be_invalid}")


if __name__ == '__main__':
    main()

