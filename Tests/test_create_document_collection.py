import logging
import os
import shutil
import unittest
import uuid
import warnings
from pathlib import Path
from pprint import pprint
from time import sleep
import pytest
import json
from selenium.webdriver.chrome.service import Service
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import pyodbc
import Enums.status_codes
from Enums.status_codes import StatusCode, ResultCode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import PyPDF2 as pypdf
from Common.all_api_methods import WesignMethodsApi
from shared import Shared

@pytest.mark.flaky(max_runs=6)
class WesignApiCreateDocumentCollectionTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).resolve().parent.parent
        file_path = p / "Settings\\DocumentCollectionSettings.json"
        with open(file_path) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)
        self.token_nirk = Shared.login_request_nirk(self)
        self.signer1 = Shared.login_signer1_account(self)

    @pytest.mark.part1
    def test_document_collection_document_sending_success(self):
        try:
            logging.info(" ---Test Start---  test_document_collection_document_sending_success  ---Test Start--- ")
            r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSuccess')
            assert r.status_code == StatusCode.OK
            logging.info("Request response is : " + str(r.status_code))
            response = r.json()
            json_response = response['signerLinks'][0]['link']
            logging.info("Link is : " + str(json_response))
            logging.info(
                " ---Test Complete---  test_document_collection_document_sending_success  ---Test Complete--- ")
            assert len(json_response) == 85
        except Exception as exception:
            logging.error(
                " ------ Test Fail ------  test_document_collection_document_sending_success  ------ Test Fail ------")
            logging.error(exception, exc_info=True)
            raise
        return response['documentCollectionId']

    @pytest.mark.part2
    def test_document_collection_document_sending_two_contacts_by_order_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingTwoRecipientnByOrderSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks']
        assert len(json_response) == 85
        assert len(json_response_two) == 1

    @pytest.mark.part3
    def test_document_collection_document_sending_two_contacts_by_group_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingTwoRecipientByGroupSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks'][1]['link']
        json_response_three = response['signerLinks']
        assert json_response != json_response_two
        assert len(json_response_two) == 85
        assert len(json_response) == 85
        assert len(json_response_three) == 2

    @pytest.mark.part1
    def test_document_collection_document_sending_with_text_field_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithTextFieldSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85

    @pytest.mark.part2
    def test_document_collection_document_sending_with_personal_note_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithPersonalNoteSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        personal_note_popup_window = self.driver.find_elements(By.CLASS_NAME, "notes_modal__container")
        assert len(personal_note_popup_window) > 0

    @pytest.mark.part3
    def test_document_collection_document_sending_using_otp_code_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingUsingOtpCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(10)
        otp_box = self.driver.find_elements(By.ID, "auth")
        assert len(otp_box) > 0

    @pytest.mark.part1
    def test_document_collection_document_sending_using_otp_code_send_to_phone_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingUsingOtpCodeSendToPhoneSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        send_request_button = self.driver.find_element(By.XPATH,
                                                       "/html/body/app-root/app-main-signer/app-otp-details/body/main/div[2]/div/div[3]/form/div[1]/a")
        send_request_button.click()
        sleep(3)
        validate_phone = self.driver.find_element(By.CLASS_NAME, "is-confirm")
        assert validate_phone.text == "OTP code sent successfully to 050482*****87"
        sleep(2)
        otp_box = self.driver.find_elements(By.ID, "auth")
        assert len(otp_box) > 0

    @pytest.mark.part2
    def test_document_collection_document_sending_using_document_code_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingUsingDocumentCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(10)
        document_code = self.driver.find_elements(By.ID, "id")
        assert len(document_code) > 0

    @pytest.mark.part3
    def test_document_collection_document_sending_using_document_code_and_otp_code_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingUsingDocumentCodeAndOtpCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        document_code = self.driver.find_element(By.XPATH, "(//input[@type='text'])[2]")
        document_code.send_keys(self.settings['DocumentCode'])
        sleep(5)
        send_request_button = self.driver.find_element(By.XPATH,
                                                       "/html/body/app-root/app-main-signer/app-otp-details/body/main/div[2]/div/div[2]/form/input")
        send_request_button.click()
        sleep(5)
        otp_box = self.driver.find_elements(By.ID, "auth")
        assert len(otp_box) > 0

    @pytest.mark.part1
    def test_document_collection_document_sending_with_invalid_sign_field_name(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithInvalidSignFieldName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.FIELD_NAME_NOT_EXIST

    @pytest.mark.part2
    def test_document_collection_document_sending_with_empty_field_name_in_read_only_fields(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithEmptyFieldNameReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST, "Status " + str(r.status_code) + " incorrect"
        response = r.json()
        json_response = response['errors']['']
        assert json_response[0] == ResultCode.READ_ONLY_FIELDS_SHOULD_CONTAIN_NAME_AND_VALUE

    @pytest.mark.part3
    def test_document_collection_document_sending_with_invalid_field_name_in_read_only_fields(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithInvalidFieldNameReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.FIELD_NAME_NOT_EXIST

    @pytest.mark.part1
    def test_document_collection_document_sending_with_empty_value_field_in_read_only_fields(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWitheEmptyFieldValueReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['']
        assert json_response[0] == ResultCode.READ_ONLY_FIELDS_SHOULD_CONTAIN_NAME_AND_VALUE

    @pytest.mark.part2
    def test_document_collection_document_sending_with_invalid_template_id(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWitheInvalidTemplateId')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['']
        assert json_response[
                   0] == ResultCode.TEMPLATES_IN_SIGNERS_FIELDS_AND_IN_READ_ONLY_FIELDS_MUST_BE_FROM_TEMPLATES_COLLECTION_INPUT

    @pytest.mark.part3
    def test_document_collection_document_sending_with_empty_document_name(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWitheEmptyDocumentName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DocumentName']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_NAME

    @pytest.mark.part1
    def test_document_collection_document_sending_with_invalid_document_mode(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithInvalidDocumentMode')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DocumentMode']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_DOCUMENT_MODE

    @pytest.mark.part2
    def test_document_collection_document_sending_with_invalid_contact_id(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithInvalidContactId')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.CONTACT_NOT_CREATED_BY_USER

    @pytest.mark.part3
    def test_document_collection_document_sending_with_duplicate_fields_name(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithDuplicateFieldsName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Signers']
        assert json_response[0] == ResultCode.THERE_IS_DUPLICATE_FIELD_FOR_SIGNER

    @pytest.mark.part1
    def test_document_collection_document_sending_not_feet_contact_means(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingNotFeetContactMeans')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.SIGNER_METHOD_NOT_FEET_TO_CONTACT_MEANS

    @pytest.mark.part2
    def test_document_collection_document_sending_with_invalid_sending_method(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithInvalidSendingMethod')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Signers']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_SIGNERS, "Validation is " + str(json_response[0])

    @pytest.mark.part3
    def test_document_collection_document_sending_with_should_send_parameter_as_false(self):
        email_prefix = uuid.uuid4().hex
        self.document_name = email_prefix
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionDocumentSendingWithShouldSendParamaterFlase.json",
                'r+') as f:
            data = json.load(f)
            data['documentName'] = self.document_name  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithShouldSendParamaterFlase')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(60)
        self.__enter_comda_mail(self.settings['dev_email'], self.settings['comda_mail_password'])
        sleep(8)
        email = self.driver.find_elements(By.XPATH, f"//span[contains(text(),'{self.document_name}')]")
        assert len(email) == 0, "Check if email sent"
        sleep(6)
        self.driver.quit()

    @pytest.mark.part1
    def test_document_collection_document_sending_with_should_send_parameter_as_true(self):
        self.__setup()
        email = self.__enter_temp_mail()
        email_prefix = uuid.uuid4().hex
        self.document_name = email_prefix
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionDocumentSendingWithShouldSendParamaterTrue.json",
                'r+') as f:
            data = json.load(f)
            data['signers'][0]['contactMeans'] = email
            data['documentName'] = self.document_name  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithShouldSendParamaterTrue')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        sleep(90)
        email = self.driver.find_elements(By.XPATH, f"//*[contains(text(),'{self.document_name}')]")
        assert len(email) > 0, "Email didn't sent"
        sleep(2)
        self.driver.quit()

    @pytest.mark.part2
    def test_document_collection_document_sending_with_should_send_sign_document_parameter_as_false(self):
        self.__setup()
        self.driver.execute_script("window.open('');")
        email_prefix = uuid.uuid4().hex
        self.document_name = email_prefix
        email = self.__enter_temp_mail()
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionDocumentSendingWithshouldSendSignedParamaterFalse.json",
                'r+') as f:
            data = json.load(f)
            data['signers'][0]['contactMeans'] = email
            data['documentName'] = self.document_name  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithshouldSendSignedParamaterFalse')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        self.driver.get(json_response)
        sleep(14)
        self.__sign_on_document()
        sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(90)
        email_notification = self.driver.find_element(By.XPATH, f"(//*[contains(text(),'{self.document_name}')])[1]")
        email_notification.click()
        sleep(8)
        attached_document = self.driver.find_elements(By.XPATH, "//img[@id=':70']")
        assert len(attached_document) == 0, "Pdf document attached"

    @pytest.mark.part3
    def test_document_collection_document_sending_with_should_send_sign_document_parameter_as_true(self):
        self.__setup()
        self.driver.execute_script("window.open('');")
        self.driver.save_screenshot("test_document_collection_document_sending_with_should_send_sign_document_parameter_as_true_before.png")
        sleep(10)
        email = self.__enter_temp_mail()
        self.driver.save_screenshot("test_document_collection_document_sending_with_should_send_sign_document_parameter_as_true.png")
        email_prefix = uuid.uuid4().hex
        self.document_name = email_prefix
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionDocumentSendingWithshouldSendSignedParamaterTrue.json",
                'r+') as f:
            data = json.load(f)
            data['signers'][0]['contactMeans'] = email
            data['documentName'] = self.document_name
            f.seek(0)
            json.dump(data, f, indent=3)
            f.truncate()
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithshouldSendSignedParamaterTrue')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        sleep(4)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        self.driver.get(json_response)
        sleep(3)
        self.__sign_on_document()
        sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(30)
        email_notification = self.driver.find_element(By.XPATH, f"(//*[contains(text(),'{self.document_name}')])[1]")
        email_notification.click()
        sleep(2.5)
        attached_document = self.driver.find_elements(By.XPATH,
                                                      f"(//*[contains(text(),'{self.document_name}.pdf')])[1]")
        assert len(attached_document) > 0, "Pdf document attached"

    # @pytest.mark.run(order=1)
    # def test_delete_all_mails(self):
    #     self.driver = webdriver.Chrome(self.settings["chrome_driver"])
    #     self.__enter_gmail()
    #     sleep(4)
    #     try:
    #         self.__delete_gmail_emails()
    #     except:
    #         self.driver.quit()
    @pytest.mark.part3
    def test_document_collection_document_sending_with_redirect_url(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithRedirectUrlSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        self.__sign_on_document()
        sleep(5)
        # self.driver.switch_to.alert.accept()
        sleep(5)
        assert self.driver.current_url == "https://www.comsign.co.il/"

    @pytest.mark.part1
    def test_document_collection_document_sending_using_signer_attachments_as_mandatory_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSignerAttachmentsAsMandatorySuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        self.__sign_on_document()
        sleep(2)
        attachment_window_pop_up = self.driver.find_elements(By.CLASS_NAME, "ct-animate-slide-down")
        assert len(attachment_window_pop_up) == 1
        sleep(1)
        self.driver.quit()

    @pytest.mark.part2
    def test_document_collection_document_sending_using_signer_appendices_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSignerAppendicesSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        appendices_icon = self.driver.find_elements(By.CLASS_NAME, "feather-bookmark")
        assert len(appendices_icon) == 1
        sleep(5)
        appendices_pop_up = self.driver.find_elements(By.CLASS_NAME, "ct-animate-slide-down")
        assert len(appendices_pop_up) == 1
        sleep(1)
        self.driver.quit()

    @pytest.mark.part3
    def test_document_collection_delete_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['documentCollectionId']
        r = WesignMethodsApi.document_collections_id_delete(self, json_response)
        assert r.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_document_collection_cancel_document_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['documentCollectionId']
        r = WesignMethodsApi.document_collections_id_cancel_put(self, json_response)
        assert r.status_code == StatusCode.OK

    @pytest.mark.part2
    def test_document_collection_resend_document_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_document_id = response['documentCollectionId']
        json_response_signer_id = response['signerLinks'][0]['signerId']
        r = WesignMethodsApi.document_collections_id_signers_signerId_method_sendingMethod_get(self, json_response_document_id, json_response_signer_id)
        assert r.status_code == StatusCode.OK

    @pytest.mark.part3
    def test_document_collection_replace_signer_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_document_id = response['documentCollectionId']
        json_response_signer_id = response['signerLinks'][0]['signerId']
        r = WesignMethodsApi.document_collections_id_signer_signerId_replace_put(self, json_response_signer_id, json_response_document_id,
                                              'DocumentCollectionReplaceSuccess')
        assert r.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_document_collection_share_document_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_document_id = response['documentCollectionId']
        json_response_link = response['signerLinks'][0]['link']
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionShareDocuemnt.json",
                'r+') as f:
            data = json.load(f)
            data['documentCollectionId'] = json_response_document_id  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        self.__setup()
        sleep(1)
        self.driver.get(json_response_link)
        sleep(8)
        self.__sign_on_document()
        r = WesignMethodsApi.document_collections_share_post_json_file(self, 'DocumentCollectionShareDocuemnt')
        assert r.status_code == StatusCode.OK

    @pytest.mark.part2
    def test_document_collection_without_fields_one_recipient_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionSendDocumentWithoutFields')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        signature_field = self.driver.find_elements(By.CLASS_NAME, "is-signature")
        assert len(signature_field) == 0
        finish_button = self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary")
        sleep(5)
        finish_button.click()
        sleep(3)
        sign_complete_msg = self.driver.find_elements(By.XPATH,
                                                      '/html/body/app-root/app-main-signer/app-success-page/body/main/h2')
        sleep(4)
        assert len(sign_complete_msg) > 0

    @pytest.mark.part3
    def test_document_collection_without_fields_two_recipient_by_group_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionSendDocumentWithoutFieldsTwoRecipients')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks'][1]['link']
        json_response_three = response['signerLinks']
        assert json_response != json_response_two
        assert len(json_response_two) == 85
        assert len(json_response) == 85
        assert len(json_response_three) == 2

    @pytest.mark.part1
    def test_document_collection_without_fields_two_recipient_by_order_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionSendDocumentWithoutFieldsTwoRecipientsOrder')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks']
        assert len(json_response) == 85
        assert len(json_response_two) == 1

    @pytest.mark.part2
    def test_document_collection_with_only_one_signature_field_two_recipient_by_order_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionSendDocumentWithOnlyOneSignatureFieldTwoRecipients')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks']
        assert len(json_response) == 85
        assert len(json_response_two) == 1

    @pytest.mark.part3
    def test_document_collection_with_only_one_signature_field_two_recipient_by_group_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionSendDocumentWithOnlyOneSignatureFieldTwoRecipientsGroup')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks'][1]['link']
        json_response_three = response['signerLinks']
        assert json_response != json_response_two
        assert len(json_response_two) == 85
        assert len(json_response) == 85
        assert len(json_response_three) == 2

    @pytest.mark.part1
    def test_document_collection_with_hidden_field_as_true(self):
        r = WesignMethodsApi.templates_post_json_file(self, 'CreateTemplatePdfBase64Success')
        response = r.json()
        template = response['templateId']
        WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithTextFieldAsHidden', template)
        d = {
            "documentMode": 1,
            "documentName": "TestApiHiddenAsTrue",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "999a7796-8687-4291-1471-08db6807b765",
                    "sendingMethod": 2,
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "sign1"
                        }
                    ]
                }
            ]
        }
        r = WesignMethodsApi.document_collections_post_dict(self, d)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        text_field = self.driver.find_elements(By.ID, "text1")
        assert len(text_field) == 0, 'Text field displayed'
        WesignMethodsApi.templates_id_delete(self, template)

    @pytest.mark.part2
    def test_document_collection_with_hidden_field_as_false(self):
        r = WesignMethodsApi.templates_post_json_file(self, 'CreateTemplatePdfBase64Success')
        response = r.json()
        template = response['templateId']
        # self.__api_update_template_request_hidden_field('UpdateTemplateWithTextFieldAsHiddenAsFalse', template)
        WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithTextFieldAsHiddenAsFalse', template)
        d = {
            "documentMode": 1,
            "documentName": "TestApiHiddenAsFalse",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "999a7796-8687-4291-1471-08db6807b765",
                    "sendingMethod": 2,
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "sign1"
                        }
                    ]
                }
            ]
        }
        r = WesignMethodsApi.document_collections_post_dict(self, d)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        text_field = self.driver.find_elements(By.ID, "text1")
        assert len(text_field) > 0, 'Text field not displayed'
        WesignMethodsApi.templates_id_delete(self, template)

    # Bug number - WES-1030
    @pytest.mark.part3
    def test_document_collection_send_twice_to_same_contact(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingTwiceToSameContact')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"

    # bug number - WES-1102
    @pytest.mark.part1
    def test_document_collection_download_document_collection_invalid_id(self):
        r = WesignMethodsApi.document_collections_id_get(self, '827b5c63-4951-4098-2ce4-08da2cedfaa9')
        assert r.status_code == StatusCode.BAD_REQUEST

    @pytest.mark.part2
    # Bug number - WES-1066
    def test_document_collection_send_global_number_with_extension_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = WesignMethodsApi.document_collections_post_json_file_using_twillio(self, 'DocumentCollectionDocumentSendingTwilioProviderWithExtensionsSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"

    @pytest.mark.part3
    def test_document_collection_send_global_number_with_extension_and_local_number_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = WesignMethodsApi.document_collections_post_json_file_using_twillio(self, 'DocumentCollectionDocumentSendingTwilioProviderWithExtensionsAndLocalNumberSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"
        driver = self.driver
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, "ct-button--titlebar-primary")))
        finish_button = self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary")
        finish_button.click()

    @pytest.mark.part1
    def test_document_collection_send_global_number_without_extension_to_local_number_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = WesignMethodsApi.document_collections_post_json_file_using_twillio(self, 'DocumentCollectionDocumentSendingTwilioProviderWithoutExtensionsLocalNumberSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"
        driver = self.driver
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, "ct-button--titlebar-primary")))
        finish_button = self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary")
        finish_button.click()

    # Bug number = WES-1106
    @pytest.mark.part2
    def test_send_distribute_duplicated_fields_in_xlsx_with_same_name_validate_values_success(self):
        self.token = Shared.login_request_gmail(self)
        self.__setup()
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self, "documentCollection_duplicated_fields_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        document_name = uuid.uuid4().hex
        self._change_values_in_file("DocumentCollectionDuplicatedFields", template, document_name)
        send_distribution = WesignMethodsApi.document_collections_post_json_file(self, "DocumentCollectionDuplicatedFields")
        assert send_distribution.status_code == StatusCode.OK
        sleep(2)
        doc_id = self.__get_documentCollectionId_from_db(document_name)

        self.__get_link_by_signers_number_without_signing(1, doc_id)
        sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            (By.ID, "Text")))
        self.__assert_number_of_live_fields(2)
        get_value_from_text_field = self.driver.find_elements(By.ID, "Text")
        for value in get_value_from_text_field:
            assert value.get_attribute('value') == "string", " value wasn't added to the fields"
        total_fields = self.driver.find_elements(By.XPATH, "//app-text-field[1]/div/input")
        assert len(total_fields) == int(2), "field wasn't duplicated"

    # Bug number = WES-1123
    @pytest.mark.part3
    def test_document_collection_download_cancel_document(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['documentCollectionId']
        sleep(8)
        cancel_document_request = WesignMethodsApi.document_collections_id_cancel_put(self, json_response)
        assert cancel_document_request.status_code == StatusCode.OK
        sleep(5)
        download_document = WesignMethodsApi.document_collections_id_get(self, json_response)
        assert download_document.status_code == 400, "Document still can be download after cancelation"

    @pytest.mark.part1
    def test_document_collection_update_signature_field_description_is_empty_success(self):
        create_template = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert create_template.status_code == StatusCode.OK
        response = create_template.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        update_template = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithSignatureFieldWithoutFieldDescription',
                                                             template)
        assert update_template.status_code == StatusCode.OK
        d = {
            "documentMode": 1,
            "documentName": "TestSignatureFieldDescriptionNull",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "999a7796-8687-4291-1471-08db6807b765",
                    "sendingMethod": 2,
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "Signature_null"
                        }
                    ]
                }
            ]
        }
        r = WesignMethodsApi.document_collections_post_dict(self, d)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(2)
        self.driver.get(json_response)
        driver = self.driver
        sleep(3)
        self.__sign_on_document()
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        WesignMethodsApi.templates_id_delete(self, template)

    @pytest.mark.part2
    def test_document_collection_update_signature_field_description_different_from_field_name_using_field_name_success(
            self):
        create_template = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert create_template.status_code == StatusCode.OK
        response = create_template.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        update_template = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithSignatureDescriptionDiffrentFromFieldName', template)
        assert update_template.status_code == StatusCode.OK
        d = {
            "documentMode": 1,
            "documentName": "TestSignatureFieldDescriptionDiffrentFromFieldName",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "999a7796-8687-4291-1471-08db6807b765",
                    "sendingMethod": 2,
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "Signature_null"
                        }
                    ]
                }
            ]
        }
        r = WesignMethodsApi.document_collections_post_dict(self, d)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(2)
        self.driver.get(json_response)
        driver = self.driver
        sleep(3)
        self.__sign_on_document()
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        WesignMethodsApi.templates_id_delete(self, template)

    @pytest.mark.part3
    def test_document_collection_update_signature_field_description_different_from_field_name_using_only_field_description_success(
            self):
        create_template = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert create_template.status_code == StatusCode.OK
        response = create_template.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        update_template = WesignMethodsApi.templates_id_put_json_file(self, 'UpdateTemplateWithSignatureDescriptionDiffrentFromFieldName', template)
        assert update_template.status_code == StatusCode.OK
        d = {
            "documentMode": 1,
            "documentName": "TestSignatureFieldDescriptionDiffrentFromFieldName",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "999a7796-8687-4291-1471-08db6807b765",
                    "sendingMethod": 2,
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "string"
                            # "fieldValue": ""
                        }
                    ]
                }
            ]
        }
        r = WesignMethodsApi.document_collections_post_dict(self, d)
        assert r.status_code == StatusCode.OK

        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(2)
        self.driver.get(json_response)
        driver = self.driver
        sleep(3)
        self.__sign_on_document()
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        WesignMethodsApi.templates_id_delete(self, template)

    @pytest.mark.part1
    def test_document_collection_update_signature_field_description_different_from_field_name_using_only_field_name_hebrew_success(
            self):
        create_template = WesignMethodsApi.templates_post_json_file(self, "CreateTemplatePdfBase64Success")
        assert create_template.status_code == StatusCode.OK
        response = create_template.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        # update template
        update_template = {
            "name": "dummy",
            "fields": {
                "signatureFields": [
                    {
                        "signingType": 1,
                        "name": "חתימה",
                        "x": 0.3596638655462185,
                        "y": 0.11757719714964371,
                        "width": 0.15999999999999998,
                        "height": 0.02350000000000004,
                        "page": 1
                    }
                ]
            }
        }
        r = WesignMethodsApi.templates_id_put_dict(self, update_template, template)
        assert r.status_code == StatusCode.OK
        d = {
            "documentMode": 1,
            "documentName": "TestSignatureFieldDescriptionDiffrentFromFieldName",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "999a7796-8687-4291-1471-08db6807b765",
                    "sendingMethod": 2,
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "חתימה",

                        }
                    ]
                }
            ]
        }
        r = WesignMethodsApi.document_collections_post_dict(self, d)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(2)
        self.driver.get(json_response)
        driver = self.driver
        sleep(3)
        self.__sign_on_document()
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        WesignMethodsApi.templates_id_delete(self, template)

    @pytest.mark.part2
    def test_document_collection_download_document_as_json_file_success(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionSendDocumentWithoutFields')
        assert r.status_code == StatusCode.OK
        response = r.json()
        document_id = response['documentCollectionId']
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        signature_field = self.driver.find_elements(By.CLASS_NAME, "is-signature")
        assert len(signature_field) == 0
        finish_button = self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary")
        sleep(5)
        finish_button.click()
        sleep(3)
        sign_complete_msg = self.driver.find_elements(By.XPATH,
                                                      '/html/body/app-root/app-main-signer/app-success-page/body/main/h2')
        sleep(4)
        assert len(sign_complete_msg) > 0
        sleep(2)
        # download request
        download_json = WesignMethodsApi.document_collections_id_json_get(self, document_id)
        assert download_json.status_code == StatusCode.OK
        response = download_json.json()
        base64 = response['files'][0]['data']
        assert len(base64) <= 34228

    @pytest.mark.part3
    def test_delete_multi_documents_by_document_collection_id_success(self):
        a = []
        for x in range(5):
            document = uuid.uuid4().hex
            self.document_name = document
            req = {
                "documentMode": 1,
                "documentName": self.document_name,
                "templates": [
                    "89ce8b6c-f3fe-49d3-83dd-08dac0825c40"
                ],
                "signers": [
                    {
                        "contactId": "999a7796-8687-4291-1471-08db6807b765",
                        "sendingMethod": 2,
                        "signerFields": [
                            {
                                "templateId": "89ce8b6c-f3fe-49d3-83dd-08dac0825c40",
                                "fieldName": "sign1"
                            }
                        ]
                    }
                ]
            }
            r = WesignMethodsApi.document_collections_post_dict(self, req)
            assert r.status_code == 200
            response = r.json()
            json_response = response['documentCollectionId']
            a.append(json_response)

        del_req = {
            "ids": [
                a[0], a[1], a[2], a[3], a[4]
            ]
        }
        delete = WesignMethodsApi.document_collections_delete_batch_put_dict(self, del_req)
        assert delete.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_document_collection_send_document_with_meta_data_and_sign_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplateWordBase64WithMetaDataSuccess")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        document = uuid.uuid4().hex
        self.document_name = document
        d = {
            "documentName": self.document_name,
            "documentMode": 1,
            "templates": [
                template
            ],
            "signers": [
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "nirk",
                    "contactMeans": "nirk@comsign.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "sig_1",

                        },
                        {
                            "templateId": template,
                            "fieldName": "sig_2",

                        },
                        {
                            "templateId": template,
                            "fieldName": "sig_3",

                        },
                        {
                            "templateId": template,
                            "fieldName": "txt_3",

                        },
                        {
                            "templateId": template,
                            "fieldName": "txt_4",

                        },
                        {
                            "templateId": template,
                            "fieldName": "phone_4",

                        },
                        {
                            "templateId": template,
                            "fieldName": "number_6",

                        },
                        {
                            "templateId": template,
                            "fieldName": "date_7",

                        },
                        {
                            "templateId": template,
                            "fieldName": "cb_2"
                        },
                        {
                            "templateId": template,
                            "fieldName": "radio_8"
                        },
                        {
                            "templateId": template,
                            "fieldName": "radio_9"
                        },
                        {
                            "templateId": template,
                            "fieldName": "radio_10"
                        },
                        {
                            "templateId": template,
                            "fieldName": "radio_11"
                        },
                        {
                            "templateId": template,
                            "fieldName": "radio_12"
                        },
                        {
                            "templateId": template,
                            "fieldName": "radio_13"
                        },
                        {
                            "templateId": template,
                            "fieldName": "chs_14"
                        }
                    ]
                }
            ],
        }
        r = WesignMethodsApi.document_collections_post_dict(self, d)
        assert r.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_document_collection_send_document_two_recipients_e2e_sign_success(self):
        r = WesignMethodsApi.templates_post_json_file(self, "CreateTemplate3PagesPdfBase64Success")
        assert r.status_code == StatusCode.OK
        response = r.json()
        template = response['templateId']
        d = {
            "name": "stringA",
            "fields": {
                "radioGroupFields": [
                    {
                        "radioFields": [
                            {
                                "groupName": "Group_DyYrL",
                                "x": 0.08396305625524769,
                                "y": 0.48990498812351546,
                                "width": 0.037783375314861464,
                                "height": 0.02349317102137767,
                                "page": 3,
                                "name": "Radio_FI1iF",
                                "description": "Radio_FI1iF"
                            },
                            {
                                "groupName": "Group_DyYrL",
                                "x": 0.16792611251049538,
                                "y": 0.48990498812351546,
                                "width": 0.037783375314861464,
                                "height": 0.02349317102137767,
                                "page": 3,
                                "name": "Radio_vKi94",
                                "description": "Radio_vKi94"
                            }
                        ],
                        "name": "Group_DyYrL"
                    },
                    {
                        "radioFields": [
                            {
                                "groupName": "Group_OAy97",
                                "x": 0.16792611251049538,
                                "y": 0.8456057007125891,
                                "width": 0.037783375314861464,
                                "height": 0.02349317102137767,
                                "page": 2,
                                "name": "Radio_kvXeS",
                                "description": "Radio_kvXeS"
                            },
                            {
                                "groupName": "Group_OAy97",
                                "x": 0.08396305625524769,
                                "y": 0.8456057007125891,
                                "width": 0.037783375314861464,
                                "height": 0.02349317102137767,
                                "page": 2,
                                "name": "Radio_nrDJZ",
                                "description": "Radio_nrDJZ"
                            }
                        ],
                        "name": "Group_OAy97"
                    },
                    {
                        "radioFields": [
                            {
                                "groupName": "Group_I3zx7",
                                "x": 0.3795130142737196,
                                "y": 0.828978622327791,
                                "width": 0.037783375314861464,
                                "height": 0.02349317102137767,
                                "page": 1,
                                "name": "Radio_NmpmY",
                                "description": "Radio_NmpmY"
                            },
                            {
                                "groupName": "Group_I3zx7",
                                "x": 0.5424013434089001,
                                "y": 0.7381235154394299,
                                "width": 0.037783375314861464,
                                "height": 0.02349317102137767,
                                "page": 1,
                                "name": "Radio_YoVQ3",
                                "description": "Radio_YoVQ3"
                            }
                        ],
                        "name": "Group_I3zx7"
                    }
                ],
                "textFields": [
                    {

                        "textFieldType": 1,
                        "x": 0.4164567590260285,
                        "y": 0.503562945368171,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 3,
                        "name": "Text_EpHgm",
                        "description": "Text_EpHgm"
                    },
                    {

                        "textFieldType": 5,
                        "x": 0.08396305625524769,
                        "y": 0.28711401425178146,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 3,
                        "name": "Email_rh7Jo",
                        "description": "Email_rh7Jo"
                    },
                    {

                        "textFieldType": 2,
                        "x": 0.29135180520570947,
                        "y": 0.2975059382422803,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 3,
                        "name": "Date_eMlHP",
                        "description": "Date_eMlHP"
                    },
                    {

                        "textFieldType": 3,
                        "x": 0.054575986565911,
                        "y": 0.5469121140142518,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 3,
                        "name": "Number_2GGe8",
                        "description": "Number_2GGe8"
                    },
                    {

                        "textFieldType": 5,
                        "x": 0.08816120906801007,
                        "y": 0.6689429928741093,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 2,
                        "name": "Email_c8a6X",
                        "description": "Email_c8a6X"
                    },
                    {

                        "textFieldType": 4,
                        "x": 0.44920235096557515,
                        "y": 0.7069477434679335,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 2,
                        "name": "Phone_LhNvi",
                        "description": "Phone_LhNvi"
                    },
                    {

                        "textFieldType": 3,
                        "x": 0.35432409739714527,
                        "y": 0.7862232779097387,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 2,
                        "name": "Number_yudKx",
                        "description": "Number_yudKx"
                    },
                    {

                        "textFieldType": 1,
                        "x": 0.5524769101595298,
                        "y": 0.8610451306413301,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 2,
                        "name": "Text_ETubB",
                        "description": "Text_ETubB"
                    },
                    {

                        "textFieldType": 1,
                        "x": 0.5138539042821159,
                        "y": 0.4002375296912114,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 1,
                        "name": "Text_dU5E2",
                        "description": "Text_dU5E2"
                    },
                    {

                        "textFieldType": 4,
                        "x": 0.581024349286314,
                        "y": 0.538895486935867,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 1,
                        "name": "Phone_Fcoea",
                        "description": "Phone_Fcoea"
                    },
                    {

                        "textFieldType": 3,
                        "x": 0.2401343408900084,
                        "y": 0.5795724465558195,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 1,
                        "name": "Number_b4iOp",
                        "description": "Number_b4iOp"
                    },
                    {

                        "textFieldType": 2,
                        "x": 0.08396305625524769,
                        "y": 0.668646080760095,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 1,
                        "name": "Date_etWjW",
                        "description": "Date_etWjW"
                    },
                    {

                        "textFieldType": 1,
                        "x": 0.08396305625524769,
                        "y": 0.27612826603325413,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 1,
                        "name": "Text_fQgdk",
                        "description": "Text_fQgdk"
                    },
                    {

                        "textFieldType": 5,
                        "x": 0.3988245172124265,
                        "y": 0.4759501187648456,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 1,
                        "name": "Email_J8UiH",
                        "description": "Email_J8UiH"
                    },
                    {

                        "textFieldType": 1,
                        "x": 0.08396305625524769,
                        "y": 0.4168646080760095,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 2,
                        "name": "Text_ziyZg",
                        "description": "Text_ziyZg"
                    },
                    {

                        "textFieldType": 5,
                        "x": 0.08396305625524769,
                        "y": 0.5834323040380047,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 2,
                        "name": "Email_1bY45",
                        "description": "Email_1bY45"
                    }
                ],
                "checkBoxFields": [
                    {

                        "x": 0.056255247691015954,
                        "y": 0.35243467933491684,
                        "width": 0.037783375314861464,
                        "height": 0.02672209026128266,
                        "page": 3,
                        "name": "Checkbox_L6DpR",
                        "description": "Checkbox_L6DpR"
                    },
                    {

                        "x": 0.08396305625524769,
                        "y": 0.47891923990498814,
                        "width": 0.037783375314861464,
                        "height": 0.02672209026128266,
                        "page": 1,
                        "name": "Checkbox_jejnz",
                        "description": "Checkbox_jejnz"
                    }
                ],
                "choiceFields": [
                    {

                        "options": [
                            "option",
                            "option A",
                            "option B"
                        ],
                        "x": 0.08396305625524769,
                        "y": 0.7384204275534442,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 2,
                        "name": "Choice_LzjnP",
                        "description": "Choice_LzjnP"
                    },
                    {

                        "options": [
                            "אופציה א",
                            "אופיצה ב",
                            "אופיצה ג",
                            "אופיצה ד"
                        ],

                        "x": 0.08396305625524769,
                        "y": 0.41953681710213775,
                        "width": 0.16,
                        "height": 0.0235,
                        "page": 1,
                        "name": "Choice_aLc8y",
                        "description": "Choice_aLc8y"
                    }
                ],
                "signatureFields": [
                    {

                        "signingType": 1,
                        "x": 0.36859781696053734,
                        "y": 0.3830166270783848,
                        "width": 0.16,
                        "height": 0.05938242280285035,
                        "page": 3,
                        "name": "Signature_zbCNA",
                        "description": "Signature_zbCNA",
                        "image": ""
                    },
                    {

                        "signingType": 1,
                        "x": 0.5356842989084802,
                        "y": 0.7660332541567696,
                        "width": 0.16,
                        "height": 0.05938242280285035,
                        "page": 3,
                        "name": "Signature_e4hGu",
                        "description": "Signature_e4hGu",
                        "image": ""
                    },
                    {

                        "signingType": 1,
                        "x": 0.08396305625524769,
                        "y": 0.6549881235154394,
                        "width": 0.16,
                        "height": 0.05938242280285035,
                        "page": 3,
                        "name": "Signature_67OV7",
                        "description": "Signature_67OV7",
                        "image": ""
                    },
                    {

                        "signingType": 1,
                        "x": 0.4441645675902603,
                        "y": 0.28919239904988125,
                        "width": 0.16,
                        "height": 0.05938242280285035,
                        "page": 1,
                        "name": "Signature_j1m7q",
                        "description": "Signature_j1m7q",
                        "image": ""
                    },
                    {

                        "signingType": 1,
                        "x": 0.5575146935348446,
                        "y": 0.3913301662707839,
                        "width": 0.16,
                        "height": 0.05938242280285035,
                        "page": 2,
                        "name": "Signature_cj5Fu",
                        "description": "Signature_cj5Fu",
                        "image": ""
                    },
                    {

                        "signingType": 1,
                        "x": 0.3904282115869018,
                        "y": 0.5213776722090261,
                        "width": 0.16,
                        "height": 0.05938242280285035,
                        "page": 2,
                        "name": "Signature_VlDyU",
                        "description": "Signature_VlDyU",
                        "image": ""
                    },
                    {

                        "signingType": 1,
                        "x": 0.08396305625524769,
                        "y": 0.2980997624703088,
                        "width": 0.16,
                        "height": 0.05938242280285035,
                        "page": 2,
                        "name": "Signature_qRJRG",
                        "description": "Signature_qRJRG",
                        "image": ""
                    }
                ]
            }
        }
        # headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        # update_template = requests.put(self.settings['Base_Url'] + 'templates/' + template, data=json.dumps(d),
        #                                headers=headers)
        update_template = WesignMethodsApi.templates_id_put_dict(self, d, template)
        assert update_template.status_code == StatusCode.OK
        document = uuid.uuid4().hex
        self.document_name = document
        document_collection = {
            "documentName": self.document_name,
            "documentMode": 1,
            "templates": [
                template
            ],
            "signers": [
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "nirk",
                    "contactMeans": "nirk@comsign.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "Signature_j1m7q",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Signature_zbCNA",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Signature_e4hGu",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Signature_67OV7",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Text_fQgdk",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Phone_Fcoea",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Number_b4iOp",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Date_etWjW",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Checkbox_jejnz"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Radio_NmpmY"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Radio_YoVQ3"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Text_ETubB",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Text_ziyZg",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Email_1bY45",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Choice_LzjnP"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Text_EpHgm",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Number_2GGe8",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Checkbox_L6DpR"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Radio_FI1iF"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Radio_vKi94"
                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "Devtest9",
                    "contactMeans": "Devtest9@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": template,
                            "fieldName": "Signature_qRJRG",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Signature_cj5Fu",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Signature_VlDyU",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Email_c8a6X",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Number_yudKx",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Phone_LhNvi",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Radio_kvXeS"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Radio_nrDJZ"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Date_eMlHP",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Email_rh7Jo",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Email_J8UiH",

                        },
                        {
                            "templateId": template,
                            "fieldName": "Choice_aLc8y"
                        },
                        {
                            "templateId": template,
                            "fieldName": "Text_dU5E2",

                        }
                    ]
                }
            ]
        }
        # headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        # r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(document_collection),
        #                   headers=headers)
        r = WesignMethodsApi.document_collections_post_dict(self, document_collection)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        driver = self.driver
        sleep(4)
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        text = self.driver.find_elements(By.XPATH, "//input[@type='text']")
        tel = self.driver.find_elements(By.XPATH, "//input[@type='tel']")
        number = self.driver.find_elements(By.XPATH, "//input[@placeholder='123456']")
        date_field = self.driver.find_elements(By.XPATH, "//*[@type='date']")
        email = self.driver.find_elements(By.XPATH, "//input[@type='email']")
        check_box = self.driver.find_elements(By.XPATH,
                                              "//input[@class='ng-untouched ng-pristine ng-valid ng-star-inserted']")
        sleep(4)
        for x in number:
            try:
                sleep(4)
                x.send_keys("5870")
            except:
                pass
        for x in text:
            try:
                sleep(4)
                x.send_keys("בדיקה שלי")
            except:
                pass
        for x in tel:
            try:
                sleep(4)
                x.send_keys("0504821881")
            except:
                pass
        for x in date_field:
            try:
                sleep(2)
                x.click()
                sleep(1)
                x.send_keys(Keys.SPACE)
                sleep(1)
                x.send_keys(Keys.ENTER)
                sleep(2)
            except:
                pass
        for x in email:
            try:
                sleep(4)
                x.send_keys("test@comda.co.il")
            except:
                pass
        for x in check_box:
            try:
                sleep(4)
                x.click()
            except:
                pass
        sleep(4)
        radio_button_one = self.driver.find_element(By.ID, "Group_I3zx7_Radio_YoVQ3")
        radio_button_one.click()
        sleep(4)
        radio_button_two = self.driver.find_element(By.ID, "Group_DyYrL_Radio_vKi94")
        radio_button_two.click()
        sleep(4)
        select = Select(self.driver.find_element(By.ID, "Choice_LzjnP"))
        select.select_by_index(2)
        sleep(4)
        self.driver.find_element(By.XPATH, "//*[@name='feather']").click()
        sleep(4)
        canvas = self.driver.find_element(By.XPATH, "//div[@class='signature-pad__canvas']")
        drawing = ActionChains(self.driver) \
            .click_and_hold(canvas) \
            .move_by_offset(-200, 10) \
            .move_by_offset(-10, -50) \
            .move_by_offset(-25, -10) \
            .move_by_offset(100, -100) \
            .move_by_offset(10, 60) \
            .move_by_offset(10, 100) \
            .move_by_offset(-10, -120) \
            .release()
        drawing.perform()
        for x in range(25):
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_by_offset(5, 0)  # move 150 pixels to the right to access Help link
            action.click()
            action.perform()
        use_signature_all_fields = self.driver.find_element(By.XPATH, "(//span[@class='ct-checkbox__checkmark'])[2]")
        use_signature_all_fields.click()
        sleep(4)
        self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
        sleep(3)
        self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
        sleep(5)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        sleep(1)
        doc_id = self.__get_documentCollectionId_from_db(self.document_name)

        self.__get_link_by_signers_number_without_signing(2, doc_id)
        sleep(2)
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        text = self.driver.find_elements(By.XPATH, "//input[@type='text']")
        tel = self.driver.find_elements(By.XPATH, "//input[@type='tel']")
        number = self.driver.find_elements(By.XPATH, "//input[@placeholder='123456']")
        date_field = self.driver.find_elements(By.XPATH, "//*[@type='date']")
        email = self.driver.find_elements(By.XPATH, "//input[@type='email']")
        sleep(3)
        for x in number:
            try:
                sleep(4)
                x.send_keys("1234")
            except:
                pass
        for x in text:
            try:
                sleep(4)
                x.send_keys("My tests")
            except:
                pass
        for x in tel:
            try:
                sleep(4)
                x.send_keys("0504821882")
            except:
                pass
        for x in date_field:
            try:
                sleep(2)
                x.click()
                sleep(1)
                x.send_keys(Keys.SPACE)
                sleep(1)
                x.send_keys(Keys.ENTER)
                sleep(2)
            except:
                pass
        for x in email:
            try:
                sleep(4)
                x.send_keys("test2@comda.co.il")
            except:
                pass
        sleep(4)
        radio_button_one = self.driver.find_element(By.ID, "Group_OAy97_Radio_kvXeS")
        radio_button_one.click()
        sleep(4)
        select = Select(self.driver.find_element(By.ID, "Choice_aLc8y"))
        select.select_by_index(2)
        sleep(4)
        self.driver.find_element(By.XPATH, "//*[@name='feather']").click()
        sleep(4)
        canvas = self.driver.find_element(By.XPATH, "//div[@class='signature-pad__canvas']")
        drawing = ActionChains(self.driver) \
            .click_and_hold(canvas) \
            .move_by_offset(-200, 10) \
            .move_by_offset(-10, -50) \
            .move_by_offset(-25, -10) \
            .move_by_offset(100, -100) \
            .move_by_offset(10, 60) \
            .move_by_offset(10, 100) \
            .move_by_offset(-10, -120) \
            .release()
        drawing.perform()
        for x in range(25):
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_by_offset(5, 0)  # move 150 pixels to the right to access Help link
            action.click()
            action.perform()
        use_signature_all_fields = self.driver.find_element(By.XPATH, "(//span[@class='ct-checkbox__checkmark'])[2]")
        use_signature_all_fields.click()
        sleep(3)
        self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
        sleep(3)
        self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
        sleep(2)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        self.__download_document()
        sleep(3)
        try:
            src_path = rf"C:\Users\JenkinsSVC\Downloads\{document}.pdf"
            dst_path = r"\\fs01\Users\NirK\pdfs"
            shutil.copy(src_path, dst_path)
        except:
            pass
        sleep(3)
        pdfobject = open(f'\\\\fs01\\Users\\NirK\\pdfs\\{document}.pdf', 'rb')
        pdf = pypdf.PdfFileReader(pdfobject)
        check_fields = pdf.get_fields()
        for x in check_fields.values():
            assert x['/V'] != '' and x['/V'] != "/Off" and x['/V'] != '/'

    @pytest.mark.part3
    @pytest.mark.success
    def test_send_sms_with_success_results(self):
        r = WesignMethodsApi.document_collections_post_json_file(self, 'sms')
        assert r.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_sending_to_25_recipients_and_sign_by_group_and_validate_document_status(self):
        self.__setup()
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {
          "readOnlyFields": [],
          "senderAppendices": [],
          "shouldSignUsingSigner1AfterDocumentSigningFlow": False,
          "signers": [
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest1",
              "contactMeans": "devtest1@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_FzfI7",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest2",
              "contactMeans": "devtest2@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_28lsE",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest3",
              "contactMeans": "devtest3@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_xXMjz",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest4",
              "contactMeans": "devtest4@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_zcF5u",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest5",
              "contactMeans": "devtest5@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_9m7PE",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest6",
              "contactMeans": "devtest6@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_4QzbT",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest7",
              "contactMeans": "devtest7@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_udOeg",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest8",
              "contactMeans": "devtest8@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_WjDQS",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest9",
              "contactMeans": "devtest9@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_HPqM6",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest10",
              "contactMeans": "devtest10@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_Pgh4X",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest1",
              "contactMeans": "devtest1@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_CgwIJ",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest2",
              "contactMeans": "devtest2@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_SEEFD",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest3",
              "contactMeans": "devtest3@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_0Rw3v",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest4",
              "contactMeans": "devtest4@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_k04Kz",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest5",
              "contactMeans": "devtest5@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_3lYlH",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest6",
              "contactMeans": "devtest6@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_ReQrM",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest7",
              "contactMeans": "devtest7@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_oa4bJ",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest8",
              "contactMeans": "devtest8@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_OMYuf",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest9",
              "contactMeans": "devtest9@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_W7RCK",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest10",
              "contactMeans": "devtest10@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_9Imis",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest1",
              "contactMeans": "devtest1@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_NVeiY",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest2",
              "contactMeans": "devtest2@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_Ni0lh",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest3",
              "contactMeans": "devtest3@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_ovnUw",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest4",
              "contactMeans": "devtest4@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_gGRnZ",
                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "devtest5",
              "contactMeans": "devtest5@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                  "fieldName": "Signature_YTICB",

                }
              ]
            }
          ],
          "documentName": self.document_name,
          "documentMode": 2,
          "templates": [
            "62226367-0456-4a82-6a5a-08daddc7e4e7"
          ]
        }
        r = WesignMethodsApi.document_collections_post_dict(self, payload)
        res = r.json()
        self.driver.get(self.settings['wesign_url'])
        self.__login_wesign()
        sleep(1)
        driver = self.driver
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "button--sent-ent")))
        my_documents_section = self.driver.find_element(By.CLASS_NAME, "button--sent-ent")
        my_documents_section.click()
        driver = self.driver
        sleep(3)
        search_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
        search_bar.send_keys(self.document_name)
        sleep(3)
        tds = self.driver.find_elements(By.XPATH, "//tr/td[3]")
        row_index = 2
        for name in tds:
            if name.text == self.document_name:
                row = self.driver.find_element(By.XPATH, f"//table/tbody/tr[{row_index}]")
                sleep(4)
                row.click()
                sleep(3)
                row.click()
                sleep(5)
                row.click()
                sleep(3)
                row.click()
                sleep(5)
                row.click()
                sleep(5)
                row.click()
        index = 2
        sent_document_status = self.driver.find_elements(By.XPATH, "//td/table/tbody/tr/td[3]")
        for sent_status in sent_document_status:
            recipient_email = self.driver.find_element(By.XPATH,f"//table/tbody/tr[3]/td/table/tbody/tr[{index}]/td[2]")
            assert sent_status.text != "", f"Sent status not displayed to {recipient_email.text}"
            index += 1
        for x in res['signerLinks']:
            sleep(2)
            self.driver.get(x['link'])
            driver = self.driver
            sleep(1)
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@name='feather']")))
            self.driver.find_element(By.XPATH, "//*[@name='feather']").click()
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='signature-pad__canvas']")))
            canvas = self.driver.find_element(By.XPATH, "//div[@class='signature-pad__canvas']")
            drawing = ActionChains(self.driver) \
                .click_and_hold(canvas) \
                .move_by_offset(-200, 10) \
                .move_by_offset(-10, -50) \
                .move_by_offset(-25, -10) \
                .move_by_offset(100, -100) \
                .move_by_offset(10, 60) \
                .move_by_offset(10, 100) \
                .move_by_offset(-10, -120) \
                .release()
            drawing.perform()
            for i in range(25):
                action = webdriver.common.action_chains.ActionChains(driver)
                action.move_by_offset(5, 0)  # move 150 pixels to the right to access Help link
                action.click()
                action.perform()
            sleep(3)
            self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
            sleep(1)
            # try:
            #     sleep(1)
            #     WebDriverWait(self.driver, 15).until(
            #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]")))
            #     yes_button = "//button[contains(text(),'Yes')]"
            #     self.driver.find_element(By.XPATH, yes_button).click()
            # except:
            #     sleep(1)
            #     WebDriverWait(self.driver, 15).until(
            #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]")))
            #     yes_button = "//button[contains(text(),'No')]"
            #     self.driver.find_element(By.XPATH, yes_button).click()
            sleep(3)
            self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
            sleep(1)
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
            signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
            assert len(signing_complete_msg) == 1
        sleep(2)
        self.driver.get(self.settings['wesign_url'])
        sleep(1)
        driver = self.driver
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "button--sent-ent")))
        my_documents_section = self.driver.find_element(By.CLASS_NAME, "button--sent-ent")
        my_documents_section.click()
        driver = self.driver
        sleep(3)
        search_bar = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
        search_bar.send_keys(self.document_name)
        sleep(3)
        tds = self.driver.find_elements(By.XPATH, "//tr/td[3]")
        row_index = 2
        for name in tds:
            if name.text == self.document_name:
                row = self.driver.find_element(By.XPATH, f"//table/tbody/tr[{row_index}]")
                sleep(4)
                row.click()
                sleep(3)
        viewed_document_status = self.driver.find_elements(By.XPATH, "//td/table/tbody/tr/td[4]")
        index = 2
        for viewed_status in viewed_document_status:
            recipient_email = self.driver.find_element(By.XPATH,
                                                       f"//table/tbody/tr[3]/td/table/tbody/tr[{index}]/td[2]")
            assert viewed_status.text != "", f"viewed status not displayed to {recipient_email.text}"
            index += 1
        index = 2
        signed_document_status = self.driver.find_elements(By.XPATH, "//td/table/tbody/tr/td[5]")
        for signed_status in signed_document_status:
            recipient_email = self.driver.find_element(By.XPATH,
                                                       f"//table/tbody/tr[3]/td/table/tbody/tr[{index}]/td[2]")
            assert signed_status.text != "", f"signed status not displayed to {recipient_email.text}"
            index += 1

    @pytest.mark.part2
    def test_download_batch_document_collection(self):
        r = WesignMethodsApi.document_collections_get_parameters_download(self)
        assert r.status_code == StatusCode.OK
        response = json.loads(r.content)
        document_collection = response["documentCollections"]
        list_of_ids = []
        for x in document_collection:
            list_of_ids.append(x["documentCollectionId"])
        n = WesignMethodsApi.document_collections_download_batch_post_ids(self, list_of_ids)
        assert n.status_code == StatusCode.OK

    @pytest.mark.part3
    def test_download_batch_with_incorrect_document_id(self):
        r = WesignMethodsApi.document_collections_get_parameters_download(self)
        assert r.status_code == StatusCode.OK
        response = json.loads(r.content)
        document_collection = response["documentCollections"]
        list_of_ids = []
        for x in document_collection:
            list_of_ids.append(x["documentCollectionId"])
        # change the id of the first document
        list_of_ids[0] = '888888e-888e-8888-8620-08dad731f3a6'
        n = WesignMethodsApi.document_collections_download_batch_post_ids(self, list_of_ids)
        assert n.status_code == StatusCode.BAD_REQUEST

    @pytest.mark.part1
    def test_download_batch_with_unsigned_document(self):
        r = WesignMethodsApi.document_collections_unsigned_get_parameters(self)
        assert r.status_code == StatusCode.OK
        response = json.loads(r.content)
        document_collection = response["documentCollections"]
        list_of_ids = []
        for x in document_collection:
            list_of_ids.append(x["documentCollectionId"])
        n = WesignMethodsApi.document_collections_download_batch_post_ids(self, list_of_ids)
        assert n.status_code == StatusCode.BAD_REQUEST

    @pytest.mark.part2
    def test_download_batch_with_30_documents(self):
        r = WesignMethodsApi.document_collections_get_parameters_download(self)
        assert r.status_code == StatusCode.OK
        response = json.loads(r.content)
        document_collection = response["documentCollections"]
        list_of_ids = []
        for x in document_collection:
            list_of_ids.append(x["documentCollectionId"])
        list_len = len(list_of_ids)
        n = WesignMethodsApi.document_collections_download_batch_post_ids(self, list_of_ids)
        if list_len <= 20:
            assert n.status_code == StatusCode.OK
        else:
            assert n.status_code == StatusCode.BAD_REQUEST

    @pytest.mark.part3
    def test_tablet_sign(self):
        create_template = WesignMethodsApi.templates_post_json_file(self, 'CreateTemplatePdfBase64Success')
        template_response = json.loads(create_template.content)
        template_id = template_response["templateId"]
        template_name = template_response["templateName"]
        sig_data = {"name": template_name, "fields": {"signatureFields": [{"signingType": 1, "name": "GG8D", "width": 0.2, "height": 0.5, "page": 1}]}}
        sig_field = WesignMethodsApi.templates_id_put_dict(self, sig_data, template_id)
        assert sig_field.status_code == StatusCode.OK
        template_data = {"documentMode": 1, "documentName": template_name, "templates": [template_id], "Signers": [{"sendingMethod": 3, "contactName": "1", "signerFields": [{"templateId": template_id, "fieldName": "GG8D"}]}]}
        assigned_and_send = WesignMethodsApi.document_collections_post_dict(self, template_data)
        assert assigned_and_send.status_code == StatusCode.OK
        tablet_response = json.loads(assigned_and_send.content)
        document_link = tablet_response["signerLinks"][0]["link"]
        # sign with Selenium
        self.__setup()
        sleep(2)
        self.driver.get(document_link)
        sleep(2)
        self.__sign_on_document()
        sleep(2)
        check_doc = WesignMethodsApi.document_collections_get_parameters_tablet(self, template_name)
        assert check_doc.status_code == StatusCode.OK
        r = json.loads(check_doc.content)
        is_signed = r["documentCollections"][0]["documentStatus"]
        assert is_signed == 4, "document isn't signed"

    @pytest.mark.part1
    def test_send_sms_and_validate_signer1_signed_and_status(self):
        self.__setup()
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {
        "readOnlyFields": [],
          "senderAppendices": [],
          "shouldSignUsingSigner1AfterDocumentSigningFlow": True,
          "signers": [
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "ניר",
              "contactMeans": "0504821887",
              "sendingMethod": 1,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "49d25a80-590f-4cb9-95d9-08db2ad069f9",
                  "fieldName": "Signature_W4mgA"

                },
                {
                  "templateId": "49d25a80-590f-4cb9-95d9-08db2ad069f9",
                  "fieldName": "Text_kIYZg",
                  "fieldValue": ""
                },
                {
                  "templateId": "49d25a80-590f-4cb9-95d9-08db2ad069f9",
                  "fieldName": "Phone_fsnbU",
                  "fieldValue": ""
                },
                {
                  "templateId": "49d25a80-590f-4cb9-95d9-08db2ad069f9",
                  "fieldName": "Number_dwEco",
                  "fieldValue": ""
                },
                {
                  "templateId": "49d25a80-590f-4cb9-95d9-08db2ad069f9",
                  "fieldName": "Date_WHnyO",
                  "fieldValue": ""
                },
                {
                  "templateId": "49d25a80-590f-4cb9-95d9-08db2ad069f9",
                  "fieldName": "Email_dTxM3",
                  "fieldValue": ""
                }
              ]
            }
          ],
          "documentName": document,
          "documentMode": 1,
          "templates": [
            "49d25a80-590f-4cb9-95d9-08db2ad069f9"
          ]
        }
        r = WesignMethodsApi.document_collections_post_dict_using_signer1(self, payload)
        res = r.json()
        for x in res['signerLinks']:
            sleep(2)
            self.driver.get(x['link'])
            driver = self.driver
            sleep(1)
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@name='feather']")))
            self.__add_values_to_all_fields()
            self.driver.find_element(By.XPATH, "//*[@name='feather']").click()
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='signature-pad__canvas']")))
            canvas = self.driver.find_element(By.XPATH, "//div[@class='signature-pad__canvas']")
            drawing = ActionChains(self.driver) \
                .click_and_hold(canvas) \
                .move_by_offset(-200, 10) \
                .move_by_offset(-10, -50) \
                .move_by_offset(-25, -10) \
                .move_by_offset(100, -100) \
                .move_by_offset(10, 60) \
                .move_by_offset(10, 100) \
                .move_by_offset(-10, -120) \
                .release()
            drawing.perform()
            for i in range(25):
                action = webdriver.common.action_chains.ActionChains(driver)
                action.move_by_offset(5, 0)  # move 150 pixels to the right to access Help link
                action.click()
                action.perform()
            sleep(2)
            self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
            sleep(1)
            # try:
            #     sleep(1)
            #     WebDriverWait(self.driver, 15).until(
            #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]")))
            #     yes_button = "//button[contains(text(),'Yes')]"
            #     self.driver.find_element(By.XPATH, yes_button).click()
            # except:
            #     sleep(1)
            #     WebDriverWait(self.driver, 15).until(
            #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]")))
            #     yes_button = "//button[contains(text(),'No')]"
            #     self.driver.find_element(By.XPATH, yes_button).click()
            sleep(3)
            self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
            sleep(1)
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
            signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
            assert len(signing_complete_msg) == 1
            sleep(3)
            self.driver.get(self.settings['wesign_url'])
            self.__login_wesign_signer1()
            sleep(1)
            driver = self.driver
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "button--sent-ent")))
            my_documents_section = self.driver.find_element(By.CLASS_NAME, "button--sent-ent")
            my_documents_section.click()
            driver = self.driver
            sleep(3)
            search_bar = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
            search_bar.send_keys(self.document_name)
            sleep(2)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[2]/td[6]")))
            signed_status = self.driver.find_element(By.XPATH, "//table/tbody/tr[2]/td[6]")
            assert signed_status.text == 'Server signed', "Signed status is incorrect"

    @pytest.mark.part2
    def test_send_document_with_same_signature_field_name(self):
        request = {
              "signers": [
                {
                  "otpMode": 0,
                  "authenticationMode": 0,
                  "contactName": "nirk",
                  "contactMeans": "nirk@comsign.co.il",
                  "sendingMethod": 2,
                  "phoneExtension": "+972",
                  "signerFields": [
                    {
                      "templateId": "4e8f5005-7c8b-4f4b-2569-08db02cf2bee",
                      "fieldName": "Signature_89a1k"
                    }
                  ]
                },
                {
                  "otpMode": 0,
                  "authenticationMode": 0,
                  "contactName": "devtest1 devtest1",
                  "contactMeans": "devtest1@comda.co.il",
                  "sendingMethod": 2,
                  "phoneExtension": "+972",
                  "signerFields": [
                    {
                      "templateId": "4e8f5005-7c8b-4f4b-2569-08db02cf2bee",
                      "fieldName": "Signature_89a1k"
                    }
                  ]
                }
              ],
              "documentName": "Dummy3Pages",
              "documentMode": 1,
              "templates": [
                "4e8f5005-7c8b-4f4b-2569-08db02cf2bee"
              ]
            }
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documentcollections', data=json.dumps(request),headers=headers)
        res = r.json()
        error = res['errors']['Signers'][0]
        assert str(error) == Enums.status_codes.ResultCode.SAME_FIELD_NAME

    @pytest.mark.part3
    def test_sending_to_25_recipients_and_sign_by_order_and_validate_document_status(self):
        self.__setup()
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {
            "readOnlyFields": [],
            "senderAppendices": [],
            "shouldSignUsingSigner1AfterDocumentSigningFlow": False,
            "signers": [
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest1",
                    "contactMeans": "devtest1@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_FzfI7",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest2",
                    "contactMeans": "devtest2@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_28lsE",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest3",
                    "contactMeans": "devtest3@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_xXMjz",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest4",
                    "contactMeans": "devtest4@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_zcF5u",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest5",
                    "contactMeans": "devtest5@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_9m7PE",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest6",
                    "contactMeans": "devtest6@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_4QzbT",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest7",
                    "contactMeans": "devtest7@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_udOeg",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest8",
                    "contactMeans": "devtest8@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_WjDQS",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest9",
                    "contactMeans": "devtest9@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_HPqM6",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest10",
                    "contactMeans": "devtest10@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_Pgh4X",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest1",
                    "contactMeans": "devtest1@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_CgwIJ",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest2",
                    "contactMeans": "devtest2@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_SEEFD",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest3",
                    "contactMeans": "devtest3@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_0Rw3v",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest4",
                    "contactMeans": "devtest4@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_k04Kz",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest5",
                    "contactMeans": "devtest5@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_3lYlH",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest6",
                    "contactMeans": "devtest6@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_ReQrM",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest7",
                    "contactMeans": "devtest7@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_oa4bJ",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest8",
                    "contactMeans": "devtest8@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_OMYuf",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest9",
                    "contactMeans": "devtest9@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_W7RCK",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest10",
                    "contactMeans": "devtest10@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_9Imis",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest1",
                    "contactMeans": "devtest1@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_NVeiY",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest2",
                    "contactMeans": "devtest2@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_Ni0lh",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest3",
                    "contactMeans": "devtest3@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_ovnUw",

                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest4",
                    "contactMeans": "devtest4@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_gGRnZ",
                        }
                    ]
                },
                {
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "contactName": "devtest5",
                    "contactMeans": "devtest5@comda.co.il",
                    "sendingMethod": 2,
                    "phoneExtension": "+972",
                    "signerFields": [
                        {
                            "templateId": "62226367-0456-4a82-6a5a-08daddc7e4e7",
                            "fieldName": "Signature_YTICB",

                        }
                    ]
                }
            ],
            "documentName": self.document_name,
            "documentMode": 1,
            "templates": [
                "62226367-0456-4a82-6a5a-08daddc7e4e7"
            ]
        }
        r = WesignMethodsApi.document_collections_post_dict(self, payload)
        res = r.json()
        documentCollectionId = res['documentCollectionId']
        index = 0
        for a in range(25):
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            cursor = conn.cursor()
            b = cursor.execute(f"SELECT * from [SignerTokensMapping] where [DocumentCollectionId] = '{documentCollectionId}'")
            links = []
            result = b.fetchall()

            for x in result:
                links.append(x[3])

            sleep(5)
            self.driver.get(f"https://devtest.comda.co.il/signer/signature/{links[index]}")
            driver = self.driver
            sleep(1)
            WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@name='feather']")))
            self.driver.find_element(By.XPATH, "//*[@name='feather']").click()
            WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='signature-pad__canvas']")))
            canvas = self.driver.find_element(By.XPATH, "//div[@class='signature-pad__canvas']")
            drawing = ActionChains(self.driver) \
                .click_and_hold(canvas) \
                .move_by_offset(-200, 10) \
                .move_by_offset(-10, -50) \
                .move_by_offset(-25, -10) \
                .move_by_offset(100, -100) \
                .move_by_offset(10, 60) \
                .move_by_offset(10, 100) \
                .move_by_offset(-10, -120) \
                .release()
            drawing.perform()
            for i in range(25):
                action = webdriver.common.action_chains.ActionChains(driver)
                action.move_by_offset(5, 0)  # move 150 pixels to the right to access Help link
                action.click()
                action.perform()
            sleep(3)
            self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
            sleep(1)
            # try:
            #     sleep(1)
            #     WebDriverWait(self.driver, 15).until(
            #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]")))
            #     yes_button = "//button[contains(text(),'Yes')]"
            #     self.driver.find_element(By.XPATH, yes_button).click()
            # except:
            #     sleep(1)
            #     WebDriverWait(self.driver, 15).until(
            #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]")))
            #     yes_button = "//button[contains(text(),'No')]"
            #     self.driver.find_element(By.XPATH, yes_button).click()
            sleep(3)
            self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
            sleep(1)
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
            signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
            assert len(signing_complete_msg) == 1
            links.clear()
            sleep(5)
            index += 1

    #Task WES-1446
    @pytest.mark.part1
    def test_sending_10_recipients_by_order_validate_return_next_signer_link_by_order(self):
        self.__setup()
        self.driver.execute_script("window.open('');")
        sleep(3)
        self.driver.get(self.settings['wesign_url'])
        self.__login_wesign()
        WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "button--sent-ent")))
        my_documents_section = self.driver.find_element(By.CLASS_NAME, "button--sent-ent")
        my_documents_section.click()
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {
                "documentMode": 1,
                "documentName": self.document_name,
                "templates": [
                "ea6f0e73-4532-4d57-caa6-08dc26dc0c42"
                ],
                "signers": [
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest1@comda.co.il",
                    "contactName": "devtest1",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest2@comda.co.il",
                    "contactName": "devtest2",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest3@comda.co.il",
                    "contactName": "devtest3",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest4@comda.co.il",
                    "contactName": "devtest4",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest5@comda.co.il",
                    "contactName": "devtest5",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest6@comda.co.il",
                    "contactName": "devtest6",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest7@comda.co.il",
                    "contactName": "devtest7",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest8@comda.co.il",
                    "contactName": "devtest8",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest9@comda.co.il",
                    "contactName": "devtest9",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                # {
                #     "sendingMethod": 2,
                #     "contactMeans": "devtest10@comda.co.il",
                #     "contactName": "devtest10",
                #     "otpMode": 0,
                #     "authenticationMode": 0,
                #     "phoneExtension": "+972"
                # },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest11@comda.co.il",
                    "contactName": "devtest11",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                }
                ],
            }
        r = WesignMethodsApi.document_collections_post_dict(self, payload)
        res = r.json()
        documentCollectionId = res['documentCollectionId']
        documentCollectionLink = res['signerLinks'][0]['link']
        sleep(3)
        next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self, documentCollectionId)
        link = next_link.json()
        assert documentCollectionLink == link[0]['link']
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(10)
        self.driver.get(documentCollectionLink)
        sleep(5)
        self.__sign_document_using_finish_button()
        sleep(1)
        WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(2)
        search_bar = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
        search_bar.send_keys(self.document_name)
        index = 2
        row_index = 2
        my_list = [11, 10, 9, 8, 7, 6, 5, 4]
        for x in range(8):
            sleep(2)
            self.driver.switch_to.window(self.driver.window_handles[0])
            sleep(3)
            row = self.driver.find_element(By.XPATH, f"//table/tbody/tr[2]")
            sleep(4)
            row.click()
            sleep(3)
            signed_document_status = self.driver.find_elements(By.XPATH, f"//td/table/tbody/tr[{row_index}]/td[5]")
            for signed_status in signed_document_status:
                recipient_email = self.driver.find_element(By.XPATH,
                                                           f"//table/tbody/tr[3]/td/table/tbody/tr[{index}]/td[2]")
                assert signed_status.text != "", f"signed status not displayed to {recipient_email.text}"
                index += 1
                row_index += 1
                sleep(2)
                break
            for index in my_list:
                sent_status = self.driver.find_element(By.XPATH, f"//table/tbody/tr[{index}]/td[3]")
                recipient_email = self.driver.find_element(By.XPATH,
                                                           f"//table/tbody/tr[3]/td/table/tbody/tr[{index}]/td[2]")
                assert sent_status.text == "", f"Sent status displayed to {recipient_email.text}"
                sleep(2)
            row.click()
            try:
                my_list.pop()
            except:
                pass
            sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[1])
            sleep(1)
            new_next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self,
                                                                                                   documentCollectionId)
            link = new_next_link.json()
            assert documentCollectionLink != link[0]['link']
            self.driver.get(link[0]['link'])
            sleep(2)
            self.__sign_document_using_finish_button()
            sleep(1)
            WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
            signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
            assert len(signing_complete_msg) == 1
            link[0]['link'] = documentCollectionLink

        new_next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self,documentCollectionId)
        link = new_next_link.json()
        assert documentCollectionLink != link[0]['link']
        self.driver.get(link[0]['link'])
        sleep(2)
        self.__sign_document_using_finish_button()
        sleep(1)
        WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(3)
        row = self.driver.find_element(By.XPATH, f"//table/tbody/tr[2]")
        sleep(4)
        row.click()
        sleep(3)
        signed_document_status = self.driver.find_elements(By.XPATH, f"//td/table/tbody/tr[12]/td[5]")
        for signed_status in signed_document_status:
            recipient_email = self.driver.find_element(By.XPATH,
                                                       f"//table/tbody/tr[3]/td/table/tbody/tr[{index}]/td[2]")
            assert signed_status.text != "", f"signed status not displayed to {recipient_email.text}"

    @pytest.mark.part2
    def test_return_next_link_in_case_first_signer_declined(self):
        self.__setup()
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {
            "documentMode": 1,
            "documentName": self.document_name,
            "templates": [
                "ea6f0e73-4532-4d57-caa6-08dc26dc0c42"
            ],
            "signers": [
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest1@comda.co.il",
                    "contactName": "devtest1",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "devtest2@comda.co.il",
                    "contactName": "devtest2",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                }
            ],
        }
        r = WesignMethodsApi.document_collections_post_dict(self, payload)
        res = r.json()
        documentCollectionId = res['documentCollectionId']
        documentCollectionLink = res['signerLinks'][0]['link']
        next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self, documentCollectionId)
        link = next_link.json()
        assert documentCollectionLink == link[0]['link']
        sleep(2)
        self.driver.get(documentCollectionLink)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "menuButton")))
        menu_button = 'menuButton'
        self.driver.find_element(By.ID, menu_button).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "color--error")))
        decline_document = 'color--error'
        self.driver.find_element(By.CLASS_NAME, decline_document).click()
        sleep(1)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/app-main-signer/body/div/app-second-header/div/app-menu/app-decline/div/div/div/input")))
        value_in_decline_window = "/html/body/app-root/app-main-signer/body/div/app-second-header/div/app-menu/app-decline/div/div/div/input"
        self.driver.find_element(By.XPATH, value_in_decline_window).send_keys("Test")
        sleep(1)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '(//*[@class="ct-button--primary"])[2]')))
        submit_button_in_decline_window = '(//*[@class="ct-button--primary"])[2]'
        sleep(3)
        self.driver.find_element(By.XPATH, submit_button_in_decline_window).click()
        sleep(3)
        WebDriverWait(self.driver, 20).until(EC.url_to_be(('https://devtest.comda.co.il/signer/decline')))
        next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self, documentCollectionId)
        response = next_link.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.SIGNER_SIGNED_OR_DECLINE
        return documentCollectionId

    @pytest.mark.part3
    def test_return_next_link_in_case_document_complete(self):
        self.__setup()
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {
            "documentMode": 1,
            "documentName": self.document_name,
            "templates": [
                "ea6f0e73-4532-4d57-caa6-08dc26dc0c42"
            ],
            "signers": [
                {
                    "sendingMethod": 2,
                    "contactMeans": "0a2e9c6a114948d1a7d200c20bdec1ec_1@comda.co.il",
                    "contactName": "0a2e9c6a114948d1a7d200c20bdec1ec",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "3efc3b51fa3743beb941291b35392a20_11@comda.co.il",
                    "contactName": "3efc3b51fa3743beb941291b35392a76",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                }
            ],
        }
        r = WesignMethodsApi.document_collections_post_dict(self, payload)
        res = r.json()
        documentCollectionId = res['documentCollectionId']
        documentCollectionLink = res['signerLinks'][0]['link']
        next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self, documentCollectionId)
        link = next_link.json()
        assert documentCollectionLink == link[0]['link']
        self.driver.get(documentCollectionLink)
        self.__sign_document_using_finish_button()
        sleep(1)
        WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        sleep(4)
        second_next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self, documentCollectionId)
        link = second_next_link.json()
        assert documentCollectionLink != link[0]['link']
        self.driver.get(link[0]['link'])
        self.__sign_document_using_finish_button()
        WebDriverWait(self.driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self, documentCollectionId)
        response = next_link.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.SIGNER_SIGNED_OR_DECLINE
        return documentCollectionId

    @pytest.mark.part1
    def test_check_links_not_return_in_case_document_not_belong_to_user(self):
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {
              "documentMode": 1,
              "documentName": self.document_name,
              "templates": [
                "152885d0-f724-473e-e0e4-08dc27a4efe7"
              ],
              "signers": [
                {
                  "sendingMethod": 2,
                  "contactMeans": "devtest1@comda.co.il",
                  "contactName": "devtest1",
                },
                {
                  "sendingMethod": 2,
                  "contactMeans": "devtest2@comda.co.il",
                  "contactName": "devtest2",
                }
              ],
              "shouldSignUsingSigner1AfterDocumentSigningFlow": True
            }
        r = WesignMethodsApi.document_collections_post_dict_using_signer1(self, payload)
        res = r.json()
        documentCollectionId = res['documentCollectionId']
        next_link = WesignMethodsApi.document_collections_id_get_document_collection_links(self, documentCollectionId)
        response = next_link.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.DOCUMENT_NOT_BELONG_TO_USER_OR_GROUP

    @pytest.mark.part2
    def test_notification_from_callback_when_user_sign(self):
        doc_id = self.test_return_next_link_in_case_document_complete()
        sleep(4)
        response = requests.get(self.settings['call_back_url'])
        data = response.json()
        document_collection_ids = [item['documentCollectionId'] for item in data]
        assert doc_id in document_collection_ids
        specific_document_collection_id = doc_id

        for item in data:
            if item['documentCollectionId'] == specific_document_collection_id:
                if item['documentStatus'] == 4 or item['documentStatus'] == 3:
                    assert item['notificationType'] == 1  ##Document Signed
                else:
                    raise AssertionError(f"Document {specific_document_collection_id} status is not 4: the status is : {item['documentStatus']} for signer name {item['signerName']}")

    @pytest.mark.part3
    def test_notification_from_callback_when_user_document_declined(self):
        doc_id = self.test_return_next_link_in_case_first_signer_declined()
        response = requests.get(self.settings['call_back_url'])
        data = response.json()
        document_collection_ids = [item['documentCollectionId'] for item in data]
        assert doc_id in document_collection_ids
        specific_document_collection_id = doc_id

        for item in data:
            if item['documentCollectionId'] == specific_document_collection_id:
                if item['documentStatus'] == 5:
                    assert item['notificationType'] == 2 ##Rejected
                    assert item['signerMessage'] == 'Test'
                break

    @pytest.mark.part1
    def test_notification_from_callback_when_document_deleted(self):
        doc_id = self.test_return_next_link_in_case_document_complete()
        sleep(4)
        response = requests.get(self.settings['call_back_url'])
        data = response.json()
        document_collection_ids = [item['documentCollectionId'] for item in data]
        assert doc_id in document_collection_ids
        WesignMethodsApi.document_collections_id_delete(self,doc_id)
        response = requests.get(self.settings['call_back_url'])
        data = response.json()
        filtered_data = [obj for obj in data if obj['notificationType'] == 3]
        specific_document_collection_id = doc_id
        assert any(obj['documentCollectionId'] == specific_document_collection_id for obj in filtered_data), f"Document collection ID '{specific_document_collection_id}' not found in notificationType: 3"

    ##WES-1455
    @pytest.mark.part2
    def test_notification_from_callback_when_document_canceled(self):
        doc_id = self.test_document_collection_document_sending_success()
        sleep(1.5)
        WesignMethodsApi.document_collections_id_cancel_put(self,doc_id)
        response = requests.get(self.settings['call_back_url'])
        data = response.json()
        document_collection_ids = [item['documentCollectionId'] for item in data]
        assert doc_id in document_collection_ids
        WesignMethodsApi.document_collections_id_delete(self,doc_id)
        response = requests.get(self.settings['call_back_url'])
        data = response.json()
        filtered_data = [obj for obj in data if obj['notificationType'] == 4]
        specific_document_collection_id = doc_id
        assert any(obj['documentCollectionId'] == specific_document_collection_id for obj in filtered_data), f"Document collection ID '{specific_document_collection_id}' not found in notificationType: 4"

    ##Task WES-1650
    @pytest.mark.part2
    def test_notification_from_callback_when_document_deleted_after_creation_time_pending_status(self):
        doc_id = self.test_return_next_link_in_case_document_complete()
        sleep(2.5)
        conn = pyodbc.connect(f'Driver=SQL Server;'
                              "Server=DEVTEST\SQLEXPRESS;"
                              f'Database={self.settings["db_name"]};'
                              f'UID={self.settings["db_user"]};'
                              F'PWD={self.settings["db_password"]};'
                              'Trusted_Connection=no;')
        cursor = conn.cursor()
        cursor.execute(f"update [DocumentCollections] set [CreationTime] = DATEADD(DAY, -361, GETDATE()) where [Id] = '{doc_id}'")
        conn.commit()
        self.driver.get(self.settings['jobs_url'])
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr[1]/td[1]/input")))
        self.driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[1]/input").click()
        sleep(2)
        self.driver.find_element(By.XPATH, "//*[@id='wrap']/div[2]/div/div/div/div[1]/button[1]").click()
        sleep(4)
        response = requests.get(self.settings['call_back_url'])
        data = response.json()
        document_collection_ids = [item['documentCollectionId'] for item in data]
        assert doc_id in document_collection_ids
        specific_document_collection_id = doc_id

        for item in data:
            if item['documentCollectionId'] == specific_document_collection_id:
                if item['notificationType'] == 3:
                    assert item['documentStatus'] == 3 or item['documentStatus'] == 4 ##Document Signed
                    break
        else:
            raise AssertionError(f"Document {specific_document_collection_id} status is not 4: the status is : {item['documentStatus']} for signer name {item['signerName']}")

    ##Task WES-1650
    @pytest.mark.part1
    def test_notification_from_callback_when_document_deleted_after_creation_time_sign_status(self):
        self.__setup()
        r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionDocumentSendingWithTextFieldSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        doc_id = response['documentCollectionId']
        sleep(2.5)
        conn = pyodbc.connect(f'Driver=SQL Server;'
                              "Server=DEVTEST\SQLEXPRESS;"
                              f'Database={self.settings["db_name"]};'
                              f'UID={self.settings["db_user"]};'
                              F'PWD={self.settings["db_password"]};'
                              'Trusted_Connection=no;')
        cursor = conn.cursor()
        cursor.execute(
            f"update [DocumentCollections] set [CreationTime] = DATEADD(DAY, -361, GETDATE()) where [Id] = '{doc_id}'")
        conn.commit()
        self.driver.get(self.settings['jobs_url'])
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr[1]/td[1]/input")))
        self.driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[1]/input").click()
        sleep(2)
        self.driver.find_element(By.XPATH, "//*[@id='wrap']/div[2]/div/div/div/div[1]/button[1]").click()
        sleep(4)
        response = requests.get(self.settings['call_back_url'])
        data = response.json()
        document_collection_ids = [item['documentCollectionId'] for item in data]
        assert doc_id in document_collection_ids
        specific_document_collection_id = doc_id
        for item in data:
            if item['documentCollectionId'] == specific_document_collection_id:
                if item['notificationType'] == 3:
                    assert item['documentStatus'] == 2
                    break
        else:
            raise AssertionError(f"Document {specific_document_collection_id} not displayed oin callback list")

    @pytest.mark.part3
    def test_get_template_id_extra_info_json_from_document_collection(self):
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {

                "documentMode": 1,
                "documentName": "TestExtraInfo",
                "templates": [
                    "0ac12edc-c2d9-4c83-e0b1-08dba9464fd6",
                    "fb26b42c-bdf2-4985-ecf7-08dbb9bf94fe",
                    "df464772-5b52-4d17-084e-08db9447b91a",
                    "2f69b46c-7a32-4bdc-d759-08db88198799"
                ],
                "signers": [
                    {
                        "sendingMethod": 2,
                        "contactMeans": "nirk@comsign.co.il",
                        "contactName": "nirk",
                    }
                ],


        }
        r = WesignMethodsApi.document_collections_post_dict(self, payload)
        res = r.json()
        documentCollectionId = res['documentCollectionId']
        templates = ["0ac12edc-c2d9-4c83-e0b1-08dba9464fd6",
                    "fb26b42c-bdf2-4985-ecf7-08dbb9bf94fe",
                    "df464772-5b52-4d17-084e-08db9447b91a",
                    "2f69b46c-7a32-4bdc-d759-08db88198799"]
        info = WesignMethodsApi.document_collections_id_get_extra_info_json(self,documentCollectionId)
        json_obj = info.json()

        ids_in_json = [item["templateId"] for item in json_obj["files"]]

        for template_id in templates:
            assert template_id in ids_in_json, f"Template with ID {template_id} not found in JSON data."

    @pytest.mark.part1
    def test_export_distribution_documents(self):
        r = WesignMethodsApi.document_collections_export_distribution(self)
        assert r.status_code == StatusCode.OK

    @pytest.mark.part2
    def test_export_document_collection_data_fields_to_json_with_signatures(self):
        get_fields_info_json = WesignMethodsApi.document_collections_id_get_data_fields_info_json(self, True)
        response = get_fields_info_json.json()
        assert len(response['signatureFields'][0]['image']) > 5000

    ##WES-1512
    @pytest.mark.part3
    def test_export_document_collection_data_fields_to_json_without_signatures(self):
        get_fields_info_json = WesignMethodsApi.document_collections_id_get_data_fields_info_json(self, False)
        data = get_fields_info_json.json()
        fields = []
        for field in data['textFields']:
            assert field['value'] != ''
            fields.append([field['value']])

    @pytest.mark.part1
    def test_reactive_document(self):
        self.__setup()
        document = uuid.uuid4().hex
        self.document_name = document
        payload = {
            "documentMode": 1,
            "documentName": self.document_name,
            "templates": [
                "ea6f0e73-4532-4d57-caa6-08dc26dc0c42"
            ],
            "signers": [
                {
                    "sendingMethod": 2,
                    "contactMeans": "0a2e9c6a114948d1a7d200c20bdec1ec_1@comda.co.il",
                    "contactName": "0a2e9c6a114948d1a7d200c20bdec1ec",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                },
                {
                    "sendingMethod": 2,
                    "contactMeans": "3efc3b51fa3743beb941291b35392a20_11@comda.co.il",
                    "contactName": "3efc3b51fa3743beb941291b35392a76",
                    "otpMode": 0,
                    "authenticationMode": 0,
                    "phoneExtension": "+972"
                }
            ],
        }
        r = WesignMethodsApi.document_collections_post_dict(self, payload)
        res = r.json()
        documentCollectionId = res['documentCollectionId']
        documentCollectionLink = res['signerLinks'][0]['link']
        self.driver.get(documentCollectionLink)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "menuButton")))
        menu_button = 'menuButton'
        self.driver.find_element(By.ID, menu_button).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "color--error")))
        decline_document = 'color--error'
        self.driver.find_element(By.CLASS_NAME, decline_document).click()
        sleep(1)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/app-root/app-main-signer/body/div/app-second-header/div/app-menu/app-decline/div/div/div/input")))
        value_in_decline_window = "/html/body/app-root/app-main-signer/body/div/app-second-header/div/app-menu/app-decline/div/div/div/input"
        self.driver.find_element(By.XPATH, value_in_decline_window).send_keys("Test")
        sleep(1)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '(//*[@class="ct-button--primary"])[2]')))
        submit_button_in_decline_window = '(//*[@class="ct-button--primary"])[2]'
        sleep(3)
        self.driver.find_element(By.XPATH, submit_button_in_decline_window).click()
        sleep(3)
        WebDriverWait(self.driver, 20).until(EC.url_to_be(('https://devtest.comda.co.il/signer/decline')))
        sleep(5)
        reactive = WesignMethodsApi.document_collections_reactive(self,documentCollectionId)
        links_response = reactive.json()
        new_link = links_response[0]['link']
        self.driver.get(new_link)
        WebDriverWait(self.driver, 50).until(
            EC.element_to_be_clickable((By.ID, "menuButton")))

    @pytest.mark.part2
    def test_delete_documents_from_db(self):
        documents = []
        for x in range(25):
            r = WesignMethodsApi.document_collections_post_json_file(self,'DocumentCollectionTestDeletFromDb')
            assert r.status_code == StatusCode.OK
            response = r.json()
            doc_id = response['documentCollectionId']
            documents.append(doc_id)

        sleep(45)

        for y in range(len(documents)):
            sleep(2)
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            cursor = conn.cursor()
            b = cursor.execute(
                f"SELECT * from [DocumentCollections] where [Id] = '{documents[y]}'")
            status = b.fetchall()
            sleep(2)
            assert status[0][4] == 2, f"Document {documents[y]} not in correct status" ##Sent / pending status

        sleep(30)

        for i in range(len(documents)):
            sleep(2)
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            cursor = conn.cursor()
            d = cursor.execute(
                f"update DocumentCollections set Status = 7 where Id = '{documents[i]}'")
            d.commit()
            sleep(2)

        sleep(25)

        for n in range(len(documents)):
            sleep(2)
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            cursor = conn.cursor()
            b = cursor.execute(
                f"SELECT * from [DocumentCollections] where [Id] = '{documents[n]}'")
            status = b.fetchall()
            sleep(2)
            assert status[0][4] == 7, f"Document {documents[n]} not in delete status" ##Sent / pending status
        self.__setup()
        self.driver.get(self.settings['jobs_url'])
        WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr[1]/td[1]/input")))
        self.driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[1]/input").click()
        sleep(2)
        self.driver.find_element(By.XPATH, "//*[@id='wrap']/div[2]/div/div/div/div[1]/button[1]").click()
        sleep(30)

        for m in range(len(documents)):
            sleep(2)
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            a = conn.execute(f"SELECT COUNT(*) FROM DocumentCollections where Id = '{documents[m]}'")
            row_count = a.fetchone()
            sleep(2)
            assert str(row_count) == '(0, )' or str(row_count) == '(0,)'

    @pytest.mark.part3
    def test_delete_documents_from_db_after_x_days_delete_company_configuration(self):
        documents = []
        for x in range(10):
            r = WesignMethodsApi.document_collections_post_json_file(self, 'DocumentCollectionTestDeletFromDb')
            assert r.status_code == StatusCode.OK
            response = r.json()
            doc_id = response['documentCollectionId']
            documents.append(doc_id)

        sleep(45)

        for y in range(len(documents)):
            sleep(2.5)

            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            cursor = conn.cursor()
            b = cursor.execute(
                f"SELECT * from [DocumentCollections] where [Id] = '{documents[y]}'")
            status = b.fetchall()
            sleep(2.5)
            assert status[0][4] == 2, f"Document {documents[y]} not in correct status"  ##Sent / pending status

        for i in range(len(documents)):
            sleep(2.5)
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            cursor = conn.cursor()
            cursor.execute(f"update [DocumentCollections] set [CreationTime] = DATEADD(DAY, -361, GETDATE()) where [Id] = '{documents[i]}'")
            conn.commit()
            sleep(1)

        self.__setup()
        self.driver.get(self.settings['jobs_url'])
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr[1]/td[1]/input")))
        self.driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[1]/input").click()
        sleep(2)
        self.driver.find_element(By.XPATH, "//*[@id='wrap']/div[2]/div/div/div/div[1]/button[1]").click()
        sleep(40)
        for m in range(len(documents)):
            sleep(2.5)
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            a = conn.execute(f"SELECT COUNT(*) FROM DocumentCollections where Id = '{documents[m]}'")
            row_count = a.fetchone()
            sleep(2.5)
            assert str(row_count) == '(0, )' or str(row_count) == '(0,)'

    # def test_token_saml(self):
    #     headers = {'content-type': 'application/json', 'IDNum': 'nirk2023', 'samlAssertion': 'PHNhbWw6QXNzZXJ0aW9uIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjEuMDphc3NlcnRpb24iIEFzc2VydGlvbklEPSJpZDlPVC1Vbk5lZ09BUDV3N2xxdFM5aDVWckdOQSIgSXNzdWVJbnN0YW50PSIyMDIzLTA4LTAxVDA5OjExOjI1WiIgSXNzdWVyPSJodHRwczovL3N0LmxvZ2luLmdvdi5pbC9uaWRwL2lkZmYvbWV0YWRhdGEiIE1ham9yVmVyc2lvbj0iMSIgTWlub3JWZXJzaW9uPSIxIj48c2FtbDpDb25kaXRpb25zIE5vdE9uT3JBZnRlcj0iMjAyMy0wOC0wMVQxMDoxMToyNVoiLz48c2FtbDpBdXRoZW50aWNhdGlvblN0YXRlbWVudCBBdXRoZW50aWNhdGlvbkluc3RhbnQ9IjIwMjMtMDgtMDFUMDk6MTE6MjVaIiBBdXRoZW50aWNhdGlvbk1ldGhvZD0idXJuOmlldGY6cmZjOjIyNDYiPjxzYW1sOlN1YmplY3Q+PHNhbWw6TmFtZUlkZW50aWZpZXIgRm9ybWF0PSIjWDUwOVN1YmplY3ROYW1lIj5jbj0wMzk1MjkyNDMsb3U9MyxvdT1Vc2VycyxvPUdPVixjPUlMPC9zYW1sOk5hbWVJZGVudGlmaWVyPjwvc2FtbDpTdWJqZWN0Pjwvc2FtbDpBdXRoZW50aWNhdGlvblN0YXRlbWVudD48ZHM6U2lnbmF0dXJlIHhtbG5zOmRzPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjIj4KPGRzOlNpZ25lZEluZm8+CjxkczpDYW5vbmljYWxpemF0aW9uTWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS8xMC94bWwtZXhjLWMxNG4jIi8+CjxkczpTaWduYXR1cmVNZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjcnNhLXNoYTEiLz4KPGRzOlJlZmVyZW5jZSBVUkk9IiNpZDlPVC1Vbk5lZ09BUDV3N2xxdFM5aDVWckdOQSI+CjxkczpUcmFuc2Zvcm1zPgo8ZHM6VHJhbnNmb3JtIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnI2VudmVsb3BlZC1zaWduYXR1cmUiLz4KPGRzOlRyYW5zZm9ybSBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnLzIwMDEvMTAveG1sLWV4Yy1jMTRuIyIvPgo8L2RzOlRyYW5zZm9ybXM+CjxkczpEaWdlc3RNZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjc2hhMSIvPgo8ZHM6RGlnZXN0VmFsdWU+eXZNVTBrVXN5VnpYZ2RuWlk4SXNZcUpLQ3I4PTwvZHM6RGlnZXN0VmFsdWU+CjwvZHM6UmVmZXJlbmNlPgo8L2RzOlNpZ25lZEluZm8+CjxkczpTaWduYXR1cmVWYWx1ZT4KZjNYZzRTVTdTVm0wTERFNFVoWno2MkRDWFI0a2JuajFzcmx6ZnVqdXZBZzlJN3RoemtDL0dVVkt4d3JPT3RpR1NkU2lqbWJjQ2xWbgpsc01qOENRckY3c1JoVmQ4Q1RIa2JBODRLWlhDVFdRVkpBa3g3dGcraStOYnJpbjRJc1o2RFNENHNKVUh0YlIxVEJCTS9ZQ3pMZndHCmFKTzVwTldDNU5GdUlwcjEweCtGL215bTA5K2h4a2lnOUt5UTRRRi9RK0kwRWtDeGd1N251ZEppMVozeHpBQitJaTRBVXJZR3pEQmcKQW01M2wxZi80cnpPM1d0N3k3aGJ0TVhIMys4b3d6eThTOUE3ZFR4MXZldlNiblBMN1NGc2phclNrUkhsSWJhVVl2SHJvNTdGRGZCSworN1c5cWxzTlJESW03MWpVcEpDdC9DR014bk5mcXI1MXNBNE1LZz09CjwvZHM6U2lnbmF0dXJlVmFsdWU+CjxkczpLZXlJbmZvPgo8ZHM6WDUwOURhdGE+CjxkczpYNTA5Q2VydGlmaWNhdGU+Ck1JSUdYRENDQkVTZ0F3SUJBZ0lUT1FBQWtKa1pObUFLWk1lUG5RQUFBQUNRbVRBTkJna3Foa2lHOXcwQkFRc0ZBREJLTVFzd0NRWUQKVlFRR0V3SkpUREVkTUJzR0ExVUVDaE1VUjI5MlpYSnViV1Z1ZENCdlppQkpjM0poWld3eEhEQWFCZ05WQkFNVEUxUkJUVlZhTFVSbApkbWxqWlhNZ1EwRWdSekl3SGhjTk1qSXhNVEF6TVRBd056RTNXaGNOTWpjeE1UQXlNVEF3TnpFM1dqQi9NUXN3Q1FZRFZRUUdFd0pKClRERVBNQTBHQTFVRUNCTUdTWE55WVdWc01SSXdFQVlEVlFRSEV3bEtaWEoxYzJGc1pXMHhJVEFmQmdOVkJBb1RHRWR2ZG1WeWJtMWwKYm5RZ1NVTlVJRUYxZEdodmNtbDBlVEVNTUFvR0ExVUVDeE1EUTBsUE1Sb3dHQVlEVlFRREV4RnpkQzV6YVdkdWFXNW5MbWR2ZGk1cApiRENDQVNJd0RRWUpLb1pJaHZjTkFRRUJCUUFEZ2dFUEFEQ0NBUW9DZ2dFQkFOUjFyQXFMVnJFNElUcEJybzlCMTd0b0YyQnR2RVp5ClJPKzRWOUNhK3o3TTlEQUFSQW5McCtmVmJ4SmdKWS9Ea1Blemg2MEZ1NDBKei9PU2tiemRPQSs4M1ZBQVNpVFpGMWgvVS9DN2dieDkKMHF3eDRJWWRwOUtEQTFHV0xlcVJqSVUxNVJiQThqZkovbmRxbG5uMHdmUVM2MThQNStBM2ljVHhMWTRDMENvcUl6aXRhYzROYnhyZApWd2p1SHJZWHE4UFFvTVdEVTl6UG54ZXpjd1RicEZLWDdtbEpjODdDWm9BVGUvSktlRndYK2NXTUhIZjBZbE5VcERhNGVIdEc5dzVkCnVmc0VvOUtCa0E5eGZwVnhZem50SHBrU3RlaDV1UGxpemJ2S1lPdHNtLzdqVWRvRmtNWERRaWFGY25DL2I4SXBaU2R5YW5BWnhwQmoKN3A2L2Y1a0NBd0VBQWFPQ0FnUXdnZ0lBTUFzR0ExVWREd1FFQXdJRXNEQWRCZ05WSFE0RUZnUVVybVM5cU9XYi8zYTUybVp0b296cgp6Nk9YaS93d013WURWUjBSQkN3d0tvSVJjM1F1YzJsbmJtbHVaeTVuYjNZdWFXeUNGWGQzZHk1emRDNXphV2R1YVc1bkxtZHZkaTVwCmJEQWZCZ05WSFNNRUdEQVdnQlMxUTlBT3hHRDVhUE9BUHRqMFVKWjliSm5aYVRCdUJnTlZIUjhFWnpCbE1HT2dZYUJmaGkxb2RIUncKT2k4dlkzSnNMblJoYlhWNkxtZHZkaTVwYkM5d2RXSnNhV012VkdGdGRYcEVaWFpITWk1amNteUdMbWgwZEhBNkx5OWpjbXd5TG5SaApiWFY2TG1kdmRpNXBiQzl3ZFdKc2FXTXZWR0Z0ZFhwRVpYWkhNaTVqY213d2dZVUdDQ3NHQVFVRkJ3RUJCSGt3ZHpBNUJnZ3JCZ0VGCkJRY3dBb1l0YUhSMGNEb3ZMMk55YkM1MFlXMTFlaTVuYjNZdWFXd3ZjSFZpYkdsakwxUmhiWFY2UkdWMlJ6SXVZMlZ5TURvR0NDc0cKQVFVRkJ6QUNoaTVvZEhSd09pOHZZM0pzTWk1MFlXMTFlaTVuYjNZdWFXd3ZjSFZpYkdsakwxUmhiWFY2UkdWMlJ6SXVZMlZ5TUR3RwpDU3NHQVFRQmdqY1ZCd1F2TUMwR0pTc0dBUVFCZ2pjVkNJS0FnU3lDK3RrNGdmV1ZNdmJ4VTRLc3JRb1loNVRPUllXR3pIUUNBV1FDCkFRZ3dIUVlEVlIwbEJCWXdGQVlJS3dZQkJRVUhBd0lHQ0NzR0FRVUZCd01CTUNjR0NTc0dBUVFCZ2pjVkNnUWFNQmd3Q2dZSUt3WUIKQlFVSEF3SXdDZ1lJS3dZQkJRVUhBd0V3RFFZSktvWklodmNOQVFFTEJRQURnZ0lCQUtYKy9hMHVHeTcxRzBGRmJLS1I1eWdxVTV1TgpiVnpHeGdtWERNV2V5K0VrZWMwMUxKYmJidGRQQjNtRUEzQVFxWTRUQ0pJTmRYaVFYY1RhTjZ0TjM4eEFJMEFUVGxyL2hwNHZCK1hyClR5bEowOGFWbXlKSlhRV24rM1hqaU5HU3A2bFZpK2dkcWVQVVlGQjZmNTQ2aU9ROThJc1pzMS9tMzVycSt2YzFaOWRqOUFaZ3ZnNTQKWmt1Ym54S2VXUDRJZ2RvbTUvN0xqTEJMREJVUVFKcWRma0kvTGtQRUVxSXNXZncxbVd6bDc5ZGZaVEpoTHJZM2ZzbjN6eHpaS2xxVApVaklFWnlWSVhoZWNFOVY1czNlS3l6Rk1YbmNyblRiK0U0RExvSUFDVncyVkYvZ09Ld2wvWjM4TFhBSkJKeVplb2QwOGpXNWswdE9vCjNkTUhHTzZWdEhsbW9iRnA0VXJVT3Y3UEtBRE5VQmd5SzA0VUo3MWQ3NEtqVFlNVVRtQzRmUnUrVmc4U1hWbkJKMnlaWjEzZjlDV1EKeGgwNGRjVUlNemlHSnAwQmJtVDdqY082dFdYV0NaRi9JKzNPY2srVUtuOUg1cjMvMklzK01wK0ZHaFRBS01tdGtiVERSVEFsUFZ3SgpyTndmR0NlbDZNd1pPRnl1NWliM2dmYThqZ1JlMHp2d0pUYXFhTEV0bDV6QnlIcTBmNnBZeFdvWGtVbDRiUE5FT1h2aW51ckRKM1ZpCjhLaVJKUjgzOEwwTWplNTBpc3cxQUx5Zjg1SDUyTUJIeWtnQWNJZzhYdXBySkZUQi94a1J3K0tJZ3VqR2VBRmljWkVFVWpaS21PRG8KT1NBbHBQZHl0N2RZYnkzVGZlL1Z1L25PaTliQjI4RHY5SmtRdDRaSDZyRlZCOVEyCjwvZHM6WDUwOUNlcnRpZmljYXRlPgo8L2RzOlg1MDlEYXRhPgo8L2RzOktleUluZm8+CjwvZHM6U2lnbmF0dXJlPjwvc2FtbDpBc3NlcnRpb24+'}
    #     r = requests.get("https://devtest.comda.co.il/auth/saml/hostedapp/token",headers=headers)

    # def test_download_document_collection_and_save_as_pdf(self):
    #     headers = {'content-type': 'application/pdf', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.get(self.settings['Base_Url'] + '/documentcollections/0f80163e-ca54-4873-5bac-08db5c2fc008',headers=headers)
    #     file = open("myfile.pdf", "wb")
    #     file.write(r.content)
    #     file.close()

    # def test_download_document_collection_and_save_as_zip(self):
    #     headers = {'content-type': 'application/octet-stream ', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.get(self.settings['Base_Url'] + '/documentcollections/c75e4a1f-9da5-47bc-f415-08db7c5fc08f',headers=headers)
    #     file = open("myfile.zip", "wb")
    #     file.write(r.content)
    #     file.close()


    # def test_delete_all_documents(self):
    #     r = self.__api_get_all_document_collection()
    #     parameters = {"sent": "true", "viewed": "true", "signed": "true", "declined": "true", "sendingFailed": "true",
    #              "canceled": "true", "limit": "200"}
    #     r = WesignMethodsApi.document_collections_get_parameters(self, parameters)
    #     assert r.status_code == StatusCode.OK
    #     response = r.json()
    #     json_response = response
    #     for id in json_response['documentCollections']:
    #         # self.__api_delete_document_request(id['documentCollectionId'])
    #         WesignMethodsApi.document_collections_id_delete(self, id['documentCollectionId'])
    #
    # def delete_all_documents(self):
    #     headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.get('https://devtest.comda.co.il/userapi/v3/documentcollections?sent=true&viewed=true&signed=true&declined=true&sendingFailed=true&canceled=true&limit=200',headers=headers)
    #     assert r.status_code == StatusCode.OK
    #     response = r.json()
    #     json_response = response
    #     for document_id in json_response['documentCollections']:
    #         headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #         requests.delete(self.settings['Base_Url'] + 'documentcollections/' + document_id['documentCollectionId'],headers=headers)


    def tearDown(self):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            pass
        sleep(3)

    if __name__ == "__main__":
        unittest.main()

    # def __api_document_collection_request(self, request_file):
    #     file = open(self.settings[request_file], 'r')
    #     json_input = file.read()
    #     requests_json = json.loads(json_input)
    #     headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(requests_json),headers=headers)
    #     return r
    #
    # def __api_delete_document_request(self, document_collection_id):
    #     headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.delete(self.settings['Base_Url'] + 'documentcollections/' + document_collection_id,
    #                         headers=headers)
    #     return r
    #
    # def __api_cancel_document_request(self, document_collection_id):
    #     headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.put(self.settings['Base_Url'] + 'documentcollections/' + document_collection_id + '/cancel',
    #                      headers=headers)
    #     return r
    #
    # def __api_resend_document_request(self, document_collection_id, signer_id):
    #     headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.get(self.settings[
    #                          'Base_Url'] + 'documentcollections/' + document_collection_id + '/signers/' + signer_id + '/method/2?shouldSend=true',
    #                      headers=headers)
    #     return r
    #
    # def __api_replace_signer_request(self, document_collection_id, signer_id, request_file):
    #     file = open(self.settings[request_file], 'r')
    #     json_input = file.read()
    #     requests_json = json.loads(json_input)
    #     headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.put(self.settings[
    #                          'Base_Url'] + 'documentcollections/' + signer_id + '/signer/' + document_collection_id + '/replace',
    #                      data=json.dumps(requests_json), headers=headers)
    #     return r
    #
    # def __api_share_document_request(self, request_file):
    #     file = open(self.settings[request_file], 'r')
    #     json_input = file.read()
    #     requests_json = json.loads(json_input)
    #     headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.post(self.settings['Base_Url'] + 'documentcollections/' + 'share', data=json.dumps(requests_json),
    #                       headers=headers)
    #     return r
    #
    # def __api_get_all_document_collection(self):
    #     headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
    #     r = requests.get(
    #         'https://devtest.comda.co.il/userapi/v3/documentcollections?sent=true&viewed=true&signed=true&declined=true&sendingFailed=true&canceled=true&limit=200',
    #         headers=headers)
    #     return r

    def __sign_on_document(self):
        driver = self.driver
        sleep(4)
        self.driver.find_element(By.XPATH, "//*[@name='feather']").click()
        sleep(4)
        canvas = self.driver.find_element(By.XPATH, "//div[@class='signature-pad__canvas']")
        drawing = ActionChains(self.driver) \
            .click_and_hold(canvas) \
            .move_by_offset(-200, 10) \
            .move_by_offset(-10, -50) \
            .move_by_offset(-25, -10) \
            .move_by_offset(100, -100) \
            .move_by_offset(10, 60) \
            .move_by_offset(10, 100) \
            .move_by_offset(-10, -120) \
            .release()
        drawing.perform()
        for x in range(25):
            action = webdriver.common.action_chains.ActionChains(driver)
            action.move_by_offset(5, 0)  # move 150 pixels to the right to access Help link
            action.click()
            action.perform()
        sleep(4)
        self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
        sleep(4)
        # try:
        #     sleep(1)
        #     WebDriverWait(self.driver, 15).until(
        #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]")))
        #     yes_button = "//button[contains(text(),'Yes')]"
        #     self.driver.find_element(By.XPATH, yes_button).click()
        # except:
        #     sleep(1)
        #     WebDriverWait(self.driver, 15).until(
        #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]")))
        #     yes_button = "//button[contains(text(),'No')]"
        #     self.driver.find_element(By.XPATH, yes_button).click()
        sleep(3)
        self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
        sleep(5)

    def __delete_gmail_emails(self):
        sleep(4)
        self.driver.find_element(By.XPATH, "(//table[@cellpadding='0'])[6]").is_displayed()
        self.driver.find_element(By.XPATH,
                                 "//body/div[7]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]").click()  ##click on email checkbox
        sleep(4)
        self.driver.find_element(By.XPATH, "(//div[@role='button'])[11]").click()  ##delete button
        sleep(3)
        self.driver.quit()

    def __enter_gmail(self):
        self.driver.get('https://mail.google.com/')
        sleep(8)
        self.driver.find_element(By.XPATH, "//input[@type='email']").send_keys("wesigntesting@gmail.com")
        self.driver.find_element(By.ID, "identifierNext").click()
        sleep(8)
        self.driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Comsign1!")
        sleep(8)
        self.driver.find_element(By.XPATH, "//div[@id='passwordNext']").click()

    def _change_values_in_file(self, file_name, tempID, documentName):
        with open(self.settings[file_name], 'r+') as f:
            data = json.load(f)
            data["documentName"] = documentName  # <--- add `id` value.
            data["signers"][0]["signerFields"][0]["templateId"] = tempID
            data["templates"][0] = tempID
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining par

    def __enter_gmail_mail(self, gmail_user_name, gmail_password):
        # self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get('https://mail.google.com/')
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "identifierId")))
        self.driver.find_element(By.XPATH, "//input[@type='email']").send_keys(gmail_user_name)
        self.driver.find_element(By.ID, "identifierNext").click()
        password = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
        password.send_keys(gmail_password)
        self.driver.find_element(By.XPATH, "//div[@id='passwordNext']").click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "qj ")))

    def __assert_number_of_fields(self, number_of_fields):
        total_fields = self.driver.find_elements(By.CLASS_NAME, "ct-input--primary")
        assert len(total_fields) == int(number_of_fields)

    def __assert_number_of_live_fields(self, number_of_fields):
        total_fields = self.driver.find_elements(By.XPATH, "//app-text-field[1]/div/input")
        assert len(total_fields) == int(number_of_fields)

    def __validate_no_emails_gmail(self, gmail_user_name, gmail_password):
        driver = self.driver
        self.driver.get('https://mail.google.com/')
        sleep(1)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        sleep(1)
        self.driver.find_element(By.XPATH, "//input[@type='email']").send_keys(gmail_user_name)
        sleep(1)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "identifierNext")))
        self.driver.find_element(By.ID, "identifierNext").click()
        sleep(1)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
        sleep(1)
        self.driver.find_element(By.XPATH, "//input[@type='password']").send_keys(gmail_password)
        sleep(1)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='passwordNext']")))
        self.driver.find_element(By.XPATH, "//div[@id='passwordNext']").click()
        sleep(2)
        # sleep(self.settings['max_wait_time'])
        # try:
        #     self.driver.find_element_by_xpath("//span[contains(text(),'devtest')]").is_displayed()
        #     self.driver.find_element_by_xpath("//body/div[7]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]").click() ##click on email checkbox
        #     sleep(self.settings['min_wait_time'])
        #     self.driver.find_element_by_xpath("(//div[@role='button'])[11]").click() ##delete button
        #     sleep(self.settings['min_wait_time'])
        # except:
        #     pass

    def __enter_gmail_mail_and_sign(self, document_name):
        self.driver.get('https://mail.google.com/')
        sleep(3)
        self.driver.refresh()
        driver = self.driver
        sleep(3)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, f"(//span[contains(text(),'document {document_name}')])[2]")))
        # self.driver.find_element_by_xpath("(//span[contains(text(),'devtest')])[2]").click()
        sleep(3)
        self.driver.find_element(By.XPATH, f"(//span[contains(text(),'document {document_name}')])[2]").click()
        sleep(2)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Click here')]")))
        sleep(3)
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]").click()
        sleep(4)

    def __download_document(self):
        driver = self.driver
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@class='ct-button--primary']")))
        download_document = self.driver.find_element(By.XPATH, "//*[@class='ct-button--primary']")
        download_document.is_displayed()
        download_document.is_enabled()
        download_document.click()
        sleep(4)

    def __setup(self):
        service = Service(self.settings['chrome_driver'])
        options = webdriver.ChromeOptions()
        options.add_argument(
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"')
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(service=service, options=options)

    def __login_wesign(self):
        driver = self.driver
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "email")))
        element = self.driver.find_element(By.NAME, "email")
        element.send_keys(self.settings["company_user"])
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "password")))
        element = self.driver.find_element(By.NAME, "password")
        element.send_keys(self.settings["company_user_password"])
        element = self.driver.find_element(By.ID, "loginInput")
        element.click()
        sleep(2)

    def __login_wesign_signer1(self):
        driver = self.driver
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "email")))
        element = self.driver.find_element(By.NAME, "email")
        element.send_keys("wesignautomation2022@gmail.com")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "password")))
        element = self.driver.find_element(By.NAME, "password")
        element.send_keys(self.settings["company_user_password"])
        element = self.driver.find_element(By.ID, "loginInput")
        element.click()
        sleep(2)


    def __enter_comda_mail_and_sign(self, document_name):
        self.driver.get('https://email.comda.co.il/owa/')
        sleep(3)
        self.driver.refresh()
        driver = self.driver
        sleep(3)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, f"(//span[contains(text(),'{document_name}')])[1]")))
        # self.driver.find_element(By.XPATH,"(//span[contains(text(),'devtest')])[2]").click()
        sleep(3)
        self.driver.find_element(By.XPATH, f"(//span[contains(text(),'{document_name}')])[1]").click()
        sleep(2)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Click here')]")))
        sleep(3)
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]").click()

    def __enter_comda_mail(self, user, user_pass):
        driver = self.driver
        self.driver.get("https://email.comda.co.il/")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username")))
        user_name = self.driver.find_element(By.ID, "username")
        user_name.send_keys(user)
        sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "password")))
        user_password = self.driver.find_element(By.ID, "password")
        user_password.send_keys(user_pass)
        sleep(2)
        signin_button = self.driver.find_element(By.XPATH, '//*[@id="lgnDiv"]/div[9]/div')
        signin_button.click()

    def __add_values_to_all_fields(self):
        driver = self.driver
        date_field = self.driver.find_element(By.XPATH,"//*[@type='date']")
        sleep(2)
        date_field.click()
        sleep(1)
        date_field.send_keys(Keys.SPACE)
        sleep(1)
        date_field.send_keys(Keys.ENTER)
        sleep(2)
        self.driver.find_element(By.XPATH,"//*[@type='email']").send_keys('Test@comda.co.il')
        sleep(2)
        self.driver.find_element(By.XPATH,"(//*[@type='text'])[2]").send_keys('234567')
        sleep(2)
        self.driver.find_element(By.XPATH,"//*[@type='tel']").send_keys('050000000')
        sleep(2)
        self.driver.find_element(By.XPATH,"//*[@type='number']").send_keys('5678')
        sleep(2)
        self.driver.find_element(By.XPATH,"(//*[@type='text'])[1]").send_keys('TestFromComda')
        sleep(2)

    def __sign_document_using_finish_button(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Finish']")))
        finish_button = "//button[normalize-space()='Finish']"
        self.driver.find_element(By.XPATH, finish_button).click()

    def __get_documentCollectionId_from_db(self, document_name):
        sleep(2)
        conn = pyodbc.connect(f'Driver=SQL Server;'
                              "Server=DEVTEST\SQLEXPRESS;"
                              f'Database={self.settings["db_name"]};'
                              f'UID={self.settings["db_user"]};'
                              F'PWD={self.settings["db_password"]};'
                              'Trusted_Connection=no;')
        cursor = conn.cursor()
        b = cursor.execute(
            f" select * from DocumentCollections where Name = '{document_name}'")
        name = b.fetchone()
        return name[0]

    def __get_link_by_signers_number_without_signing(self, signers_number: int, document_collection_id: str):
        index = 0
        for a in range(signers_number):
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            cursor = conn.cursor()
            b = cursor.execute(
                f"SELECT * from [SignerTokensMapping] where [DocumentCollectionId] = '{document_collection_id}'")
            links = []
            result = b.fetchall()
            for x in result:
                links.append(x[3])
            sleep(4)
            self.driver.get(f"https://devtest.comda.co.il/signer/signature/{links[index]}")
            sleep(1)
            index += 1
            links.clear()

    def __enter_temp_mail(self):
        driver = self.driver
        self.driver.get('https://www.1secmail.com/')
        sleep(3)
        self.driver.refresh()
        sleep(3)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "login")))
        name = self.driver.find_element(By.XPATH, "//input[@id='login']")
        art_name = name.get_attribute('value')
        sleep(3)
        domain = self.driver.find_element(By.XPATH, "//select[@id='domain']")
        art_domain = domain.get_attribute('value')
        email = str(art_name) + '@' + str(art_domain)
        return email

