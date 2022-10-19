from utils.base_case import BaseCase
from utils.assertions import Assertions
from utils.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(path="/user/", data=register_data)

        Assertions.assert_code_status(response=response1, expected_status_code=200)
        Assertions.assert_json_has_key(response=response1, name="id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response=response1, name="id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post(path="/user/login", data=login_data)
        auth_sid = self.get_cookie(response=response2, cookie_name="auth_sid")
        token = self.get_header(response=response2, header_name="x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            path=f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response=response3, expected_status_code=200)

        # GET
        response4 = MyRequests.get(
            path=f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_value_by_name(response=response4,
                                             name="firstName",
                                             expected_value=new_name,
                                             error_message="Wrong name of the user after edit")