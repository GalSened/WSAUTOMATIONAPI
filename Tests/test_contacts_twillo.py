import unittest
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from Enums.status_codes import StatusCode, ResultCode
from shared import Shared


@pytest.mark.flaky(max_runs=3)
class WesignContactsApi(unittest.TestCase):
    def setUp(self):
        # p = Path(__file__).with_name('ContactsSettings.json')
        # with open(p) as f:
        #     self.settings = json.load(f)
        p = Path(__file__).resolve().parent.parent
        file_path = p / "Settings\\ContactsSettings.json"
        with open(file_path) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request_twillo(self)

    @pytest.mark.part1
    def test_create_new_contact_with_global_number_with_twilio_provider_success(self):
        r = self.__api_create_contact_request('CreateNewContactWithGlobalPhoneWhenProviderTwiilo')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        assert len(json_response) > 0
        r = self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    @pytest.mark.part2
    def test_create_new_contact_with_local_number_with_twilio_provider_success(self):
        r = self.__api_create_contact_request('CreateNewContactWithLocalPhoneWhenProviderTwiilo')
        assert r.status_code == StatusCode.OK
        response = r.json()
        json_response = response['contactId']
        assert len(json_response) > 0
        r = self.__api_delete_contact_request(json_response)
        assert r.status_code == StatusCode.OK

    @pytest.mark.part3
    def test_create_new_contact_with_local_number_with_twilio_provider_with_phone_extension_in_number(self):
        r = self.__api_create_contact_request('CreateNewContactWithGlobalPhoneWhenProviderTwiiloPhoneExtensionInvalid')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Phone']
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_VALID_PHONE
        assert len(json_response) > 0

    def tearDown(self):
        sleep(3)

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