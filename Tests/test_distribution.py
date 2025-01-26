import random
import string
import unittest
import uuid
import warnings
from pathlib import Path
from time import sleep

import pyodbc
import pytest
import json
import names
import openpyxl
import base64
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from Enums.status_codes import StatusCode, ResultCode
from telnetlib import EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common.all_api_methods import WesignMethodsApi
from shared import Shared
from selenium.webdriver.chrome.service import Service


@pytest.mark.flaky(max_runs=6)
class WesignApiCreateDocumentDistributionTests(unittest.TestCase):
    def setUp(self):
        # p = Path(__file__).with_name('DistributeCollection.json')
        # with open(p) as f:
        #     self.settings = json.load(f)

        p = Path(__file__).resolve().parent.parent
        file_path = p / "Settings\\DistributeCollection.json"
        with open(file_path) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    @pytest.mark.part1
    def test_api_sending_distribution_and_receiving_confirmation_for_document_viewed_and_signed_success(self):
        self.token = Shared.login_request(self)
        self.__setup()
        sleep(2)
        emails = [self.settings['dev_email']]
        self.__enter_name_and_email_to_xlsx_file(self.settings["empty_xlsx_file"],
                                                 self.settings["empty_file_with_no_fields_Copy"], emails)
        data = open(self.settings["empty_file_with_no_fields_Copy"], "rb").read()
        encode_signers_to_base64 = base64.b64encode(data)
        signers_base64 = encode_signers_to_base64.decode('utf-8')
        signers = WesignMethodsApi.distribution_signers_post_xlsx_file(self, {
            "base64File": "data:application/vnd.ms-excel;base64," + signers_base64 + ""})
        signers_json = signers.json()
        assert signers.status_code == StatusCode.OK
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        self.document_name = uuid.uuid4().hex
        with open(self.settings["DistributeSignersApi_Copy"], 'r+') as f:
            data = json.load(f)
            data["name"] = self.document_name  # <--- add `id` value.
            data["templateId"] = template
            data["signers"] = signers_json['signers']
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "DistributeSignersApi_Copy")
        assert send_distribution.status_code == StatusCode.OK
        sleep(2)
        doc_id = self.__get_documentCollectionId_from_db(self.document_name)

        self.__get_link_by_signers_number_without_signing(1, doc_id)
        sleep(2.5)

        WebDriverWait(self.driver, 50).until(EC.presence_of_element_located((By.ID, "logo_image")))
        sleep(2.5)
        self.driver.find_element(By.XPATH, "//button[@class='ct-button--titlebar-primary ng-star-inserted']").click()
        sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "ct-button--primary")))
        sleep(400)
        self.__enter_comda_mail(self.settings['second_dev_email'], self.settings['comda_mail_password'])
        sleep(1.5)
        WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH,
                                                                             f"(//*[contains(text(), '{self.document_name} has been completed')])[1]")))
        assert self.driver.find_element(By.XPATH,
                                        f"//*[contains(text(), '({self.settings['dev_email']}) has viewed {self.document_name}')]")
        assert self.driver.find_element(By.XPATH,
                                        f"//*[contains(text(), '({self.settings['dev_email']}) has signed {self.document_name}')]")

        # Bug number = WES-1021

    @pytest.mark.part2
    def test_api_sending_distribution_document_with_duplicated_signer_email_success(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "duplicated_signer_email_base64")
        signers_json = signers.json()
        self._change_values_in_file("duplicated_template_and_signer", template, signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "duplicated_template_and_signer")
        assert send_distribution.status_code == StatusCode.OK

    @pytest.mark.part3
    def test_api_sending_distribution_with_valid_email_all_fields_filled_from_xlsx_success(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self, "fields_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "signers_for_template_with_fields")
        signers_json = signers.json()
        self._change_values_in_file("distribute_file_with_users_and_field", template, signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribute_file_with_users_and_field")
        assert send_distribution.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_sending_distribution_email_with_valid_email_value_and_all_fields_in_template_and_no_fields_in_xlsx_success(
            self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        WesignMethodsApi.templates_id_put_json_file(self, "fields_for_template_not_in_xlsx_file", template)
        signers = WesignMethodsApi.distribution_signers_post_json_file(self,
                                                                       "signers_base64_for_templates_with_fields_no_fields_in_xlsx_file")
        signers_json = signers.json()
        self._change_values_in_file("fields_only_in_template", template, signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "fields_only_in_template")
        assert send_distribution.status_code == StatusCode.OK

    @pytest.mark.part2
    def test_api_sending_distribution_large_file_success(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "signers_no_field")
        signers_json = signers.json()
        self._change_values_in_file("distribute_10mega_file", template, signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribute_10mega_file")
        assert send_distribution.status_code == StatusCode.OK

    @pytest.mark.part3
    def test_api_distribution_two_signers_no_fields_success(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "seven_signers_no_fields - Copy")
        signers_json = signers.json()
        self._change_values_in_file("DistributeSignersApi_no_fields", template, signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "DistributeSignersApi_no_fields")
        assert send_distribution.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_sending_distribution_with_invalid_data_from_xlsx_file(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        WesignMethodsApi.templates_id_put_json_file(self, "template_with_invalid_fields", template)
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "signers_for_template_with_invalid_values")
        signers_json = signers.json()
        self._change_values_in_file("distribute_file_for_template_with_invalid_values", template,
                                    signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self,
                                                                         "distribute_file_for_template_with_invalid_values")
        assert send_distribution.status_code == StatusCode.BAD_REQUEST

    # Bug number = WES-1046/WES-1042
    @pytest.mark.part2
    def test_api_sending_distribution_with_xlsx_file_with_fields_but_no_fields_in_template(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "signers_for_template_with_fields")
        signers_json = signers.json()
        self._change_values_in_file("distribute_file_with_users_and_fields_in_xlsx", template, signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self,
                                                                         "distribute_file_with_users_and_fields_in_xlsx")
        assert send_distribution.status_code == StatusCode.BAD_REQUEST

    @pytest.mark.part3
    def test_api_distribution_seven_recipients_success(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "seven_signers_no_fields")
        signers_json = signers.json()
        self._change_values_in_file("distribute_seven_signers_api", template, signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribute_seven_signers_api")
        assert send_distribution.status_code == StatusCode.OK

    @pytest.mark.part1
    def test_send_distribute_invalid_email(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "invalid_signer_email")
        assert signers.status_code == StatusCode.BAD_REQUEST

    @pytest.mark.part2
    def test_send_distribute_empty_first_name_and_empty_last_name(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "signer_data_without_name")
        assert signers.status_code == StatusCode.BAD_REQUEST

    @pytest.mark.part3
    def test_send_distribute_empty_signer_means(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        signers = WesignMethodsApi.distribution_signers_post_json_file(self, "signer_data_without_means")
        assert signers.status_code == StatusCode.BAD_REQUEST

    # Bug number = WES-1106
    @pytest.mark.part1
    def test_send_distribute_duplicated_fields_in_xlsx_with_same_name_validate_values_success(self):
        self.__setup()
        sleep(1)
        emails = [self.settings['dev_email'], self.settings['second_dev_email']]
        self.__enter_name_and_email_to_xlsx_file(
            self.settings["sending_distribution_duplicated_fields_with_same_name_and_value_in_xlsx_edit"],
            self.settings["sending_distribution_duplicated_fields_with_same_name_and_value_in_xlsx_edit - Copy"],
            emails)
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        sleep(1)
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self,
                                                                          "Distribute_duplicated_fields_for_template",
                                                                          template)
        assert fields_for_template.status_code == StatusCode.OK
        sleep(1)
        data = open(
            self.settings["sending_distribution_duplicated_fields_with_same_name_and_value_in_xlsx_edit - Copy"],
            "rb").read()
        sleep(1)
        encode_signers_to_base64 = base64.b64encode(data)
        sleep(1)
        signers_base64 = encode_signers_to_base64.decode('utf-8')
        sleep(2)
        signers = WesignMethodsApi.distribution_signers_post_xlsx_file(self, {
            "base64File": "data:application/vnd.ms-excel;base64," + signers_base64 + ""})
        sleep(2)
        signers_json = signers.json()
        sleep(2)
        assert signers.status_code == StatusCode.OK
        sleep(2)
        self._change_values_in_file("DistributeSigners_duplicated_fields_in_xlsx_with_same_name", template,
                                    signers_json['signers'])
        sleep(2)
        send_distribution = WesignMethodsApi.distribution_post_json_file(self,
                                                                         "DistributeSigners_duplicated_fields_in_xlsx_with_same_name")
        assert send_distribution.status_code == StatusCode.OK
        sleep(1)
        doc_id = self.__get_documentCollectionId_from_db_distribute(self.document)
        ##first signer
        self.__get_link_by_signers_number_without_signing(1, doc_id[1])
        sleep(2)
        WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ct-input--primary")))
        self.__assert_number_of_fields(10)
        self.__assert_values_in_fields("Test1", "9012", "test1@comsign.co.il", "504821885", "1990-12-17")
        driver = self.driver
        sleep(1)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='ct-button--titlebar-primary ng-star-inserted']")))
        finish_button = "//button[@class='ct-button--titlebar-primary ng-star-inserted']"
        self.driver.find_element(By.XPATH, finish_button).click()
        sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(2)
        doc_id = self.__get_documentCollectionId_from_db_distribute(self.document)
        ##first signer
        self.__get_link_by_signers_number_without_signing(1, doc_id[0])
        sleep(2)
        WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ct-input--primary")))
        self.__assert_number_of_fields(10)
        self.__assert_values_in_fields("Test", "5678", "test@comsign.co.il", "504821887", "1989-08-23")
        sleep(1)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='ct-button--titlebar-primary ng-star-inserted']")))
        finish_button = "//button[@class='ct-button--titlebar-primary ng-star-inserted']"
        self.driver.find_element(By.XPATH, finish_button).click()
        sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//main/h2")))
        signing_complete_msg = self.driver.find_elements(By.XPATH, "//main/h2")
        assert len(signing_complete_msg) == 1

    @pytest.mark.part2
    def test_distribution_OTP_xlsx_file_success(self):
        self.token = Shared.login_request(self)
        self.__setup()
        email = self.__enter_temp_mail()
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        document_name = uuid.uuid4().hex
        full_name = names.get_full_name()
        self.__change_values_in_file_for_otp("Distribution_OTP", template, document_name, full_name, email)
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "Distribution_OTP")
        assert send_distribution.status_code == StatusCode.OK
        sleep(45)
        self.__enter_temp_mail_and_sign_dc(document_name)
        sleep(1)
        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'OTP' )] ")))
        OTP = self.driver.find_element(By.XPATH, "//*[contains(text(), 'OTP' )] ")
        assert OTP != 0, " no OTP requirement "

    # #bug number = WES-1049
    @pytest.mark.part3
    def test_elements_values_in_distribution_doesnt_change_when_template_is_changed_success(self):
        self.token = Shared.login_request(self)
        self.__setup()
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self, "values_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        name = names.get_full_name()
        document_name = uuid.uuid4().hex
        self.__change_values_in_file("distribute_elements_values", template, document_name, name)
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribute_elements_values")
        assert send_distribution.status_code == StatusCode.OK
        sleep(2)
        doc_id = self.__get_documentCollectionId_from_db(document_name)

        self.__get_link_by_signers_number_without_signing(1, doc_id)
        sleep(2)
        get_value_from_text_field = self.driver.find_element(By.XPATH, "//*[@type='text']")
        assert get_value_from_text_field.get_attribute('value') == "old erech", "value wasnt added to field"
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self, "changed_values_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        sleep(4)
        doc_id = self.__get_documentCollectionId_from_db(document_name)

        self.__get_link_by_signers_number_without_signing(1, doc_id)
        sleep(1)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@type='text']")))
        get_new_value_from_text_field = self.driver.find_element(By.XPATH, "//*[@type='text']")
        assert get_new_value_from_text_field.get_attribute('value') == "old erech", "value changed"

    # Bug number = WES-1041
    @pytest.mark.part1
    def test_distribution_xlsx_file_with_empty_rows_success(self):
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        data = open(self.settings["distribution_list_empty_rows"], "rb").read()
        encode_signers_to_base64 = base64.b64encode(data)
        signers_base64 = encode_signers_to_base64.decode('utf-8')
        signers = WesignMethodsApi.distribution_signers_post_xlsx_file(self, {
            "base64File": "data:application/vnd.ms-excel;base64," + signers_base64 + ""})
        signers_json = signers.json()
        assert signers.status_code == StatusCode.OK
        self._change_values_in_file("distribute_xlsx_with_empty_rows", template, signers_json['signers'])
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribute_xlsx_with_empty_rows")
        assert send_distribution.status_code == StatusCode.OK

    # # Bug number = WES-1019
    @pytest.mark.part2
    def test_distribution_add_date_field_with_value_validate_date_displayed_to_signer_success(self):
        self.token = Shared.login_request(self)
        self.__setup()
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self, "date_field_for_tempate", template)
        assert fields_for_template.status_code == StatusCode.OK
        name = names.get_full_name()
        document_name = uuid.uuid4().hex
        self.__change_values_in_file("distribution_with_date_field", template, document_name, name)
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribution_with_date_field")
        assert send_distribution.status_code == StatusCode.OK
        sleep(2)
        doc_id = self.__get_documentCollectionId_from_db(document_name)

        self.__get_link_by_signers_number_without_signing(1, doc_id)
        sleep(1)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@type='date']")))
        get_value_from_date_field = self.driver.find_element(By.XPATH, "//*[@type='date']")
        assert get_value_from_date_field.get_attribute('value') == "1989-08-23", "Check date field"

    # Bug number = WES-1050
    @pytest.mark.part3
    def test_distribution_add_date_field_and_number_with_value_validate_date_and_number_displayed_to_signer_success(
            self):
        self.token = Shared.login_request(self)
        self.__setup()
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self, "fields_for_template_date_and_number",
                                                                          template)
        assert fields_for_template.status_code == StatusCode.OK
        name = names.get_full_name()
        document_name = uuid.uuid4().hex
        self.__change_values_in_file("distribute_date_and_number_fiels", template, document_name, name)
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribute_date_and_number_fiels")
        assert send_distribution.status_code == StatusCode.OK
        sleep(1)
        doc_id = self.__get_documentCollectionId_from_db(document_name)

        self.__get_link_by_signers_number_without_signing(1, doc_id)
        sleep(1.5)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@type='date']")))
        get_value_from_date_field = self.driver.find_element(By.XPATH, "//*[@type='date']")
        get_value_from_number_field = self.driver.find_element(By.ID, "Number")
        assert get_value_from_date_field.get_attribute('value') == "1989-08-23", "Check date field"
        assert get_value_from_number_field.get_attribute('value') == "1234", "Check number field"

    # Bug number = WES-1023
    @pytest.mark.part1
    def test_distribution_validate_values_displayed_to_signer_from_xlsx_and_not_from_template_success(self):
        self.token = Shared.login_request(self)
        self.__setup()
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self, "field_for_template_number_field",
                                                                          template)
        assert fields_for_template.status_code == StatusCode.OK
        signers = WesignMethodsApi.distribution_signers_post_json_file(self,
                                                                       "signer_base64_for_distribution_with_fields_from_xlsx_and_template")
        assert signers.status_code == StatusCode.OK
        signers_json = signers.json()
        file_name = uuid.uuid4().hex
        with open(self.settings["distribute_file_with_number_field"], 'r+') as f:
            data = json.load(f)
            data["name"] = file_name  # <--- add `id` value.
            data["templateId"] = template
            data["signers"] = signers_json['signers']
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribute_file_with_number_field")
        assert send_distribution.status_code == StatusCode.OK
        sleep(1)
        doc_id = self.__get_documentCollectionId_from_db(file_name)

        self.__get_link_by_signers_number_without_signing(1, doc_id)
        sleep(2)
        get_value_from_number_field = self.driver.find_element(By.ID, "Number")
        assert get_value_from_number_field.get_attribute(
            'value') == "1234", "took value from template and not from xlsx file"

    # bug number  =  WES-1110
    # bug number  =  WES-1110
    @pytest.mark.part2
    def test_distribution_doesnt_update_value_in_fields(self):
        self.token = Shared.login_request(self)
        self.__setup()
        template = WesignMethodsApi.templates_post_json_file(self, "PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = WesignMethodsApi.templates_id_put_json_file(self, "values_for_template_bug1011", template)
        assert fields_for_template.status_code == StatusCode.OK
        name = names.get_full_name()
        document_name = uuid.uuid4().hex
        self.__change_values_in_file("distribution_bug1011", template, document_name, name)
        send_distribution = WesignMethodsApi.distribution_post_json_file(self, "distribution_bug1011")
        assert send_distribution.status_code == StatusCode.OK
        sleep(1)
        doc_id = self.__get_documentCollectionId_from_db(document_name)

        self.__get_link_by_signers_number_without_signing(1, doc_id)
        sleep(1.5)
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[@type='text']")))
        get_value_from_text_field = self.driver.find_element(By.XPATH, "//*[@type='text']")
        assert get_value_from_text_field.get_attribute('value') == "new erech", "value changed"

    def tearDown(self):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            pass
        sleep(3)

    if __name__ == "__main__":
        unittest.main()

    def __enter_mail_to_get_email_value(self, window_number):
        # self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.execute_script("window.open('');")
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[window_number])
        sleep(2)
        self.driver.get("https://mail.tm/en/")
        while True:
            email = self.driver.find_element(By.ID, 'DontUseWEBuseAPI').get_attribute('value')
            if email == "...":
                self.driver.refresh()
                sleep(10)
            else:
                self.email_address = email
                break
        # self.driver.execute_script("window.open('');")
        # sleep(1)
        # self.driver.switch_to.window(self.driver.window_handles[window_number+1])
        # self.driver.get("https://fakermail.com/")
        # try:
        #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "email-address")))
        #     get_email_address = self.driver.find_element_by_id("email-address")
        #     second_email = get_email_address.get_attribute("value")
        #     self.second_email_address = second_email
        # except:
        #     self.driver.refresh()
        #     WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "email-address")))
        #     get_email_address = self.driver.find_element_by_id("email-address")
        #     second_email = get_email_address.get_attribute("value")
        #     self.second_email_address = second_email
        # self.driver.get("https://cryptogmail.com/")
        # try:
        #     self.driver.find_element_by_class_name("button--remove").click()
        #     WebDriverWait(driver, 20).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@class='field--value js-email']")))
        #     sleep(2)
        #     get_email_address = self.driver.find_element_by_xpath("//div[@class='field--value js-email']")
        #     second_email = get_email_address.text
        #     self.second_email_address = second_email
        # except:
        #     self.driver.find_element_by_class_name("button--remove").click()
        #     sleep(2)
        #     WebDriverWait(driver, 20).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@class='field--value js-email']")))
        #     sleep(2)
        #     get_email_address = self.driver.find_element_by_xpath("//div[@class='field--value js-email']").text
        #     second_email = get_email_address.text
        #     self.second_email_address = second_email

    def __enter_name_and_email_to_xlsx_file(self, original_file, copied_file, emails):
        xfile = openpyxl.load_workbook(original_file)
        for row in range(len(emails)):
            sheet = xfile.get_sheet_by_name('Sheet1')
            sheet['A{}'.format(row + 2)] = names.get_first_name()
            sheet['B{}'.format(row + 2)] = names.get_last_name()
            sheet['C{}'.format(row + 2)] = '{}'.format(emails[row])
            sleep(3)
        xfile.save(copied_file)

    def __enter_gmail_mail(self, gmail_user_name, gmail_password):
        # self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get('https://mail.google.com/')
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "identifierId")))
        self.driver.find_element(By.XPATH, "//input[@type='email']").send_keys(gmail_user_name)
        self.driver.find_element(By.ID, "identifierNext").click()
        password = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
        password.send_keys(gmail_password)
        self.driver.find_element(By.XPATH, "//div[@id='passwordNext']").click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "qj ")))

        # try:
        #     self.driver.find_element_by_xpath("//span[contains(text(),'devtest')]").is_displayed()
        #     self.driver.find_element_by_xpath("//body/div[7]/div[3]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]").click() ##click on email checkbox
        #     sleep(self.settings['min_wait_time'])
        #     self.driver.find_element_by_xpath("(//div[@role='button'])[11]").click() ##delete button
        #     sleep(self.settings['min_wait_time'])
        # except:
        #     pass

    def __enter_mail_tm_mail_and_sign(self, window_number):
        driver = self.driver
        self.driver.switch_to.window(self.driver.window_handles[window_number])
        try:
            sleep(3)
            refresh_button = self.driver.find_element(By.XPATH, "//*[contains(text(),'Refresh')]")
            refresh_button.click()
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'devtest@comda.co.il')]")))
            click_on_email_title = WebDriverWait(driver, 80).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'devtest@comda.co.il')]")))
            click_on_email_title.click()
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iFrameResizer0")))
            self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]").click()
        except:
            sleep(3)
            refresh_button = self.driver.find_element(By.XPATH, "//*[contains(text(),'Refresh')]")
            refresh_button.click()
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'devtest@comda.co.il')]")))
            click_on_email_title = WebDriverWait(driver, 80).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'devtest@comda.co.il')]")))
            click_on_email_title.click()
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iFrameResizer0")))
            self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]").click()

    def _change_values_in_file(self, file_name, tempID, signer):
        with open(self.settings[file_name], 'r+') as f:
            data = json.load(f)
            data["name"] = uuid.uuid4().hex  # <--- add `id` value.
            data["templateId"] = tempID
            data["signers"] = signer
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
            self.document = data["name"]

    def __change_values_in_file_for_otp(self, file_name, tempID, name, full_name, contact_email):
        with open(self.settings[file_name], 'r+') as f:
            data = json.load(f)
            data["signers"][0]["signerMeans"] = contact_email
            data["name"] = name  # <--- add `id` value.
            data["templateId"] = tempID
            data["signers"][0]["fullName"] = full_name
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()  # remove remaining part

    def __change_values_in_file(self, file_name, tempID, name, full_name):
        with open(self.settings[file_name], 'r+') as f:
            data = json.load(f)
            data["name"] = name  # <--- add `id` value.
            data["templateId"] = tempID
            data["signers"][0]["fullName"] = full_name
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()  # remove remaining part

    def __assert_values_in_fields(self, text_fields_value, number_fields_value, email_fields_value, phone_number_value,
                                  date_fields_value):
        get_value_from_text_field = self.driver.find_elements(By.XPATH, "//*[@type='text']")
        for value in get_value_from_text_field:
            assert value.get_attribute('value') == text_fields_value
            break
        get_value_from_number_field = self.driver.find_elements(By.XPATH, "//*[@placeholder='123456']")
        for value in get_value_from_number_field:
            assert value.get_attribute('value') == number_fields_value, "Check number field"
            break
        get_value_from_email_field = self.driver.find_elements(By.XPATH, "//*[@type='email']")
        for value in get_value_from_email_field:
            assert value.get_attribute('value') == email_fields_value, "Check email field"
            break
        get_value_from_tel_field = self.driver.find_elements(By.XPATH, "//*[@type='tel']")
        for value in get_value_from_tel_field:
            assert value.get_attribute('value') == phone_number_value, "Check phone field"
            break
        get_value_from_date_field = self.driver.find_elements(By.XPATH, "//*[@type='date']")
        for value in get_value_from_date_field:
            assert value.get_attribute('value') == date_fields_value, "Check date field"
            break

    def __assert_number_of_fields(self, number_of_fields):
        total_fields = self.driver.find_elements(By.CLASS_NAME, "ct-input--primary")
        assert len(total_fields) == int(number_of_fields)

    def __enter_temp_faker_mail_and_sign(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'wesign')]")))
        click_on_email_title = self.driver.find_element(By.XPATH, "//*[contains(text(),'sent you the document')]")
        click_on_email_title.click()
        click_on_email_title = WebDriverWait(self.driver, 80).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Click here')]")))
        click_on_email_title.click()

    def __enter_cryptogmail_and_sign(self):
        driver = self.driver
        sleep(3)
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'sent you the document')]")))
        sleep(3)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        sleep(5)
        try:
            click_on_email_title = self.driver.find_element(By.CLASS_NAME, "message--container-bold")
            click_on_email_title.click()
        except:
            click_on_email_title = self.driver.find_element(By.CLASS_NAME, "message--container-bold")
            click_on_email_title.click()
        sleep(3)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Click here')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]").click()

    def __enter_yahoo_mail_and_sign(self, document_name):
        driver = self.driver
        self.driver.get("https://mail.yahoo.com/")
        sleep(4)
        self.driver.refresh()
        sleep(4)
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located(
                (By.XPATH, f"(//*[contains(text(),'sent you the document {document_name}')])[1]")))
        self.driver.find_element(By.XPATH,
                                 f"(//*[contains(text(),'sent you the document {document_name}')])[1]").click()
        sleep(3)
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(),'Click here')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]").click()

    def __validate_no_emails_yahoo(self, yahoo_user_name, yahoo_password):
        driver = self.driver
        sleep(1)
        self.driver.get(
            "https://login.yahoo.com/manage_account?pspid=159600001&activity=mail-direct&.lang=en-IL&.intl=il&src=ym&signin=true&done=https%3A%2F%2Fmail.yahoo.com%2Fd&eid=100")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.NAME, "username")))
        self.driver.find_element(By.NAME, "username").send_keys(yahoo_user_name)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.ID, "login-signin")))
        self.driver.find_element(By.ID, "login-signin").click()
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.NAME, "password")))
        self.driver.find_element(By.NAME, "password").send_keys(yahoo_password)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.ID, "login-signin")))
        self.driver.find_element(By.ID, "login-signin").click()
        sleep(2)
        # try:
        #     self.driver.find_element_by_xpath("//*[@data-test-id='list-result-empty']").is_displayed()
        #     pass
        # except:
        #     self.driver.find_element_by_xpath("//*[@data-test-id='checkbox']").click()
        #     sleep(self.settings['element_wait'])
        #     self.driver.find_element_by_xpath("//*[@data-test-id='toolbar-delete']").click()  ## click on delete button
        #     sleep(self.settings['element_wait'])

    def __setup(self):
        service = Service(self.settings['chrome_driver'])
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(service=service, options=options)

    def __enter_gmail_mail_and_sign(self, document_name):
        self.driver.get('https://mail.google.com/')
        sleep(3)
        self.driver.refresh()
        driver = self.driver
        sleep(3)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, f"(//span[contains(text(),'document {document_name}')])[2]")))
        # self.driver.find_element_by_xpath("(//span[contains(text(),'devtest')])[2]").click()
        sleep(3)
        self.driver.find_element(By.XPATH, f"(//span[contains(text(),'document {document_name}')])[2]").click()
        sleep(2)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Click here')]")))
        sleep(3)
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]").click()
        sleep(4)

    def __enter_comda_mail_and_sign(self, document_name):
        self.driver.get('https://email.comda.co.il/owa/')
        sleep(10)
        self.driver.refresh()
        driver = self.driver
        sleep(3)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, f"(//span[contains(text(),'{document_name}')])[1]")))
        # self.driver.find_element(By.XPATH,"(//span[contains(text(),'devtest')])[2]").click()
        sleep(3)
        self.driver.find_element(By.XPATH, f"(//span[contains(text(),'{document_name}')])[1]").click()
        sleep(2)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Click here')]")))
        sleep(3)
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]").click()

    def __change_comda_mail_box(self, user, user_pass):
        driver = self.driver
        profile_image = self.driver.find_element(By.XPATH, "//button[@autoid='_ho2_0']")
        profile_image.click()
        sleep(3)
        sign_out_button = self.driver.find_element(By.XPATH, "(//button[@autoid='_ho2_1'])[2]")
        sign_out_button.click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username")))
        user_name = self.driver.find_element(By.ID, "username")
        user_name.clear()
        user_name.send_keys(user)
        sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "password")))
        user_password = self.driver.find_element(By.ID, "password")
        user_password.send_keys(user_pass)
        sleep(2)
        signin_button = self.driver.find_element(By.XPATH, '//*[@id="lgnDiv"]/div[9]/div')
        signin_button.click()

    def __enter_comda_mail(self, user, user_pass):
        driver = self.driver
        self.driver.get("https://email.comda.co.il/")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username")))
        user_name = self.driver.find_element(By.ID, "username")
        user_name.send_keys(user)
        sleep(1)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "password")))
        user_password = self.driver.find_element(By.ID, "password")
        user_password.send_keys(user_pass)
        sleep(2)
        signin_button = self.driver.find_element(By.XPATH, '//*[@id="lgnDiv"]/div[9]/div')
        signin_button.click()

    def __get_documentCollectionId_from_db(self, document_name):
        sleep(2)
        conn = pyodbc.connect(f'Driver=SQL Server;'
                              "Server=DEVTEST\SQLEXPRESS;"
                              f'Database={self.settings["db_name"]};'
                              f'UID={self.settings["db_user"]};'
                              F'PWD={self.settings["db_password"]};'
                              'Trusted_Connection=no;')
        cursor = conn.cursor()
        b = cursor.execute(
            f" select * from DocumentCollections where Name = '{document_name}'")
        name = b.fetchone()
        return name[0]

    def __get_documentCollectionId_from_db_distribute(self, document_name):
        sleep(2)
        conn = pyodbc.connect(f'Driver=SQL Server;'
                              "Server=DEVTEST\SQLEXPRESS;"
                              f'Database={self.settings["db_name"]};'
                              f'UID={self.settings["db_user"]};'
                              F'PWD={self.settings["db_password"]};'
                              'Trusted_Connection=no;')
        cursor = conn.cursor()
        b = cursor.execute(
            f" select * from DocumentCollections where Name = '{document_name}'")
        name = b.fetchall()
        return name[0][0], name[1][0]

    def __get_link_by_signers_number_without_signing(self, signers_number: int, document_collection_id: str):
        index = 0
        for a in range(signers_number):
            conn = pyodbc.connect(f'Driver=SQL Server;'
                                  "Server=DEVTEST\SQLEXPRESS;"
                                  f'Database={self.settings["db_name"]};'
                                  f'UID={self.settings["db_user"]};'
                                  F'PWD={self.settings["db_password"]};'
                                  'Trusted_Connection=no;')
            cursor = conn.cursor()
            b = cursor.execute(
                f"SELECT * from [SignerTokensMapping] where [DocumentCollectionId] = '{document_collection_id}'")
            links = []
            result = b.fetchall()
            for x in result:
                links.append(x[3])
            sleep(4)
            self.driver.get(f"https://devtest.comda.co.il/signer/signature/{links[index]}")
            sleep(1)
            index += 1
            links.clear()

    def __enter_temp_mail(self):
        driver = self.driver
        name_length = 6
        name = ''.join(random.choices(string.ascii_letters, k=name_length))
        number = random.randint(1000, 9999)
        name_number = f"{name}{number}"

        driver.get('https://fviainboxes.com/')
        sleep(1)
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        sleep(1)

        new_username = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username"))
        )
        sleep(1)
        new_username.clear()
        sleep(1.5)
        new_username.send_keys(name_number)
        sleep(3)
        email = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[type="text"]'))
        )
        email_address = email.get_attribute("value")

        return email_address + '@fviainboxes.com'

    def __enter_temp_mail_and_sign(self, document_name):
        driver = self.driver
        for x in range(3):
            WebDriverWait(self.driver, 100).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     f"//body/div[@id='app']/div[3]/main[1]/section[1]/div[1]/div[2]/*[1]"))).click()
            sleep(1)
        sleep(2)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, f"(//*[contains(text(),'{document_name}')])[1]")))
        sleep(3)
        notification = self.driver.find_element(By.XPATH, f"(//*[contains(text(),'{document_name}')])[1]").click()
        self.driver.execute_script("arguments[0].click();", notification)
        sleep(2)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Click here')]")))
        sleep(3)
        click = self.driver.find_element(By.XPATH, "//a[contains(text(),'Click here')]")
        self.driver.execute_script("arguments[0].click();", click)

    def __enter_temp_mail_and_sign_dc(self, document_name):
        driver = self.driver
        sleep(3)
        WebDriverWait(self.driver, 100).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 f"//body/div[@id='app']/div[3]/main[1]/section[1]/div[1]/div[2]/*[1]"))).click()
        sleep(3)
        try:

            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, f"(//*[contains(text(),'{document_name}')])[1]")))
            sleep(3)
            notification = self.driver.find_element(By.XPATH, f"(//*[contains(text(),'{document_name}')])[1]")
            self.driver.execute_script("arguments[0].click();", notification)
            sleep(2)
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//td/table/tbody/tr/td/a")))
            sleep(3)
            click = self.driver.find_element(By.XPATH, "//td/table/tbody/tr/td/a")
            self.driver.execute_script("arguments[0].click();", click)
        except:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"(//tbody/tr[2]/td)[2]")))
            sleep(3)
            notification = self.driver.find_element(By.XPATH, f"(//tbody/tr[2]/td)[2]")
            self.driver.execute_script("arguments[0].click();", notification)
            sleep(2)
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//td/table/tbody/tr/td/a")))
            sleep(3)
            click = self.driver.find_element(By.XPATH, "//td/table/tbody/tr/td/a")
            self.driver.execute_script("arguments[0].click();", click)
