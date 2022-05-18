import unittest
import uuid
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import names
import openpyxl
import json
import base64
from selenium.webdriver import ActionChains
from shared import Shared
from status_codes import StatusCode, ResultCode
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.mark.flaky(max_runs=5)
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
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85

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
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        personal_note_popup_window = self.driver.find_elements_by_class_name("modal__container")
        assert len(personal_note_popup_window) > 0

    @pytest.mark.run(order=20)
    def test_document_collection_document_sending_using_otp_code_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingOtpCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(10)
        otp_box = self.driver.find_elements_by_id("auth")
        assert len(otp_box) > 0

    @pytest.mark.run(order=19)
    def test_document_collection_document_sending_using_otp_code_send_to_phone_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingOtpCodeSendToPhoneSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        send_request_button = self.driver.find_element_by_xpath(
            "/html/body/app-root/app-main-signer/app-otp-details/body/main/div[2]/div/div[3]/form/div[1]/a")
        send_request_button.click()
        sleep(3)
        validate_phone = self.driver.find_element_by_class_name("is-confirm")
        assert validate_phone.text == "OTP code sent successfully to 050482*****87"
        sleep(2)
        otp_box = self.driver.find_elements_by_id("auth")
        assert len(otp_box) > 0

    @pytest.mark.run(order=18)
    def test_document_collection_document_sending_using_document_code_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingDocumentCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(10)
        document_code = self.driver.find_elements_by_id("id")
        assert len(document_code) > 0

    @pytest.mark.run(order=17)
    def test_document_collection_document_sending_using_document_code_and_otp_code_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingDocumentCodeAndOtpCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        document_code = self.driver.find_element_by_xpath("//input[@type='text']")
        document_code.send_keys(self.settings['DocumentCode'])
        sleep(5)
        send_request_button = self.driver.find_element_by_xpath("/html/body/app-root/app-main-signer/app-otp-details/body/main/div[2]/div/div[2]/form/input")
        send_request_button.click()
        sleep(5)
        otp_box = self.driver.find_elements_by_id("auth")
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
        assert json_response[0] == ResultCode.TEMPLATES_IN_SIGNERS_FIELDS_AND_IN_READ_ONLY_FIELDS_MUST_BE_FROM_TEMPLATES_COLLECTION_INPUT

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
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(5)
        self.__enter_gmail()
        sleep(8)
        email = self.driver.find_elements_by_xpath(f"//span[contains(text(),'{self.document_name}')]")
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
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.__enter_gmail()
        sleep(8)
        email = self.driver.find_elements_by_xpath(f"//span[contains(text(),'{self.document_name}')]")
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
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithshouldSendSignedParamaterFalse')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(14)
        self.__sign_on_document()
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(4)
        self.__enter_gmail()
        sleep(10)
        email_notification = self.driver.find_element_by_xpath(f"(//*[contains(text(),'{self.document_name}')])[2]")
        email_notification.click()
        sleep(8)
        attached_document = self.driver.find_elements_by_xpath("//img[@id=':70']")
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
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(8)
        self.__sign_on_document()
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(4)
        self.__enter_gmail()
        sleep(15)
        email_notification = self.driver.find_element_by_xpath(f"(//*[contains(text(),'{self.document_name}')])[2]")
        email_notification.click()
        sleep(10)
        attached_document = self.driver.find_elements_by_xpath(f"(//span[contains(text(),'{self.document_name}.pdf')])[3]")
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
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        self.__sign_on_document()
        sleep(5)
        self.driver.switch_to.alert.accept()
        sleep(5)
        assert self.driver.current_url == "https://www.comsign.co.il/"

    def test_document_collection_document_sending_using_signer_attachments_as_mandatory_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSignerAttachmentsAsMandatorySuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        self.__sign_on_document()
        sleep(2)
        attachment_window_pop_up = self.driver.find_elements_by_class_name("ct-animate-slide-down")
        assert len(attachment_window_pop_up) == 1
        sleep(1)
        self.driver.quit()

    def test_document_collection_document_sending_using_signer_appendices_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSignerAppendicesSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        appendices_icon = self.driver.find_elements_by_class_name("feather-bookmark")
        assert len(appendices_icon) == 1
        sleep(2)
        appendices_icon = self.driver.find_element_by_class_name("feather-bookmark")
        appendices_icon.click()
        sleep(2)
        appendices_pop_up = self.driver.find_elements_by_class_name("ct-animate-slide-down")
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
        r = self.__api_resend_document_request(json_response_document_id,json_response_signer_id)
        assert r.status_code == StatusCode.OK

    def test_document_collection_replace_signer_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_document_id = response['documentCollectionId']
        json_response_signer_id = response['signerLinks'][0]['signerId']
        r = self.__api_replace_signer_request(json_response_signer_id,json_response_document_id,'DocumentCollectionReplaceSuccess')
        assert r.status_code == StatusCode.OK

    def test_document_collection_share_document_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response_document_id = response['documentCollectionId']
        json_response_link = response['signerLinks'][0]['link']
        with open("\\\\fs01\\Users\\NirK\\PythonAutomation\\DocumentCollectionRequest\\DocumentCollectionShareDocuemnt.json", 'r+') as f:
            data = json.load(f)
            data['documentCollectionId'] = json_response_document_id  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
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
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        signature_field = self.driver.find_elements_by_class_name("is-signature")
        assert len(signature_field) == 0
        finish_button = self.driver.find_element_by_class_name("ct-button--titlebar-primary")
        sleep(5)
        finish_button.click()
        sleep(3)
        sign_complete_msg = self.driver.find_elements_by_xpath('/html/body/app-root/app-main-signer/app-success-page/body/main/h2')
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
        r = self.__api_document_collection_request('DocumentCollectionSendDocumentWithOnlyOneSignatureFieldTwoRecipients')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks']
        assert len(json_response) == 85
        assert len(json_response_two) == 1

    @pytest.mark.run(order=27)
    def test_document_collection_with_only_one_signature_field_two_recipient_by_group_success(self):
        r = self.__api_document_collection_request('DocumentCollectionSendDocumentWithOnlyOneSignatureFieldTwoRecipientsGroup')
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
                    "contactId": "f56beec6-8fd0-4633-811e-08da0a7f7607",
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
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        text_field = self.driver.find_elements_by_id("text1")
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
                    "contactId": "f56beec6-8fd0-4633-811e-08da0a7f7607",
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
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        text_field = self.driver.find_elements_by_id("text1")
        assert len(text_field) > 0, 'Text field not displayed'
        self.__delete_template_created(template)

    #Bug number - WES-1030
    def test_document_collection_send_twice_to_same_contact(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingTwiceToSameContact')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"

    #bug number - WES-1102
    def test_document_collection_download_document_collection_invalid_id(self):
        r = self.__api_document_collection_download_document('827b5c63-4951-4098-2ce4-08da2cedfaa9')
        assert r.status_code == StatusCode.BAD_REQUEST

    # Bug number - WES-1066
    def test_document_collection_send_global_number_with_extension_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = self.__api_document_collection_request_twilio('DocumentCollectionDocumentSendingTwilioProviderWithExtensionsSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"

    def test_document_collection_send_global_number_with_extension_and_local_number_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = self.__api_document_collection_request_twilio('DocumentCollectionDocumentSendingTwilioProviderWithExtensionsAndLocalNumberSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"
        driver = self.driver
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, "ct-button--titlebar-primary")))
        finish_button = self.driver.find_element_by_class_name("ct-button--titlebar-primary")
        finish_button.click()

    def test_document_collection_send_global_number_without_extension_to_local_number_twilio_provider_success(self):
        self.token_twillio = Shared.login_request_twillo(self)
        r = self.__api_document_collection_request_twilio('DocumentCollectionDocumentSendingTwilioProviderWithoutExtensionsLocalNumberSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(1)
        self.driver.maximize_window()
        sleep(1)
        self.driver.get(json_response)
        sleep(5)
        assert self.driver.current_url != 'https://devtest.comda.co.il/signer/', "Link is broken"
        driver = self.driver
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME, "ct-button--titlebar-primary")))
        finish_button = self.driver.find_element_by_class_name("ct-button--titlebar-primary")
        finish_button.click()

    #Bug number = WES-1106
    def test_send_distribute_duplicated_fields_in_xlsx_with_same_name_validate_values_success(self):
        self.token = Shared.login_request_gmail(self)
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.__enter_gmail_mail(self.settings['first_recipient_name'], self.settings['gmail_login_password'])
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request("documentCollection_duplicated_fields_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        document_name = uuid.uuid4().hex
        self._change_values_in_file("DocumentCollectionDuplicatedFields", template, document_name)
        send_distribution = self.__api_create_documentCollection_request("DocumentCollectionDuplicatedFields")
        assert send_distribution.status_code == StatusCode.OK
        WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.XPATH,"(//*[contains(text(),'wesign test sent you the document {}')])[2]".format(document_name))))
        self.driver.find_element(By.XPATH, "(//*[contains(text(),'wesign test sent you the document {}')])[2]".format(document_name)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        self.__assert_number_of_fields(2)
        get_value_from_text_field = self.driver.find_elements_by_xpath("//*[@type='text']")
        for value in get_value_from_text_field:
            assert value.get_attribute('value') == "string", " value wasn't added to the fields"
        total_fields = self.driver.find_elements_by_class_name("ct-input--primary")
        assert len(total_fields) == int(2), "field wasn't duplicated"


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
            self.driver.quit()
        except:
            pass
        sleep(3)

    if __name__ == "__main__":
        unittest.main()


    def __api_document_collection_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_delete_document_request(self, document_collection_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'documentcollections/' + document_collection_id,headers=headers)
        return r

    def __api_cancel_document_request(self, document_collection_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'documentcollections/'+document_collection_id+'/cancel', headers=headers)
        return r

    def __api_resend_document_request(self, document_collection_id,signer_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'documentcollections/'+document_collection_id+'/signers/'+signer_id+'/method/2?shouldSend=true', headers=headers)
        return r

    def __api_replace_signer_request(self,document_collection_id,signer_id,request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'documentcollections/' + signer_id + '/signer/' + document_collection_id + '/replace',data=json.dumps(requests_json),headers=headers)
        return r

    def __api_share_document_request(self,request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections/' + 'share', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_get_all_document_collection(self):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get('https://devtest.comda.co.il/userapi/v3/documentcollections?sent=true&viewed=true&signed=true&declined=true&sendingFailed=true&canceled=true&limit=200', headers=headers)
        return r

    def __sign_on_document(self):
        sleep(4)
        self.driver.find_element_by_xpath("//*[@name='feather']").click()
        sleep(4)
        canvas = self.driver.find_element_by_xpath("//div[@class='signature-pad__canvas']")
        drawing = ActionChains(self.driver) \
            .click_and_hold(canvas) \
            .move_by_offset(-200, 10) \
            .move_by_offset(-10, -50) \
            .move_by_offset(25, 10) \
            .move_by_offset(80, 50) \
            .move_by_offset(10, 60) \
            .move_by_offset(10, 60) \
            .release()
        drawing.perform()
        self.driver.find_element_by_class_name("ct-button--primary").click() ##Sign button
        sleep(4)
        self.driver.find_element_by_class_name("ct-button--titlebar-primary").click() ##Finish button
        sleep(5)

    def __delete_gmail_emails(self):
        sleep(4)
        self.driver.find_element_by_xpath("(//table[@cellpadding='0'])[6]").is_displayed()
        self.driver.find_element_by_xpath(
                "//body/div[7]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]").click()  ##click on email checkbox
        sleep(4)
        self.driver.find_element_by_xpath("(//div[@role='button'])[11]").click()  ##delete button
        sleep(3)
        self.driver.quit()

    def __enter_gmail(self):
        self.driver.get('https://mail.google.com/')
        sleep(8)
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys("wesigntesting@gmail.com")
        self.driver.find_element_by_id("identifierNext").click()
        sleep(8)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys("Comsign1!")
        sleep(8)
        self.driver.find_element_by_xpath("//div[@id='passwordNext']").click()

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
        r = requests.put(self.settings['Base_Url'] + 'templates/' + template_id, data=json.dumps(requests_json), headers=headers)
        return r

    def __api_document_collection_request_twilio(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token_twillio}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(requests_json), headers=headers)
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
        r = requests.put(self.settings["Base_Url"] + f'templates/{templateId}', data=json.dumps(requests_json) ,headers=headers)
        return r

    def __api_extract_signers_from_base64(self, signers_base64):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documents/distribution/signers', data=json.dumps(signers_base64), headers=headers)
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
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(requests_json), headers=headers)
        return r


    def __enter_gmail_mail(self, gmail_user_name, gmail_password):
        # self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get('https://mail.google.com/')
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "identifierId")))
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys(gmail_user_name)
        self.driver.find_element_by_id("identifierNext").click()
        password = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
        password.send_keys(gmail_password)
        self.driver.find_element_by_xpath("//div[@id='passwordNext']").click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "qj ")))

    def __assert_number_of_fields(self, number_of_fields):
        total_fields = self.driver.find_elements_by_class_name("ct-input--primary")
        assert len(total_fields) == int(number_of_fields)
