import requests
import unittest

class TestSignIn(unittest.TestCase):
    def test_sign_in(self):
        url = "https://www.nktoolbox.com/app/account/signin"

        headers = {
            "content-type": "application/json",
            "Authorization": "Basic dXNlckBnbWFpbC5jb206QFVzZXIxMjM0"
        }

        test_profile = {'userType': 'consumer', 'uuid': 'a39c35b7-78fd-4be4-8b6f-b3417dc2b4f9', 'username': 'user@gmail.com', 'email': 'user@gmail.com', 'firstName': 'William', 'lastName': 'Bart', 'phone': '+91112345677899', 'address': 'Main street', 'area': 'Downtown', 'city': 'San Jose', 'appointments': []}
        resp = requests.get(url, headers=headers)

        if resp:
            body = resp.json()
            print(body)
            received_profile = body["data"]["profile"]
            self.assertEqual(True, received_profile == test_profile)


unittest.main()
