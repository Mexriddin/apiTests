import requests


class MyRequests():
    @staticmethod
    def post(path: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(path, "POST", data, headers, cookies)

    @staticmethod
    def get(path: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(path, "GET", data, headers, cookies)

    @staticmethod
    def put(path: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(path, "PUT", data, headers, cookies)

    @staticmethod
    def delete(path: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(path, "DELETE", data, headers, cookies)

    @staticmethod
    def _send(path: str, method: str, data: dict, headers: dict, cookies: dict):

        url = f"https://playground.learnqa.ru/api{path}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

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
        return response
