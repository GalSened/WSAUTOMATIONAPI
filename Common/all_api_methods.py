import requests
import json

class WesignMethodsApi:
    # Contacts
    def contacts_id_get(self, contact_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'contacts/' + contact_id, headers=headers)
        return r

    def contacts_bulk_post_xlsx_file(self, base64_string: str):
        data = '{' + base64_string + '"}'
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'contacts/bulk', data=data, headers=headers)
        return r

    def contacts_id_delete(self, contact_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'contacts/' + contact_id, headers=headers)
        return r

    def contacts_get(self, parameters: dict):
        # to get all contacts send parameters = {}
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

    # Distribution

    def distribution_signers_post_json_file(self, signers_file: str):
        file = open(self.settings[signers_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documents/distribution/signers', data=json.dumps(requests_json), headers=headers)
        return r

    def distribution_signers_post_xlsx_file(self, signers_base64: dict):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documents/distribution/signers', data=json.dumps(signers_base64), headers=headers)
        return r

    def distribution_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documents/distribution', data=json.dumps(requests_json), headers=headers)
        return r

    # Templates

    def templates_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/templates', data=json.dumps(requests_json), headers=headers)
        return r

    def templates_id_delete(self, template_guid: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + '/templates/' + template_guid, headers=headers)
        assert r.status_code == 200

    def templates_id_put_json_file(self, field_file: str, template_id: str):
        file = open(self.settings[field_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings["Base_Url"] + f'/templates/{template_id}', data=json.dumps(requests_json), headers=headers)
        return r

    def templates_id_put_dict(self, data: dict, template_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings["Base_Url"] + f'/templates/{template_id}', data=json.dumps(data), headers=headers)
        return r

    def templates_id_post_json_file(self, request_file: str, template_id: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + f'/templates/{template_id}', data=json.dumps(requests_json), headers=headers)
        return r

    def templates_id_download_get(self, template_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + f'/templates/{template_id}' + "/download", headers=headers)
        return r

    def templates_delete_batch_put(self, del_req: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + '/templates/deletebatch', data=json.dumps(del_req), headers=headers)
        return r

    # Admins

    def admins_groups_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'admins/groups', data=json.dumps(requests_json), headers=headers)
        return r

    def admins_groups_delete(self, group_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'admins/groups/' + group_id, headers=headers)
        return r

    def admins_groups_put_json_file(self, request_file: str, group_id: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'admins/groups/' + group_id, data=json.dumps(requests_json), headers=headers)
        return r

    def admins_groups_get(self):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'admins/groups', headers=headers)
        return r

    def admins_users_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'admins/users', data=json.dumps(requests_json), headers=headers)
        return r

    def admins_users_id_delete(self, user_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'admins/users/' + user_id, headers=headers)
        return r

    def admins_users_get(self):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'admins/users', headers=headers)
        return r

    def admins_users_id_put_json_file(self, request_file: str, user_id: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'admins/users/' + user_id, data=json.dumps(requests_json),
                         headers=headers)
        return r

    # Users

    def users_login_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json'}
        r = requests.post(self.settings['Base_Url'] + 'users/login', data=json.dumps(requests_json), headers=headers)
        return r

    # Self sign

    def self_sign_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + 'selfsign', data=json.dumps(requests_json), headers=headers)
        return r

    def self_sign_put_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + 'selfsign', data=json.dumps(requests_json), headers=headers)
        return r

    def self_sign_id_delete(self, document_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + 'selfsign/' + document_id, headers=headers)
        return r

    def self_sign_download_smartcard_get(self):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + 'selfsign/download/smartcard', headers=headers)
        return r

    # Document collections

    def document_collections_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documentcollections', data=json.dumps(requests_json), headers=headers)
        return r

    def document_collections_post_json_file_using_twillio(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token_twillio}
        r = requests.post(self.settings['Base_Url'] + '/documentcollections', data=json.dumps(requests_json), headers=headers)
        return r

    def document_collections_id_delete(self, document_collection_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + '/documentcollections/' + document_collection_id,
                            headers=headers)
        return r

    def document_collections_id_cancel_put(self, document_collection_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + '/documentcollections/' + document_collection_id + '/cancel',
                         headers=headers)
        return r

    def document_collections_id_signers_signerId_method_sendingMethod_get(self, document_collection_id: str, signer_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings[
                             'Base_Url'] + '/documentcollections/' + document_collection_id + '/signers/' + signer_id + '/method/2?shouldSend=true',
                         headers=headers)
        return r

    def document_collections_id_signer_signerId_replace_put(self, document_collection_id: str, signer_id: str, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings[
                             'Base_Url'] + '/documentcollections/' + signer_id + '/signer/' + document_collection_id + '/replace',
                         data=json.dumps(requests_json), headers=headers)
        return r

    def document_collections_share_post_json_file(self, request_file: str):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documentcollections/' + 'share', data=json.dumps(requests_json),
                          headers=headers)
        return r

    def document_collections_post_dict(self, data: dict):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documentcollections', data=json.dumps(data), headers=headers)
        return r

    def document_collections_post_dict_using_signer1(self, data: dict):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.signer1}
        r = requests.post(self.settings['Base_Url'] + '/documentcollections', data=json.dumps(data), headers=headers)
        return r

    def document_collections_delete_batch_put_dict(self, del_req: dict):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings['Base_Url'] + '/documentcollections/deletebatch', data=json.dumps(del_req),
                              headers=headers)
        return r

    def document_collections_id_get(self, document_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + '/documentcollections/' + document_id, headers=headers)
        return r

    def document_collections_id_json_get(self, document_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + '/documentcollections/' + document_id + '/json', headers=headers)
        return r

    def document_collections_download_batch_post_ids(self, list_of_ids: list):
        ids_str = ""
        for x in range(len(list_of_ids)-1):
            ids_str = ids_str + '"' + list_of_ids[x] + '",'
        ids_str = ids_str + '"' + list_of_ids[len(list_of_ids)-1] + '"'
        data = '{"ids": [' + ids_str + ']}'
        header = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        new_request = requests.post(self.settings['Base_Url'] + '/documentcollections/downloadbatch/', data=data, headers=header)
        return new_request

    def document_collections_get_parameters(self, parameters: dict):
        header = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        new_request = requests.get(self.settings['Base_Url'] + '/documentcollections/', params=parameters,
                                   headers=header)
        return new_request

    def document_collections_id_get_fields_xml(self, document_id: str):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.get(self.settings['Base_Url'] + '/documentcollections/' + document_id, headers=headers)
        return r
