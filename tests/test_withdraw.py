import allure

from helpers.user_helper import UserHelper


@allure.testcase('3.1 User can withdraw money with valid amount.')
def test_withdraw(new_user_with_balance):
    user = UserHelper()
    withdraw = user.withdraw_money(new_user_with_balance, 25)
    with allure.step('Check status code is 200'):
        assert withdraw.status_code == 200
    balance = user.get_balance(new_user_with_balance)
    with allure.step('Check balance is 75.0'):
        assert balance.json().get('balance') == 75.0


@allure.testcase('3.2 User can\'t withdraw if amount is negative.')
def test_withdraw_negative_amount(new_user_with_balance):
    user = UserHelper()
    withdraw = user.withdraw_money(new_user_with_balance, -15)
    with allure.step('Check status code is 400'):
        assert withdraw.status_code == 400
    balance = user.get_balance(new_user_with_balance)
    with allure.step('Check balance hasn\'t changed, 100.0'):
        assert balance.json().get('balance') == 100.0


@allure.testcase('3.3 User can\'t withdraw if balance is 0.')
def test_withdraw_with_empty_balance(new_user):
    user = UserHelper()
    withdraw = user.withdraw_money(new_user, 25)
    with allure.step('Check status code is 400'):
        assert withdraw.status_code == 400
    balance = user.get_balance(new_user)
    with allure.step('Check balance hasn\'t changed is 0.0'):
        assert balance.json().get('balance') == 0.0



@allure.testcase('3.4 User with invalid email can\'t withdraw money.')
def test_withdraw_with_invalid_email(new_user_with_balance):
    user = UserHelper()
    withdraw = user.withdraw_money(new_user_with_balance[1:], 25)
    with allure.step('Check status code is 404'):
        assert withdraw.status_code == 404
    balance = user.get_balance(new_user_with_balance)
    with allure.step('Check similar account balance hasn\'t changed, 100.0'):
        assert balance.json().get('balance') == 100.0
