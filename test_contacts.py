import unittest
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode

@pytest.mark.flaky(max_runs=2)
class WesignContactsApi(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('ContactsSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)


    def test_create_new_contact_by_email_success(self):
        r = self.__api_create_contact_request('CreateNewValidContactWithEmailAndPhone')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        assert len(json_response) > 0
        r = self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_create_new_contact_by_phone_success(self):
        r = self.__api_create_contact_request('CreateNewValidContactSendingBySms')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        assert len(json_response) > 0
        r = self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_create_new_contact_by_invalid_email(self):
        r = self.__api_create_contact_request('CreateNewContactWithInvalidEmail')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_EMAIL

    def test_create_new_contact_by_invalid_phone(self):
        r = self.__api_create_contact_request('CreateNewContactWithInvalidPhone')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Phone']
        assert  json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_PHONE

    def test_create_new_contact_by_empty_name(self):
        r = self.__api_create_contact_request('CreateNewContactWithEmptyName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Name']
        assert json_response == ResultCode.INVALID_NAME

    def test_create_new_contact_by_phone_invalid_sending_type(self):
        r = self.__api_create_contact_request('CreateNewValidContactByPhoneInvalidSendingMethod')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DefaultSendingMethod']
        assert json_response == ResultCode.DEFAULT_SENDING_METHOD

    def test_create_new_contact_by_email_invalid_sending_type(self):
        r = self.__api_create_contact_request('CreateNewValidContactByEmailInvalidSendingMethod')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DefaultSendingMethod']
        assert json_response == ResultCode.DEFAULT_SENDING_METHOD

    def test_create_new_contact_by_email_invalid_default_sending_method(self):
        r = self.__api_create_contact_request('CreateNewValidContactByEmailInvalidSendingMethod')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['DefaultSendingMethod']
        assert json_response == ResultCode.DEFAULT_SENDING_METHOD

    def test_create_new_contact_with_name_already_exists(self):
        r = self.__api_create_contact_request('CreateNewValidContactNameExists')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.CONTACT_WITH_SAME_MEANS_ALREADY_EXISTS

    def test_create_new_contact_with_email_already_exists(self):
        r = self.__api_create_contact_request('CreateNewValidContactEmailExists')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.CONTACT_WITH_SAME_MEANS_ALREADY_EXISTS

    def test_create_new_contact_with_phone_already_exists(self):
        r = self.__api_create_contact_request('CreateNewValidContactPhoneExists')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.CONTACT_WITH_SAME_MEANS_ALREADY_EXISTS

    def test_create_new_contact_from_bulk_csv_file_success(self):
        r = self.__api_create_contact_request_csv('CreateNewContactFromBulkCsv')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactsId']
        assert len(json_response[0]) == 36
        r = self.__api_delete_contact_request(json_response[0])
        assert r.status_code == StatusCode.OK

    def test_create_new_contacts_from_bulk_csv_sending_method_sms_success(self):
        r = self.__api_create_contact_request_csv('CreateNewContactsFromBulkCsvSendingMehtodSms')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactsId']
        assert len(json_response) == 20
        for contacts in json_response:
            self.__api_delete_contact_request(contacts)

    def test_create_new_contacts_from_bulk_csv_sending_method_email_success(self):
        r = self.__api_create_contact_request_csv('CreateNewContactsFromBulkCsvSendingMehtodEmail')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactsId']
        assert len(json_response) == 20
        for contacts in json_response:
            self.__api_delete_contact_request(contacts)

    def test_create_new_contacts_from_bulk_csv_sending_method_email_and_sms_success(self):
        r = self.__api_create_contact_request_csv('CreateNewContactsFromBulkCsvSendingMehtodEmailAndSms')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactsId']
        assert len(json_response) == 20
        for contacts in json_response:
            self.__api_delete_contact_request(contacts)

    def test_create_new_contact_from_bulk_csv_valid_name_and_email_invalid_phone(self):
        r = self.__api_create_contact_request_csv('CreateNewContactsFromBulkCsvInvalidNameAndEmailInvalidPhone')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        json_response[0] == ResultCode.INVALID_PHONE

    def test_create_new_contact_from_bulk_csv_empty_csv(self):
        r = self.__api_create_contact_request_csv('CreateNewContactsFromBulkCsvEmpty')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Base64File']
        json_response[0] == ResultCode.INVALID_CSV

    def test_create_new_contact_from_bulk_csv_empty_fullname_valid_phone(self):
        r = self.__api_create_contact_request_csv('CreateNewContactsFromBulkCsvEmptyFullnameValidPhone')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.NAME_IS_MISSING

    def test_update_contact_mail(self):
        r = self.__api_create_contact_request('CreateNewValidContactWithEmailAndPhone')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        r = self.__api_update_contact(json_response,'UpdateContactMail')
        assert r.status_code == StatusCode.OK
        self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_update_contact_phone(self):
        r = self.__api_create_contact_request('CreateNewValidContactWithEmailAndPhone')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        r = self.__api_update_contact(json_response,'UpdateContactPhone')
        assert r.status_code == StatusCode.OK
        self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_update_contact_seal(self):
        r = self.__api_create_contact_request('CreateNewValidContactWithEmailAndPhone')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        r = self.__api_update_contact(json_response,'UpdateContactSeal')
        assert r.status_code == StatusCode.OK
        self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_update_contact_invalid_email(self):
        r = self.__api_create_contact_request('CreateNewValidContactWithEmailAndPhone')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        r = self.__api_update_contact(json_response,'UpdateContactInvalidPhone')
        assert r.status_code == StatusCode.BAD_REQUEST
        response_error = r.json()
        json_response_error = response_error['errors']['Phone']
        assert json_response_error[0] == ResultCode.PLEASE_SPECIFY_VALID_PHONE
        r = self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_update_contact_invalid_name(self):
        r = self.__api_create_contact_request('CreateNewValidContactWithEmailAndPhone')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        r = self.__api_update_contact(json_response,'UpdateContactInvalidName')
        assert r.status_code == StatusCode.BAD_REQUEST
        response_error = r.json()
        json_response_error = response_error['errors']['Name']
        json_response_error[0] == ResultCode.NAME_SHOULD_CONTAIN_ONLY_CHARACTERS
        r = self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    def test_get_all_contacts(self):
        r = self.__api_get_all_contacts()
        assert r.status_code == StatusCode.OK

    def tearDown(self):
        sleep(4)

    if __name__ == "__main__":
        unittest.main()


    def __api_create_contact_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'contacts', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_delete_contact_request(self, contact_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'contacts/' + contact_id, headers=headers)
        return r

    def __api_create_contact_request_csv(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'contacts/bulk', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_update_contact(self,contact_id, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'contacts/' + contact_id, data=json.dumps(requests_json), headers=headers)
        return r

    def __api_get_all_contacts(self):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'contacts/' + "?limit=20&includeTabletMode=true", headers=headers)
        return r