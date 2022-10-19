import requests
import allure
from utils.logger import Logger
from environment import ENV_OBJECT


class MyRequests:
    @staticmethod
    def post(path: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to URL '{path}'"):
            return MyRequests._send(path, "POST", data, headers, cookies)

    @staticmethod
    def get(path: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to URL '{path}'"):
            return MyRequests._send(path, "GET", data, headers, cookies)

    @staticmethod
    def put(path: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request to URL '{path}'"):
            return MyRequests._send(path, "PUT", data, headers, cookies)

    @staticmethod
    def delete(path: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to URL '{path}'"):
            return MyRequests._send(path, "DELETE", data, headers, cookies)

    @staticmethod
    def _send(path: str, method: str, data: dict, headers: dict, cookies: dict):
        url = f"{ENV_OBJECT.get_base_url()}{path}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, method, data, headers, cookies)

        if method == "GET":
            response = requests.get(url, params=data, cookies=cookies, headers=headers)
        elif method == "POST":
            response = requests.post(url, data=data, cookies=cookies, headers=headers)
        elif method == "PUT":
            response = requests.put(url, data=data, cookies=cookies, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, data=data, cookies=cookies, headers=headers)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response)

        return response
