import allure

from helpers.user_helper import UserHelper


@allure.testcase('4.1 Registered user can get his balance with an email.')
def test_get_balance(new_user_with_balance):
    user = UserHelper()
    balance = user.get_balance(new_user_with_balance)
    with allure.step('Check balance is 100.0'):
        assert balance.json().get('balance') == 100.0
