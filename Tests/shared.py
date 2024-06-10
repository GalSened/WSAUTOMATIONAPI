from pathlib import Path
import json
from time import sleep

import requests

class Shared:

        def login_request(self):
            # p = Path(__file__).with_name('settings.json')
            # with open(p) as f:
            #     settings = json.load(f)
            p = Path(__file__).resolve().parent.parent
            file_path = p / "Settings\\settings.json"
            with open(file_path) as f:
                settings = json.load(f)
            file = open(settings['LoginRequestSuccess'], 'r')
            json_input = file.read()
            sleep(0.6)
            requests_json = json.loads(json_input)
            headers = {'content-type': 'application/json'}
            sleep(0.6)
            r = requests.post(settings['Base_Url'] + 'users/login', data=json.dumps(requests_json), headers=headers)
            sleep(0.6)
            login = json.loads(r.content)
            sleep(0.6)
            return login['token']

        def login_request_twillo(self):
            # p = Path(__file__).with_name('settings.json')
            # with open(p) as f:
            #     settings = json.load(f)
            p = Path(__file__).resolve().parent.parent
            file_path = p / "Settings\\settings.json"
            with open(file_path) as f:
                settings = json.load(f)
            file = open(settings['LoginRequestSuccessTwilio'], 'r')
            json_input = file.read()
            requests_json = json.loads(json_input)
            headers = {'content-type': 'application/json'}
            r = requests.post(settings['Base_Url'] + 'users/login', data=json.dumps(requests_json), headers=headers)
            login = json.loads(r.content)
            return login['token']

        def login_request_gmail(self):
            # p = Path(__file__).with_name('settings.json')
            # with open(p) as f:
            #     settings = json.load(f)
            p = Path(__file__).resolve().parent.parent
            file_path = p / "Settings\\settings.json"
            with open(file_path) as f:
                settings = json.load(f)
            file = open(settings['LoginRequestSuccessGmail'], 'r')
            json_input = file.read()
            requests_json = json.loads(json_input)
            headers = {'content-type': 'application/json'}
            r = requests.post(settings['Base_Url'] + 'users/login', data=json.dumps(requests_json), headers=headers)
            login = json.loads(r.content)
            return login['token']

        def login_signer1_account(self):
            # p = Path(__file__).with_name('settings.json')
            # with open(p) as f:
            #     settings = json.load(f)
            p = Path(__file__).resolve().parent.parent
            file_path = p / "Settings\\settings.json"
            with open(file_path) as f:
                settings = json.load(f)
            file = open(settings['LoginRequestSigner1Success'], 'r')
            json_input = file.read()
            requests_json = json.loads(json_input)
            headers = {'content-type': 'application/json'}
            r = requests.post(settings['Base_Url'] + 'users/login', data=json.dumps(requests_json), headers=headers)
            login = json.loads(r.content)
            return login['token']
