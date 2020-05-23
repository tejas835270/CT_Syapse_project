import time
from types import new_class

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import *
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils import JS_tricks


class GeneralVerification:
    xpath_section_text = "//div[./h3[text() = '%s']]//div[@class = 'section-body']"
    xpath_next_page = "//div[@class = 'pagination-container']//*[contains(@class,'ant-pagination')]"
    xpath_button = "//button[contains(@class, '%s')][contains(., 'Apply')]"
    button_locator = "//button/span[contains(text(),'%s')]"
    dropdown_xpath = "//*[@id='%s']|//div[@class='%s']|%s"
    xpath_textfield_locator = "//*[@data-qa-key='%s']|//textarea[contains(@id,'%s')]|//input[contains(@id,'%s')]|//span[@data-test='%s']"
    field_xpath = "//*[@data-qa-key='%s']"

    def __init__(self, app):
        self.app = app

    #purpose- to check given text is present on the page
    #page_text is passed from test file
    def text_present_on_page(self, page_text, is_not=True):
            log.info('Verify the text "%s" is present= %s on the page' % (page_text, is_not))
            if is_not:
                try:
                    element = WebDriverWait(self.app.driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, "//*[text()[contains(.,\"%s\")]]" % page_text)))
                    if element:
                        assert True, 'The text {' + page_text + '}  is displayed on the page'
                        log.info(' The text "%s" is displayed on the page', format(page_text))
                        print("\n The text %s is displayed on the page" % page_text)
                except:
                    log.error(" The text %s is NOT displayed on the page", format(page_text))
                    assert False, 'The text {' + page_text + '}  is not displayed on the page'
            if not is_not:
                element = find_elements(self.app.driver, "//*[contains(text(),'%s')]" % page_text)
                if not element:
                    print("\n The text %s is NOT displayed on the page (as expected!)" % page_text)
                else:
                    log.error("The text %s IS displayed on the page (but it must not!)" % page_text)
                    assert False, "The text %s IS displayed on the page (but it must not!)" % page_text


    def all_field_text_present_on_case_creation_page(self):
        mtb = find_element(self.app.driver, '//*[text()[contains(.,\'Molecular Tumor Board Meeting\')]]')
        daignosis = find_element(self.app.driver, '//*[text()[contains(.,\'Diagnosis\')]]')
        attach = find_element(self.app.driver, '//*[text()[contains(.,\'Attachments\')]]')
        recommend = find_element(self.app.driver, '//*[text()[contains(.,\'Recommendations\')]]')
        recomend_summary = find_element(self.app.driver, '//*[text()[contains(.,\'Recommendations Summary\')]]')
        treatment = find_element(self.app.driver, '//*[text()[contains(.,\'Treatment History\')]]')
        case_narrative = find_element(self.app.driver, '//*[text()[contains(.,\'Case Narrative\')]]')

        if mtb and daignosis and attach and recommend and recomend_summary and treatment and case_narrative:
            log.info("Molecular Tumor Board Meetiing\n", "Daignosis\n", "Attachment\n ", "Recommendations \n",
                     "Recommendations Summary \n", "Treatment History \n", "Case Narative")
            # print("All fields are present")
            assert True, "All fields are present"
        else:
            log.error("One of field is missing")
            # print("One of field is missing")
            assert False, "One of field is missing"

    def verify_current_url_contains(self, appendix):
            log.info('Verify current URL contains "%s"' % appendix)
            current_url = self.app.driver.current_url
            if appendix not in current_url:
                log.info('url does not contains {' + appendix + '} .Current url is {' + current_url + '}')
                assert False, (
                        'Redirection went wrong. {' + appendix + '} not reached. Current url is {' + current_url + '}')
            else:
                log.info('url contains {' + appendix + '} .Current url is {' + current_url + '}')

    def patient_info(self, patient_name, expected_info):

            log.info('Patient "%s" info should be: %s' % (patient_name, expected_info))
            mismatches = []
            print('Patient "%s" info should be: %s' % (patient_name, expected_info))
            if not expected_info:
                mismatches.append('Patient Case Summary')
            else:
                for head in expected_info.keys():
                    print(head)
                    if head == 'Deceased':
                        expected_result = expected_info[head]
                        print(expected_result)
                        value = find_elements(self.app.driver,
                                              "//span[@class='value' and contains(text(),'Deceased')][text()[contains(.,'%s')]]" % expected_result)
                        if len(value) == 0:
                            mismatches.append(head)
                            log.info("No info for " + head)
                            assert False, "No info for " + head
                        else:
                            log.info("found info for " + head)

                    else:

                        value = find_elements(self.app.driver,
                                              "//*[@class='key' and contains(text(),'%s')]/../span[@class='value']" % head)
                        if len(value) > 0:
                            log.info("found info for " + head)
                            assert len(value) > 0, "No info for " + head
                        else:
                            log.error("No info for " + head)
                        actual_result = value[0].text
                        print(actual_result)
                        expected_result = expected_info[head]
                        if actual_result != expected_result:
                            mismatches.append(head)
            if mismatches:
                assert len(mismatches) == 0, 'Mismatch(es) found in: %s' % mismatches

            time.sleep(2)

    def modal_window_title(self, name):
        """
        Verify modal window title
        """
        log.info('Verify modal window title "%s"' % (name))
        time.sleep(2)
        self.app.driver.implicitly_wait(10)
        try:
            modal_window = find_elements(self.app.driver,
                                         "//div[@class='ant-modal-title' and text()='%s']" % name)
        except:
            modal_window = find_elements \
                (self.app.driver,
                 "//div[contains(@class,'modal-dialog')]//*[@class='modal-title' or @class='modal-header']")
        if not modal_window:
            assert False, ('Modal window with title %s has not been found' % name)
        elif modal_window and modal_window[0].text.strip().lower() != name.lower():
            assert False, ('Modal window exist but with different title.\n '
                           'Expected: %s\n '
                           'Actual:   %s' % (name, modal_window[0].text))

    def button_is_disable(self, btn_name):
            log.info('Button "%s" should be disabled' % (btn_name))
            target = [btn for btn in find_elements(self.app.driver, "//*[text()='%s']" % btn_name) if
                      btn.is_enabled()]
            if target:
                log.error("BUG! Button with text '%s' is enabled." % btn_name)
                assert False, ("BUG! Button with text '%s' is enabled." % btn_name)

    def search_box(self):
        '''
        :purpose: to check search box is present on [serach patient] page
        :return: nothing
        '''
        locator = "//input[@placeholder='Patient Name or MRN...']"
        # box = find_elements(self.app.driver, "//input[@placeholder='Patient Name or MRN...']")
        box = get_element_after_wait(self.app.driver,locator, timeout=60)
        if box:
            log.info("user is successfully landed on [serach patient] page")
            log.info("'search box' is present on [serach patient] page")
            assert True, 'BUG! Search box did not show up'
        else:
            log.error('BUG! Search box did not shown up')

    # def pagination(self):
    #     """
    #             Verify pagination in pages
    #             """
    #
    #     pagination_next = find_elements(self.app.driver, "//div[@class = 'ant-pagination-item ant-pagination-item-1 ant-pagination-item-active']")
    #     assert pagination_next, 'BUG! Pagination did not show up'

    def scroll_to_bottom_of_page(self):
        '''
        :purpose: Scroll down to the bottom of the page
        '''
        self.app.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        log.info("Scroll down to the bottom of the page")


    def scroll_to_top_of_page(self):
        self.app.driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")
        log.info("Scroll up to the top of the page")
        time.sleep(1)

    def click_nxt_pagenum(self, pagenum):
        next_pg = find_elements(self.app.driver, self.xpath_next_page)
        if next_pg:
            log.info("next_pg section is present")
            assert True,'next_pg section is not present'
        else:
            log.info("next_pg section is not present")
        next_pg[pagenum].click()

    def go_next_tab_verify_title(self, appendix):
            log.info('Verify current URL contains title as "%s"' % appendix)
            windows = self.app.driver.window_handles
            self.app.driver.switch_to.window(windows[1])
            try:
                WebDriverWait(self.app.driver, 30).until(EC.title_contains(appendix))
                print("Page is ready!")
            except TimeoutException:
                print("Loading took too much time!")
            title_verification = self.app.driver.title
            log.info(title_verification)
            if appendix != title_verification:
                log.info('Title is not matched with {' + title_verification + '}')
                assert False, ('Redirection went wrong . {' + appendix + '} Title is not matched with {' + title_verification + '}')
            else:
                log.info(' Title is  matched with {' + title_verification + '}')

    # verify url contains the right appendix being passed and give the control back to main browser
    def go_next_tab_verify_url(self, appendix):
            log.info('Verify current URL contains "%s"' % appendix)
            windows = self.app.driver.window_handles
            new_current_url = self.app.driver.switch_to.window(windows[1])
            WebDriverWait(self.app.driver, 20).until(EC.url_contains(appendix))
            url_new_tab = self.app.driver.current_url
            # print(url_new_tab)
            if appendix not in url_new_tab:
                assert False, (
                        'Redirection went wrong. {' + appendix + '} not reached. Current url is {' + url_new_tab + '}')
            else:
                log.info('Redirection went successfully. {' + appendix + '} is present in the Current url {' + url_new_tab + '}')

    # verify url contains the right appendix being passed and give the control back to main browser
    def go_next_tab_verify_url_and_close(self, appendix):
            log.info('Verify current URL contains "%s"' % appendix)
            windows = self.app.driver.window_handles
            new_current_url = self.app.driver.switch_to.window(windows[1])
            time.sleep(3)
            url_new_tab = self.app.driver.current_url
            # print(url_new_tab)
            if appendix not in url_new_tab:
                assert False, (
                        'Redirection went wrong. {' + appendix + '} not reached. Current url is {' + url_new_tab + '}')
            else:
                log.info('Redirection went wrong. {' + appendix + '} not reached. Current url is {' + url_new_tab + '}')
            # close the tab browser which was opened
            self.app.driver.close()
            # give control back to main browser
            self.app.driver.switch_to.window(windows[0])

    def verify_button_on_page(self, button_text, is_not=True):
            log.info('Verify the button "%s" is present= %s on the page' % (button_text, is_not))
            if is_not:
                element = find_elements(self.app.driver, "//*[text()[contains(.,\"%s\")]]" % button_text)
                if element:
                    print("\n The button text %s is displayed on the page" % button_text)
                    log.info('The button text %s is displayed on the page', format(button_text))
                else:
                    raise Exception("\n The button text %s is NOT displayed on the page" % button_text)
            if not is_not:
                element = find_elements(self.app.driver, "//*[contains(text(),'%s')]" % button_text)
                if not element:
                    print("\n The button text %s is NOT displayed on the page (as expected!)" % button_text)
                    log.error('The button text %s is NOT displayed on the page (as expected!)', format(button_text))
                else:
                    raise Exception("\n The button text %s IS displayed on the page (but it must not!)" % button_text)

    def verify_column_headers_on_table(self, column_header_name):
            '''
            :purpose: Verify the given column header on [mtb case management] page
            '''
            log.info('Verify the column header "%s" on the [mtb case management] page' % (column_header_name))
            element = find_elements(self.app.driver, "//*[text()[contains(.,\"%s\")]]" % column_header_name)
            if element:
                log.info('The column header "%s" is displayed on the page' % column_header_name)
            else:
                log.error(("The column header %s is NOT displayed on the page" % column_header_name))
                raise Exception("\n The column header %s is NOT displayed on the page" % column_header_name)

    def verify_partial_text(self, text):
            '''
            :purpose: verify given text is partially present or not
            :param text: It will be passed from test file
            '''
            element = find_elements(self.app.driver, "//*[contains(text(),'%s')]" % text)
            if element:
                log.info("the last 4 digit of mrn are present into the case id")
            else:
                raise Exception("\n The  text %s is NOT displayed on the page" % text)

    def verify_scroll_for_recommdations_summary(self, text="hello \n World \n India \n mumbai \n bombay \n "
                                                           "CITIUS \n USA \n \n"):
            log.info('Verify the Scroll is displayed on "recommdations summary" section')

            element = WebDriverWait(self.app.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='createCase_recommendationsSummary']")))
            ActionChains(self.app.driver).move_to_element(element).click()
            element.send_keys('%s' % text)
            text_from_textbox = element.get_attribute('value')
            log.info("text entered is %s", format(text_from_textbox))
            print("text entered is ", text_from_textbox)
            lines = text_from_textbox.count("\n")
            if lines != 0:
                print("validate the number of new lines are present in Text Box :- ", lines)
                log.info("validate the number of new lines are present in Text Box :- ", format(lines))
                if lines >= 7:
                    log.info("Scroll is available in Recommdations Summary as it has  %s no of lines", format(lines))
                    print("Scroll is available in Recommdations Summary as it has  %s no of lines" % lines)
                    assert True, ("Scroll is available in Recommdations Summary as it has  %s no of lines" % lines)

                elif lines < 7:
                    log.error("Scroll is not available in Recommdations Summary as it has only %s no of lines",
                              format(lines))
                    assert False, (
                            "Scroll is not available in Recommdations Summary as it has only %s no of lines" % lines)
            else:
                print("Scroll is not activated as the condition is not matched.")

    def verify_case_id_is_displayed_with_middle_digits_mrn(self):
        case_id = find_element(self.app.driver, "//*[contains(text(),'C-')]")
        value = case_id.text
        print("Case ID is ", value)
        log.info('Case ID is "%s" is displayed on the page', format(value))
        mrn_no = value.split('-').pop(3)
        return mrn_no

    def verify_case_id_is_displayed_on_case_managment_screen(self):
        time.sleep(3)
        case_id = find_element(self.app.driver, "//*[contains(text(),'C-')]")
        value = case_id.text
        new_value = value.replace(' ', '-')
        strip_value = new_value.rsplit('Case-').pop(1)
        log.info("Case ID is:- %s", format(strip_value))
        print("Case ID is:- ", strip_value)
        return strip_value

    def verify_case_id_present_on_mtb_page(self, case_id):
        dates = find_elements(self.app.driver, "//tbody/tr/td[2]")
        print("length of data is ", len(dates))
        log.info("length of data is %s", format(len(dates)))
        text = []
        for matched_element in dates:
            case_id_text = matched_element.text
            text.append(case_id_text)
        flag = True
        print(text)
        if case_id in text:
            # print("Case ID ", case_id, "is present on page")
            log.info("Case ID %s is present on page", format(case_id))
            assert True, "Case ID is present on page"

        else:
            log.info("Case is absent on page please load more")
            # print("Case is absent on page please load more")
            flag = False
            # assert False, "Case is absent on page "
        return flag

    def verify_cancel_button_popup_is_displayed(self):
        '''
        :purpose:Verify popup is Displayed when clicked on Cancel button
        '''
        log.info('Verify popup is Display when clicked on Cancel button')
        popup = find_element(self.app.driver, "//*[contains(text(),'You have unsaved changes')]")
        if popup.is_displayed():
            log.info('Popup is displayed')
            flag_popup = True
            assert True,"Popup is displayed"
        else:
            # assert False, 'PopUp is not displayed'
            log.error('PopUp is not displayed')
            flag_popup = False
            assert False, 'PopUp is not displayed'
        return flag_popup

    def verify_user_stay_on_create_form_when_cancel_is_click_on_popup(self):
        time.sleep(1.5)
        cancel_popup = find_element(self.app.driver, "//*[@class='ant-modal']//span[contains(text(),'Cancel')]")
        self.app.driver.execute_script("arguments[0].click();", cancel_popup)
        text = str(self.text_present_on_page("MTB Case Management"))
        if text.find("MTB Case Management"):
            log.info("User is on same page")
            # print("User is on same page")
        return False

    def verify_user_is_navigated_to_user_case_management_when_continue_is_clicked(self):
        time.sleep(1)

        continue_popup = find_element(self.app.driver, "//*[@class='ant-modal']//span[contains(text(),'Continue')]")
        self.app.driver.execute_script("arguments[0].click();", continue_popup)
        time.sleep(2)
        text = str(self.text_present_on_page("Molecular Tumor Board"))
        if text.find("Molecular Tumor Board"):
            print("User is on Create Case page")
        return True

    def verify_user_clicks_on_cancel(self):
        time.sleep(1.5)
        cancel_popup = find_element(self.app.driver, "//*[@class='ant-modal']//span[contains(text(),'Cancel')]")
        self.app.driver.execute_script("arguments[0].click();", cancel_popup)
        text = str(self.text_present_on_page("MTB Case Management"))
        if text.find("MTB Case Management"):
            assert True, 'User is on Create Case form page '
            print("User is on same page")
            log.info("User is on same page")

    def verify_user_clicks_on_continue(self):
        continue_popup = find_element(self.app.driver, "//*[@class='ant-modal']//span[contains(text(),'Continue')]")
        self.app.driver.execute_script("arguments[0].click();", continue_popup)
        time.sleep(2)
        text = str(self.text_present_on_page("Molecular Tumor Board"))
        if text.find("Molecular Tumor Board"):
            assert True, 'User is on User Case Management Screen'
            print("User is on User Case Management Screen")
            log.info("User is on User Case Management Screen")


    def verify_case_id_DOB_are_present_on_MTB_page(self):
        '''
        :purpose: Verify case_id ,DOB,sex field headers are present on [create new case] page'
        '''
        log.info('Verify case_id ,DOB,sex field headers are present on [create new case] page')
        case_id = find_element(self.app.driver, "//*[contains(text(),'C-')]")
        dob = find_element(self.app.driver, "//*[contains(text(),'DOB')]")
        sex_field = find_element(self.app.driver, "//*[contains(text(),'Sex')]")
        if case_id and dob and sex_field:
            assert True, "case_id ,DOB,sex field headers are not present"
            log.info("case_id ,DOB,sex field headers are present")
        else:
            assert False, "Either of the fields are missing"

    #purpose- to check data is prepopulated in the given field
    def verify_prepopulated_fileds_in_cases(self):
        '''
        :purpose:Verify the data is present in "Primary Site" field
        '''
        log.info('Verify the data is present in "Primary Site" field')
        value = find_element(self.app.driver, "//*[@data-qa-key='createCase_physician_display']")
        value_text = value.text
        print(value_text)
        if value_text is not None:
            log.info("Primary Site value %s is already present in field", format(value_text))
            assert True, "Value is already present in field"
        else:
            log.error("Values are not present in the field")
            assert False, "Values are not present in the field"

    def verify_contents_of_MTB_module(self, text):

        if not self.text_present_on_page('Molecular Tumor Board Manager'):
            if not self.text_present_on_page(text):
                assert True, "text is present on portal page"
                print('MTB module is presernt with  text ', text, 'on the portal page ')
            else:
                print("The given text", text, "is not associated with MTB")
                assert False, ("The given text", text, "is not associated with MTB")
        else:
            log.error("MTB Module is not present in Portal Page")
            assert False, "MTB Module is not present in Portal Page"

    def select_all_checkbox_in_dashboard(self):
        sort_field = find_element(self.app.driver,"//*[@class='FICheckRadio']").click()


    def click_on_button(self, btn_name):
        """
        click on element with text if its displayed
        """
        click_btn = find_elements(self.app.driver, "//*[@title='%s']" % btn_name)
        assert len(click_btn) > 0, 'Sort field have not been found'
        click_btn[0].click()
        time.sleep(2)

    def sleep_time(self, seconds):
        time.sleep(seconds)

    #purpose:- verify the given error msg is not present on the page
    #errormsg is the error message whic is passed from test file
    def verify_no_error_in_page(self, errormsg):
            log.info('Verify error msg "%s"' % errormsg)

            element = find_elements(self.app.driver, "//*[text()[contains(.,\"%s\")]]" % errormsg)
            if element:
                log.error(" The text %s is displayed on the page", format(errormsg))
                raise Exception("\n The text %s is NOT displayed on the page" % errormsg)
            else:
                log.error(" The text %s is NOT displayed on the page", format(errormsg))

    def verify_counts(self, total):
        # verify_cnt = find_elements(self.app.driver, "//*[@tb-test-id='Number of Test Results BAN - Adoption']")
        verify_cnt = find_elements(self.app.driver, "//*[@id='view11448476496450518663_10600224292145905202']")
                     
        # verify_cnt = find_element(self.app.driver, "//*[text()[contains(.,\"%s\")]]")
        assert len(verify_cnt) > 0, 'Count of Total patients field have not been found'
        # text_from_textbox = verify_cnt.get_attribute('value')
        print(f"Count is : {verify_cnt[0]}")
        time.sleep(2)

    # purpose - to verify the value entered successfully in the text field
    # idVal is the locator of text field which needs to be tested and it is declared in page class files
    # expected_text is the expected value which is passed from test file
    def verify_textarea_value(self, expected_text, idVal, i=0):
        log.info('Verify the text value present in "%s" field' %idVal)
        text_val = find_elements(self.app.driver, self.xpath_textfield_locator % (idVal, idVal, idVal, idVal))
        if not text_val:
            assert False, ('text field has not been found')
        actual_value = text_val[i].text or text_val[i].get_attribute("value")
        log.info('actual_value=', actual_value)
        log.info('expected_text=', expected_text)
        if not actual_value == expected_text:
            assert False, "actual value '%s' is not matching the expected value '%s'" % (actual_value, expected_text)
        else:
            log.info("actual value is matching the expected value")

    # purpose - to verify that button is displayed on the page
    # button_locator is the locator of button declared at the top
    # button_text is button text which user needs to pass
    def verify_button_is_present(self, button_text):
        element = find_elements(self.app.driver, self.button_locator % button_text)
        if element:
            assert True, 'The button %s is not displayed on the page'
            log.info('The button %s is displayed on the page', format(button_text))
        else:
            log.error('The button %s is not displayed on the page', format(button_text))
            raise Exception("\n The button text %s is NOT displayed on the page" % button_text)

    # purpose - to verify the column headers of the table
    # column_header_name is the column title
    def verify_column_header_on_table(self, column_header_name):
        element = find_elements(self.app.driver,
                                "//table//span[@class='ant-table-column-title']/div[text()[contains(.,'%s')]]|//table//span[@class='ant-table-column-title'][text()[contains(.,'%s')]]" % (
                                    column_header_name, column_header_name))
        if element:
            assert True, 'The  column header %s is not displayed on the page' % column_header_name
            log.info("\n The column header %s is displayed on the page" % column_header_name)
        else:
            log.error("\n The  column header  %s is NOT displayed on the page" % column_header_name)
            raise Exception("\n The  column header  %s is NOT displayed on the page" % column_header_name)

    # purpose - to verify the options of dropdown
    # dd_class is the locator of dropdown which needs to be tested
    # data contains coption values which is passed from test file
    def verify_dd_values(self, data,dd_class='null',dd_xpath='null'):
        mismatches = []
        data_ex = data
        data_ac = []
        el = find_element(self.app.driver, self.dropdown_xpath % (dd_class, dd_class,dd_xpath)).click()
        time.sleep(1)
        vocab_list = find_elements(self.app.driver,
                                   "//div[contains(@class,'ant-select-dropdown')]//li[@role='option']")
        for e in vocab_list:
            if e.text != '':
                data_ac.append(e.text.strip())
        print(data_ac)

        if sorted(data_ac) != sorted(data_ex):
            print("actual values of dropdown '%s' does not match the pattern" % dd_class)
            print(set(sorted(data_ac)) - set(sorted(data_ex)))
            log.info("actual values of dropdown '%s' does not match the pattern" % dd_class)
            log.info(set(sorted(data_ac)) - set(sorted(data_ex)))
            mismatches = set(sorted(data_ac)) - set(sorted(data_ex))
        else:
            log.info('actual values %s is equal to the expected values %s' % (data_ac, data_ex))

        if len(mismatches) > 0:
            log.info('actual values %s is not equal to the expected values %s' % (data_ac, data_ex))
            assert False, 'actual values %s is not equal to the expected values %s' % (data_ac, data_ex)
        time.sleep(1)

    # purpose - to verify the present value of dropdown
    # dd_name is the locator of dropdown which needs to be tested and it will be passed form test file
    # option contains expected value which is passed from test file
    def verify_dd_default_value(self, expected_option, dd_name='null', dd_xpath='null', i=0):
        dropdown = WebDriverWait(self.app.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, self.dropdown_xpath % (dd_name, dd_name,dd_xpath))))
        # dropdown = find_elements(self.app.driver, self.dropdown_xpath % (dd_name, dd_name, dd_xpath))
        assert len(dropdown) > 0, 'dropdown not present'
        actual_option = dropdown[i].text
        assert actual_option == expected_option, "actual option '%s' is not matching the expected default value '%s'" % (
        actual_option, expected_option)
        log.info(
            "actual option '%s' is matching the expected default value '%s'" % (actual_option, expected_option))

    # purpose - to verify the value of calender field
    # calendar_field is the locator of calender field
    # expected_date will be passed from test file
    def verify_calender_value(self, calendar_field, expected_date):
        input_fields = find_elements(self.app.driver, self.field_xpath % calendar_field)
        assert len(input_fields) > 0, 'Input field has not been found for' + calendar_field
        input_value = input_fields[0].get_attribute('value')
        print(input_value)
        assert input_value == expected_date, 'input_value %s is not matching expected_date %s' % (
        input_value, expected_date)
        log.info("calender_value is verified successfully")