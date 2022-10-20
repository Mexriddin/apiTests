import pytest
import allure

from utils.base_case import BaseCase
from utils.assertions import Assertions
from utils.my_requests import MyRequests


@allure.epic("User edit cases")
class TestUserEdit(BaseCase):

    def setup(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post(path="/user/", data=register_data)

        Assertions.assert_code_status(response=response, expected_status_code=200)
        Assertions.assert_json_has_key(response=response, name="id")

        email = register_data["email"]
        password = register_data["password"]
        self.user_id = self.get_json_value(response=response, name="id")

        self.login_data = {
            "email": email,
            "password": password
        }

    def teardown(self):
        # LOGIN
        response1 = MyRequests.post(path="/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response=response1, cookie_name="auth_sid")
        token = self.get_header(response=response1, header_name="x-csrf-token")

        # DELETE
        response2 = MyRequests.delete(path=f'/user/{self.user_id}',
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response=response2, expected_status_code=200)

    @allure.title("Positive test edit created user")
    @allure.description("This test successfully edit created user by valid fields")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_edit_just_created_user(self):
        # LOGIN
        response1 = MyRequests.post(path="/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response=response1, cookie_name="auth_sid")
        token = self.get_header(response=response1, header_name="x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response2 = MyRequests.put(
            path=f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response=response2, expected_status_code=200)

        # GET
        response3 = MyRequests.get(
            path=f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(response=response3,
                                             name="firstName",
                                             expected_value=new_name,
                                             error_message="Wrong name of the user after edit")

    @allure.title("Negative test edit created user without authorization")
    @allure.description("This test checks status code and content without authorize")
    @pytest.mark.negative
    def test_edit_just_created_user_not_auth(self):
        # EDIT
        last_name = "Changed Name"
        response = MyRequests.put(
            path=f"/user/{self.user_id}",
            data={"lastName": last_name}
        )
        Assertions.assert_code_status(response=response, expected_status_code=400)
        Assertions.assert_content(response=response, expected_content="Auth token not supplied",
                                  error_message=f"Unexpected response content {response.content}")

    @allure.title("Negative test edit created user while being authorized by another user")
    @allure.description("This test checks status code and content while being authorized by another user")
    @pytest.mark.negative
    @pytest.mark.skip
    def test_edit_other_user_auth_as_same_user(self):
        # LOGIN
        response1 = MyRequests.post(path="/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response=response1, cookie_name="auth_sid")
        token = self.get_header(response=response1, header_name="x-csrf-token")
        # EDIT
        username = "qwerty"
        response2 = MyRequests.put(
            path=f"/user/46600",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"username": username}
        )
        Assertions.assert_code_status(response=response2, expected_status_code=200)

        # GET
        response3 = MyRequests.get(
            path=f"/user/46600",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(response=response3,
                                             name="username",
                                             expected_value=username,
                                             error_message="Wrong name of the user after edit")

    @allure.title("Negative test edit created user 'email' being authorized by the same user")
    @allure.description("This test checks status code and content being authorized "
                        "by the same user with sending email without letter '@'")
    @pytest.mark.negative
    def test_edit_email_user_auth_same_user(self):
        # LOGIN
        response1 = MyRequests.post(path="/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response=response1, cookie_name="auth_sid")
        token = self.get_header(response=response1, header_name="x-csrf-token")

        # EDIT
        email = "qalearnexample.com"
        response2 = MyRequests.put(
            path=f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": email}
        )
        Assertions.assert_code_status(response=response2, expected_status_code=400)
        Assertions.assert_content(response=response2, expected_content="Invalid email format",
                                  error_message=f"Unexpected response content {response2.content}")

    @allure.title("Negative test edit created user 'firstName' being authorized by the same user")
    @allure.description("This test checks status code and error message being authorized "
                        "by the same user with with sending invalid 'firstName'")
    @pytest.mark.negative
    def test_edit_firstName_user_auth_same_user(self):
        # LOGIN
        response1 = MyRequests.post(path="/user/login", data=self.login_data)
        auth_sid = self.get_cookie(response=response1, cookie_name="auth_sid")
        token = self.get_header(response=response1, header_name="x-csrf-token")

        # EDIT
        firstName = "a"
        response2 = MyRequests.put(
            path=f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": firstName}
        )
        Assertions.assert_code_status(response=response2, expected_status_code=400)
        Assertions.assert_json_value_by_name(response=response2,
                                             name="error",
                                             expected_value="Too short value for field firstName",
                                             error_message=f"Unexpected response content")
