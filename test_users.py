import unittest
import warnings
from pathlib import Path
import pytest
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode

@pytest.mark.flaky(max_runs=3)
class WesignApiUsersTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('UsersSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_create_new_basic_user_success(self):
        r = self.__api_create_user_request('CreateNewBasicUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_user_id = response['userId']
        assert len(json_response_user_id) > 0
        self.__api_delete_user_request(json_response_user_id)

    def test_create_new_editor_user_success(self):
        r = self.__api_create_user_request('CreateNewEditorUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_user_id = response['userId']
        assert len(json_response_user_id) > 0
        self.__api_delete_user_request(json_response_user_id)

    def test_create_new_admin_user_success(self):
        r = self.__api_create_user_request('CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_user_id = response['userId']
        assert len(json_response_user_id) > 0
        self.__api_delete_user_request(json_response_user_id)

    def test_create_new_user_with_invalid_user_type(self):
        r = self.__api_create_user_request('CreateNewUserInvalidUserTypeRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Type']
        assert json_response[0] == ResultCode.INVALID_USER_TYPE


    if __name__ == "__main__":
        unittest.main()

    def __api_create_user_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'admins/users', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_delete_user_request(self, user_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'admins/users/' + user_id, headers=headers)
        return r
