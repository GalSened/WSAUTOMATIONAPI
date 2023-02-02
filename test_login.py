import unittest
import warnings
from pathlib import Path
from time import sleep
import json
from status_codes import StatusCode
from status_codes import ResultCode
import pytest
from all_api_methods import WesignMethodsApi

@pytest.mark.flaky(max_runs=3)
class WesignApiLoginTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('settings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)

    def test_login_success(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestSuccess')
        assert r.status_code == StatusCode.OK
        login = json.loads(r.content)
        return login['token']

    def test_login_invalid_password(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestInvalidPassword')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        status_response = r.json()['status']
        assert status_response == ResultCode.INVALID_CREDENTIAL[0]
        assert json_response[0] == ResultCode.INVALID_CREDENTIAL[1]

    def test_login_invalid_email(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestInvalidEmail')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        status_response = r.json()['status']
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_VALID_EMAIL

    def test_login_empty_email(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestEmptyEmail')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        status_response = r.json()['status']
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_AN_EMAIL
        assert json_response[1] == ResultCode.PLEASE_SPECIFY_A_VALID_EMAIL

    def test_login_empty_email_empty_password(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestEmptyEmailEmptyPassword')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        status_response = r.json()['status']
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_AN_EMAIL
        assert json_response[1] == ResultCode.PLEASE_SPECIFY_A_VALID_EMAIL

    def tearDown(self):
        sleep(3)

    if __name__ == "__main__":
        unittest.main()

