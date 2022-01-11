import unittest
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


@pytest.mark.flaky(max_runs=2)
class WesignApiCreateDocumentCollectionTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('DocumentCollectionSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_document_collection_document_sending_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85

    def test_document_collection_document_sending_two_contacts_by_order_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingTwoRecipientnByOrderSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        json_response_two = response['signerLinks']
        assert len(json_response) == 85
        assert len(json_response_two) == 1

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

    def test_document_collection_document_sending_with_text_field_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithTextFieldSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85

    def test_document_collection_document_sending_with_personal_note_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithPersonalNoteSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get(json_response)
        sleep(5)
        personal_note_popup_window = self.driver.find_elements_by_class_name("modal__container")
        assert len(personal_note_popup_window) > 0

    def test_document_collection_document_sending_using_otp_code_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingOtpCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get(json_response)
        sleep(5)
        otp_box = self.driver.find_elements_by_id("auth")
        assert len(otp_box) > 0

    def test_document_collection_document_sending_using_otp_code_send_to_phone_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingOtpCodeSendToPhoneSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get(json_response)
        sleep(5)
        send_request_button = self.driver.find_element_by_xpath(
            "/html/body/app-root/app-main-signer/app-otp-details/body/main/div[2]/div/div[3]/form/div[1]/a")
        send_request_button.click()
        sleep(2)
        otp_box = self.driver.find_elements_by_id("auth")
        assert len(otp_box) > 0

    def test_document_collection_document_sending_using_document_code_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingDocumentCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get(json_response)
        sleep(5)
        document_code = self.driver.find_elements_by_id("id")
        assert len(document_code) > 0

    def test_document_collection_document_sending_using_document_code_and_otp_code_success(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingUsingDocumentCodeAndOtpCodeSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
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

    def test_document_collection_document_sending_with_invalid_sign_field_name(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidSignFieldName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.FIELD_NAME_NOT_EXIST

    def test_document_collection_document_sending_with_empty_field_name_in_read_only_fields(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithEmptyFieldNameReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST, "Status " + str(r.status_code) + " incorrect"
        response = r.json()
        json_response = response['errors']['']
        assert json_response[0] == ResultCode.READ_ONLY_FIELDS_SHOULD_CONTAIN_NAME_AND_VALUE

    def test_document_collection_document_sending_with_invalid_field_name_in_read_only_fields(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidFieldNameReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.FIELD_NAME_NOT_EXIST

    def test_document_collection_document_sending_with_empty_value_field_in_read_only_fields(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWitheEmptyFieldValueReadOnly')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['']
        assert json_response[0] == ResultCode.READ_ONLY_FIELDS_SHOULD_CONTAIN_NAME_AND_VALUE

    def test_document_collection_document_sending_with_invalid_template_id(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWitheInvalidTemplateId')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['']
        assert json_response[0] == ResultCode.TEMPLATES_IN_SIGNERS_FIELDS_AND_IN_READ_ONLY_FIELDS_MUST_BE_FROM_TEMPLATES_COLLECTION_INPUT

    def test_document_collection_document_sending_with_empty_document_name(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWitheEmptyDocumentName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DocumentName']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_A_NAME

    def test_document_collection_document_sending_with_invalid_document_mode(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidDocumentMode')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DocumentMode']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_DOCUMENT_MODE

    def test_document_collection_document_sending_with_invalid_contact_id(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidContactId')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.CONTACT_NOT_CREATED_BY_USER

    def test_document_collection_document_sending_with_duplicate_fields_name(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithDuplicateFieldsName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Signers']
        assert json_response[0] == ResultCode.THERE_IS_DUPLICATE_FIELD_FOR_SIGNER

    def test_document_collection_document_sending_not_feet_contact_means(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingNotFeetContactMeans')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.SIGNER_METHOD_NOT_FEET_TO_CONTACT_MEANS

    def test_document_collection_document_sending_with_invalid_sending_method(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithInvalidSendingMethod')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Signers']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_SIGNERS, "Validation is " + str(json_response[0])

    @pytest.mark.run(order=4)
    def test_document_collection_document_sending_with_should_send_parameter_as_false(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithShouldSendParamaterFlase')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        sleep(5)
        self.__enter_gmail()
        sleep(8)
        email = self.driver.find_elements_by_xpath("//span[contains(text(),'dev')]")
        assert len(email) == 0, "Check if email sent"
        sleep(6)
        self.driver.quit()

    @pytest.mark.run(order=3)
    def test_document_collection_document_sending_with_should_send_parameter_as_true(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithShouldSendParamaterTrue')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.__enter_gmail()
        sleep(8)
        email = self.driver.find_elements_by_xpath("//span[contains(text(),'dev')]")
        assert len(email) > 0, "Email didn't sent"
        sleep(8)
        self.__delete_gmail_emails()

    @pytest.mark.run(order=2)
    def test_document_collection_document_sending_with_should_send_sign_document_parameter_as_false(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithshouldSendSignedParamaterFalse')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get(json_response)
        sleep(14)
        self.__sign_on_document()
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(4)
        self.__enter_gmail()
        sleep(8)
        email_notification = self.driver.find_element_by_id(":23")
        email_notification.click()
        sleep(8)
        attached_document = self.driver.find_elements_by_xpath("//img[@id=':70']")
        assert len(attached_document) == 0, "Pdf document attached"
        sleep(3)
        self.driver.back()
        self.__delete_gmail_emails()

    @pytest.mark.run(order=5)
    def test_document_collection_document_sending_with_should_send_sign_document_parameter_as_true(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithshouldSendSignedParamaterTrue')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get(json_response)
        sleep(8)
        self.__sign_on_document()
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(4)
        self.__enter_gmail()
        sleep(15)
        email_notification = self.driver.find_element_by_xpath("//tbody/tr[@id=':25']/td[4]/div[2]/span[1]/span[1]")
        email_notification.click()
        sleep(10)
        attached_document = self.driver.find_elements_by_xpath("//*[@id=':7a']")
        assert len(attached_document) > 0, "Pdf document attached"
        sleep(3)
        self.driver.back()
        self.__delete_gmail_emails()

    @pytest.mark.run(order=1)
    def test_delete_all_mails(self):
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.__enter_gmail()
        sleep(4)
        try:
            self.__delete_gmail_emails()
        except:
            self.driver.quit()

    def test_document_collection_document_sending_with_redirect_url(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithRedirectUrlSuccess')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
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