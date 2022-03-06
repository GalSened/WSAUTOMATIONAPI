import pyodbc
import unittest
import warnings
from pathlib import Path
from time import sleep
import pytest
import requests
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from shared import Shared
from status_codes import StatusCode, ResultCode
from selenium import webdriver
from test_self_sign import WesignApiSelfSignTestTests as sl
from test_create_document_collection import WesignApiCreateDocumentCollectionTests as cd


@pytest.mark.flaky(max_runs=2)
class WesignJobs(unittest.TestCase):
    def setUp(self):
        p = Path(__file__).with_name('SelfSignSettings.json')
        with open(p) as f:
            self.settings = json.load(f)
        a = Path(__file__).with_name('settings.json')
        with open(a) as f:
            self.settings_jobs = json.load(f)
        warnings.simplefilter('ignore', ResourceWarning)
        warnings.simplefilter('ignore', DeprecationWarning)
        self.token = Shared.login_request(self)

    def test_clean_db_job_after_delete_documents(self):
        #Create 20 documents
        for x in range(100):
            sleep(2)
            sl.self_sign_create_document(self,'SelfSignUploadPdfDocument')
        #Delete documents
        cd.delete_all_documents(self)
        sleep(20)
        #Enter jobs ui and click on clean db
        self.driver = webdriver.Chrome(self.settings_jobs["chrome_driver"])
        self.driver.get(self.settings_jobs['jobs_url'])
        sleep(10)
        #click on clean db job check box
        self.driver.find_element_by_name("jobs[]").click()
        #click on trigger button
        self.driver.find_element(By.CLASS_NAME, 'btn-primary').click()
        #Enter DB to check if documents deleted
        sleep(60)
        conn = pyodbc.connect(f'Driver=SQL Server;'
                                "Server=DEVTEST\SQLEXPRESS;"
                                f'Database={self.settings_jobs["db_name"]};'
                                f'UID={self.settings_jobs["db_user"]};'
                                F'PWD={self.settings_jobs["db_password"]};'
                                'Trusted_Connection=no;')
        cursor = conn.cursor()
        cursor.execute(f"SELECT count(Id) as a FROM DocumentCollections WHERE Status = '{self.settings_jobs['deleted_status']}'")
        row = cursor.fetchone()
        document_number = str(row)
        assert document_number == '(0, )', "There is "+document_number+" document that not deleted"


    def tearDown(self):
        sleep(5)

    if __name__ == "__main__":
        unittest.main()