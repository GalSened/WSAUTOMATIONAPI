class StatusCode:
    BAD_REQUEST = 400
    OK = 200
    SERVER_ERROR = 500
    UNAUTHORIZED = 401

class ResultCode:
    INVALID_CREDENTIAL = 2, "Invalid credential"
    PLEASE_SPECIFY_A_VALID_EMAIL = 'Please specify a valid Email'
    PLEASE_SPECIFY_AN_EMAIL = 'Please specify an Email'
    FIELD_NAME_NOT_EXIST = 'Field name not exist'
    PLEASE_SPECIFY_FIELD_NAME_IN_READ_ONLY_FIELDS = 'Field name not exist'
    READ_ONLY_FIELDS_SHOULD_CONTAIN_VALUE = "Read only fields should contain value"
    TEMPLATES_IN_SIGNERS_FIELDS_AND_IN_READ_ONLY_FIELDS_MUST_BE_FROM_TEMPLATES_COLLECTION_INPUT = "Templates in signers fields and in read only fields must be from templates collection input"
    PLEASE_SPECIFY_A_NAME = "Please specify a Name"
    PLEASE_SPECIFY_VALID_DOCUMENT_MODE = "Please specify valid DocumentMode: 1 (OrderedGroupSign ) or 2 (GroupSign) or 3 (Online)"
    CONTACT_NOT_CREATED_BY_USER = "Contact not created by user"
    THERE_IS_DUPLICATE_FIELD_FOR_SIGNER = 'There is duplicate field for signer'
    SIGNER_METHOD_NOT_FEET_TO_CONTACT_MEANS = "Signer method not feet to contact means"
    OVERLAYING_FIELDS_PLEASE_MOVE_THE_FIELDS = "Signature fields coordinates must be unique, remove duplication fields with same X , Y - [X=0.1397916666666666;Y=0.1559055118110236]"
    SIGNATURE_FIELDS_MUST_BE_UNIQUE = "Signature fields must be unique, remove duplication fields- [sign1]"
    INVALID_TEMPLATE_ID = 'Invalid template id'
    RADIOGROUP_FIELDS_MUST_BE_UNIQUE_REMOVE_DUPLICATION_FIELDS = "RadioGroup fields must be unique, remove duplication fields- [test]"
    INVALID_FIELD_TYPE_NUMBER = 'Field type [8] for a text field named [text1] not supported'
    BASE_64_FILE_UNSUPPORTED_TYPE = 'Supported FileType are: PDF, DOCX, PNG, JPG , JPEG. Please specify a valid Base64File in format data:application/FILE_TYPE;base64,.... '
    READ_ONLY_FIELDS_SHOULD_CONTAIN_NAME_AND_VALUE = 'Read only fields should contain name and value'
    PLEASE_SPECIFY_VALID_SIGNERS = 'Please specify valid signers (signer should contain contactId with valid sendingMethod (sms-1,email-2 or tablet-3) or contantMeans with contactName)'
    GROUP_WITH_SAME_NAME = 'Group with same name already exist in company'
    EMPTY_NAME = "'Name' must not be empty."
    THERE_ARE_USERS_IN_GROUP = 'There are users in group'
    INVALID_USER_TYPE = 'Valid UserType: 1 (Basic) or 2 (Editor) or 3 (CompanyAdmin)'
    INVALID_GROUP_ID = 'Invalid GroupId'