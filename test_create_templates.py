import unittest
import warnings
from pathlib import Path
from time import sleep

import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode

class WesignApiCreateTemplateTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('CreateTemplateSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_create_pdf_template_base64_success(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        self.__delete_template_created(template)

    def test_create_word_template_base64_success(self):
        r = self.__api_create_template_request("CreateTemplateWordBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        self.__delete_template_created(template)

    def test_create_xlsx_template_base64_success(self):
        r = self.__api_create_template_request("CreateTemplateXlsxBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        self.__delete_template_created(template)

    def test_create_png_template_base64_success(self):
        r = self.__api_create_template_request("CreateTemplatePngBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        self.__delete_template_created(template)

    def test_create_jpg_template_base64_success(self):
        r = self.__api_create_template_request("CreateTemplateJpgBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        self.__delete_template_created(template)

    def test_create_word_template_base64_with_meta_data_success(self):
        r = self.__api_create_template_request("CreateTemplateWordBase64WithMetaDataSuccess")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        self.__delete_template_created(template)

    def test_create_template_pdf_base_64_empty_name(self):
        r = self.__api_create_template_request("CreateTemplatePdfBase64EmptyName")
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_NAME

    def test_create_template_without_file_type(self):
        r = self.__api_create_template_request("CreateTemplatefBase64WithoutFileType")
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Base64File']
        assert json_response[0] == ResultCode.BASE_64_FILE_UNSUPPORTED_TYPE

    def tearDown(self):
        sleep(3)

    if __name__ == "__main__":
        unittest.main()

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
