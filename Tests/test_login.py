import unittest
import warnings
from pathlib import Path
from time import sleep
import json
from Enums.status_codes import StatusCode, ResultCode
import pytest
from Common.all_api_methods import WesignMethodsApi
from shared import Shared


@pytest.mark.flaky(max_runs=3)
class WesignApiLoginTests(unittest.TestCase):
    def setUp(self):
        # p = Path(__file__).with_name('settings.json')
        # with open(p) as f:
        #     self.settings = json.load(f)

        p = Path(__file__).resolve().parent.parent
        file_path = p / "Settings\\settings.json"
        with open(file_path) as f:
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
        assert json_response[0] == ResultCode.INVALID_CREDENTIAL

    def test_login_invalid_email(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestInvalidEmail')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        status_response = r.status_code
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.INVALID_CREDENTIAL

    def test_login_empty_email(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestEmptyEmail')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        status_response = r.json()['status']
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_AN_EMAIL
        assert json_response[1] == ResultCode.MINIMUN_LENGTH_OF_EMAIL_OR_USERNAME

    def test_login_empty_email_empty_password(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestEmptyEmailEmptyPassword')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        status_response = r.json()['status']
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_AN_EMAIL
        assert json_response[1] == ResultCode.MINIMUN_LENGTH_OF_EMAIL_OR_USERNAME

    def tearDown(self):
        sleep(3)

    if __name__ == "__main__":
        unittest.main()

