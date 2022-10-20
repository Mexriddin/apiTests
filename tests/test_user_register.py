import pytest
import allure

from utils.base_case import BaseCase
from utils.assertions import Assertions
from utils.my_requests import MyRequests


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    @allure.title("Positive test registration user")
    @allure.description("This test successfully registrate user by valid fields")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="id")

    @allure.title("Negative test registration user with existing email")
    @allure.description("This test checks registration status and content with sending existing email")
    @pytest.mark.negative
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        Assertions.assert_content(response=response, expected_content=f"Users with email '{email}' already exists",
                                  error_message=f"Unexpected response content {response.content}")

    @allure.title("Negative test registration user with invalid email")
    @allure.description("This test checks registration status and content with sending email without letter '@'")
    @pytest.mark.negative
    def test_create_user_with_invalid_email(self):
        invalid_email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email=invalid_email)
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        Assertions.assert_content(response=response, expected_content="Invalid email format",
                                  error_message=f"Unexpected response content {response.content}")

    @allure.title("Negative test registration user without specifying one of the fields")
    @allure.description("This test checks registration status and content with sending without "
                        "specifying one of the fields")
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
        Assertions.assert_content(response=response,
                                  expected_content=f"The following required params are missed: {without_field}",
                                  error_message=f"Unexpected response content {response.content}")

    @allure.title("Negative test registration user with invalid username")
    @allure.description("This test checks registration status and content with sending invalid username")
    @pytest.mark.negative
    @pytest.mark.parametrize("username,error_message", [
        ('a', "The value of 'username' field is too short"),
        (BaseCase.max_length_name(), "The value of 'username' field is too long")],
                             ids=['min length name', 'max length name'])
    def test_create_user_with_invalid_username(self, username, error_message):
        data = self.prepare_invalid_username_data(username=username)
        response = MyRequests.post(path="/user/", data=data)
        Assertions.assert_code_status(response=response, expected_status_code=400)
        Assertions.assert_content(response=response, expected_content=f"{error_message}",
                                  error_message=f"Unexpected response content {response.content}")