import unittest
import warnings
from pathlib import Path
from time import sleep
import pytest
import json
from Enums.status_codes import StatusCode, ResultCode
from Common.all_api_methods import WesignMethodsApi
from shared import Shared


@pytest.mark.flaky(max_runs=3)
class WesignApiSelfSignTestTests(unittest.TestCase):
    def setUp(self):
        # p = Path(__file__).with_name('SelfSignSettings.json')
        # with open(p) as f:
        #     self.settings = json.load(f)
        p = Path(__file__).resolve().parent.parent
        file_path = p / "Settings\\SelfSignSettings.json"
        with open(file_path) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    @pytest.mark.part1
    def test_self_sign_pdf_document_upload_success(self):
        r = WesignMethodsApi.self_sign_post_json_file(self, 'SelfSignUploadPdfDocument')
        assert r.status_code == StatusCode.OK

    @pytest.mark.part2
    def test_self_sign_word_document_upload_success(self):
        r = WesignMethodsApi.self_sign_post_json_file(self, 'SelfSignUploadWordDocument')
        assert r.status_code == StatusCode.OK

    @pytest.mark.part3
    def test_self_sign_xlsx_document_upload_success(self):
        r = WesignMethodsApi.self_sign_post_json_file(self, 'SelfSignUploadXlsxDocument')
        assert r.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_self_sign_png_document_upload_success(self):
        r = WesignMethodsApi.self_sign_post_json_file(self, 'SelfSignUploadPngDocument')
        assert r.status_code == StatusCode.OK

    @pytest.mark.part2
    def test_self_sign_delete_document_success(self):
        r = WesignMethodsApi.self_sign_post_json_file(self, 'SelfSignUploadPdfDocument')
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
        r = WesignMethodsApi.self_sign_id_delete(self, documentcollectionid)
        assert r.status_code == StatusCode.OK

    @pytest.mark.part3
    def test_self_sign_download_smart_card(self):
        r = WesignMethodsApi.self_sign_download_smartcard_get(self)
        assert r.status_code == StatusCode.OK

    def tearDown(self):
        try:
            self.driver.quit()
        except:
            pass
        sleep(3)

    if __name__ == "__main__":
        unittest.main()
