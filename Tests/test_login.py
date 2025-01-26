import unittest
import warnings
from pathlib import Path
from telnetlib import EC
from time import sleep
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from Enums.status_codes import StatusCode, ResultCode
import pytest
from Common.all_api_methods import WesignMethodsApi
from shared import Shared


@pytest.mark.flaky(max_runs=6)
class WesignApiLoginTests(unittest.TestCase):
    def setUp(self):
        # p = Path(__file__).with_name('settings.json')
        # with open(p) as f:
        #     self.settings = json.load(f)

        p = Path(__file__).resolve().parent.parent
        file_path = p / "Settings\\settings.json"
        with open(file_path) as f:
            self.settings = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)

    @pytest.mark.part1
    def test_login_success(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestSuccess')
        assert r.status_code == StatusCode.OK
        login = json.loads(r.content)
        return login['token']

    @pytest.mark.part2
    def test_login_username_success(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginUserNameRequestSuccess')
        assert r.status_code == StatusCode.OK
        login = json.loads(r.content)
        return login['token']

    @pytest.mark.part3
    def test_login_invalid_password(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestInvalidPassword')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        assert json_response[0] == ResultCode.INVALID_CREDENTIAL

    @pytest.mark.part1
    def test_login_invalid_email(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestInvalidEmail')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['error']
        status_response = r.status_code
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.INVALID_CREDENTIAL

    @pytest.mark.part2
    def test_login_empty_email(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestEmptyEmail')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        status_response = r.json()['status']
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_AN_EMAIL
        assert json_response[1] == ResultCode.MINIMUN_LENGTH_OF_EMAIL_OR_USERNAME

    @pytest.mark.part3
    def test_login_empty_email_empty_password(self):
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestEmptyEmailEmptyPassword')
        assert r.status_code == StatusCode.BAD_REQUEST
        response = r.json()
        json_response = response['errors']['Email']
        status_response = r.json()['status']
        assert status_response == StatusCode.BAD_REQUEST
        assert json_response[0] == ResultCode.PLEASE_SPECIFY_AN_EMAIL
        assert json_response[1] == ResultCode.MINIMUN_LENGTH_OF_EMAIL_OR_USERNAME

    ##WES-1505
    @pytest.mark.part1
    def test_login_using_otp(self):
        self.__setup()
        r = WesignMethodsApi.users_login_post_json_file(self, 'LoginRequestSuccessUsingOtp')
        assert r.status_code == StatusCode.OK
        login = r.json()
        assert login['token'] == ''
        assert len(login['refreshToken']) > 30
        assert login['authToken'] == 'OTP'
        sleep(60)
        self.__enter_comda_mail(self.settings['DevtestMailUsingOtp'], self.settings['company_user_password'])
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "(//*[contains(text(),'Your validation code is')])[1]")))
        self.driver.find_element(By.XPATH, "(//*[contains(text(),'Your validation code is')])[1]").click()
        sleep(10)
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//*[@style='direction:LTR']")))
        otp_number = self.driver.find_element(By.XPATH, "//*[@style='direction:LTR']").text
        sleep(1.5)
        delete_mail = self.driver.find_element(By.XPATH,
                                               "//div[5]/div/div[1]/div/div[5]/div[1]/div/div[1]/div/div/div[3]/div/button/span[2]")
        delete_mail.click()
        sleep(3)
        otp = otp_number[24:30]
        payload = {
                  "otpToken": login['refreshToken'],
                  "code": otp
                }
        login_using_otp = WesignMethodsApi.users_validate_otp_flow(self, payload)
        sleep(5)
        response = login_using_otp.json()
        sleep(5)
        assert len(response['token']) != '' and not None
        assert response['refreshToken'] != ''
        assert response['authToken'] != ''


    def tearDown(self):
        sleep(3)

    if __name__ == "__main__":
        unittest.main()

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
