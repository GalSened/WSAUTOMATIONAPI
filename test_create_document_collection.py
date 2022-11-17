import logging
import shutil
import unittest
import uuid
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from shared import Shared
from status_codes import StatusCode, ResultCode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.mark.flaky(max_runs=6)
class WesignApiCreateDocumentCollectionTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('DocumentCollectionSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    @pytest.mark.run(order=26)
    def test_document_collection_document_sending_success(self):
        try:
            logging.info(" ---Test Start---  test_document_collection_document_sending_success  ---Test Start--- ")
            r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
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

    @pytest.mark.run(order=25)
    def test_document_collection_document_sending_two_contacts_by_order_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingTwoRecipientnByOrderSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks']
        assert len(json_response) == 85
        assert len(json_response_two) == 1

    @pytest.mark.run(order=24)
    def test_document_collection_document_sending_two_contacts_by_group_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingTwoRecipientByGroupSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks'][1]['link']
        json_response_three = response['signerLinks']
        assert json_response != json_response_two
        assert len(json_response_two) == 85
        assert len(json_response) == 85
        assert len(json_response_three) == 2

    @pytest.mark.run(order=23)
    def test_document_collection_document_sending_with_text_field_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithTextFieldSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85

    @pytest.mark.run(order=21)
    def test_document_collection_document_sending_with_personal_note_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithPersonalNoteSuccess')
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
        personal_note_popup_window = self.driver.find_elements(By.CLASS_NAME, "modal__container")
        assert len(personal_note_popup_window) > 0

    @pytest.mark.run(order=20)
    def test_document_collection_document_sending_using_otp_code_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingOtpCodeSuccess')
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

    @pytest.mark.run(order=19)
    def test_document_collection_document_sending_using_otp_code_send_to_phone_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingOtpCodeSendToPhoneSuccess')
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

    @pytest.mark.run(order=18)
    def test_document_collection_document_sending_using_document_code_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingDocumentCodeSuccess')
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

    @pytest.mark.run(order=17)
    def test_document_collection_document_sending_using_document_code_and_otp_code_success(self):
        r = self.__api_document_collection_request(
            'DocumentCollectionDocumentSendingUsingDocumentCodeAndOtpCodeSuccess')
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

    @pytest.mark.run(order=16)
    def test_document_collection_document_sending_with_invalid_sign_field_name(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidSignFieldName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.FIELD_NAME_NOT_EXIST

    @pytest.mark.run(order=15)
    def test_document_collection_document_sending_with_empty_field_name_in_read_only_fields(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithEmptyFieldNameReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST, "Status " + str(r.status_code) + " incorrect"
        response = r.json()
        json_response = response['errors']['']
        assert json_response[0] == ResultCode.READ_ONLY_FIELDS_SHOULD_CONTAIN_NAME_AND_VALUE

    @pytest.mark.run(order=14)
    def test_document_collection_document_sending_with_invalid_field_name_in_read_only_fields(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidFieldNameReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.FIELD_NAME_NOT_EXIST

    @pytest.mark.run(order=13)
    def test_document_collection_document_sending_with_empty_value_field_in_read_only_fields(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWitheEmptyFieldValueReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['']
        assert json_response[0] == ResultCode.READ_ONLY_FIELDS_SHOULD_CONTAIN_NAME_AND_VALUE

    @pytest.mark.run(order=12)
    def test_document_collection_document_sending_with_invalid_template_id(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWitheInvalidTemplateId')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['']
        assert json_response[
                   0] == ResultCode.TEMPLATES_IN_SIGNERS_FIELDS_AND_IN_READ_ONLY_FIELDS_MUST_BE_FROM_TEMPLATES_COLLECTION_INPUT

    @pytest.mark.run(order=11)
    def test_document_collection_document_sending_with_empty_document_name(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWitheEmptyDocumentName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DocumentName']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_NAME

    @pytest.mark.run(order=10)
    def test_document_collection_document_sending_with_invalid_document_mode(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidDocumentMode')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DocumentMode']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_DOCUMENT_MODE

    @pytest.mark.run(order=9)
    def test_document_collection_document_sending_with_invalid_contact_id(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidContactId')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.CONTACT_NOT_CREATED_BY_USER

    @pytest.mark.run(order=8)
    def test_document_collection_document_sending_with_duplicate_fields_name(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithDuplicateFieldsName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Signers']
        assert json_response[0] == ResultCode.THERE_IS_DUPLICATE_FIELD_FOR_SIGNER

    @pytest.mark.run(order=7)
    def test_document_collection_document_sending_not_feet_contact_means(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingNotFeetContactMeans')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.SIGNER_METHOD_NOT_FEET_TO_CONTACT_MEANS

    @pytest.mark.run(order=6)
    def test_document_collection_document_sending_with_invalid_sending_method(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidSendingMethod')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Signers']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_SIGNERS, "Validation is " + str(json_response[0])

    @pytest.mark.run(order=4)
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
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithShouldSendParamaterFlase')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(5)
        self.__enter_comda_mail(self.settings['dev_email'], self.settings['comda_mail_password'])
        sleep(8)
        email = self.driver.find_elements(By.XPATH, f"//span[contains(text(),'{self.document_name}')]")
        assert len(email) == 0, "Check if email sent"
        sleep(6)
        self.driver.quit()

    @pytest.mark.run(order=2)
    def test_document_collection_document_sending_with_should_send_parameter_as_true(self):
        email_prefix = uuid.uuid4().hex
        self.document_name = email_prefix
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionDocumentSendingWithShouldSendParamaterTrue.json",
                'r+') as f:
            data = json.load(f)
            data['documentName'] = self.document_name  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithShouldSendParamaterTrue')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.__enter_comda_mail(self.settings['dev_email'], self.settings['comda_mail_password'])
        sleep(8)
        email = self.driver.find_elements(By.XPATH, f"//span[contains(text(),'{self.document_name}')]")
        assert len(email) > 0, "Email didn't sent"
        sleep(8)
        self.driver.quit()

    @pytest.mark.run(order=3)
    def test_document_collection_document_sending_with_should_send_sign_document_parameter_as_false(self):
        email_prefix = uuid.uuid4().hex
        self.document_name = email_prefix
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionDocumentSendingWithshouldSendSignedParamaterFalse.json",
                'r+') as f:
            data = json.load(f)
            data['documentName'] = self.document_name  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = self.__api_document_collection_request(
            'DocumentCollectionDocumentSendingWithshouldSendSignedParamaterFalse')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(14)
        self.__sign_on_document()
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(4)
        self.__enter_comda_mail(self.settings['dev_email'], self.settings['comda_mail_password'])
        sleep(4)
        email_notification = self.driver.find_element(By.XPATH, f"(//*[contains(text(),'{self.document_name}')])[1]")
        email_notification.click()
        sleep(8)
        attached_document = self.driver.find_elements(By.XPATH, "//img[@id=':70']")
        assert len(attached_document) == 0, "Pdf document attached"

    @pytest.mark.run(order=5)
    def test_document_collection_document_sending_with_should_send_sign_document_parameter_as_true(self):
        email_prefix = uuid.uuid4().hex
        self.document_name = email_prefix
        with open(
                "\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionDocumentSendingWithshouldSendSignedParamaterTrue.json",
                'r+') as f:
            data = json.load(f)
            data['documentName'] = self.document_name  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithshouldSendSignedParamaterTrue')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(8)
        self.__sign_on_document()
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(4)
        self.__enter_comda_mail(self.settings['dev_email'], self.settings['comda_mail_password'])
        sleep(3)
        email_notification = self.driver.find_element(By.XPATH, f"(//*[contains(text(),'{self.document_name}')])[1]")
        email_notification.click()
        sleep(10)
        attached_document = self.driver.find_elements(By.XPATH,
                                                      f"(//span[contains(text(),'{self.document_name}.pdf')])[1]")
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

    def test_document_collection_document_sending_with_redirect_url(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithRedirectUrlSuccess')
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

    def test_document_collection_document_sending_using_signer_attachments_as_mandatory_success(self):
        r = self.__api_document_collection_request(
            'DocumentCollectionDocumentSendingSignerAttachmentsAsMandatorySuccess')
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

    def test_document_collection_document_sending_using_signer_appendices_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSignerAppendicesSuccess')
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
        sleep(2)
        appendices_icon = self.driver.find_element(By.CLASS_NAME, "feather-bookmark")
        appendices_icon.click()
        sleep(2)
        appendices_pop_up = self.driver.find_elements(By.CLASS_NAME, "ct-animate-slide-down")
        assert len(appendices_pop_up) == 1
        sleep(1)
        self.driver.quit()

    def test_document_collection_delete_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['documentCollectionId']
        r = self.__api_delete_document_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_document_collection_cancel_document_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['documentCollectionId']
        r = self.__api_cancel_document_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_document_collection_resend_document_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_document_id = response['documentCollectionId']
        json_response_signer_id = response['signerLinks'][0]['signerId']
        r = self.__api_resend_document_request(json_response_document_id, json_response_signer_id)
        assert r.status_code == StatusCode.OK

    def test_document_collection_replace_signer_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_document_id = response['documentCollectionId']
        json_response_signer_id = response['signerLinks'][0]['signerId']
        r = self.__api_replace_signer_request(json_response_signer_id, json_response_document_id,
                                              'DocumentCollectionReplaceSuccess')
        assert r.status_code == StatusCode.OK

    def test_document_collection_share_document_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
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
        r = self.__api_share_document_request('DocumentCollectionShareDocuemnt')
        assert r.status_code == StatusCode.OK

    @pytest.mark.run(order=31)
    def test_document_collection_without_fields_one_recipient_success(self):
        r = self.__api_document_collection_request('DocumentCollectionSendDocumentWithoutFields')
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

    @pytest.mark.run(order=30)
    def test_document_collection_without_fields_two_recipient_by_group_success(self):
        r = self.__api_document_collection_request('DocumentCollectionSendDocumentWithoutFieldsTwoRecipients')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks'][1]['link']
        json_response_three = response['signerLinks']
        assert json_response != json_response_two
        assert len(json_response_two) == 85
        assert len(json_response) == 85
        assert len(json_response_three) == 2

    @pytest.mark.run(order=29)
    def test_document_collection_without_fields_two_recipient_by_order_success(self):
        r = self.__api_document_collection_request('DocumentCollectionSendDocumentWithoutFieldsTwoRecipientsOrder')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks']
        assert len(json_response) == 85
        assert len(json_response_two) == 1

    @pytest.mark.run(order=28)
    def test_document_collection_with_only_one_signature_field_two_recipient_by_order_success(self):
        r = self.__api_document_collection_request(
            'DocumentCollectionSendDocumentWithOnlyOneSignatureFieldTwoRecipients')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks']
        assert len(json_response) == 85
        assert len(json_response_two) == 1

    @pytest.mark.run(order=27)
    def test_document_collection_with_only_one_signature_field_two_recipient_by_group_success(self):
        r = self.__api_document_collection_request(
            'DocumentCollectionSendDocumentWithOnlyOneSignatureFieldTwoRecipientsGroup')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks'][1]['link']
        json_response_three = response['signerLinks']
        assert json_response != json_response_two
        assert len(json_response_two) == 85
        assert len(json_response) == 85
        assert len(json_response_three) == 2

    def test_document_collection_with_hidden_field_as_true(self):
        r = self.__api_create_template_request('CreateTemplatePdfBase64Success')
        response = r.json()
        template = response['templateId']
        self.__api_update_template_request_hidden_field('UpdateTemplateWithTextFieldAsHidden', template)
        d = {
            "documentMode": 1,
            "documentName": "TestApiHiddenAsTrue",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "1d8a4a7f-5b83-45ee-dee5-08dac0859eef",
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(d), headers=headers)
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
        self.__delete_template_created(template)

    def test_document_collection_with_hidden_field_as_false(self):
        r = self.__api_create_template_request('CreateTemplatePdfBase64Success')
        response = r.json()
        template = response['templateId']
        self.__api_update_template_request_hidden_field('UpdateTemplateWithTextFieldAsHiddenAsFalse', template)
        d = {
            "documentMode": 1,
            "documentName": "TestApiHiddenAsFalse",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "1d8a4a7f-5b83-45ee-dee5-08dac0859eef",
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(d), headers=headers)
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
        self.__delete_template_created(template)

    # Bug number - WES-1030
    def test_document_collection_send_twice_to_same_contact(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingTwiceToSameContact')
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
    def test_document_collection_download_document_collection_invalid_id(self):
        r = self.__api_document_collection_download_document('827b5c63-4951-4098-2ce4-08da2cedfaa9')
        assert r.status_code == StatusCode.BAD_REQUEST

    # Bug number - WES-1066
    def test_document_collection_send_global_number_with_extension_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = self.__api_document_collection_request_twilio(
            'DocumentCollectionDocumentSendingTwilioProviderWithExtensionsSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"

    def test_document_collection_send_global_number_with_extension_and_local_number_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = self.__api_document_collection_request_twilio(
            'DocumentCollectionDocumentSendingTwilioProviderWithExtensionsAndLocalNumberSuccess')
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

    def test_document_collection_send_global_number_without_extension_to_local_number_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = self.__api_document_collection_request_twilio(
            'DocumentCollectionDocumentSendingTwilioProviderWithoutExtensionsLocalNumberSuccess')
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
    def test_send_distribute_duplicated_fields_in_xlsx_with_same_name_validate_values_success(self):
        self.token = Shared.login_request_gmail(self)
        self.__setup()
        self.__enter_comda_mail(self.settings['dev_email'], self.settings['comda_mail_password'])
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request(
            "documentCollection_duplicated_fields_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        document_name = uuid.uuid4().hex
        self._change_values_in_file("DocumentCollectionDuplicatedFields", template, document_name)
        send_distribution = self.__api_create_documentCollection_request("DocumentCollectionDuplicatedFields")
        assert send_distribution.status_code == StatusCode.OK
        sleep(1)
        self.driver.refresh()
        sleep(2)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "(//*[contains(text(),'sent you the document {}')])[1]".format(document_name))))
        self.driver.find_element(By.XPATH,
                                 "(//*[contains(text(),'sent you the document {}')])[1]".format(document_name)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        self.__assert_number_of_live_fields(2)
        get_value_from_text_field = self.driver.find_elements(By.ID, "Text")
        for value in get_value_from_text_field:
            assert value.get_attribute('value') == "string", " value wasn't added to the fields"
        total_fields = self.driver.find_elements(By.CLASS_NAME, "is-mandatory")
        assert len(total_fields) == int(2), "field wasn't duplicated"

    # Bug number = WES-1123
    def test_document_collection_download_cancel_document(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['documentCollectionId']
        cancel_document_request = self.__api_cancel_document_request(json_response)
        assert cancel_document_request.status_code == StatusCode.OK
        download_document = self.__api_document_collection_download_document(json_response)
        assert download_document.status_code == 400, "Document still can be download after cancelation"

    def test_document_collection_update_signature_field_description_is_empty_success(self):
        create_template = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert create_template.status_code == StatusCode.OK
        response = create_template.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        update_template = self.__api_update_template_request('UpdateTemplateWithSignatureFieldWithoutFieldDescription',
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
                    "contactId": "1d8a4a7f-5b83-45ee-dee5-08dac0859eef",
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(d), headers=headers)
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
        self.__delete_template_created(template)

    def test_document_collection_update_signature_field_description_different_from_field_name_using_field_name_success(
            self):
        create_template = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert create_template.status_code == StatusCode.OK
        response = create_template.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        update_template = self.__api_update_template_request(
            'UpdateTemplateWithSignatureDescriptionDiffrentFromFieldName', template)
        assert update_template.status_code == StatusCode.OK
        d = {
            "documentMode": 1,
            "documentName": "TestSignatureFieldDescriptionDiffrentFromFieldName",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "1d8a4a7f-5b83-45ee-dee5-08dac0859eef",
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(d), headers=headers)
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
        self.__delete_template_created(template)

    def test_document_collection_update_signature_field_description_different_from_field_name_using_only_field_description_success(
            self):
        create_template = self.__api_create_template_request("CreateTemplatePdfBase64Success")
        assert create_template.status_code == StatusCode.OK
        response = create_template.json()
        template = response['templateId']
        templatename = response['templateName']
        assert len(template) == 36, "Template not created"
        assert len(templatename) > 0
        update_template = self.__api_update_template_request(
            'UpdateTemplateWithSignatureDescriptionDiffrentFromFieldName', template)
        assert update_template.status_code == StatusCode.OK
        d = {
            "documentMode": 1,
            "documentName": "TestSignatureFieldDescriptionDiffrentFromFieldName",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "1d8a4a7f-5b83-45ee-dee5-08dac0859eef",
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(d), headers=headers)
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
        self.__delete_template_created(template)

    def test_document_collection_update_signature_field_description_different_from_field_name_using_only_field_name_hebrew_success(
            self):
        create_template = self.__api_create_template_request("CreateTemplatePdfBase64Success")
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'templates/' + template, data=json.dumps(update_template),
                         headers=headers)
        assert r.status_code == StatusCode.OK
        d = {
            "documentMode": 1,
            "documentName": "TestSignatureFieldDescriptionDiffrentFromFieldName",
            "templates": [
                template
            ],
            "signers": [
                {
                    "contactId": "1d8a4a7f-5b83-45ee-dee5-08dac0859eef",
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(d), headers=headers)
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
        self.__delete_template_created(template)

    def test_document_collection_download_document_as_json_file_success(self):
        r = self.__api_document_collection_request('DocumentCollectionSendDocumentWithoutFields')
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        download_json = requests.get(self.settings['Base_Url'] + 'documentcollections/' + document_id + '/json',
                                     headers=headers)
        assert download_json.status_code == StatusCode.OK
        response = download_json.json()
        base64 = response['files'][0]['data']
        assert len(base64) == 64928

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
                        "contactId": "d5554e18-25bf-4572-dee3-08dac0859eef",
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
            headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
            r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(req), headers=headers)
            assert r.status_code == 200
            response = r.json()
            json_response = response['documentCollectionId']
            a.append(json_response)

        del_req = {
            "ids": [
                a[0], a[1], a[2], a[3], a[4]
            ]
        }
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        delete = requests.put(self.settings['Base_Url'] + 'documentcollections/deletebatch', data=json.dumps(del_req),
                              headers=headers)
        assert delete.status_code == StatusCode.OK

    def test_document_collection_send_document_with_meta_data_and_sign_success(self):
        r = self.__api_create_template_request("CreateTemplateWordBase64WithMetaDataSuccess")
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(d), headers=headers)
        assert r.status_code == StatusCode.OK

    def test_document_collection_send_document_two_recipients_e2e_sign_success(self):
        r = self.__api_create_template_request("CreateTemplate3PagesPdfBase64Success")
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        update_template = requests.put(self.settings['Base_Url'] + 'templates/' + template, data=json.dumps(d),
                                       headers=headers)
        assert update_template.status_code == 200
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
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(document_collection),
                          headers=headers)
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.__setup()
        sleep(1)
        self.driver.get(json_response)
        driver = self.driver
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        text = self.driver.find_elements(By.XPATH, "//input[@type='text']")
        tel = self.driver.find_elements(By.XPATH, "//input[@type='tel']")
        number = self.driver.find_elements(By.XPATH, "//input[@type='number']")
        date_field = self.driver.find_elements(By.XPATH, "//*[@type='date']")
        email = self.driver.find_elements(By.XPATH, "//input[@type='email']")
        check_box = self.driver.find_elements(By.XPATH,
                                              "//input[@class='ng-untouched ng-pristine ng-valid ng-star-inserted']")
        for x in number:
            try:
                x.send_keys("5870")
            except:
                pass
        for x in text:
            try:
                x.send_keys("בדיקה שלי")
            except:
                pass
        for x in tel:
            try:
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
                x.send_keys("test@comda.co.il")
            except:
                pass
        for x in check_box:
            try:
                x.click()
            except:
                pass
        radio_button_one = self.driver.find_element(By.ID, "Group_I3zx7_Radio_YoVQ3")
        radio_button_one.click()
        sleep(2)
        radio_button_two = self.driver.find_element(By.ID, "Group_DyYrL_Radio_vKi94")
        radio_button_two.click()
        sleep(2)
        select = Select(self.driver.find_element(By.ID, "Choice_LzjnP"))
        select.select_by_index(2)
        sleep(2)
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
        use_signature_all_fields = self.driver.find_element(By.XPATH, "(//span[@class='ct-checkbox__checkmark'])[1]")
        use_signature_all_fields.click()
        sleep(4)
        self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
        sleep(4)
        self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
        sleep(5)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        sleep(1)
        driver.execute_script("window.open('');")
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        self.__enter_comda_mail(self.settings['dev_email'], self.settings['comda_mail_password'])
        sleep(2)
        self.__enter_comda_mail_and_sign(document)
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[2])
        sleep(2)
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        text = self.driver.find_elements(By.XPATH, "//input[@type='text']")
        tel = self.driver.find_elements(By.XPATH, "//input[@type='tel']")
        number = self.driver.find_elements(By.XPATH, "//input[@type='number']")
        date_field = self.driver.find_elements(By.XPATH, "//*[@type='date']")
        email = self.driver.find_elements(By.XPATH, "//input[@type='email']")
        for x in number:
            try:
                x.send_keys("1234")
            except:
                pass
        for x in text:
            try:
                x.send_keys("My tests")
            except:
                pass
        for x in tel:
            try:
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
                x.send_keys("test2@comda.co.il")
            except:
                pass
        radio_button_one = self.driver.find_element(By.ID, "Group_OAy97_Radio_kvXeS")
        radio_button_one.click()
        sleep(2)
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
        use_signature_all_fields = self.driver.find_element(By.XPATH, "(//span[@class='ct-checkbox__checkmark'])[1]")
        use_signature_all_fields.click()
        sleep(4)
        self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
        sleep(4)
        self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
        sleep(2)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        self.__download_document()
        sleep(3)
        try:
            src_path = rf"C:\Users\ComdaIT\Downloads\{document}.pdf"
            dst_path = r"\\fs01\Users\NirK\pdfs"
            shutil.copy(src_path, dst_path)
        except:
            pass

    @pytest.mark.success
    def test_send_sms_with_success_results(self):
        r = self.__api_document_collection_request('sms')
        assert r.status_code == StatusCode.OK

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
              "contactName": "3efc3b51fa3743beb941291b35392a76",
              "contactMeans": "3efc3b51fa3743beb941291b35392a76@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_lOa7B",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "35a41cc83bea4f1497515bc14e688cd4",
              "contactMeans": "35a41cc83bea4f1497515bc14e688cd4@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_pb9bT",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "f6cdbb062e2d446ab213861c6b4a6987",
              "contactMeans": "f6cdbb062e2d446ab213861c6b4a6987@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_lT9Wd",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "0a2e9c6a114948d1a7d200c20bdec1ec",
              "contactMeans": "0a2e9c6a114948d1a7d200c20bdec1ec@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_caME1",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "ac833a2512db4023935b3f265921a808",
              "contactMeans": "ac833a2512db4023935b3f265921a808@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_93MRi",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "0d6992ce432d49eb8ca6b9dbfc45a4be",
              "contactMeans": "0d6992ce432d49eb8ca6b9dbfc45a4be@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_NUFB1",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "0d5f7ec292b643f2935354227a5c6c08",
              "contactMeans": "0d5f7ec292b643f2935354227a5c6c08@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_nO6Xq",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "76500ff0a2184b3d8f7cc9dfd824a174",
              "contactMeans": "76500ff0a2184b3d8f7cc9dfd824a174@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_GuamX",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "b3d5c9706807478a908e1cc4ba381c92",
              "contactMeans": "b3d5c9706807478a908e1cc4ba381c92@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_7u6Zb",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "2f384bbaf22d4cf9a97169ff3621f222",
              "contactMeans": "2f384bbaf22d4cf9a97169ff3621f222@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_dcXSi",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "182c8227e5ed4d7ba65b5f9c37213d71",
              "contactMeans": "182c8227e5ed4d7ba65b5f9c37213d71@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_IgBZC",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "b509941d08da49ff87042fc7303d7df1",
              "contactMeans": "b509941d08da49ff87042fc7303d7df1@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_WnMl8",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "9ae850fc0806477ca7785d4fd681fd6e",
              "contactMeans": "9ae850fc0806477ca7785d4fd681fd6e@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_eA4O3",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "826ca7140f14468da46865fbf4899bb4",
              "contactMeans": "826ca7140f14468da46865fbf4899bb4@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_ZbZPY",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "776a3adcee654793bb8081a07b99c5b2",
              "contactMeans": "776a3adcee654793bb8081a07b99c5b2@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_yi57y",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "9c2a166e1206461294ead0af24b734d7",
              "contactMeans": "9c2a166e1206461294ead0af24b734d7@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_NirVa",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "b8a86919ab9548cfa39aa573a120ee58",
              "contactMeans": "b8a86919ab9548cfa39aa573a120ee58@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_4dPsl",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "6a7335c17bfb4e688aeeaa4c3bf09e9c",
              "contactMeans": "6a7335c17bfb4e688aeeaa4c3bf09e9c@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_paGWr",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "a762a65d61e945998205198085380f2e",
              "contactMeans": "a762a65d61e945998205198085380f2e@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_PnWjx",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "9af9872a4bc74818b3565bf313c0c53d",
              "contactMeans": "9af9872a4bc74818b3565bf313c0c53d@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_yivJ0",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "94f05c0e140044bd9f84ca145df5cc2c",
              "contactMeans": "94f05c0e140044bd9f84ca145df5cc2c@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_majYh",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "3ad82e93161e40b1a9b035ddf89574f6",
              "contactMeans": "3ad82e93161e40b1a9b035ddf89574f6@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_H4Lkw",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "30e0f675b7664ba4a448a21e70dc7d92",
              "contactMeans": "30e0f675b7664ba4a448a21e70dc7d92@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_ektGu",

                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "7506b19783d542eda18f25458e7c1b1d",
              "contactMeans": "7506b19783d542eda18f25458e7c1b1d@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_n4c3n",
                }
              ]
            },
            {
              "otpMode": 0,
              "authenticationMode": 0,
              "contactName": "5e2dc2f2bb7c46d784101087cb0332e9",
              "contactMeans": "5e2dc2f2bb7c46d784101087cb0332e9@comda.co.il",
              "sendingMethod": 2,
              "phoneExtension": "+972",
              "signerFields": [
                {
                  "templateId": "a94937b8-bbce-49f8-8f9f-08dac70402d3",
                  "fieldName": "Signature_rupre",

                }
              ]
            }
          ],
          "documentName": self.document_name,
          "documentMode": 2,
          "templates": [
            "a94937b8-bbce-49f8-8f9f-08dac70402d3"
          ]
        }
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(payload),headers=headers)
        res = r.json()
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
            self.driver.find_element(By.CLASS_NAME, "ct-button--primary").click()  ##Sign button
            sleep(1)
            self.driver.find_element(By.CLASS_NAME, "ct-button--titlebar-primary").click()  ##Finish button
            sleep(1)
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
            signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
            assert len(signing_complete_msg) == 1
        sleep(2)
        self.driver.get(self.settings['wesign_url'])
        self.__login_wesign()
        sleep(1)
        driver = self.driver
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "button--sent-ent")))
        my_documents_section = self.driver.find_element(By.CLASS_NAME, "button--sent-ent")
        my_documents_section.click()
        sleep(3)
        tds = self.driver.find_elements(By.XPATH, "//tr/td[3]")
        row_index = 2
        for name in tds:
            if name.text == self.document_name:
                row = self.driver.find_element(By.XPATH, f"//table/tbody/tr[{row_index}]")
                sleep(4)
                row.click()
                sleep(3)
        sent_document_status = self.driver.find_elements(By.XPATH, "//td/table/tbody/tr/td[3]")
        index = 2
        for sent_status in sent_document_status:
            recipient_email = self.driver.find_element(By.XPATH,f"//table/tbody/tr[3]/td/table/tbody/tr[{index}]/td[2]")
            assert sent_status.text != "", f"Sent status not displayed to {recipient_email.text}"
            index += 1
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

    # def test_delete_all_documents(self):
    #     r = self.__api_get_all_document_collection()
    #     assert r.status_code == StatusCode.OK
    #     response = r.json()
    #     json_response = response
    #     for id in json_response['documentCollections']:
    #         self.__api_delete_document_request(id['documentCollectionId'])
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
        sleep(1)

    if __name__ == "__main__":
        unittest.main()

    def __api_document_collection_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(requests_json),
                          headers=headers)
        return r

    def __api_delete_document_request(self, document_collection_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'documentcollections/' + document_collection_id,
                            headers=headers)
        return r

    def __api_cancel_document_request(self, document_collection_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'documentcollections/' + document_collection_id + '/cancel',
                         headers=headers)
        return r

    def __api_resend_document_request(self, document_collection_id, signer_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings[
                             'Base_Url'] + 'documentcollections/' + document_collection_id + '/signers/' + signer_id + '/method/2?shouldSend=true',
                         headers=headers)
        return r

    def __api_replace_signer_request(self, document_collection_id, signer_id, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings[
                             'Base_Url'] + 'documentcollections/' + signer_id + '/signer/' + document_collection_id + '/replace',
                         data=json.dumps(requests_json), headers=headers)
        return r

    def __api_share_document_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections/' + 'share', data=json.dumps(requests_json),
                          headers=headers)
        return r

    def __api_get_all_document_collection(self):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(
            'https://devtest.comda.co.il/userapi/v3/documentcollections?sent=true&viewed=true&signed=true&declined=true&sendingFailed=true&canceled=true&limit=200',
            headers=headers)
        return r

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

    def __api_create_template_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'templates', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_update_template_request_hidden_field(self, request_file, template_id):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'templates/' + template_id, data=json.dumps(requests_json),
                         headers=headers)
        return r

    def __api_document_collection_request_twilio(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token_twillio}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(requests_json),
                          headers=headers)
        return r

    def __delete_template_created(self, template_guid):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'templates/' + template_guid, headers=headers)
        assert r.status_code == 200

    def __api_document_collection_download_document(self, id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'documentcollections/' + id, headers=headers)
        return r

    def __api_create_template_field_request(self, field_file, templateId):
        file = open(self.settings[field_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings["Base_Url"] + f'templates/{templateId}', data=json.dumps(requests_json),
                         headers=headers)
        return r

    def __api_extract_signers_from_base64(self, signers_base64):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documents/distribution/signers', data=json.dumps(signers_base64),
                          headers=headers)
        return r

    def _change_values_in_file(self, file_name, tempID, documentName):
        with open(self.settings[file_name], 'r+') as f:
            data = json.load(f)
            data["documentName"] = documentName  # <--- add `id` value.
            data["signers"][0]["signerFields"][0]["templateId"] = tempID
            data["templates"][0] = tempID
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part

    def __api_create_documentCollection_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(requests_json),
                          headers=headers)
        return r

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
        total_fields = self.driver.find_elements(By.CLASS_NAME, "is-mandatory")
        assert len(total_fields) == int(number_of_fields)

    def __api_update_template_request(self, request_file, template):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'templates/' + template, data=json.dumps(requests_json),
                         headers=headers)
        return r

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
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        sleep(3)
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
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
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument(
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"')
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(executable_path=service, options=options)

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
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        sleep(3)
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()

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

