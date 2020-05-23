import json
import string
import time
import jwt
from qa_automation_core.api import Service
from qa_automation_core.api.api_headers import get_default_headers
from selenium.webdriver import ActionChains

from qa_automation_drt_haw.ui.model.endpoints_flatstore import endpoints
from selenium.webdriver.common.keys import Keys
from qa_automation_drt_haw.ui.model.mtb_create_case_page import Mtb_Create_Case_page as MTBC
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import *
from qa_automation_drt_haw.ui.ui_utils.Logs import log


class Finder:
    xpath_search_field = '//input[@data-qa-key="patient-finder-ui_search"]'
    # xpath_search_field = "//form[contains(@class, 'search-bar')]//input"
    # xpath_search_fields = "//div[@class='modal-content']//div[@class='search-bar-container']//input"

    xpath_search_results = "//div[@class = 'modal-content']//tbody//tr"
    xpath_search_noresult = "//div[@class = 'no-results-msg-desc']"
    # xpath_textfield_val = '//input[@id="createCase_physician"]'
    xpath_textfield_val = "//input[@id='%s']"
    xpath_textarea_val = "//textarea[@id='%s']"
    xpath_mrn_no = "//*[@id=\"id-1-1\"]/div[1]/div/div/div/div/div/table/tbody/tr[1]/td[4]"
    xpath_textfield_locator = "//textarea[contains(@id,'%s')]|//input[contains(@id,'%s')]|//textarea[@data-qa-key='%s']"
    cases_table = "//tbody/tr"
    current_page_number = "//li[contains(@class,'ant-pagination-item-active')]"
    next_page_btn = "//i[contains(@class,'anticon-right')]"

    def __init__(self, app):
        self.app = app

    def header_search(self, what):
        search_field = find_elements(self.app.driver, self.xpath_search_field)
        if not search_field:
            log.info('Search field has not been found')
            assert False, 'Search field has not been found'
        else:
            log.info('Search field has been found')
            search_field[0].clear()
            search_field[0].send_keys(what)
            search_field[0].send_keys(Keys.RETURN)
            log.info('Searching for patient')
            time.sleep(4)

    # purpose - to enter the value in the text field
    # idVal is the locator of text field which needs to be tested and it is declared in page class files
    # what is the data which user wants to enter which is passed from test file
    def text_field_enter(self, what, idVal):
        text_val = find_elements(self.app.driver, self.xpath_textfield_locator % ( idVal, idVal, idVal))
        if not text_val:
            log.error('Search field has not been found')
            assert False, 'Search field has not been found'
        else:
            text_val[0].clear()
            text_val[0].send_keys(what)

    def finder_pick_value(self, value):
        '''
        :purpose: click on the 1st patient from the table
        :param value: value stores patient's name or mrn which is passed from "find_and_pick_patient" function
        :return:  it will navigate to [create case] page
        '''
        # table_search = find_elements(self.app.driver, "//tbody[@class='ant-table-tbody']//tr")
        table_search = get_element_list_after_wait(self.app.driver, "//tbody[@class='ant-table-tbody']//tr",timeout=60,pollFrequency=1)
        if table_search:
            log.info('patient record has been found')
            table_search[0].click()
            log.info('clicked on patient record')
            self.app.mtb_case_management_page.verify_mtb_case_management_text_present_on_page()
        else:
            log.error('Records for "%s" has not been found', format(value))
            assert False, ('Records for "%s" has not been found' % value)

    def find_only_patient_name(self, value):
        search_field = find_elements(self.app.driver, self.xpath_search_field)
        if not search_field:
            log.error('Search field has not been found')
            assert False, 'Search field has not been found'
        else:
            search_field[0].clear()
            time.sleep(0.5)
            search_field[0].send_keys(value)
            time.sleep(0.5)
            search_field[0].send_keys(Keys.RETURN)
            # time.sleep(2)

    def pick_only_patient_name(self, value):
        # self.find_only_patient_name(value)
        self.finder_pick_value(value)

    def pick_only_patient(self, param='Johnson'):
        self.pick_only_patient_name(param)

    def find_and_pick_patient(self, value):
        '''
            :purpose: search given patient and select that record
            :param value: It store patient's name or mrn
            '''
        log.info('Find and pick patient with the name which is picked up from previous step')
        self.header_search(value)
        self.finder_pick_value(value)

    def search(self, search_string):
        search_field = find_elements(self.app.driver, "//input[@type = 'text']")
        assert search_field, 'Search field has not been found'
        log.info('Search field has been found')
        search_field[0].send_keys(search_string)
        time.sleep(2)
        search_field[0].send_keys(Keys.RETURN)
        log.info('Searching for {' + search_string + '}')
        time.sleep(2)

    def text_search(self, what):
        search_field = find_elements(self.app.driver, self.xpath_search_noresult)
        if not search_field:
            log.error(' text {' + what + '} has not been found')
            assert False, 'text has not been found'
        else:
            log.info(' text {' + what + '} has been found')

    # purpose - to enter the value in the text field and verify text entered correctly
    # idVal is the locator of text field which needs to be tested and it is declared in page class files
    # what is the data which user wants to enter which is passed from test file
    def text_area_enter(self, what, idVal,i=0):
        text_val = find_elements(self.app.driver, self.xpath_textfield_locator % (idVal, idVal, idVal))
        if not text_val:
            log.error('text field has not been found')
            assert False, 'text field has not been found'
        else:
            text_val[i].clear()
            text_val[i].send_keys(what)

    def find_last_4_digits_from_MRN(self):
        '''
        :purpose: pick up the last 4 digit of mrn number
        :return: mrn_last_4_digit
        '''
        log.info("Pick up last 4 Digits from the MRN")
        mrn = find_element(self.app.driver, self.xpath_mrn_no)
        mrn_no = mrn.text
        if mrn_no.isalnum():
            mrn_last_4_digit = str(mrn_no[-4:])
            log.info("Last 4 Digits from MRN is picked up")
            return mrn_last_4_digit

    def search_patient_info(self):
        '''
        purpose:- Search the patient using endpoints by passing different strings
        :return: this function returns 'patient_json_res' that contains 1 patient info in json format
        '''
        from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceInfo, Token
        from qa_automation_drt_haw.settings import Config

        username = Config.portal_2_roles_username
        psw = Config.portal_2_roles_password
        flatstore_patient_info = ServiceInfo('flatstore-patient')
        valid_jwt = Token(username, psw)

        flatstore_patient_service_valid_token = Service(flatstore_patient_info.url, token=str(valid_jwt), sslcert=False)
        flatstore_patients = endpoints.FLATSTORE_PATIENTS
        patient_json_res = ''

        log.info("find and pick up patient info using api")
        for k in list(string.ascii_lowercase):
            for j in list(string.ascii_lowercase):
                i = k + j
                print(i)
                endpoint_temp = flatstore_patients + '?searchString=%s' % i

                res = flatstore_patient_service_valid_token.get(endpoint_temp, get_default_headers())
                assert 200 == res.status_code, "Patient %s has not been found" % i
                json_res = res.json_payload

                if json_res['pageInfo']['total'] > 0:
                    log.info('Patient with string "%s" has been found' % i)
                    patient_json_res = json_res
                    log.info("patient info is picked up and stored")
                    break
            else:
                log.error("Patient %s has not been found , please try another string" % i)
                continue
            break

        return patient_json_res

    def pick_patient_first_and_last_name(self, patient_info):
        '''
        :param patient_info: 'patient_info' contains 1 patient info in json format which will be passed from test file
        :return: this function returns 'patient' which contains patient's first and last name
        '''
        log.info("pick up patient's full name from the received patient info")
        patient = patient_info['matchingPatients'][0]['humanNameFirst'] + " " + \
                  patient_info['matchingPatients'][0][
                      'humanNameLast']
        log.info("patient's full name is picked up and stored")
        return patient

    def pick_patient_mrn(self):
        '''
        :param patient_info: 'patient_info' contains 1 patient info in json format which will be passed from test file
        :return:  this function returns 'mrn' which contains patient's mrn info
        '''
        if self.app.env == "dev":
            log.info("pick up patient's mrn from the patient info")
            patient_info = self.search_patient_info()
            mrn = patient_info['matchingPatients'][0]['mrn']
            print(mrn)
        elif self.app.env == "sqa":
            log.info("pick up patient's mrn from the given patient")
            self.header_search(what='Joh')
            mrn = self.find_last_4_digits_from_MRN()
        log.info("patient's mrn is picked up and stored")
        return mrn

    def get_patient_Sex_Value(self):
        '''
            :param patient_info: 'patient_info' contains 1 patient info in json format which will be passed from test file
            :return:  this function returns 'sex value' which contains patient's sex info
        '''
        if self.app.env == "dev":
            log.info("pick up patient's mrn from the patient info")
            patient_info = self.search_patient_info()
            sex_value = patient_info['matchingPatients'][0]['sex']
            print(sex_value)
        elif self.app.env == "sqa":
            log.info("pick up patient's mrn from the given patient")
            self.header_search(what='Joh')
            sex_value = find_element(self.app.driver, MTBC.sex_value)
        log.info("patient's mrn is picked up and stored")
        return sex_value

    def search_specific_patient(self):
        '''
        purpose: This function search patient using endpoints(steps are mentioned in function search_patient_info()) and select one patient
        search_patient_info:Search the patient using endpoints by passing different strings
        '''
        # If env is dev then use api approach to find the patient
        if self.app.env == "dev":
            patient_info = self.search_patient_info()
            patient = self.pick_patient_first_and_last_name(patient_info)
            self.find_and_pick_patient(patient)

        # If env is sqa then search patient by passing string "Joh"
        elif self.app.env == "sqa":
            self.find_and_pick_patient('Joh')

    def show_searched_patient(self):
        '''
        purpose: This function search patient using endpoints(steps are mentioned in function search_patient_info()) and select one patient
        search_patient_info:Search the patient using endpoints by passing different strings
        '''
        patient_info = self.search_patient_info()
        patient = self.pick_patient_first_and_last_name(patient_info)
        self.find_only_patient_name(patient)

    def verify_Please_search_text_present(self):
        self.app.verification.text_present_on_page('Please search for a patient by Name or MRN.')

    def verify_text_No_Results_found(self):
        self.text_search('No Results found')

    def verify_text_search_did_not_match(self):
        self.text_search('Your search did not match any patients. Please check the spelling of patient name or MRN.')

    def find_user_full_name(self, username, password):
        '''
        :purpose-find the full name of the user
        :Discription: This function decode the token,convert it to json and then retrives full name from decoded jwt token
        :param username: It will be pass from test file
        :param password: It will be pass from test file
        :return:
        '''
        from qa_automation_drt_haw.api.api_utils.serviceApi import ServiceAPI, ServiceInfo, Token

        log.info("pick up user's first_name and last_name from the token")
        jwt_token = Token(username, password)
        if jwt_token != 0:
            log.info("Token is non-empty")
        else:
            log.info("token is empty!!")
            assert False, "token is empty!!"

        log.info("Decode the token and convert it to the json")
        decode_token = jwt.decode(str(jwt_token), verify=False)
        loaded_token = json.loads(json.dumps(decode_token))
        log.info("token is decoded and loaded as json")

        log.info("pick up the user's first_name and last_name from the decoded token")
        user_full_name = loaded_token['custom']['user_full_name']
        if len(user_full_name) > 0:
            log.info("user's first_name and last_name is picked up")
            assert True, "user_name is not present in the Token"
        return user_full_name

    def get_patient_count_on_current_page(self):
        '''
        Purpose: To get the current count of patients from the patient search
        :return: count of cases
        '''
        # cases = find_elements(self.app.driver, self.cases_table)
        cases = get_element_list_after_wait(self.app.driver,self.cases_table,timeout=60,pollFrequency=1)
        if cases:
            count = len(cases)
            log.info("In Patient Finder '%s' patients are available" % count)
            return count
        else:
            log.warning("In Patient Finder, patients are not obtained")

    def open_and_verify_patient_next_page(self, no_of_times=1):
        '''
        Purpose: This method is used to open the next page and verify if it is opened
        :param no_of_times: No of times next page to be opened. Default value is 1.
        :return: nothing
        '''
        print("Into it")
        assert self.goto_patient_next_page(
            no_of_times=no_of_times) != 0, "Error encountered while navigation amongst the " \
                                           "pages "

    def goto_patient_next_page(self, no_of_times=1):
        '''
        Purpose: To naviagate to next page
        :param no_of_times: Next page will be opened as per this parameter. By Default value is 1
        :return: Page number after opening new page
        '''
        next_page_num = ""
        for num in range(no_of_times):
            cur_page_num = self.get_patient_current_page_number()
            next_button = find_elements(self.app.driver, self.next_page_btn)
            if len(next_button) > 0:
                log.info("Navigate to next page")
                # next_button[0].click()
                # ActionChains(self.app.driver).move_to_element(next_button[0]).click().perform()
                action = ActionChains(self.app.driver).move_to_element(next_button[0]).click().perform()
                time.sleep(2)
                print("Clicked on next ")
                next_page_num = self.get_patient_current_page_number()
                wait_counter = 0
                while wait_counter <= 60 and int(next_page_num) != int(cur_page_num) + 1:
                    wait_counter = wait_counter + 1
                    time.sleep(1)
                    next_page_num = self.get_patient_current_page_number()
                log.info('Next page num is %s' % next_page_num)
                if int(next_page_num) == int(cur_page_num) + 1:
                    log.info("Navigation to page num '%s' is successful." % next_page_num)
                else:
                    log.error("Navigation to page num '%s' is unsuccessful." % (int(cur_page_num) + 1))
                    next_page_num = 0

        return int(next_page_num)

    def get_patient_current_page_number(self):
        '''
        Purpose: To fetch the current page number
        :return: The number of current page
        '''

        page_num = find_elements(self.app.driver, self.current_page_number)
        if len(page_num) > 0:
            val = page_num[0].get_attribute('title')
            log.info('Current page number is %s' % val)
            return val
        else:
            log.error("Unable to get current page number")
            return None

    def mdx_finder_pick_patient(self, value):
        '''
        :purpose: click on the 1st patient from the table
        :param value: value stores patient's name or mrn
        :return:  it will navigate to Molecular Result Summary page
        '''
        table_search = find_elements(self.app.driver, "//tbody[@class='ant-table-tbody']//tr")
        if len(table_search) == 0:
            log.error('Record "%s" has not been found', format(value))
            assert False, ('Record "%s" has not been found' % value)
        else:
            log.info('patient record has been found')
            table_search[0].click()
            log.info('clicked on patient record')

    def search_mdx_patien(self):
        if self.app.env == "dev":
            self.search_patient_info()
            print(self.app.env)
            patient_info = self.search_patient_info()
            patient = self.pick_patient_first_and_last_name(patient_info)
            self.header_search(patient)
            self.mdx_finder_pick_patient(patient)
        # If env is sqa then search patient by passing string "Joh"
        elif self.app.env == "sqa":
            self.header_search('joh')
            self.mdx_finder_pick_patient('joh')
