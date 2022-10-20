import pytest
from utils.base_case import BaseCase
from utils.assertions import Assertions
from utils.my_requests import MyRequests
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookies"),
        ("no_token")
    ]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response1 = MyRequests.post(path="/user/login", data=data)
        self.auth_sid = self.get_cookie(response=response1, cookie_name="auth_sid")
        self.token = self.get_header(response=response1, header_name="x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response=response1, name="user_id")

    @allure.title("Positive test authorization user")
    @allure.description("This test successfully authorize user by email and password")
    @pytest.mark.authorization
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_auth_user(self):
        response2 = MyRequests.get(path="/user/auth",
                                   headers={"x-csrf-token": self.token},
                                   cookies={"auth_sid": self.auth_sid}
                                   )
        Assertions.assert_json_value_by_name(
            response=response2,
            name="user_id",
            expected_value=self.user_id_from_auth_method,
            error_message="User id from auth method is not equal to user_id from check method"
        )

    @allure.title("Negative test authorization")
    @allure.description("This test checks authorization status without sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    @pytest.mark.authorization
    @pytest.mark.negative
    def test_negative_auth_check(self, condition):

        if condition == "no_cookies":
            response2 = MyRequests.get(path="/user/auth",
                                       headers={"x-csrf-token": self.token}
                                       )
        else:
            response2 = MyRequests.get(path="/user/auth",
                                       cookies={"auth_sid": self.auth_sid}
                                       )

        Assertions.assert_json_value_by_name(
            response=response2,
            name="user_id",
            expected_value=0,
            error_message=f"User is authorized with condition {condition}"
        )
