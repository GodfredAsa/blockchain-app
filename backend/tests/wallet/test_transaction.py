import pytest

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify_signature(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_transaction_exceeds_balance_exception():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(Wallet(), 'recipient', 9001)


def test_update_transaction_exceeds_balance_raise_exception():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    with pytest.raises(Exception, match='Amount exceeds balance'):
        transaction.update_transaction(sender_wallet, 'new_recipient', 9001)


def test_update_transaction_new_recipient():
    sender_wallet = Wallet()
    first_recipient = 'first_recipient'
    first_amount = 20

    transaction = Transaction(sender_wallet, first_recipient, first_amount)

    next_recipient = 'next_recipient'
    next_amount = 75
    transaction.update_transaction(sender_wallet, next_recipient, next_amount)

    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - (first_amount + next_amount)
    assert Wallet.verify_signature(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_update_transaction_existing_recipient() -> None:
    sender_wallet = Wallet()
    recipient = 'recipient'
    first_amount = 20
    transaction = Transaction(sender_wallet, recipient, first_amount)

    new_amount = 25
    transaction.update_transaction(sender_wallet, recipient, new_amount)
    assert transaction.output[recipient] == first_amount + new_amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - (first_amount + new_amount)

    assert Wallet.verify_signature(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )


def test_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 50))


def test_valid_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.output[sender_wallet.address] = 9001

    with pytest.raises(Exception, match='Invalid transaction output values'):
        Transaction.is_valid_transaction(transaction)


def test_valid_transaction_with_invalid_signature():
    transaction = Transaction(Wallet(), 'recipient', 50)
    transaction.input['signature'] = Wallet().generate_signature(transaction.output)
    with pytest.raises(Exception, match='Invalid signature'):
        Transaction.is_valid_transaction(transaction)



