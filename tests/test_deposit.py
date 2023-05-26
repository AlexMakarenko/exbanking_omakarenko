import allure

from helpers.user_helper import UserHelper
    

@allure.testcase('2.1 User can deposit his balance.')
def test_deposit(new_user):
    user = UserHelper()
    deposit = user.deposit_balance(new_user, 100)
    with allure.step('Check status code is 200'):
        assert deposit.status_code == 200
    balance = user.get_balance(new_user)
    with allure.step('Check balance is 100.0'):
        assert balance.json().get('balance') == 100.0


@allure.testcase('2.2 Deposit amount can not be negative.')
def test_deposit_negative_amount(new_user_with_balance):
    user = UserHelper()
    deposit = user.deposit_balance(new_user_with_balance, -50)
    with allure.step('Check status code is 400'):
        assert deposit.status_code == 400
    balance = user.get_balance(new_user_with_balance)
    with allure.step('Check balance is not changed: 100.0'):
        assert balance.json().get('balance') == 100.0


@allure.testcase('2.3 Only existing user can deposit the balance.')
def test_deposit_without_account(new_user_with_balance):
    user = UserHelper()
    not_existing_email = 'notRegistered@email.ee'
    deposit = user.deposit_balance(not_existing_email, 1500)
    with allure.step('Check status code is 404'):
        assert deposit.status_code == 404
    with allure.step('Verify the error message is User not found'):
        assert deposit.json().get('detail') == 'User not found'

