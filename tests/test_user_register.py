from utils.base_case import BaseCase
from utils.assertions import Assertions
from utils.my_requests import MyRequests


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content} "
