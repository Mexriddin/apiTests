import json.decoder
from datetime import datetime
import random
import string

from requests import Response


class BaseCase:
    data = {
        'password': '1234',
        'username': 'learnqa',
        'firstName': 'learnqa',
        'lastName': 'learnqa',
        'email': 'learqa@example.com'
    }

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Cannot find header with name {header_name} in the last response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "examole.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        data_ex = self.data.copy()
        data_ex['email'] = email
        return data_ex

    def prepare_invalid_registration_data(self, invalid_field):
        data_ex = self.data.copy()
        if invalid_field in self.data.keys():
            del data_ex[invalid_field]
        else:
            raise Exception(f"'{invalid_field}' field not have")
        return data_ex

    def prepare_invalid_username_data(self, username):
        data_ex = self.data.copy()
        data_ex["username"] = username
        return data_ex

    @staticmethod
    def max_length_name():
        name = ''.join([random.choice(string.ascii_lowercase + string.digits) for i in range(255)])
        return name
