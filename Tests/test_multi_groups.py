import unittest
import uuid
import warnings
from pathlib import Path
from time import sleep
import pytest
import json
from Enums.status_codes import StatusCode, ResultCode
from Common.all_api_methods import WesignMethodsApi
from shared import Shared


@pytest.mark.flaky(max_runs=4)
class WesignApiMultiGroupsTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).resolve().parent.parent
        file_path = p / "Settings\\UsersSettings.json"
        with open(file_path) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_multi_groups_account(self)

    @pytest.mark.multi
    def test_add_user_to_another_group_success(self):
        group = uuid.uuid4().hex
        self.group_name = group
        payload = {
              "name": self.group_name
            }

        r = WesignMethodsApi.admins_groups_post_payload(self, payload)
        assert r.status_code == StatusCode.OK
        response = r.json()
        user = "befa2043-c7a6-4762-0d56-08dc999e2a64"
        new_group_id = response['groupId']
        assert len(new_group_id) > 0
        req = {
                  "name": "MultiGroups",
                  "email": "MultiGroups@comda.co.il",
                  "username": "string",
                  "type": 3,
                  "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
                  "additionalGroupsIds": [
                    new_group_id
                  ]
                }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, user)
        assert update_user.status_code == StatusCode.OK

        sleep(5)

        get_groups = WesignMethodsApi.admins_groups_get(self)
        data = get_groups.json()

        response = data['groups']
        groups = []
        for x in response:
            groups.append(x['groupId'])

        for item in groups:
            if item == new_group_id:
                break
        else:
            raise Exception(f"{new_group_id} Not found")

        delete_group = WesignMethodsApi.admins_groups_delete(self, f'{new_group_id}')
        assert delete_group.status_code == StatusCode.BAD_REQUEST

        response = delete_group.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.THERE_ARE_USERS_IN_GROUP
        sleep(5)
        switch_group = WesignMethodsApi.users_switch_group_payload(self, new_group_id)
        sleep(5)
        new_token = switch_group.json()
        old_token = self.token
        assert new_token['token'] != old_token

        sleep(2)

        req = {
            "name": "MultiGroups",
            "email": "MultiGroups@comda.co.il",
            "username": "string",
            "type": 3,
            "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
            "additionalGroupsIds": []
        }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, user)
        assert update_user.status_code == StatusCode.OK

        delete_group = WesignMethodsApi.admins_groups_delete(self, f'{new_group_id}')
        assert delete_group.status_code == StatusCode.OK

    @pytest.mark.multi
    def test_add_user_to_another_group_validate_data_success(self):
        old_token = self.token
        r = WesignMethodsApi.document_collections_get_parameters(self)
        assert r.status_code == StatusCode.OK
        response = json.loads(r.content)
        document_collection = response["documentCollections"]
        first_group_document = []
        for x in document_collection:
            first_group_document.append(x["documentCollectionId"])

        templates_first_group = []
        templates = WesignMethodsApi.templates_get_all_templates(self)
        assert templates.status_code == StatusCode.OK
        temp = json.loads(templates.content)
        templates = temp["templates"]
        for x in templates:
            templates_first_group.append(x["templateId"])

        contacts_first_group = []
        contacts = WesignMethodsApi.contacts_get(self)
        assert contacts.status_code == StatusCode.OK
        con = json.loads(contacts.content)
        contacts_response = con["contacts"]
        for x in contacts_response:
            contacts_first_group.append(x["id"])

        group = uuid.uuid4().hex
        self.group_name = group
        payload = {
            "name": self.group_name
        }

        r = WesignMethodsApi.admins_groups_post_payload(self, payload)
        assert r.status_code == StatusCode.OK
        response = r.json()
        user = "befa2043-c7a6-4762-0d56-08dc999e2a64"
        new_group_id = response['groupId']
        assert len(new_group_id) > 0
        req = {
            "name": "MultiGroups",
            "email": "MultiGroups@comda.co.il",
            "username": "string",
            "type": 3,
            "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
            "additionalGroupsIds": [
                new_group_id
            ]
        }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, user)
        assert update_user.status_code == StatusCode.OK

        sleep(2)
        get_groups = WesignMethodsApi.admins_groups_get(self)
        data = get_groups.json()

        response = data['groups']
        groups = []
        for x in response:
            groups.append(x['groupId'])

        for item in groups:
            if item == new_group_id:
                break
        else:
            raise Exception(f"{new_group_id} Not found")

        delete_group = WesignMethodsApi.admins_groups_delete(self, f'{new_group_id}')
        assert delete_group.status_code == StatusCode.BAD_REQUEST

        response = delete_group.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.THERE_ARE_USERS_IN_GROUP
        sleep(120)
        switch_group = WesignMethodsApi.users_switch_group_payload(self, new_group_id)
        new = switch_group.json()
        response = new['token']

        sleep(2)
        assert response != old_token

        self.token = response

        r = WesignMethodsApi.document_collections_get_parameters(self)
        assert r.status_code == StatusCode.OK
        response = json.loads(r.content)
        document_collection = response["documentCollections"]
        second_group_document = []
        for x in document_collection:
            second_group_document.append(x["documentCollectionId"])

        set1 = set(first_group_document)
        set2 = set(second_group_document)
        common_values = set1.intersection(set2)
        if common_values:
            raise Exception(f"Common values found: {common_values}")

        templates_second_group = []
        templates_second = WesignMethodsApi.templates_get_all_templates(self)
        assert templates_second.status_code == StatusCode.OK
        temp = json.loads(templates_second.content)
        res = temp["templates"]
        for x in res:
            templates_second.append(x["templateId"])

        set1 = set(templates_first_group)
        set2 = set(templates_second_group)
        common_values = set1.intersection(set2)
        if common_values:
            raise Exception(f"Common values found: {common_values}")

        contacts_second_group = []
        contacts_second = WesignMethodsApi.contacts_get(self)
        assert contacts_second.status_code == StatusCode.OK
        con_second = json.loads(contacts_second.content)
        contacts_second_response = con_second["contacts"]
        for x in contacts_second_response:
            contacts_second_group.append(x["id"])

        set1 = set(contacts_first_group)
        set2 = set(contacts_second_response)
        common_values = set1.intersection(set2)
        if common_values:
            raise Exception(f"Common values found: {common_values}")

        sleep(2)
        switch_group = WesignMethodsApi.users_switch_group_payload(self, "9de765cd-2892-4f7e-e071-08dc999e2a5d")
        sleep(0.5)
        new_token = switch_group.json()
        self.token = new_token['token']

        req = {
            "name": "MultiGroups",
            "email": "MultiGroups@comda.co.il",
            "username": "string",
            "type": 3,
            "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
            "additionalGroupsIds": []
        }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, user)
        assert update_user.status_code == StatusCode.OK

        delete_group = WesignMethodsApi.admins_groups_delete(self, f'{new_group_id}')
        assert delete_group.status_code == StatusCode.OK

    @pytest.mark.multi
    def test_add_user_to_multi_groups_success(self):
        all_groups_id = ["9de765cd-2892-4f7e-e071-08dc999e2a5d"]
        for x in range(5):
            group = uuid.uuid4().hex
            self.group_name = group
            payload = {
                "name": self.group_name
            }
            r = WesignMethodsApi.admins_groups_post_payload(self, payload)
            assert r.status_code == StatusCode.OK

            response = r.json()
            new_group_id = response['groupId']
            assert len(new_group_id) > 0
            all_groups_id.append(new_group_id)

        user = "befa2043-c7a6-4762-0d56-08dc999e2a64"
        req = {
            "name": "MultiGroups",
            "email": "MultiGroups@comda.co.il",
            "username": "string",
            "type": 3,
            "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
            "additionalGroupsIds": all_groups_id

        }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, user)
        assert update_user.status_code == StatusCode.OK

        sleep(5)


        get_groups = WesignMethodsApi.admins_groups_get(self)
        data = get_groups.json()
        for group in data['groups']:
            group_id = group['groupId']
            if group_id in all_groups_id:
                print(f"{group_id} is found in all_groups_id.")
            else:
                print(f"{group_id} is not found in all_groups_id.")

        indices_to_remove = [0, 1]
        for index in sorted(indices_to_remove, reverse=True):
            all_groups_id.pop(index)

        # del all_groups_id[0]

        for x in range(len(all_groups_id)):
            delete_group = WesignMethodsApi.admins_groups_delete(self, f'{all_groups_id[x]}')
            assert delete_group.status_code == StatusCode.BAD_REQUEST

            response = delete_group.json()
            json_response = response['errors']['error']
            assert json_response[0] == ResultCode.THERE_ARE_USERS_IN_GROUP

        req = {
            "name": "MultiGroups",
            "email": "MultiGroups@comda.co.il",
            "username": "string",
            "type": 3,
            "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
            "additionalGroupsIds": [
                "ca80a7bc-a4e7-42f5-b5a0-08dca18dc640"

            ]
        }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, user)
        assert update_user.status_code == StatusCode.OK

        for x in range(len(all_groups_id)):
            delete_group = WesignMethodsApi.admins_groups_delete(self, f'{all_groups_id[x]}')
            assert delete_group.status_code == StatusCode.OK

    @pytest.mark.multi
    def test_delete_user_from_multi_groups(self):
        group = uuid.uuid4().hex
        self.group_name = group
        payload = {
            "name": self.group_name
        }

        r = WesignMethodsApi.admins_groups_post_payload(self, payload)
        assert r.status_code == StatusCode.OK
        response = r.json()
        user = "befa2043-c7a6-4762-0d56-08dc999e2a64"
        new_group_id = response['groupId']
        assert len(new_group_id) > 0
        req = {
            "name": "MultiGroups",
            "email": "MultiGroups@comda.co.il",
            "username": "string",
            "type": 3,
            "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
            "additionalGroupsIds": [
                new_group_id
            ]
        }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, user)
        assert update_user.status_code == StatusCode.OK

        delete_group = WesignMethodsApi.admins_groups_delete(self, f'{new_group_id}')
        assert delete_group.status_code == StatusCode.BAD_REQUEST

        response = delete_group.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.THERE_ARE_USERS_IN_GROUP

        req = {
            "name": "MultiGroups",
            "email": "MultiGroups@comda.co.il",
            "username": "string",
            "type": 3,
            "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
            "additionalGroupsIds": []
        }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, user)
        assert update_user.status_code == StatusCode.OK

        delete_group = WesignMethodsApi.admins_groups_delete(self, f'{new_group_id}')
        assert delete_group.status_code == StatusCode.OK

        get_groups = WesignMethodsApi.admins_groups_get(self)
        data = get_groups.json()
        for group in data['groups']:
            assert new_group_id not in group['groupId']

    @pytest.mark.multi
    def test_add_user_to_another_group_validate_data_in_existing_group_success(self):
        old_token = self.token
        r = WesignMethodsApi.document_collections_get_parameters(self)
        assert r.status_code == StatusCode.OK
        response = json.loads(r.content)
        document_collection = response["documentCollections"]
        first_group_document = []
        for x in document_collection:
            first_group_document.append(x["documentCollectionId"])

        templates_first_group = []
        templates = WesignMethodsApi.templates_get_all_templates(self)
        assert templates.status_code == StatusCode.OK
        temp = json.loads(templates.content)
        templates = temp["templates"]
        for x in templates:
            templates_first_group.append(x["templateId"])

        contacts_first_group = []
        contacts = WesignMethodsApi.contacts_get(self)
        assert contacts.status_code == StatusCode.OK
        con = json.loads(contacts.content)
        contacts_response = con["contacts"]
        for x in contacts_response:
            contacts_first_group.append(x["id"])

        sleep(120)
        switch_group = WesignMethodsApi.users_switch_group_payload(self, "ca80a7bc-a4e7-42f5-b5a0-08dca18dc640")
        new = switch_group.json()
        response = new['token']

        sleep(2)
        assert response != old_token

        self.token = response

        r = WesignMethodsApi.document_collections_get_parameters(self)
        assert r.status_code == StatusCode.OK
        response = json.loads(r.content)
        document_collection = response["documentCollections"]
        second_group_document = []
        for x in document_collection:
            second_group_document.append(x["documentCollectionId"])

        set1 = set(first_group_document)
        set2 = set(second_group_document)
        common_values = set1.intersection(set2)
        if common_values:
            raise Exception(f"Common values found: {common_values}")

        templates_second_group = []
        templates_second = WesignMethodsApi.templates_get_all_templates(self)
        assert templates_second.status_code == StatusCode.OK
        temp = json.loads(templates_second.content)
        res = temp["templates"]
        for x in res:
            templates_second_group.append(x["templateId"])

        set1 = set(templates_first_group)
        set2 = set(templates_second_group)
        common_values = set1.intersection(set2)
        if common_values:
            raise Exception(f"Common values found: {common_values}")

        contacts_second_group = []
        contacts_second = WesignMethodsApi.contacts_get(self)
        assert contacts_second.status_code == StatusCode.OK
        con_second = json.loads(contacts_second.content)
        contacts_second_response = con_second["contacts"]
        for x in contacts_second_response:
            contacts_second_group.append(x["id"])

        set1 = set(contacts_first_group)
        set2 = set(contacts_second_group)
        common_values = set1.intersection(set2)
        if common_values:
            raise Exception(f"Common values found: {common_values}")

    @pytest.mark.multi
    def test_switch_group_not_attached(self):
        group = uuid.uuid4().hex
        self.group_name = group
        payload = {
            "name": self.group_name
        }

        r = WesignMethodsApi.admins_groups_post_payload(self, payload)
        assert r.status_code == StatusCode.OK
        response = r.json()
        new_group_id = response['groupId']
        assert len(new_group_id) > 0
        sleep(60)
        switch_group = WesignMethodsApi.users_switch_group_payload(self, new_group_id)
        assert switch_group.status_code == StatusCode.BAD_REQUEST
        delete_group = WesignMethodsApi.admins_groups_delete(self, f'{new_group_id}')
        assert delete_group.status_code == StatusCode.OK

    @pytest.mark.multi
    def test_switch_group_user_connected_to_attached(self):
        sleep(5)
        switch_group = WesignMethodsApi.users_switch_group_payload(self, "9de765cd-2892-4f7e-e071-08dc999e2a5d")
        res = switch_group.json()
        assert switch_group.status_code == StatusCode.BAD_REQUEST
        assert res['errors']['error'] == ResultCode.USER_IS_ALREADY_CONNECTED_TO_THE_GROUP

    def delete_all_groups(self):
        try:
            all_groups_id = []
            get_groups = WesignMethodsApi.admins_groups_get(self)
            data = get_groups.json()
            for group in data['groups']:
                group_id = group['groupId']
                all_groups_id.append(group_id)
            indices_to_remove = [0, 1]
            for index in sorted(indices_to_remove, reverse=True):
                all_groups_id.pop(index)

            delete_group = WesignMethodsApi.admins_groups_delete(self, f'{all_groups_id[0]}')
            assert delete_group.status_code == StatusCode.OK
        except:
            pass

    def tearDown(self):
        req = {
            "name": "MultiGroups",
            "email": "MultiGroups@comda.co.il",
            "username": "string",
            "type": 3,
            "groupId": "9de765cd-2892-4f7e-e071-08dc999e2a5d",
            "additionalGroupsIds": [
                "ca80a7bc-a4e7-42f5-b5a0-08dca18dc640"

            ]
        }

        update_user = WesignMethodsApi.admins_users_id_put_file(self, req, "befa2043-c7a6-4762-0d56-08dc999e2a64")
        assert update_user.status_code == StatusCode.OK
        sleep(1)
        self.delete_all_groups()
        sleep(3)

    if __name__ == "__main__":
        unittest.main()


