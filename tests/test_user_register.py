import pytest

from utils.base_case import BaseCase
from utils.assertions import Assertions
from utils.my_requests import MyRequests


class TestUserRegister(BaseCase):
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="id")

    @pytest.mark.negative
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content {response.content} "

    @pytest.mark.negative
    def test_create_user_with_invalid_email(self):
        invalid_email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email=invalid_email)
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content {response.content} "

    @pytest.mark.negative
    @pytest.mark.parametrize("without_field", BaseCase.data.keys(), ids=[
        'without password',
        'without username',
        'without firstName',
        'without lastName',
        'without email'])
    def test_create_user_without_field(self, without_field):
        data = self.prepare_invalid_registration_data(without_field)
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {without_field}", \
            f"Unexpected response content {response.content} "

    @pytest.mark.negative
    @pytest.mark.parametrize("username,error_message", [
        ('a', "The value of 'username' field is too short"),
        (BaseCase.max_length_name(), "The value of 'username' field is too long")],
                             ids=['min length name', 'max length name'])
    def test_create_user_with_invalid_username(self, username, error_message):
        data = self.prepare_invalid_username_data(username=username)
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"{error_message}", \
            f"Unexpected response content {response.content} "

