import unittest
import warnings
from pathlib import Path
from time import sleep
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode
import pytest

@pytest.mark.flaky(max_runs=3)
class WesignApiUpdateTemplateTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('UpdateTemplateSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        a = Path(__file__).with_name('CreateTemplateSettings.json')
        with open(a) as f:
            self.settings_create_template = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_update_template_with_signature_field_success(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithSignatureFieldSuccess',template)
        assert r.status_code == StatusCode.OK
        self.__delete_template_created(template)

    def test_update_template_with_two_signature_field_success(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithTwoSignatureFieldSuccess',template)
        assert r.status_code == StatusCode.OK
        self.__delete_template_created(template)

    def test_update_template_with_minimized_field_success(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithMinimizedFieldSuccess',template)
        assert r.status_code == StatusCode.OK
        self.__delete_template_created(template)

    def test_update_template_with_maximized_field_success(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithMaximizedFieldSuccess',template)
        assert r.status_code == StatusCode.OK
        self.__delete_template_created(template)

    def test_update_template_with_overlaying_fields(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithOverlayingFieldsFields',template)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Fields.SignatureFields']
        assert json_response[0] == ResultCode.OVERLAYING_FIELDS_PLEASE_MOVE_THE_FIELDS
        self.__delete_template_created(template)

    def test_update_template_with_same_fields_name(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithTwoSignatureFieldWithSameFieldsName',template)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Fields.SignatureFields']
        assert json_response[0] == ResultCode.SIGNATURE_FIELDS_MUST_BE_UNIQUE
        self.__delete_template_created(template)

    def test_update_template_with_invalid_template_id(self):
        r = self.__api_update_invalid_template_id_request('UpdateTemplateWithInvalidTemplateId')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.INVALID_TEMPLATE_ID

    def test_update_template_with_same_radio_group_name(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithRadioButtonsWithTwoSameGroupName',template)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Fields.RadioGroupFields']
        assert json_response[0] == ResultCode.RADIOGROUP_FIELDS_MUST_BE_UNIQUE_REMOVE_DUPLICATION_FIELDS
        self.__delete_template_created(template)

    def test_update_template_with_invalid_field_type_number(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithInvalidFieldType',template)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Fields.TextFields[0].TextFieldType']
        assert json_response[0] == ResultCode.INVALID_FIELD_TYPE_NUMBER
        self.__delete_template_created(template)

    def test_update_template_without_template_name_parameter(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplateWithoutNameParameter',template)
        assert r.status_code == StatusCode.BAD_REQUEST
        self.__delete_template_created(template)

    def test_update_template_with_0_width_and_height_success(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = self.__api_update_template_request('UpdateTemplatePdfBase64With0TextParameter',template)
        assert r.status_code == StatusCode.OK
        self.__delete_template_created(template)

    def tearDown(self):
        sleep(1)

    if __name__ == "__main__":
        unittest.main()

    def __api_update_template_request(self, request_file, template):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'templates/' + template, data=json.dumps(requests_json), headers=headers)
        return r

    def __api_update_invalid_template_id_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers ={'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'templates/' + self.settings['InvalidTemplateId'], data=json.dumps(requests_json), headers=headers)
        return r

    def __api_create_template_request(self, request_file):
        file = open(self.settings_create_template[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings_create_template['Base_Url'] + 'templates', data=json.dumps(requests_json), headers=headers)
        return r

    def __delete_template_created(self, template_guid):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings_create_template['Base_Url'] + 'templates/' + template_guid, headers=headers)
        assert r.status_code == 200