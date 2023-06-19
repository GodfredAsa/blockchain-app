import hashlib, json


def crypto_hash(*args):
    """
    Returns a sha-256 of the given arguments
    to make the hash values same regardless of the other of same inputs 
    we sort it while transforming the data
    """
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(stringified_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f"crypto_hash('one', 3, [3]): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(2, 'one', [3]): {crypto_hash(2, 'one', [3])}")


if __name__=='__main__':
    main()