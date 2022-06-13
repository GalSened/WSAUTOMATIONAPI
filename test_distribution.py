import unittest
import uuid
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
import names
import openpyxl
import base64

from webdriver_manager.chrome import ChromeDriverManager

from shared import Shared
from status_codes import StatusCode, ResultCode
from telnetlib import EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.flaky(max_runs=10)
class WesignApiCreateDocumentDistributionTests(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('DistributeCollection.json')
        with open(p) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_api_sending_distribution_and_receiving_confirmation_for_document_viewed_and_signed_success(self):
        self.token = Shared.login_request_gmail(self)
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        self.driver = webdriver.Chrome(executable_path=service, options=options)
        self.__enter_gmail_mail(self.settings['first_recipient_name'], self.settings['gmail_login_password'])
        sleep(2)
        self.__enter_mail_to_get_email_value(1)
        emails = [self.email_address, self.second_email_address]
        self.__enter_name_and_email_to_xlsx_file(self.settings["empty_xlsx_file"], self.settings["empty_file_with_no_fields_Copy"], emails)
        data = open(self.settings["empty_file_with_no_fields_Copy"], "rb").read()
        encode_signers_to_base64 = base64.b64encode(data)
        signers_base64 = encode_signers_to_base64.decode('utf-8')
        signers = self.__api_extract_signers_from_base64({"base64File": "data:application/vnd.ms-excel;base64," + signers_base64 +"" })
        signers_json = signers.json()
        assert signers.status_code == StatusCode.OK
        template = self.__api_create_template_request("PDF_file_base64")
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
        send_distribution = self.__api_create_distribution_request("DistributeSignersApi_Copy")
        assert send_distribution.status_code == StatusCode.OK
        self.__enter_mail_tm_mail_and_sign(1)
        sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[3])
        sleep(1)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "logo_image")))
        sleep(2)
        self.driver.find_element_by_xpath("//button[@class='ct-button--titlebar-primary ng-star-inserted']").click()
        sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "ct-button--primary")))
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[2])
        sleep(2)
        self.__enter_temp_faker_mail_and_sign()
        sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "logo_image")))
        sleep(2)
        self.driver.find_element_by_xpath("//button[@class='ct-button--titlebar-primary ng-star-inserted']").click()
        sleep(2)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "ct-button--primary")))
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(2)
        self.driver.refresh()
        sleep(8)
        WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '{} has been completed by all participants')]".format(self.document_name))))
        assert self.driver.find_element(By.XPATH, "//*[contains(text(), '({}) has viewed {}')]".format(self.email_address, self.document_name)), "confirmation email that signer viewed the document wasn't received"
        assert self.driver.find_element(By.XPATH, "//*[contains(text(), '({}) has signed {}')]".format(self.email_address, self.document_name)), "confirmation email that signer signed the document wasn't received"
        assert self.driver.find_element(By.XPATH, "//*[contains(text(), '({}) has viewed {}')]".format(self.second_email_address, self.document_name)), "confirmation email that signer viewed the document wasn't received"
        assert self.driver.find_element(By.XPATH, "//*[contains(text(), '({}) has signed {}')]".format(self.second_email_address, self.document_name)), "confirmation email that signer signed the document wasn't received"

    #Bug number = WES-1021
    def test_api_sending_distribution_document_with_duplicated_signer_email_success(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = self.__api_extract_signers_from_base64_file("duplicated_signer_email_base64")
        signers_json = signers.json()
        self._change_values_in_file("duplicated_template_and_signer", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("duplicated_template_and_signer")
        assert send_distribution.status_code == StatusCode.OK

    def test_api_sending_distribution_with_valid_email_all_fields_filled_from_xlsx_success(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request("fields_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        signers = self.__api_extract_signers_from_base64_file("signers_for_template_with_fields")
        signers_json = signers.json()
        self._change_values_in_file("distribute_file_with_users_and_field", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("distribute_file_with_users_and_field")
        assert send_distribution.status_code == StatusCode.OK

    def test_sending_distribution_email_with_valid_email_value_and_all_fields_in_template_and_no_fields_in_xlsx_success(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        self.__api_create_template_field_request("fields_for_template_not_in_xlsx_file", template)
        signers = self.__api_extract_signers_from_base64_file("signers_base64_for_templates_with_fields_no_fields_in_xlsx_file")
        signers_json = signers.json()
        self._change_values_in_file("fields_only_in_template", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("fields_only_in_template")
        assert send_distribution.status_code == StatusCode.OK

    def test_api_sending_distribution_large_file_success(self):
        template = self.__api_create_template_request("large_PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = self.__api_extract_signers_from_base64_file("signers_no_field")
        signers_json = signers.json()
        self._change_values_in_file("distribute_10mega_file", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("distribute_10mega_file")
        assert send_distribution.status_code == StatusCode.OK

    def test_api_distribution_two_signers_no_fields_success(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = self.__api_extract_signers_from_base64_file("seven_signers_no_fields - Copy")
        signers_json = signers.json()
        self._change_values_in_file("DistributeSignersApi_no_fields", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("DistributeSignersApi_no_fields")
        assert send_distribution.status_code == StatusCode.OK

    def test_sending_distribution_with_invalid_data_from_xlsx_file(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        self.__api_create_template_field_request("template_with_invalid_fields", template)
        signers = self.__api_extract_signers_from_base64_file("signers_for_template_with_invalid_values")
        signers_json = signers.json()
        self._change_values_in_file("distribute_file_for_template_with_invalid_values", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("distribute_file_for_template_with_invalid_values")
        assert send_distribution.status_code == StatusCode.BAD_REQUEST

    #Bug number = WES-1046/WES-1042
    def test_api_sending_distribution_with_xlsx_file_with_fields_but_no_fields_in_template(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = self.__api_extract_signers_from_base64_file("signers_for_template_with_fields")
        signers_json = signers.json()
        self._change_values_in_file("distribute_file_with_users_and_fields_in_xlsx", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("distribute_file_with_users_and_fields_in_xlsx")
        assert send_distribution.status_code == StatusCode.BAD_REQUEST

    def test_api_distribution_seven_recipients_success(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        signers = self.__api_extract_signers_from_base64_file("seven_signers_no_fields")
        signers_json = signers.json()
        self._change_values_in_file("distribute_seven_signers_api", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("distribute_seven_signers_api")
        assert send_distribution.status_code == StatusCode.OK

    def test_send_distribute_invalid_email(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        signers = self.__api_extract_signers_from_base64_file("invalid_signer_email")
        assert signers.status_code == StatusCode.BAD_REQUEST

    def test_send_distribute_empty_first_name_and_empty_last_name(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        signers = self.__api_extract_signers_from_base64_file("signer_data_without_name")
        assert signers.status_code == StatusCode.BAD_REQUEST

    def test_send_distribute_empty_signer_means(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        signers = self.__api_extract_signers_from_base64_file("signer_data_without_means")
        assert signers.status_code == StatusCode.BAD_REQUEST

    #Bug number = WES-1106
    def test_send_distribute_duplicated_fields_in_xlsx_with_same_name_validate_values_success(self):
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        self.driver = webdriver.Chrome(executable_path=service, options=options)
        self.__enter_mail_to_get_email_value(0)
        emails = [self.email_address, self.second_email_address]
        self.__enter_name_and_email_to_xlsx_file(self.settings["sending_distribution_duplicated_fields_with_same_name_and_value_in_xlsx_edit"], self.settings["sending_distribution_duplicated_fields_with_same_name_and_value_in_xlsx_edit - Copy"], emails)
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request("Distribute_duplicated_fields_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        data = open(self.settings["sending_distribution_duplicated_fields_with_same_name_and_value_in_xlsx_edit - Copy"], "rb").read()
        encode_signers_to_base64 = base64.b64encode(data)
        signers_base64 = encode_signers_to_base64.decode('utf-8')
        signers = self.__api_extract_signers_from_base64({"base64File": "data:application/vnd.ms-excel;base64," + signers_base64 +"" })
        signers_json = signers.json()
        assert signers.status_code == StatusCode.OK
        print(signers_json['signers'])
        self.document_name = uuid.uuid4().hex
        self._change_values_in_file("DistributeSigners_duplicated_fields_in_xlsx_with_same_name" , template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("DistributeSigners_duplicated_fields_in_xlsx_with_same_name")
        assert send_distribution.status_code == StatusCode.OK
        self.__enter_mail_tm_mail_and_sign(0)
        self.driver.switch_to.window(self.driver.window_handles[3])
        WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ct-input--primary")))
        self.__assert_number_of_fields(10)
        self.__assert_values_in_fields("Test", "5678", "test@comsign.co.il", "504821887", "1989-08-23")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.__enter_temp_faker_mail_and_sign()
        sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[1])
        WebDriverWait(self.driver, 80).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ct-input--primary")))
        self.__assert_number_of_fields(10)
        self.__assert_values_in_fields("Test1", "9012", "test1@comsign.co.il", "504821885", "1990-12-17")

    def test_distribution_OTP_xlsx_file_success(self):
        self.token = Shared.login_request_gmail(self)
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        self.driver = webdriver.Chrome(executable_path=service, options=options)
        self.__enter_gmail_mail(self.settings['first_recipient_name'], self.settings['gmail_login_password'])
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        document_name = uuid.uuid4().hex
        full_name = names.get_full_name()
        self.__change_values_in_file("Distribution_OTP", template, document_name, full_name)
        send_distribution = self.__api_create_distribution_request("Distribution_OTP")
        assert send_distribution.status_code == StatusCode.OK
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "(//*[contains(text(),'sent you the document {}')])[2]".format(document_name))))
        self.driver.find_element(By.XPATH, "(//*[contains(text(),'sent you the document {}')])[2]".format(document_name)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        OTP = self.driver.find_element(By.XPATH, "//*[contains(text(), 'OTP' )] ")
        assert OTP != 0, " no OTP requirement "

    # #bug number = WES-1049
    def test_elements_values_in_distribution_doesnt_change_when_template_is_changed_success(self):
        self.token = Shared.login_request_gmail(self)
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        self.driver = webdriver.Chrome(executable_path=service, options=options)
        self.__enter_gmail_mail(self.settings['first_recipient_name'], self.settings['gmail_login_password'])
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request("values_for_template",template)
        assert fields_for_template.status_code == StatusCode.OK
        name = names.get_full_name()
        document_name = uuid.uuid4().hex
        self.__change_values_in_file("distribute_elements_values", template, document_name, name)
        send_distribution = self.__api_create_distribution_request("distribute_elements_values")
        assert send_distribution.status_code == StatusCode.OK
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,"(//*[contains(text(),'sent you the document {}')])[2]".format(document_name))))
        sleep(1)
        self.driver.find_element(By.XPATH, "(//*[contains(text(),'wesign test sent you the document {}')])[2]".format(document_name)).click()
        sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        get_value_from_text_field = self.driver.find_element_by_xpath("//*[@type='text']")
        assert get_value_from_text_field.get_attribute('value') == "old erech" , "value wasnt added to field"
        fields_for_template = self.__api_create_template_field_request("changed_values_for_template", template)
        assert fields_for_template.status_code == StatusCode.OK
        self.driver.switch_to.window(self.driver.window_handles[0])
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[2])
        sleep(2)
        get_new_value_from_text_field = self.driver.find_element_by_xpath("//*[@type='text']")
        assert get_new_value_from_text_field.get_attribute('value') == "old erech" , "value changed"


    #Bug number = WES-1041
    def test_distribution_xlsx_file_with_empty_rows_success(self):
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        data = open(self.settings["distribution_list_empty_rows"], "rb").read()
        encode_signers_to_base64 = base64.b64encode(data)
        signers_base64 = encode_signers_to_base64.decode('utf-8')
        signers = self.__api_extract_signers_from_base64({"base64File": "data:application/vnd.ms-excel;base64," + signers_base64 +"" })
        signers_json = signers.json()
        assert signers.status_code == StatusCode.OK
        self._change_values_in_file("distribute_xlsx_with_empty_rows", template, signers_json['signers'])
        send_distribution = self.__api_create_distribution_request("distribute_xlsx_with_empty_rows")
        assert send_distribution.status_code == StatusCode.OK


    # # Bug number = WES-1019
    def test_distribution_add_date_field_with_value_validate_date_displayed_to_signer_success(self):
        self.token = Shared.login_request_gmail(self)
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        self.driver = webdriver.Chrome(executable_path=service, options=options)
        self.__enter_gmail_mail(self.settings['first_recipient_name'], self.settings['gmail_login_password'])
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request("date_field_for_tempate", template)
        assert fields_for_template.status_code == StatusCode.OK
        name = names.get_full_name()
        document_name = uuid.uuid4().hex
        self.__change_values_in_file("distribution_with_date_field", template, document_name, name)
        send_distribution = self.__api_create_distribution_request("distribution_with_date_field")
        assert send_distribution.status_code == StatusCode.OK
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH, "(//*[contains(text(),'sent you the document {}')])[2]".format(document_name))))
        sleep(1)
        self.driver.find_element(By.XPATH, "(//*[contains(text(),'wesign test sent you the document {}')])[2]".format(document_name)).click()
        sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        get_value_from_date_field = self.driver.find_element_by_xpath("//*[@type='date']")
        assert get_value_from_date_field.get_attribute('value') == "1989-08-23", "Check date field"

    # Bug number = WES-1050
    def test_distribution_add_date_field_and_number_with_value_validate_date_and_number_displayed_to_signer_success(self):
        self.token = Shared.login_request_gmail(self)
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        self.driver = webdriver.Chrome(executable_path=service, options=options)
        self.__enter_gmail_mail(self.settings['first_recipient_name'], self.settings['gmail_login_password'])
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request("fields_for_template_date_and_number", template)
        assert fields_for_template.status_code == StatusCode.OK
        name = names.get_full_name()
        document_name = uuid.uuid4().hex
        self.__change_values_in_file("distribute_date_and_number_fiels", template, document_name, name)
        send_distribution = self.__api_create_distribution_request("distribute_date_and_number_fiels")
        assert send_distribution.status_code == StatusCode.OK
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, "(//*[contains(text(),'sent you the document {}')])[2]".format(document_name))))
        sleep(1)
        self.driver.find_element(By.XPATH, "(//*[contains(text(),'wesign test sent you the document {}')])[2]".format(
            document_name)).click()
        sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        get_value_from_date_field = self.driver.find_element_by_xpath("//*[@type='date']")
        get_value_from_number_field = self.driver.find_element(By.ID, "Number")
        assert get_value_from_date_field.get_attribute('value') == "1989-08-23", "Check date field"
        assert get_value_from_number_field.get_attribute('value') == "1234", "Check number field"

    # Bug number = WES-1023
    def test_distribution_validate_values_displayed_to_signer_from_xlsx_and_not_from_template_success(self):
        self.token = Shared.login_request_gmail(self)
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        self.driver = webdriver.Chrome(executable_path=service, options=options)
        self.__enter_gmail_mail(self.settings['first_recipient_name'], self.settings['gmail_login_password'])
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request("field_for_template_number_field", template)
        assert fields_for_template.status_code == StatusCode.OK
        signers = self.__api_extract_signers_from_base64_file("signer_base64_for_distribution_with_fields_from_xlsx_and_template")
        assert signers.status_code == StatusCode.OK
        signers_json = signers.json()
        file_name = uuid.uuid4().hex
        with open(self.settings["distribute_file_with_number_field"], 'r+') as f:
            data = json.load(f)
            data["name"] = file_name # <--- add `id` value.
            data["templateId"] = template
            data["signers"] = signers_json['signers']
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
            f.truncate()  # remove remaining part
        send_distribution = self.__api_create_distribution_request("distribute_file_with_number_field")
        assert send_distribution.status_code == StatusCode.OK
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located(
            (By.XPATH, "(//*[contains(text(),'sent you the document {}')])[2]".format(file_name))))
        sleep(1)
        self.driver.find_element(By.XPATH, "(//*[contains(text(),'wesign test sent you the document {}')])[2]".format(
            file_name)).click()
        sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        get_value_from_number_field = self.driver.find_element(By.ID, "Number")
        assert get_value_from_number_field.get_attribute('value') == "1234", "took value from template and not from xlsx file"

    # bug number  =  WES-1110
    def test_distribution_doesnt_update_value_in_fields(self):
        self.token = Shared.login_request_gmail(self)
        service = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extenstions")
        options.add_argument("disable-infobars")
        options.add_argument("force-device-scale-factor=0.75")
        options.add_argument("high-dpi-support=0.75")
        self.driver = webdriver.Chrome(executable_path=service, options=options)
        self.__enter_gmail_mail(self.settings['first_recipient_name'], self.settings['gmail_login_password'])
        template = self.__api_create_template_request("PDF_file_base64")
        assert template.status_code == StatusCode.OK
        template_json = template.json()
        template = template_json['templateId']
        fields_for_template = self.__api_create_template_field_request("values_for_template_bug1011",template)
        assert fields_for_template.status_code == StatusCode.OK
        name = names.get_full_name()
        document_name = uuid.uuid4().hex
        self.__change_values_in_file("distribution_bug1011", template, document_name, name)
        send_distribution = self.__api_create_distribution_request("distribution_bug1011")
        assert send_distribution.status_code == StatusCode.OK
        WebDriverWait(self.driver, 80).until(EC.presence_of_element_located((By.XPATH,"(//*[contains(text(),'sent you the document {}')])[2]".format(document_name))))
        sleep(1)
        self.driver.find_element(By.XPATH, "(//*[contains(text(),'wesign test sent you the document {}')])[2]".format(document_name)).click()
        sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        self.driver.find_element(By.XPATH, "//a[contains(text(),'SIGN NOW')]").click()
        sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(2)
        get_value_from_text_field = self.driver.find_element_by_xpath("//*[@type='text']")
        assert get_value_from_text_field.get_attribute('value') == "new erech" , "value changed"

    def tearDown(self):
        try:
            sleep(3)
            self.driver.close()
            self.driver.quit()
        except:
            pass

    if __name__ == "__main__":
        unittest.main()

    def __api_extract_signers_from_base64_file(self, signers_file):
        file = open(self.settings[signers_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documents/distribution/signers', data=json.dumps(requests_json), headers=headers)
        return r

    def __api_extract_signers_from_base64(self, signers_base64):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documents/distribution/signers', data=json.dumps(signers_base64), headers=headers)
        return r

    def __api_create_template_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/templates', data=json.dumps(requests_json), headers=headers)
        return r

    def __delete_template_created(self, template_guid):
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.delete(self.settings['Base_Url'] + '/templates/' + template_guid, headers=headers)
        assert r.status_code == 200

    def __api_create_template_field_request(self, field_file, templateId):
        file = open(self.settings[field_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.put(self.settings["Base_Url"] + f'/templates/{templateId}', data=json.dumps(requests_json) ,headers=headers)
        return r

    def __api_create_distribution_request(self, request_file):
        file = open(self.settings[request_file], 'r')
        json_input = file.read()
        requests_json = json.loads(json_input)
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + self.token}
        r = requests.post(self.settings['Base_Url'] + '/documents/distribution', data=json.dumps(requests_json), headers=headers)
        return r

    def __enter_mail_to_get_email_value(self, window_number):
        # self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[window_number])
        self.driver.get("https://mail.tm/en/")
        while True:
            email = self.driver.find_element(By.ID, 'address').get_attribute('value')
            if email == "...":
                self.driver.refresh()
                sleep(10)
            else:
                self.email_address = email
                break
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[window_number+1])
        self.driver.get("https://fakermail.com/")
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "email-address")))
            get_email_address = self.driver.find_element_by_id("email-address")
            second_email = get_email_address.get_attribute("value")
            self.second_email_address = second_email
        except:
            self.driver.refresh()
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "email-address")))
            get_email_address = self.driver.find_element_by_id("email-address")
            second_email = get_email_address.get_attribute("value")
            self.second_email_address = second_email

    def __enter_name_and_email_to_xlsx_file(self, original_file, copied_file, emails):
        xfile = openpyxl.load_workbook(original_file)
        for row in range(len(emails)):
            sheet = xfile.get_sheet_by_name('Sheet1')
            sheet['A{}'.format(row+2)] = names.get_first_name()
            sheet['B{}'.format(row+2)] = names.get_last_name()
            sheet['C{}'.format(row+2)] = '{}'.format(emails[row])
            sleep(3)
        xfile.save(copied_file)

    def __enter_gmail_mail(self, gmail_user_name, gmail_password):
        # self.driver = webdriver.Chrome(self.settings["chrome_driver"])
        self.driver.get('https://mail.google.com/')
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "identifierId")))
        self.driver.find_element_by_xpath("//input[@type='email']").send_keys(gmail_user_name)
        self.driver.find_element_by_id("identifierNext").click()
        password = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
        password.send_keys(gmail_password)
        self.driver.find_element_by_xpath("//div[@id='passwordNext']").click()
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
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'devtest@comda.co.il')]")))
        refresh_button = self.driver.find_element_by_xpath("//*[contains(text(),'Refresh')]")
        refresh_button.click()
        click_on_email_title = WebDriverWait(driver, 80).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'devtest@comda.co.il')]")))
        click_on_email_title.click()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iFrameResizer0")))
        self.driver.find_element_by_xpath("//a[contains(text(),'SIGN NOW')]").click()


    def _change_values_in_file(self, file_name, tempID,signer):
        with open(self.settings[file_name], 'r+') as f:
            data = json.load(f)
            data["name"] = uuid.uuid4().hex  # <--- add `id` value.
            data["templateId"] = tempID
            data["signers"] = signer
            f.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, f, indent=3)
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

    def __assert_values_in_fields(self, text_fields_value, number_fields_value, email_fields_value, phone_number_value, date_fields_value):
        get_value_from_text_field = self.driver.find_elements_by_xpath("//*[@type='text']")
        for value in get_value_from_text_field:
            assert value.get_attribute('value') == text_fields_value
            break
        get_value_from_number_field = self.driver.find_elements_by_xpath("//*[@placeholder='123456']")
        for value in get_value_from_number_field:
            assert value.get_attribute('value') == number_fields_value, "Check number field"
            break
        get_value_from_email_field = self.driver.find_elements_by_xpath("//*[@type='email']")
        for value in get_value_from_email_field:
            assert value.get_attribute('value') == email_fields_value, "Check email field"
            break
        get_value_from_tel_field = self.driver.find_elements_by_xpath("//*[@type='tel']")
        for value in get_value_from_tel_field:
            assert value.get_attribute('value') == phone_number_value, "Check phone field"
            break
        get_value_from_date_field = self.driver.find_elements_by_xpath("//*[@type='date']")
        for value in get_value_from_date_field:
            assert value.get_attribute('value') == date_fields_value, "Check date field"
            break


    def __assert_number_of_fields(self, number_of_fields):
        total_fields = self.driver.find_elements_by_class_name("ct-input--primary")
        assert len(total_fields) == int(number_of_fields)

    def __enter_temp_faker_mail_and_sign(self):
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'wesign')]")))
        click_on_email_title = self.driver.find_element_by_xpath("//*[contains(text(),'sent you the document')]")
        click_on_email_title.click()
        click_on_email_title = WebDriverWait(self.driver, 80).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'SIGN NOW')]")))
        click_on_email_title.click()
