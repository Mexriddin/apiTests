import pytest
from utils.base_case import BaseCase
from utils.assertions import Assertions
from utils.my_requests import MyRequests
import allure


@allure.epic("User delete cases")
class TestUserDelete(BaseCase):
    @allure.title("Positive test delete created user")
    @allure.description("This test successfully delete created user by valid fields")
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(path="/user/", data=register_data)

        Assertions.assert_code_status(response=response1, expected_status_code=200)
        Assertions.assert_json_has_key(response=response1, name="id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response=response1, name="id")

        login_data = {
            "email": email,
            "password": password
        }

        # LOGIN
        response2 = MyRequests.post(path="/user/login", data=login_data)
        auth_sid = self.get_cookie(response=response2, cookie_name="auth_sid")
        token = self.get_header(response=response2, header_name="x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(path=f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )
        Assertions.assert_code_status(response=response3, expected_status_code=200)

        # GET
        response4 = MyRequests.get(
            path=f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response=response4, expected_status_code=404)
        Assertions.assert_content(response=response4, expected_content="User not found",
                                  error_message=f"Unexpected response content {response4.content}")

    @allure.title("Negative test delete admin")
    @allure.description("This test check status and content with admin datas")
    @pytest.mark.negative
    def test_delete_user_admin(self):
        # LOGIN
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = MyRequests.post(path="/user/login", data=data)
        auth_sid = self.get_cookie(response=response1, cookie_name="auth_sid")
        token = self.get_header(response=response1, header_name="x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response=response1, name="user_id")
        # DELETE
        response2 = MyRequests.delete(path=f'/user/{user_id_from_auth_method}',
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )
        Assertions.assert_code_status(response=response2, expected_status_code=400)
        Assertions.assert_content(response=response2,
                                  expected_content="Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                                  error_message=f"Unexpected response content {response2.content}")

    @allure.title("Negative test delete created user while being authorized by another user")
    @allure.description("This test checks status code and content while being authorized by another user")
    @pytest.mark.negative
    @pytest.mark.skip
    def test_delete_other_user_auth_as_same_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(path="/user/", data=register_data)

        Assertions.assert_code_status(response=response1, expected_status_code=200)
        Assertions.assert_json_has_key(response=response1, name="id")

        user_id = self.get_json_value(response=response1, name="id")

        # LOGIN
        login_data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = MyRequests.post(path="/user/login", data=login_data)
        auth_sid = self.get_cookie(response=response1, cookie_name="auth_sid")
        token = self.get_header(response=response1, header_name="x-csrf-token")
        # DELETE
        response2 = MyRequests.delete(
            path=f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        print(response2.content)
        Assertions.assert_code_status(response=response2, expected_status_code=400)
