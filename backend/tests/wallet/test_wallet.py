from backend.wallet.wallet import Wallet


def test_verify_valid_generated_signature():
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.generate_signature(data)
    assert Wallet.verify_signature(wallet.public_key, data, signature)


def test_verify_invalid_generated_signature():
    data = {'foo': 'test_data'}
    wallet = Wallet()
    signature = wallet.generate_signature(data)
    # using random wallet public key
    assert not Wallet.verify_signature(Wallet().public_key, data, signature)