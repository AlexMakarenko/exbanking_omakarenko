import json, time, logging, allure
import aiohttp
import asyncio
import uuid

from helpers.user_helper import BASE_URL

log = logging.getLogger(__name__)


async def create_user(session, email, password='Qwerty1!'):
    api_url = f'{BASE_URL}/create-user'
    headers = {'Content-Type': 'application/json'}
    payload = json.dumps({"email": email,"password": password})
    log.info(f'POST {api_url} \nHEADERS: {headers} \nPAYLOAD: {payload}')
    async with session.post(url=api_url, data=payload, headers=headers) as response:
        log.info(f'{response.status} {await response.text()}')
        return await response.json()

@allure.step
async def generate_users(amount_of_users):
    new_email = lambda : f'{uuid.uuid4()}@email.com'
    emails = [new_email() for _ in range(amount_of_users)]
    tasks = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        for email in emails:
            tasks.append(create_user(session, email))
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        time_spent = end_time - start_time
        log.info(f'Time spent: {time_spent} seconds')
        for response in responses:
            emails.remove(response.get('email'))
        return emails, time_spent


@allure.testcase('Load test with 100 users creating accounts.')
def test_load_create_user(mock_server):
    loop = asyncio.get_event_loop()
    failed_emails, time_spent = loop.run_until_complete(generate_users(100))
    log.error(failed_emails) if failed_emails else log.info('All emails were registered')
    with allure.step('Check all emails were registered'):
        assert not failed_emails, f'Some emails were not registered.'
    with allure.step('Check time spent is within 2 seconds'):
        assert time_spent <= 2
