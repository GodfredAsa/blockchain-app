from backend.utils.crypto_hash import crypto_hash


def test_crypto_hash():
    # with the crypto hash algorithm we ensure the following is achieved 
    # 1. hashes all types of data eg numbers, letters and anything 

    # 2. hash values of two or more inputs remain the same regardless of order 
    assert crypto_hash(1, [21], 'three') == crypto_hash('three', 1, [21])

    expected = 'b2213295d564916f89a6a42455567c87c3f480fcd7a1c15e220f17d7169a790b'

    assert crypto_hash( 'foo') == expected