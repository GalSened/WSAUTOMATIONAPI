# import unittest
# import uuid
# import warnings
# from pathlib import Path
# from time import sleep
# import pytest
# import json
# from Enums.status_codes import StatusCode, ResultCode
# from Common.all_api_methods import WesignMethodsApi
# from shared import Shared
#
#
# @pytest.mark.flaky(max_runs=3)
# class WesignApiMultiGroupsTests(unittest.TestCase):
#     def setUp(self):
#         # p = Path(__file__).with_name('UsersSettings.json')
#         # with open(p) as f:
#         #     self.settings = json.load(f)
#         p = Path(__file__).resolve().parent.parent
#         file_path = p / "Settings\\UsersSettings.json"
#         with open(file_path) as f:
#             self.settings = json.load(f)
#         warnings.simplefilter('ignore', ResourceWarning)
#         warnings.simplefilter('ignore', DeprecationWarning)
#         self.token = Shared.login_multi_groups_account(self)
#
#     @pytest.mark.part1
#     def test_add_user_to_another_group_success(self):
#         group = uuid.uuid4().hex
#         self.group_name = group
#         payload = {
#               "name": self.group_name
#             }
#
#         r = WesignMethodsApi.admins_groups_post_payload(self, payload)
#         assert r.status_code == StatusCode.OK
#         response = r.json()
#         json_response = response['groupId']
#         assert len(json_response) > 0
#         delete_group = WesignMethodsApi.admins_groups_delete(self, f'{json_response}')
#         assert delete_group.status_code == StatusCode.OK
#
#
#     def tearDown(self):
#         sleep(3)
#
#     if __name__ == "__main__":
#         unittest.main()
#
