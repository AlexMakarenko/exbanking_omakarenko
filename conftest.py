import pytest
import subprocess
import time

from tests.user_helper import UserHelper


@pytest.fixture(autouse=True, scope="session")
def mock_server():
    mock_proc = subprocess.Popen(
        [
            'uvicorn', 
            'app.exbanking_mock_server:app',
            '--host',
            '127.0.0.1',
            '--port',
            '8041'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    # Give the server time to start
    time.sleep(2)
    # Check it started successfully
    assert not mock_proc.poll(), mock_proc.stdout.read().decode("utf-8")
    yield mock_proc
    # Shut it down at the end of the pytest session
    mock_proc.terminate()


@pytest.fixture(scope="function")
def new_user():
    user = UserHelper(email=f'{time.time()}@email.com')
    user.create_user('Qwerty1!')
    yield user


@pytest.fixture(scope="function")
def new_user_with_balance():
    user = UserHelper(email=f'{time.time()}@email.com')
    user.create_user('Qwerty1!')
    user.deposit_balance(100)
    yield user
