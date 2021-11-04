import unittest
import warnings
from pathlib import Path
from time import sleep
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode
from selenium import webdriver

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
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_FIELD_NAME_IN_READ_ONLY_FIELDS

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
        assert json_response[0] == ResultCode.READ_ONLY_FIELDS_SHOULD_CONTAIN_VALUE

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
        assert json_response[0] == ResultCode.SIGNER_METHOD_NOT_FEET_TO_CONTACT_MEANS, "Validation is " + str(json_response[0])

    def test_document_collection_document_sending_with_should_send_parameter_as_false(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithShouldSignParamaterFlase')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get('https://mail.google.com/')
        sleep(8)
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys("wesigntesting@gmail.com")
        self.driver.find_element_by_id("identifierNext").click()
        sleep(8)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys("Comsign1!")
        sleep(8)
        self.driver.find_element_by_xpath("//div[@id='passwordNext']").click()
        sleep(8)
        email = self.driver.find_elements_by_xpath("//span[contains(text(),'devSignIt')]")
        assert len(email) == 0, "Check if email sent"
        sleep(4)
        self.driver.quit()

    def test_document_collection_document_sending_with_should_send_parameter_as_true(self):
        r = self.__api_document_collection_request('DocumentCollectionDocumentSendingWithShouldSignParamaterTrue')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['signerLinks'][0]['link']
        assert len(json_response) == 85
        self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get('https://mail.google.com/')
        sleep(8)
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys("wesigntesting@gmail.com")
        self.driver.find_element_by_id("identifierNext").click()
        sleep(8)
        self.driver.find_element_by_xpath("//input[@type='password']").send_keys("Comsign1!")
        sleep(8)
        self.driver.find_element_by_xpath("//div[@id='passwordNext']").click()
        sleep(8)
        email = self.driver.find_elements_by_xpath("//span[contains(text(),'devSignIt')]")
        assert len(email) > 0, "Email didn't sent"
        sleep(8)
        self.driver.find_element_by_xpath("(//table[@cellpadding='0'])[6]").is_displayed()
        self.driver.find_element_by_xpath(
                "//body/div[7]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]").click()  ##click on email checkbox
        sleep(4)
        self.driver.find_element_by_xpath("(//div[@role='button'])[11]").click()  ##delete button
        sleep(3)
        self.driver.quit()


    if __name__ == "__main__":
        unittest.main()

    def __api_document_collection_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'documentcollections', data=json.dumps(requests_json), headers=headers)
        return r
