import allure

from helpers.user_helper import UserHelper


@allure.testcase('1.1 User is created with valid email and password.')
def test_create_user(mock_server):
    user = UserHelper()
    user_email = 'test@email.com'
    response = user.create_user(email=user_email, password='Qwerty1!')
    with allure.step('Check status code is 200'):
        assert response.status_code == 200
    balance = user.get_balance(user_email)
    with allure.step('Check balance is 0.0'):
        assert balance.json().get('balance') == 0.0


@allure.testcase('1.2 User is not created with email missing @.')
def test_create_user_with_invalid_email(mock_server):
    user = UserHelper()
    user_email = 'testemail.com'
    response = user.create_user(email=user_email, password='Qwerty1!')
    with allure.step('Check status code is 400'):
        assert response.status_code == 400
    with allure.step('Check error message is Invalid email'):
        assert response.json().get('detail') == 'Invalid email'
    balance = user.get_balance(user_email)
    with allure.step('Check error message is User not found'):
        assert balance.json().get('detail') == 'User not found'


@allure.testcase('1.3 User is not created with empty email.')
def test_create_user_with_empty_email(mock_server):
    user = UserHelper()
    user_email = ''
    response = user.create_user(email=user_email, password='Qwerty1!')
    with allure.step('Check status code is 400'):
        assert response.status_code == 400
    with allure.step('Check error message is Email is empty'):
        assert response.json().get('detail') == 'Email is empty'


@allure.testcase('1.4 User is not created if password empty.')
def test_create_user_with_empty_password(mock_server):
    user = UserHelper()
    user_email = 'emptyPassword@email.com'
    response = user.create_user(email=user_email, password='')
    with allure.step('Check status code is 400'):
        assert response.status_code == 400
    with allure.step('Check error message is Minimum length of password is 8 symbols'):
        assert response.json().get('detail') == 'Minimum length of password is 8 symbols'


@allure.testcase('1.5 User is not created if password has less than 8 symbols.')
def test_create_user_with_short_password(mock_server):
    user = UserHelper()
    user_email = 'shortPassword@email.com'
    response = user.create_user(email=user_email, password='Qwerty1')
    with allure.step('Check status code is 400'):
        assert response.status_code == 400
    with allure.step('Check error message is Minimum length of password is 8 symbols'):
        assert response.json().get('detail') == 'Minimum length of password is 8 symbols'
