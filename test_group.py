import unittest
import uuid
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
class WesignApiGroupTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('GroupSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_create_new_group_success(self):
        r = WesignMethodsApi.admins_groups_post_json_file(self, 'CreateNewGroupRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['groupId']
        assert len(json_response) > 0
        WesignMethodsApi.admins_groups_delete(self, f'{json_response}')

    def test_create_same_group_name(self):
        r = WesignMethodsApi.admins_groups_post_json_file(self, 'CreateSameGroupNameRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.GROUP_WITH_SAME_NAME

    def test_create_empty_group_name(self):
        r = WesignMethodsApi.admins_groups_post_json_file(self, 'CreateEmptyGroupNameRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.EMPTY_NAME

    def test_update_group_name_success(self):
        group = uuid.uuid4().hex
        self.group_name = group
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\CreateGroup\\CreateNewGroupRequest.json",'r+') as f:
            data = json.load(f)
            data['name'] = self.group_name  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = WesignMethodsApi.admins_groups_post_json_file(self, 'CreateNewGroupRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['groupId']
        assert len(json_response) > 0
        r = WesignMethodsApi.admins_groups_put_json_file(self, 'ChangeGroupNameRequest', json_response)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.admins_groups_delete(self, f'{json_response}')

    def test_get_all_groups_success(self):
        r = WesignMethodsApi.admins_groups_get(self)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_group_id = response['groups'][0]['groupId']
        json_response_group_name = response['groups'][0]['name']
        assert json_response_group_id == self.settings['GroupID']
        assert json_response_group_name == 'api testing'

    def test_delete_group_success(self):
        r = WesignMethodsApi.admins_groups_post_json_file(self, 'CreateNewGroupRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['groupId']
        assert len(json_response) > 0
        WesignMethodsApi.admins_groups_delete(self, f'{json_response}')

    def test_delete_group_with_users(self):
        r = WesignMethodsApi.admins_groups_delete(self, self.settings['GroupID'])
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.THERE_ARE_USERS_IN_GROUP

    ##Bug number = WES-977
    def test_delete_group_with_invalid_id(self):
        r = WesignMethodsApi.admins_groups_delete(self, self.settings['InvalidGroupID'])
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.INVALID_GROUP_ID

    def tearDown(self):
        sleep(1)

    if __name__ == "__main__":
        unittest.main()
