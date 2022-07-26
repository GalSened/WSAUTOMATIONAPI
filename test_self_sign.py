import unittest
import warnings
import smtplib
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from shared import Shared
from status_codes import StatusCode

@pytest.mark.flaky(max_runs=10)
class WesignApiSelfSignTestTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('SelfSignSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_self_sign_pdf_document_upload_success(self):
        r = self.__api_self_sign_create_document('SelfSignUploadPdfDocument')
        assert r.status_code == StatusCode.OK

    def test_self_sign_word_document_upload_success(self):
        r = self.__api_self_sign_create_document('SelfSignUploadWordDocument')
        assert r.status_code == StatusCode.OK

    def test_self_sign_xlsx_document_upload_success(self):
        r = self.__api_self_sign_create_document('SelfSignUploadXlsxDocument')
        assert r.status_code == StatusCode.OK

    def test_self_sign_png_document_upload_success(self):
        r = self.__api_self_sign_create_document('SelfSignUploadPngDocument')
        assert r.status_code == StatusCode.OK

    def test_self_sign_pdf_sign_success(self):
        r = self.__api_self_sign_create_document('SelfSignUploadPdfDocument')
        assert r.status_code == StatusCode.OK
        response = r.json()
        documentcollectionid = response['documentCollectionId']
        documentid = response['documentId']
        with open("\\\\fs01\\Users\\NirK\\PythonAutomation\\\SelfSignRequest\\SelfSignDocumentSigning.json", 'r+') as f:
            data = json.load(f)
            data['documentCollectionId'] = documentcollectionid  # <--- add `id` value.
            data['documentId'] = documentid  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = self.__api_self_sign_document_signing("SelfSignDocumentSigning")
        assert r.status_code == StatusCode.OK

    def test_self_sign_delete_document_success(self):
        r = self.__api_self_sign_create_document('SelfSignUploadPdfDocument')
        assert r.status_code == StatusCode.OK
        response = r.json()
        documentcollectionid = response['documentCollectionId']
        documentid = response['documentId']
        with open("\\\\fs01\\Users\\NirK\\PythonAutomation\\SelfSignRequest\\SelfSignDocumentSigning.json", 'r+') as f:
            data = json.load(f)
            data['documentCollectionId'] = documentcollectionid  # <--- add `id` value.
            data['documentId'] = documentid  # <--- add `id` value.
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        r = self.__api_self_sign_delete_document(documentcollectionid)
        assert r.status_code == StatusCode.OK

    def test_self_sign_download_smart_card(self):
        url = "https://devtest.comda.co.il/userapi/v3/selfsign/download/smartcard"
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(url, headers=headers)
        assert r.status_code == StatusCode.OK

    def self_sign_create_document(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'selfsign', data=json.dumps(requests_json), headers=headers)
        return r

    def tearDown(self):
        try:
            self.driver.quit()
        except:
            pass
        sleep(3)

    if __name__ == "__main__":
        unittest.main()


    def __api_self_sign_create_document(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'selfsign', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_self_sign_document_signing(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'selfsign', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_self_sign_delete_document(self, documentid):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'selfsign/' + documentid, headers=headers)
        return r
