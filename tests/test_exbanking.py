import pytest

from tests.user_helper import UserHelper


def test_create_user():
    user = UserHelper(email='test@email.com')
    response = user.create_user('Qwerty1!').response
    assert response.status_code == 200
    balance = user.get_balance().response
    assert balance.json().get('balance') == 0.0
    
    
def test_deposit(new_user):
    deposit = new_user.deposit_balance(100).response
    assert deposit.status_code == 200
    balance = new_user.get_balance().response
    assert balance.json().get('balance') == 100.0


def test_withdraw(new_user_with_balance):
    withdraw = new_user_with_balance.withdraw_money(25).response
    assert withdraw.status_code == 200
    balance = new_user_with_balance.get_balance().response
    assert balance.json().get('balance') == 75.0


def test_get_balance(new_user_with_balance):
    balance = new_user_with_balance.get_balance().response
    assert balance.json().get('balance') == 100.0


def test_send_amount(new_user_with_balance):
    user2 = UserHelper(email='test2@email.com')
    user2.create_user(password='Qwerty1!')
    sent = new_user_with_balance.send_money(receiver=user2.email, amount=15).response
    assert sent.status_code == 200
    user2_balance = user2.get_balance().response
    assert user2_balance.json().get('balance') == 15.0
