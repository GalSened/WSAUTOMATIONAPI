# WeSign Automation API

This repository contains automated API tests and helper utilities for the WeSign service. The main entry point for interacting with the API is the `WesignMethodsApi` class located under `Common/all_api_methods.py`.

## Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Repository Structure

- **Common/** – implementation of the `WesignMethodsApi` class containing helper methods for all HTTP endpoints.
- **Enums/** – enumerations for status codes and result codes used in tests.
- **Settings/** – JSON configuration files used by the tests.
- **Python Api Requests/** – example request payloads for various API calls.
- **Tests/** – pytest test suites that exercise the API.

## Using `WesignMethodsApi`

`WesignMethodsApi` is a collection of static‑like methods grouped by feature area. Each method assumes that `self.settings` contains configuration values (such as `Base_Url`) and that `self.token` contains a valid authentication token. Tests inherit these methods by passing their own `self` instance.

Example usage within a test:

```python
from Common.all_api_methods import WesignMethodsApi

class MyTests(unittest.TestCase):
    def setUp(self):
        with open('Settings/settings.json') as f:
            self.settings = json.load(f)
        self.token = obtain_token_somehow()

    def test_get_contacts(self):
        response = WesignMethodsApi.contacts_get(self)
        assert response.status_code == 200
```

## Available API Methods

Below is a non-exhaustive list of available helper methods grouped by category. Each line also notes the expected request payload or where to find sample JSON. For detailed parameter information see the implementation in `Common/all_api_methods.py`.

### Contacts
- `contacts_id_get(contact_id)` – **GET** `/contacts/{contact_id}` – Retrieve a contact by ID. Payload: none. Response: 200 OK.
- `contacts_bulk_post_xlsx_file(base64_string)` – **POST** `/contacts/bulk` – Upload contacts via XLSX. Payload: base64 XLSX. Response: 200 OK.
- `contacts_id_delete(contact_id)` – **DELETE** `/contacts/{contact_id}` – Delete a contact by ID. Payload: none. Response: 200 OK.
- `contacts_get()` – **GET** `/contacts` – Fetch contacts list. Payload: none. Response: 200 OK.
- `contacts_id_put(contact_id, request_file)` – **PUT** `/contacts/{contact_id}` – Update a contact. Payload: `{ "name": "ApiUser", "email": "ApiUserTest@ApiUser.com", "phone": "05012345678" }`. Response: 200 OK.
- `contacts_bulk_post_json_file(request_file)` – **POST** `/contacts/bulk` – Bulk create contacts. Payload: `[{"name": "ApiUser", "email": "ApiUserTest@ApiUser.com"}]`. Response: 200 OK.
- `contacts_post_json_file(request_file)` – **POST** `/contacts` – Create a contact. Payload: `{ "name": "ApiUser", "email": "ApiUserTest@ApiUser.com", "phone": "05012345678" }`. Response: 200 OK.
- `contacts_post(parameters)` – **POST** `/contacts` – Create a contact from a dictionary. Payload: `{"name": "ApiUser"}`. Response: 200 OK.
- `contacts_delete_batch_put(list_of_ids)` – **PUT** `/contacts/deletebatch` – Delete contacts in batch. Payload: `{"ids": ["id1", "id2"]}`. Response: 200 OK.
- `contacts_group_post(request_file)` – **POST** `/contacts/Group` – Create a contacts group. Payload: `{ "name": "TestApi" }`. Response: 200 OK.
- `contacts_group_put(payload, group_id)` – **PUT** `/contacts/Group/{group_id}` – Update a contacts group. Payload: `{ "name": "Updated" }`. Response: 200 OK.
- `contacts_group_delete(group_id)` – **DELETE** `/contacts/Group/{group_id}` – Delete a contacts group. Payload: none. Response: 200 OK.
- `contacts_group_get(group_id)` – **GET** `/contacts/Group/{group_id}` – Retrieve a specific group. Payload: none. Response: 200 OK.
- `contacts_all_group_get()` – **GET** `/contacts/Groups` – Retrieve all groups. Payload: none. Response: 200 OK.

### Distribution
- `distribution_signers_post_json_file(signers_file)` – **POST** `/documents/distribution/signers` – Add signers via JSON file. Payload: `{ "signers": [{"contactId": "58999b4b-2596-4809-7685-08d98f12bf81", "sendingMethod": 2}] }`. Response: 200 OK.
- `distribution_signers_post_xlsx_file(signers_base64)` – **POST** `/documents/distribution/signers` – Add signers via XLSX file. Payload: base64 XLSX. Response: 200 OK.
- `distribution_post_json_file(request_file)` – **POST** `/documents/distribution` – Distribute a document. Payload: `{ "documentName": "TestApi", "templates": ["bc1ea668-9e1e-4d3f-22d5-08d9bd4c8663"] }`. Response: 200 OK.

### Templates
- `templates_post_json_file(request_file)` – **POST** `/templates` – Create a template. Payload: `{ "base64File": "data:application/pdf;base64,...", "name": "Test" }`. Response: 200 OK.
- `templates_id_delete(template_guid)` – **DELETE** `/templates/{template_guid}` – Delete a template. Payload: none. Response: 200 OK.
- `templates_id_put_json_file(field_file, template_id)` – **PUT** `/templates/{template_id}` – Update a template. Payload: `{ "name": "Updated" }`. Response: 200 OK.
- `templates_id_put_dict(data, template_id)` – **PUT** `/templates/{template_id}` – Update a template using a dictionary. Payload: dict. Response: 200 OK.
- `templates_id_post_json_file(request_file, template_id)` – **POST** `/templates/{template_id}` – Upload a file to a template. Payload: `{ "base64File": "data:application/pdf;base64,..." }`. Response: 200 OK.
- `templates_id_download_get(template_id)` – **GET** `/templates/{template_id}/download` – Download the template file. Payload: none. Response: 200 OK.
- `templates_delete_batch_put(del_req)` – **PUT** `/templates/deletebatch` – Batch delete templates. Payload: dict. Response: 200 OK.
- `templates_merge_post(merge)` – **POST** `/templates/merge` – Merge templates from a dictionary. Payload: dict. Response: 200 OK.
- `templates_merge_post_json_file(request_file)` – **POST** `/templates/merge` – Merge templates using JSON file. Payload: `{ "templateIds": ["id1", "id2"] }`. Response: 200 OK.
- `templates_get_all_templates()` – **GET** `/templates` – List templates. Payload: none. Response: 200 OK.

### Admins
- `admins_groups_post_json_file(request_file)` – **POST** `/admins/groups` – Create an admin group from JSON file. Payload: `{ "name": "TestApi" }`. Response: 200 OK.
- `admins_groups_post_payload(paylod)` – **POST** `/admins/groups` – Create an admin group using a dictionary. Payload: `{"name": "TestApi"}`. Response: 200 OK.
- `admins_groups_delete(group_id)` – **DELETE** `/admins/groups/{group_id}` – Delete an admin group. Payload: none. Response: 200 OK.
- `admins_groups_put_json_file(request_file, group_id)` – **PUT** `/admins/groups/{group_id}` – Update an admin group. Payload: `{ "name": "Updated" }`. Response: 200 OK.
- `admins_groups_get()` – **GET** `/admins/groups` – List admin groups. Payload: none. Response: 200 OK.
- `admins_users_post_json_file(request_file)` – **POST** `/admins/users` – Create an admin user from JSON. Payload: `{ "name": "Admin", "email": "AdminApi@comsign.co.il" }`. Response: 200 OK.
- `admins_users_id_delete(user_id)` – **DELETE** `/admins/users/{user_id}` – Delete an admin user. Payload: none. Response: 200 OK.
- `admins_users_get()` – **GET** `/admins/users` – List admin users. Payload: none. Response: 200 OK.
- `admins_users_id_put_json_file(request_file, user_id)` – **PUT** `/admins/users/{user_id}` – Update an admin user. Payload: `{ "name": "Admin" }`. Response: 200 OK.
- `admins_users_id_put_file(payload, user_id)` – **PUT** `/admins/users/{user_id}` – Update an admin user using a dictionary. Payload: `{"email": "admin@update.com"}`. Response: 200 OK.

### Users
- `users_validate_otp_flow(payload)` – **POST** `/users/validateOtpflow` – Validate OTP during login flow. Payload: `{"otp": "123456"}`. Response: 200 OK.
- `users_login_post_json_file(request_file)` – **POST** `/users/login` – Perform login using a JSON file. Payload: `{ "email": "wesignautomation@gmail.com", "password": "Comsign1!" }`. Response: 200 OK.
- `users_login_post_payload(data)` – **POST** `/users/login` – Perform login using a dictionary. Payload: `{ "email": "wesignautomation@gmail.com" }`. Response: 200 OK.
- `users_login_change_json_file(data)` – **POST** `/users/change` – Change password for logged‑in user. Payload: `{ "password": "newPass" }`. Response: 200 OK.
- `users_switch_group_payload(group_id)` – **POST** `/users/SwitchGroup/{group_id}` – Switch current user group. Payload: `{}`. Response: 200 OK.
- `users_sign_up(payload)` – **POST** `/users` – Sign up a new user. Payload: `{ "name": "User", "email": "user@example.com" }`. Response: 200 OK.

### Self Sign
- `self_sign_post_json_file(request_file)` – **POST** `/selfsign` – Initiate self‑signing flow. Payload: `{ "documentName": "SelfSign" }`. Response: 200 OK.
- `self_sign_put_json_file(request_file)` – **PUT** `/selfsign` – Update self‑signing flow. Payload: `{ "documentName": "SelfSign" }`. Response: 200 OK.
- `self_sign_id_delete(document_id)` – **DELETE** `/selfsign/{document_id}` – Delete a self‑signed document. Payload: none. Response: 200 OK.
- `self_sign_download_smartcard_get()` – **GET** `/selfsign/download/smartcard` – Download a smartcard for self‑sign. Payload: none. Response: 200 OK.

### Document Collections
- `document_collections_post_json_file(request_file)` – **POST** `/documentcollections` – Create a document collection. Payload: `{ "documentName": "TestApi" }`. Response: 200 OK.
- `document_collections_post_json_file_using_twillio(request_file)` – **POST** `/documentcollections` – Create using Twilio settings. Payload: `{ "documentName": "TestApi" }`. Response: 200 OK.
- `document_collections_id_delete(document_collection_id)` – **DELETE** `/documentcollections/{id}` – Delete a document collection. Payload: none. Response: 200 OK.
- `document_collections_id_cancel_put(document_collection_id)` – **PUT** `/documentcollections/{id}/cancel` – Cancel a document collection. Payload: none. Response: 200 OK.
- `document_collections_id_signers_signerId_method_sendingMethod_get(document_collection_id, signer_id)` – **GET** `/documentcollections/{id}/signers/{signer_id}/method/2` – Retrieve signer sending method. Payload: none. Response: 200 OK.
- `document_collections_id_signer_signerId_replace_put(document_collection_id, signer_id, request_file)` – **PUT** `/documentcollections/{signer_id}/signer/{document_collection_id}/replace` – Replace signer details. Payload: `{ "signers": [{"contactId": "58999b4b"}] }`. Response: 200 OK.
- `document_collections_share_post_json_file(request_file)` – **POST** `/documentcollections/share` – Share a document collection. Payload: `{ "message": "please sign" }`. Response: 200 OK.
- `document_collections_post_dict(data)` – **POST** `/documentcollections` – Create using a dictionary payload. Payload: `{}`. Response: 200 OK.
- `document_collections_post_dict_using_signer1(data)` – **POST** `/documentcollections` with `signer1` token – Create using signer1 token. Payload: `{}`. Response: 200 OK.
- `document_collections_delete_batch_put_dict(del_req)` – **PUT** `/documentcollections/deletebatch` – Batch delete document collections. Payload: `{"ids": ["id1"]}`. Response: 200 OK.
- `document_collections_id_get(document_id)` – **GET** `/documentcollections/{document_id}` – Retrieve a document collection. Payload: none. Response: 200 OK.
- `document_collections_id_json_get(document_id)` – **GET** `/documentcollections/{document_id}/json` – Retrieve a document collection in JSON format. Payload: none. Response: 200 OK.
- `document_collections_download_batch_post_ids(list_of_ids)` – **POST** `/documentcollections/downloadbatch` – Download multiple documents. Payload: list of ids. Response: 200 OK.
- `document_collections_get_parameters()` – **GET** `/documentcollections` with parameters – List document collections with parameters. Payload: none. Response: 200 OK.
- `document_collections_get_parameters_download()` – **GET** `/documentcollections` with parameters – List with download info. Payload: none. Response: 200 OK.
- `document_collections_get_parameters_tablet(template_key)` – **GET** `/documentcollections` with tablet parameters – List for tablet mode. Payload: none. Response: 200 OK.
- `document_collections_unsigned_get_parameters()` – **GET** `/documentcollections` with parameters – List unsigned document collections. Payload: none. Response: 200 OK.
- `document_collections_id_get_fields_xml(document_id)` – **GET** `/documentcollections/{document_id}` – Get fields XML. Payload: none. Response: 200 OK.
- `document_collections_id_get_document_collection_links(document_id)` – **GET** `/documentcollections/{document_id}/DocumentCollectionLinks` – Get document links. Payload: none. Response: 200 OK.
- `document_collections_id_get_extra_info_json(document_id)` – **GET** `/documentcollections/{document_id}/ExtraInfo/json` – Get extra information. Payload: none. Response: 200 OK.
- `document_collections_export_distribution()` – **GET** `/documentcollections/exportDistribution` – Export distribution. Payload: none. Response: 200 OK.
- `document_collections_id_get_data_fields_info_json(with_signatures)` – **GET** `/documentcollections/<id>/fields/json?includeSigantures={with_signatures}` – Get data field info. Payload: none. Response: 200 OK.
- `document_collections_reactive(document_id)` – **GET** `/documentcollections/{document_id}/reactivate` – Reactivate a cancelled collection. Payload: none. Response: 200 OK.

## Request Payload Samples

Ready-made JSON bodies are available under the `Python Api Requests/` directory.
Each subfolder groups payloads by feature and the `Settings/*.json` files
reference them. Main folders include:

- `ContactRequest/` – contact creation and update payloads
- `CreateGroup/` – group management payloads
- `CreateTemplateRequest/` – template creation examples
- `UpdateTemplateRequest/` – template update examples
- `DocumentCollectionRequest/` – document distribution and collection samples
- `LoginRequest/` – login request bodies
- `UsersRequest/` – user management payloads

Opening any of these files reveals the exact JSON sent to the API. For example
`Python Api Requests/ContactRequest/CreateNewValidContactWithEmailAndPhone.json`
contains:

```json
{
  "name": "ApiUser",
  "email": "ApiUserTest@ApiUser.com",
  "phone": "05012345678",
  "defaultSendingMethod": 1
}
```

Adjust the paths in the configuration files if your payloads reside elsewhere.

## Response Status Codes

Most helper methods return JSON and follow common HTTP status codes defined in
`Enums/status_codes.py`:

- **200 OK** – Successful request. For example creating a contact returns
  `{ "contactId": "<guid>" }`.
- **400 BAD_REQUEST** – Validation failed. Responses include an `errors`
  dictionary such as `{ "errors": { "Phone": ["Please specify valid Phone"] } }`.
- **401 UNAUTHORIZED** – Authentication is missing or expired.
- **500 SERVER_ERROR** – The server encountered an unexpected condition.

## Running Tests

The `Tests/` directory contains a suite of pytest tests. To run the tests locally:

```bash
pytest -q
```

Some tests rely on external resources (such as Selenium drivers and network access). Ensure the environment has all dependencies installed and required services are reachable.

