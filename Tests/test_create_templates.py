import unittest
import warnings
from pathlib import Path
from time import sleep
import pytest
import json
from shared import Shared
from Enums.status_codes import StatusCode, ResultCode
import logging
import uuid
from Common.all_api_methods import WesignMethodsApi

@pytest.mark.flaky(max_runs=3)
class WesignApiCreateTemplateTests(unittest.TestCase):
    def setUp(self):
        # p = Path(__file__).with_name('CreateTemplateSettings.json')
        # with open(p) as f:
        #     self.settings = json.load(f)

        p = Path(__file__).resolve().parent.parent
        file_path = p / "Settings\\CreateTemplateSettings.json"
        with open(file_path) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_create_pdf_template_base64_success(self):
        try:
            logging.info(" ---Test Start---         test_create_pdf_template_base64_success         ---Test Start--- ")
            r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
            assert r.status_code == StatusCode.OK
            logging.info("Request response is : " + str(r.status_code))
            logging.info("Template created successfully")
            response = r.json()
            template = response['templateId']
            templatename = response['templateName']
            logging.info("Template id is " + str(template) + " and template name is : " + str(templatename))
            assert len(template) == 36, "Template not created"
            assert len(templatename) > 0
            WesignMethodsApi.templates_id_delete(self, template)
            logging.info(f" Template {templatename} as deleted successfully")
        except Exception as exception:
            logging.error(" ------ Test Fail ------     test_create_pdf_template_base64_success     ------ Test Fail ------")
            logging.error(exception, exc_info=True)
            raise

    def test_create_word_template_base64_success(self):
        try:
            r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplateWordBase64Success")
            logging.info(" ---Test Start---         test_create_word_template_base64_success        ---Test Start--- ")
            assert r.status_code == StatusCode.OK
            logging.info("Request response is : " + str(r.status_code))
            logging.info("Template created successfully")
            response = r.json()
            template = response['templateId']
            templatename = response['templateName']
            logging.info("Template id is " + str(template) + "and template name is : " + str(templatename))
            assert len(template) == 36, "Template not created"
            assert len(templatename) > 0
            WesignMethodsApi.templates_id_delete(self, template)
            logging.info(f" Template {templatename} as deleted successfully")
        except Exception as exception:
            logging.error(" ------ Test Fail ------     test_create_word_template_base64_success     ------ Test Fail ------")
            logging.error(exception, exc_info=True)
            raise

    def test_create_xlsx_template_base64_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplateXlsxBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        WesignMethodsApi.templates_id_delete(self, template)

    def test_create_png_template_base64_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePngBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        WesignMethodsApi.templates_id_delete(self, template)

    def test_create_jpg_template_base64_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplateJpgBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        WesignMethodsApi.templates_id_delete(self, template)

    def test_create_word_template_base64_with_meta_data_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplateWordBase64WithMetaDataSuccess")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        WesignMethodsApi.templates_id_delete(self, template)

    def test_create_template_pdf_base_64_empty_name(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64EmptyName")
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_NAME

    def test_create_template_without_file_type(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatefBase64WithoutFileType")
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Base64File']
        assert json_response[0] == ResultCode.BASE_64_FILE_UNSUPPORTED_TYPE

    def test_create_template_duplicate_template_success(self):
        r = WesignMethodsApi.templates_id_post_json_file(self, "CreateTemplateDuplicateTemplate", 'fec7d1ad-18ff-46fa-83b8-08dac0825c40')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['newTemplateId']
        WesignMethodsApi.templates_id_delete(self, json_response)

    def test_create_template_and_download_template_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        download_req = WesignMethodsApi.templates_id_download_get(self, template)
        assert download_req.status_code == 200
        assert 'Test' in download_req.headers['x-file-name']
        WesignMethodsApi.templates_id_delete(self, template)

    def test_delete_multi_documents_by_document_collection_id_success(self):
        a = []
        for x in range(5):
            template = uuid.uuid4().hex
            self.template_name = template
            self.__replace_template_name_to_unique_name_in_existing_file('CreateTemplatePdfBase64UniqueNameSuccess', self.template_name)
            r = WesignMethodsApi.templates_post_json_file(self, 'CreateTemplatePdfBase64UniqueNameSuccess')
            assert r.status_code == 200
            response = r.json()
            template_id = response['templateId']
            a.append(template_id)
        del_req = {
            "ids": [
                a[0], a[1], a[2], a[3], a[4]
            ]
        }
        r = WesignMethodsApi.templates_delete_batch_put(self, del_req)
        assert r.status_code == StatusCode.OK

    def tearDown(self):
        sleep(3)

    if __name__ == "__main__":
        unittest.main()

    def __replace_template_name_to_unique_name_in_existing_file(self, file_name, template_name):
        with open(self.settings['CreateTemplatePdfBase64UniqueNameSuccess']) as file:
            lines = file.readlines()
        lines[2] = '    "name": "' + template_name + '"' + "\n"
        with open(self.settings['CreateTemplatePdfBase64UniqueNameSuccess'], 'w') as file:
            for line in lines:
                file.write(line)
