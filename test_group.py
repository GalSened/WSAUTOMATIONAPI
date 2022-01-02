import unittest
import warnings
from pathlib import Path
import pytest
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode

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
        r = self.__api_create_group_request('CreateNewGroupRequest')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['groupId']
        assert len(json_response) > 0
        self.__api_delete_group_request(f'{json_response}')

    def test_create_same_group_name(self):
        r = self.__api_create_group_request('CreateSameGroupNameRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.GROUP_WITH_SAME_NAME

    def test_create_empty_group_name(self):
        r = self.__api_create_group_request('CreateEmptyGroupNameRequest')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.EMPTY_NAME

    def test_update_group_name(self):
        r = self.__api_update_group_request('ChangeGroupNameRequest')
        assert r.status_code == StatusCode.OK
        self.__api_update_group_request('ChangeGroupNameToOriginalRequest')


    if __name__ == "__main__":
        unittest.main()

    def __api_create_group_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'admins/groups', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_delete_group_request(self, group_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        requests.delete(self.settings['Base_Url'] + 'admins/groups/' + group_id,headers=headers)


    def __api_update_group_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'admins/groups/' + self.settings['GroupID'], data=json.dumps(requests_json), headers=headers)
        return r
