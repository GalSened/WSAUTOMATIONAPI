from pathlib import Path
import json
import requests

class Shared:
        def login_request(self):
            p = Path(__file__).with_name('settings.json')
            with open(p) as f:
                settings = json.load(f)
            file = open(settings['LoginRequestSuccess'], 'r')
            json_input = file.read()
            requests_json = json.loads(json_input)
            headers = {'content-type': 'application/json'}
            r = requests.post(settings['Base_Url'] + 'users/login', data=json.dumps(requests_json), headers=headers)
            login = json.loads(r.content)
            return login['token']

        def login_request_twillo(self):
            p = Path(__file__).with_name('settings.json')
            with open(p) as f:
                settings = json.load(f)
            file = open(settings['LoginRequestSuccessTwilio'], 'r')
            json_input = file.read()
            requests_json = json.loads(json_input)
            headers = {'content-type': 'application/json'}
            r = requests.post(settings['Base_Url'] + 'users/login', data=json.dumps(requests_json), headers=headers)
            login = json.loads(r.content)
            return login['token']