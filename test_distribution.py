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
        p = Path(__file__).with_name('DistributeCollection.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_distribution_two_signers_api_success(self):
        signers = self.__api_extract_signers_from_xlsx_file("base64signers")
        signers_json = signers.json()
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        template_with_field = self.__api_create_template_field_request("text_field_for_template", template)
        self.document_name = uuid.uuid4().hex
        with open(self.settings["distribute_file_with_users_and_field"], 'r+') as f:
            data = json.load(f)
            data["name"] = self.document_name  # <--- add `id` value.
            data["templateId"] = template
            data["signers"] = signers_json['signers']

            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        send_distribution = self.__api_create_distribution_request("distribute_file_with_users_and_field")
        assert send_distribution.status_code == StatusCode.OK


    def tearDown(self):
        sleep(5)

    if __name__ == "__main__":
        unittest.main()

    def __api_extract_signers_from_xlsx_file(self, signers_file):
        file = open(self.settings[signers_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documents/distribution/signers', data=json.dumps(requests_json), headers=headers)
        return r


    def __api_create_template_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/templates', data=json.dumps(requests_json), headers=headers)
        return r

    def __delete_template_created(self, template_guid):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + '/templates/' + template_guid, headers=headers)
        assert r.status_code == 200

    def __api_create_template_field_request(self, field_file, templateId):
        file = open(self.settings[field_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings["Base_Url"] + f'/templates/{templateId}', data=json.dumps(requests_json) ,headers=headers)
        return r

    def __api_create_distribution_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documents/distribution', data=json.dumps(requests_json), headers=headers)
        return r
