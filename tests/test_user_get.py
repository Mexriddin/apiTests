from utils.my_requests import MyRequests
from utils.base_case import BaseCase
from utils.assertions import Assertions


class TestUserGet(BaseCase):
    def test_get_user_detail_not_auth(self):
        response = MyRequests.get(path="/user/2")

        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_key(response=response, name="username")
        Assertions.assert_json_has_not_keys(response=response, names=unexpected_fields)

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post(path="/user/login", data=data)
        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(path=f"/user/{user_id_from_auth_method}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid})
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response=response2, names=expected_fields)
