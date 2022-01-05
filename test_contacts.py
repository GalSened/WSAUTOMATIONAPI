import unittest
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from shared import Shared
from status_codes import StatusCode, ResultCode


class WesignContactsApi(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('UsersSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)



    def tearDown(self):
        sleep(3)

    if __name__ == "__main__":
        unittest.main()


    def __api_create_contact_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'admins/users', data=json.dumps(requests_json), headers=headers)
        return r