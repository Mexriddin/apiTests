import datetime
import requests
from datetime import datetime
from utils.base_case import BaseCase
from utils.assertions import Assertions


class TestUserRegister(BaseCase):

    def setup(self):
        base_part = "learnqa"
        domain = "examole.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content} "


