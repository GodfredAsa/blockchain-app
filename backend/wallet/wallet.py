import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

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


def main():
    wallet = Wallet()
    print(f'Wallet__dict__: {wallet.__dict__}')


if __name__ == '__main__':
    main()

