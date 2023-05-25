import logging
import pytest
import subprocess
import time

from helpers.user_helper import UserHelper

log = logging.getLogger(__name__)


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
    log.info('Server started')
    yield mock_proc
    # Shut it down at the end of the pytest session
    log.info('Terminating server')
    mock_proc.terminate()


@pytest.fixture(scope="function")
def new_user():
    email = f'{time.time()}@email.com'
    log.info(f'Creating a new user: {email}')
    user = UserHelper()
    user.create_user(email, 'Qwerty1!')
    yield email


@pytest.fixture(scope="function")
def new_user_with_balance():
    email = f'{time.time()}@email.com'
    log.info(f'Creating new_user_with_balance: {email}')
    user = UserHelper()
    user.create_user(email, 'Qwerty1!')
    user.deposit_balance(email, 100)
    yield email
