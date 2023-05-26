import allure

from helpers.user_helper import UserHelper


@allure.testcase('5.1 User can send money to other user.')
def test_send_amount(new_user_with_balance):
    user2_email = 'secondUser@email.com'
    user = UserHelper()
    user.create_user(user2_email, password='Qwerty1!')
    sent = user.send_money(receiver=user2_email, amount=15, sender=new_user_with_balance)
    with allure.step('Check status code is 200'):
        assert sent.status_code == 200
    user2_balance = user.get_balance(user2_email)
    with allure.step('Check balance is 15.0'):
        assert user2_balance.json().get('balance') == 15.0


@allure.testcase('5.2 Not registered user can\'t send money.')
def test_send_amount_from_non_exiting_account(new_user_with_balance):
    non_existent_email = 'nonExistent@email.com'
    user = UserHelper()
    sent = user.send_money(receiver=new_user_with_balance, amount=15, sender=non_existent_email)
    with allure.step('Check status code is 404'):
        assert sent.status_code == 404
    user_balance = user.get_balance(new_user_with_balance)
    with allure.step('Check balance is 100.0'):
        assert user_balance.json().get('balance') == 100.0


@allure.testcase('5.3 User can\'t send money to unregistered email.')
def test_send_amount_to_unregistered_account(new_user_with_balance):
    user2_email = 'fakeUser@email.com'
    user = UserHelper()
    sent = user.send_money(receiver=user2_email, amount=15, sender=new_user_with_balance)
    with allure.step('Check status code is 404'):
        assert sent.status_code == 404
    user_balance = user.get_balance(new_user_with_balance)
    with allure.step('Check balance is 100.0'):
        assert user_balance.json().get('balance') == 100.0
