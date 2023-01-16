import requests
import json

BASE_URL = "http://127.0.0.1:8041"


class UserHelper:
    def __init__(self, email, response=None) -> None:
        self.email = email
        self.response = None

    def create_user(self, password):
        api_url = f'{BASE_URL}/create-user'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"email": self.email,"password": password})
        self.response = requests.post(url=api_url, headers=headers, data=payload)
        return self

    def deposit_balance(self, amount):
        api_url = f'{BASE_URL}/deposit'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"email": self.email, "amount": amount})
        self.response = requests.post(url=api_url, headers=headers, data=payload)
        return self

    def withdraw_money(self, amount):
        api_url = f'{BASE_URL}/withdraw'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"email": self.email, "amount": amount})
        self.response = requests.post(url=api_url, headers=headers, data=payload)
        return self

    def get_balance(self):
        api_url = f'{BASE_URL}/get-balance'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"email": self.email})
        self.response = requests.get(url=api_url, headers=headers, data=payload)
        return self

    def send_money(self, receiver, amount):
        api_url = f'{BASE_URL}/send'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"email": self.email, "receiver_email": receiver, "amount": amount})
        self.response = requests.post(url=api_url, headers=headers, data=payload)
        return self
