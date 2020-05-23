import time
import datetime
import os
import re
from datetime import datetime
from selenium.webdriver.common.keys import Keys

from qa_automation_drt_haw.ui.ui_utils import JS_tricks
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from qa_automation_drt_haw.ui.ui_utils.Logs import log

class MTB:

    #xpath for the input fields
    input_xpath="//textarea[@id='%s']|//input[contains(@id,'%s')]|//*[@data-qa-key='%s']"


    def __init__(self, app):
        self.app = app

    def verify_case_table(self, tableKey, values):
            log.info('Verify "%s" section %s displayed' % (tableKey, values))
            section = find_elements(self.app.driver, "//*[@class='%s']" % tableKey)
            assert len(section) > 0, 'Cell Value has not been found for option {0}'.format(section)
            # section[0].click()
            # time.sleep(1)
            option = find_elements(self.app.driver,
                                   "//*[@class='ant-table-row-indent indent-level-0'] and text()='%s'" % values)
            assert len(option) > 0, 'Option %s has not been found' % values

            time.sleep(3)

    def verify_populated_data(self,data):
            log.info('Verify Chronicle pre-populated info')

            actual_results = []

            headers = [x.text for x in find_elements(self.app.driver,'//thead//th') if len(x.text) != 0]
            rows = find_elements(self.app.driver,"//tbody/tr")
            assert len(rows) > 0, 'Pre-populated values have not been found'
            for row in rows:
                pre_values = [y.text for y in row.find_elements_by_xpath("td[not(contains(@class, 'selection-column'))]")]
                actual_results.append(dict(zip(headers, pre_values)))

            print(actual_results)

            expected_results = [data]
            expected_headers = [y for y in data.keys()]
            # for table_row in context.table.rows:
            #     cells = [n for n in table_row.cells]
            #     prep_dict = dict(zip(expected_headers, cells))
            #     expected_results.append(prep_dict)
            print(expected_results)
            assert expected_results == actual_results, "Expected: %s, Actual: %s" % (expected_results, actual_results)

    def click_sorting(self, sortfield):
            log.info('Verify Default "%s" is available' % sortfield)
            sort_field = find_elements(self.app.driver, "//*[@title='%s']" % sortfield)
            assert len(sort_field) > 0, 'Sort field have not been found'
            sort_field[0].click()
            time.sleep(3)
            sort_field[0].click()
            time.sleep(3)
            sort_field[0].click()
            time.sleep(3)

    def meeting_date_ascending_sorting(self, sortfield='Sort'):
            log.info('Verify Default "%s" is available' % sortfield)
            sort_field = find_elements(self.app.driver, "//*[@title='%s']" % sortfield)
            assert len(sort_field) > 0, 'Sort field have not been found'
            table1 = find_element(self.app.driver, "//tbody/tr[1]/td[1]")
            table20 = find_element(self.app.driver, "//tbody/tr[20]/td[1]")
            before_sort_max = table1.text
            before_sort_min = table20.text

            sort_field[0].click()
            time.sleep(0.5)
            sort_field[0].click()
            time.sleep(0.5)
            after_sort_max = table20.text
            after_sort_min = table1.text
            print("Before sort Max", before_sort_max)
            print("Before Sort Min", before_sort_min)
            print("After Sort Max", after_sort_max)
            print("After Sort Min", after_sort_min)

            if before_sort_max == after_sort_min and before_sort_min == after_sort_max:
                log.info("Meeting List is sorted in ascending order")
                assert True, "Meeting List is sorted in ascending order"
            else:
                log.error("Meeting List is not sorted")
                assert False, "Meeting List is not sorted"

    def pick_case(self, patientName):
        log.info('Click case for patient "%s" ' % patientName)
        row_field = find_elements(self.app.driver, "//*[contains(text(),'%s')]" % patientName)
        assert len(row_field) > 0, 'Row field have not been found'
        row_field[0].click()
        time.sleep(3)

    def verify_special_character_in_recommdation_summary(self, text='Tejas Shirke-'):

        # element = find_element(self.app.driver, "//*[@id='createCase_recommendationsSummary']")

        element = WebDriverWait(self.app.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='createCase_recommendationsSummary']")))
        ActionChains(self.app.driver).move_to_element(element).click()
        # ActionChains(self.app.driver).move_to_element(element).perform()
        # element.click()

        element.send_keys('%s' % text)
        text_from_textbox = element.get_attribute('value')
        print("text entered is ", text_from_textbox)
        log.info("text entered is %s ", format(text_from_textbox))
        time.sleep(2)
        # self.verify_error_msg()

    def verify_error_msg(self):
        msg = find_element(self.app.driver,
                           "//*[@id=\"root\"]/div/section/main/div[2]/section/form/div[7]/div/div[2]/div/div/div/div")
        msg_text = msg.text

        if 'Recommendation Summary contains disallowed characters' in msg_text:
            log.error("Error is appeared")
            assert False, "Error is appeared"
        else:
            log.info("Error is not appeared")
            assert True, "Error is not appeared"

    # purpose - to check the url contain 'mtb'
    def verify_url_contains_mtb(self):
        self.app.verification.verify_current_url_contains('mtb')

    # purpose is to remove data from input field by sending Keys.BACKSPACE
    #input_xpath parameter is the locator which is defined at the top
    def clear_input_field_using_backspace(self, field_name):
            log.info('clear the field %s if it is not empty' %field_name,field_name,field_name)
            field = find_elements(self.app.driver, self.input_xpath % (field_name,field_name,field_name))
            assert len(field) > 0, 'field %s has not been found' % field_name

            lenText = field[0].get_attribute('value')
            lenth = len(lenText)
            i=0
            if i < lenth:
                while i < lenth:
                    field[0].send_keys(Keys.BACKSPACE)
                    i=i+1
                lenText = field[0].get_attribute('value')
                if len(lenText) == 0:
                    log.info("data is cleared")
                    assert True
                else:
                    log.info("data is not cleared")

            else:
                log.info("There is no data to clear")
