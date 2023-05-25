import pytest, allure

from helpers.user_helper import UserHelper


@allure.testcase('User is created with valid email and password.')
def test_create_user():
    user = UserHelper()
    user_email = 'test@email.com'
    response = user.create_user(email=user_email, password='Qwerty1!')
    with allure.step('Check status code is 200'):
        assert response.status_code == 200
    balance = user.get_balance(user_email)
    with allure.step('Check balance is 0.0'):
        assert balance.json().get('balance') == 0.0
    

@allure.testcase('User can deposit his balance.')
def test_deposit(new_user):
    user = UserHelper()
    deposit = user.deposit_balance(new_user, 100)
    with allure.step('Check status code is 200'):
        assert deposit.status_code == 200
    balance = user.get_balance(new_user)
    with allure.step('Check balance is 100.0'):
        assert balance.json().get('balance') == 100.0


@allure.testcase('User can withdraw money with valid amount.')
def test_withdraw(new_user_with_balance):
    user = UserHelper()
    withdraw = user.withdraw_money(new_user_with_balance, 25)
    with allure.step('Check status code is 200'):
        assert withdraw.status_code == 200
    balance = user.get_balance(new_user_with_balance)
    with allure.step('Check balance is 75.0'):
        assert balance.json().get('balance') == 75.0


@allure.testcase('Registered user can get his balance with an email.')
def test_get_balance(new_user_with_balance):
    user = UserHelper()
    balance = user.get_balance(new_user_with_balance)
    with allure.step('Check balance is 100.0'):
        assert balance.json().get('balance') == 100.0


@allure.testcase('User can send money to other user.')
def test_send_amount(new_user_with_balance):
    user2_email = 'test2@email.com'
    user = UserHelper()
    user.create_user(user2_email, password='Qwerty1!')
    sent = user.send_money(receiver=user2_email, amount=15, sender=new_user_with_balance)
    with allure.step('Check status code is 200'):
        assert sent.status_code == 200
    user2_balance = user.get_balance(user2_email)
    with allure.step('Check balance is 15.0'):
        assert user2_balance.json().get('balance') == 15.0
