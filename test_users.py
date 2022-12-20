import unittest
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode
from all_api_methods import WesignMethodsApi

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
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewBasicUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_user_id = response['userId']
        assert len(json_response_user_id) > 0
        WesignMethodsApi.admins_users_id_delete(self, json_response_user_id)

    def test_create_new_editor_user_success(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewEditorUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_user_id = response['userId']
        assert len(json_response_user_id) > 0
        WesignMethodsApi.admins_users_id_delete(self, json_response_user_id)

    def test_create_new_admin_user_success(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_user_id = response['userId']
        assert len(json_response_user_id) > 0
        WesignMethodsApi.admins_users_id_delete(self, json_response_user_id)

    def test_create_new_user_with_invalid_user_type(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewUserInvalidUserTypeRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Type']
        assert json_response[0] == ResultCode.INVALID_USER_TYPE

    def test_create_new_user_with_empty_name(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewUserWhitEmptyNameRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.EMPTY_NAME

    def test_create_new_user_with_invalid_email(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewUserWhitInvalidEmailRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_VALID_EMAIL

    def test_create_new_user_with_invalid_group_id(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewUserWhitInvalidGroupIdRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.INVALID_GROUP_ID

    def test_get_all_users_in_company_success(self):
        r = WesignMethodsApi.admins_users_get(self)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['users'][0]['id'] + ' ' + response['users'][1]['id']
        assert len(json_response) > 0 and len(json_response) == 73

    def test_update_existing_user_name_success(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['userId']
        r = WesignMethodsApi.admins_users_id_put_json_file(self, 'UpdateUserNameRequest', json_response)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.admins_users_id_delete(self, json_response)

    def test_update_existing_user_email_success(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['userId']
        r = WesignMethodsApi.admins_users_id_put_json_file(self, 'UpdateUserEmailRequest', json_response)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.admins_users_id_delete(self, json_response)

    def test_update_existing_user_to_basic_user_success(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['userId']
        r = WesignMethodsApi.admins_users_id_put_json_file(self, 'UpdateUserToBasicRequest', json_response)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.admins_users_id_delete(self, json_response)

    def test_update_existing_user_to_editor_user_success(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['userId']
        r = WesignMethodsApi.admins_users_id_put_json_file(self, 'UpdateUserToEditorRequest', json_response)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.admins_users_id_delete(self, json_response)

    def test_update_existing_user_empty_name(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_id = response['userId']
        r = WesignMethodsApi.admins_users_id_put_json_file(self, 'UpdateUserEmptyNameRequest', json_response_id)
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.EMPTY_NAME
        WesignMethodsApi.admins_users_id_delete(self, json_response_id)

    def test_update_existing_user_empty_email(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_id = response['userId']
        r = WesignMethodsApi.admins_users_id_put_json_file(self, 'UpdateUserEmptyEmailRequest', json_response_id)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_VALID_EMAIL
        WesignMethodsApi.admins_users_id_delete(self, json_response_id)

    ##Bug number = WES-981
    def test_update_existing_user_invalid_group_id(self):
        r = WesignMethodsApi.admins_users_post_json_file(self, 'CreateNewAdminUserRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_id = response['userId']
        r = WesignMethodsApi.admins_users_id_put_json_file(self, 'UpdateUserInvalidGroupIdRequest', json_response_id)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.INVALID_GROUP_ID
        WesignMethodsApi.admins_users_id_delete(self, json_response_id)


    def tearDown(self):
        sleep(1)

    if __name__ == "__main__":
        unittest.main()

