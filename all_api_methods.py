import requests
import json

class WesignMethodssApi:
    # Contacts
    def contacts_id_get(self, contact_id: int):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'contacts/' + contact_id, headers=headers)
        return r

    def contacts_bulk_post_xlsx_file(self, base64_string: str):
        data = '{' + base64_string + '"}'
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'contacts/bulk', data=data, headers=headers)
        return r

    def contacts_id_delete(self, contact_id):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'contacts/' + contact_id, headers=headers)
        return r

    def contacts_get(self, parameters: dict):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'contacts/', params=parameters, headers=headers)
        return r

    def contacts_id_put(self, contact_id: int, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'contacts/' + contact_id, data=json.dumps(requests_json), headers=headers)
        return r

    def contacts_bulk_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'contacts/bulk', data=json.dumps(requests_json), headers=headers)
        return r

    def contacts_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'contacts', data=json.dumps(requests_json), headers=headers)
        return r

    def contacts_post(self, parameters: dict):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'contacts/', data=json.dumps(parameters), headers=headers)
        return r

    def contacts_delete_batch_put(self, list_of_ids: dict):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'contacts/deletebatch', data=json.dumps(list_of_ids), headers=headers)
        return r

