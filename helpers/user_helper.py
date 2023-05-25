import requests
import json
import logging
import allure

from helpers.http_client import HttpClient


BASE_URL = "http://127.0.0.1:8041"
log = logging.getLogger(__name__)


class UserHelper(HttpClient):

    @allure.step('/create-user')
    def create_user(self, email, password):
        api_url = f'{BASE_URL}/create-user'
        headers = {'Content-Type': 'application/json'}
        payload = {"email": email,"password": password}
        return self.send_post(url=api_url, headers=headers, data=payload)

    @allure.step('/deposit')
    def deposit_balance(self, email, amount):
        api_url = f'{BASE_URL}/deposit'
        headers = {'Content-Type': 'application/json'}
        payload = {"email": email, "amount": amount}
        return self.send_post(url=api_url, headers=headers, data=payload)

    @allure.step('/withdraw')
    def withdraw_money(self, email, amount):
        api_url = f'{BASE_URL}/withdraw'
        headers = {'Content-Type': 'application/json'}
        payload = {"email": email, "amount": amount}
        return self.send_post(url=api_url, headers=headers, data=payload)

    @allure.step('/get-balance')
    def get_balance(self, email):
        api_url = f'{BASE_URL}/get-balance'
        headers = {'Content-Type': 'application/json'}
        payload = {"email": email}
        return self.send_get(url=api_url, headers=headers, data=payload)

    @allure.step('/send')
    def send_money(self, receiver, amount, sender):
        api_url = f'{BASE_URL}/send'
        headers = {'Content-Type': 'application/json'}
        payload = {"email": sender, "receiver_email": receiver, "amount": amount}
        return self.send_post(url=api_url, headers=headers, data=payload)
