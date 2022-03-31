import unittest
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode

@pytest.mark.flaky(max_runs=5)
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

    def test_create_new_user_with_empty_name(self):
        r = self.__api_create_user_request('CreateNewUserWhitEmptyNameRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.EMPTY_NAME

    def test_create_new_user_with_invalid_email(self):
        r = self.__api_create_user_request('CreateNewUserWhitInvalidEmailRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_VALID_EMAIL

    def test_create_new_user_with_invalid_group_id(self):
        r = self.__api_create_user_request('CreateNewUserWhitInvalidGroupIdRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.INVALID_GROUP_ID

    def test_get_all_users_in_company_success(self):
        r = self.__api_get_user_request()
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['users'][0]['id'] + ' ' + response['users'][1]['id']
        assert len(json_response) > 0 and len(json_response) == 73

    def test_update_existing_user_name_success(self):
        r = self.__api_create_user_request('CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['userId']
        r = self.__update_user_request('UpdateUserNameRequest', json_response)
        assert r.status_code == StatusCode.OK
        self.__api_delete_user_request(json_response)

    def test_update_existing_user_email_success(self):
        r = self.__api_create_user_request('CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['userId']
        r = self.__update_user_request('UpdateUserEmailRequest', json_response)
        assert r.status_code == StatusCode.OK
        self.__api_delete_user_request(json_response)

    def test_update_existing_user_to_basic_user_success(self):
        r = self.__api_create_user_request('CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['userId']
        r = self.__update_user_request('UpdateUserToBasicRequest', json_response)
        assert r.status_code == StatusCode.OK
        self.__api_delete_user_request(json_response)

    def test_update_existing_user_to_editor_user_success(self):
        r = self.__api_create_user_request('CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['userId']
        r = self.__update_user_request('UpdateUserToEditorRequest', json_response)
        assert r.status_code == StatusCode.OK
        self.__api_delete_user_request(json_response)

    def test_update_existing_user_empty_name(self):
        r = self.__api_create_user_request('CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_id = response['userId']
        r = self.__update_user_request('UpdateUserEmptyNameRequest', json_response_id)
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.EMPTY_NAME
        self.__api_delete_user_request(json_response_id)

    def test_update_existing_user_empty_email(self):
        r = self.__api_create_user_request('CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_id = response['userId']
        r = self.__update_user_request('UpdateUserEmptyEmailRequest', json_response_id)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_VALID_EMAIL
        self.__api_delete_user_request(json_response_id)

    ##Bug number = WES-981
    def test_update_existing_user_invalid_group_id(self):
        r = self.__api_create_user_request('CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_id = response['userId']
        r = self.__update_user_request('UpdateUserInvalidGroupIdRequest', json_response_id)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.INVALID_GROUP_ID
        self.__api_delete_user_request(json_response_id)


    def tearDown(self):
        sleep(4)

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

    def __api_get_user_request(self):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'admins/users', headers=headers)
        return r

    def __update_user_request(self, request_file, user_id):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'admins/users/' + user_id, data=json.dumps(requests_json),
                         headers=headers)
        return r
