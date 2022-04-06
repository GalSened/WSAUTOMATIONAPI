import unittest
import uuid
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from selenium.webdriver import ActionChains
from shared import Shared
from status_codes import StatusCode, ResultCode
from selenium import webdriver


@pytest.mark.flaky(max_runs=5)
class WesignApiCreateDocumentDistributionTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('DocumentCollectionSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_distribution_two_signers_api_success(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64EmptyName")
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_NAME


    def tearDown(self):
        sleep(5)

    if __name__ == "__main__":
        unittest.main()

    def __api_extract_signers_from_xlsx_file(self, signers_file):
        file = open(self.settings[signers_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/userapi/v3/documents/distribution/signers', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_create_template_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'templates', data=json.dumps(requests_json), headers=headers)
        return r

    def __delete_template_created(self, template_guid):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'templates/' + template_guid, headers=headers)
        assert r.status_code == 200

    def __api_create_template_duplicate_request(self, request_file, template_id):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + f'templates/{template_id}', data=json.dumps(requests_json),
                          headers=headers)
        return r

