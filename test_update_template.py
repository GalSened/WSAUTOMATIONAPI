import unittest
import warnings
from pathlib import Path
from time import sleep
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode
import pytest
from all_api_methods import WesignMethodsApi

@pytest.mark.flaky(max_runs=3)
class WesignApiUpdateTemplateTests(unittest.TestCase):
    def setUp(self):
        a = Path(__file__).with_name('CreateTemplateSettings.json')
        with open(a) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_update_template_with_signature_field_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithSignatureFieldSuccess', template)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_with_two_signature_field_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithTwoSignatureFieldSuccess', template)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_with_minimized_field_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithMinimizedFieldSuccess', template)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_with_maximized_field_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithMaximizedFieldSuccess', template)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_with_overlaying_fields(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithOverlayingFieldsFields', template)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Fields.SignatureFields']
        assert json_response[0] == ResultCode.OVERLAYING_FIELDS_PLEASE_MOVE_THE_FIELDS
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_with_same_fields_name(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithTwoSignatureFieldWithSameFieldsName', template)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Fields.SignatureFields']
        assert json_response[0] == ResultCode.SIGNATURE_FIELDS_MUST_BE_UNIQUE
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_with_invalid_template_id(self):
        r = WesignMethodsApi.templates_id_post_json_file(self, 'UpdateTemplateWithInvalidTemplateId', self.settings['InvalidTemplateId'])
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.INVALID_TEMPLATE_ID

    def test_update_template_with_same_radio_group_name(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithRadioButtonsWithTwoSameGroupName', template)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Fields.RadioGroupFields']
        assert json_response[0] == ResultCode.RADIOGROUP_FIELDS_MUST_BE_UNIQUE_REMOVE_DUPLICATION_FIELDS
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_with_invalid_field_type_number(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithInvalidFieldType', template)
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Fields.TextFields[0].TextFieldType']
        assert json_response[0] == ResultCode.INVALID_FIELD_TYPE_NUMBER
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_without_template_name_parameter(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithoutNameParameter', template)
        assert r.status_code == StatusCode.BAD_REQUEST
        WesignMethodsApi.templates_id_delete(self, template)

    def test_update_template_with_0_width_and_height_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        r = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplatePdfBase64With0TextParameter', template)
        assert r.status_code == StatusCode.OK
        WesignMethodsApi.templates_id_delete(self, template)

    def tearDown(self):
        sleep(1)

    if __name__ == "__main__":
        unittest.main()
