import time
# import random
# from datetime import datetime, timedelta


# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from qa_automation_drt_haw.ui.ui_utils import JS_tricks
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements
from selenium.webdriver.common.keys import Keys
from qa_automation_drt_haw.ui.ui_utils.Logs import log

from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GeneralNavigation:
    xpath_button_by_name = "//*[normalize-space(text())='%s']"
    xpath_text_field = "//div[@id = 'createCase_physician']"
    xpath_dropdown_field = "//div[@id = '%s']"
    xpath_button_by_name1 = "//button[contains(@class, '%s')][contains(., 'Create Case')]"
    xpath_select_text_from_dropdown = "//div[@class = 'ant-select-selection-selected-value']//*[contains(@title,'%s')]"
    button_xpath = "//button/span[contains(text(),'%s')]|//button[@data-qa-key='%s']"
    xpath_contains="//*[text()[contains(.,'%s')]]"
    xpath_syapse_logo = "//a[@href='%s']"
    xpath_case_page = "//*[@class='anticon anticon-right']"


    def __init__(self, app):
        self.app = app
        # self.app.driver = app.driver
        self.window_before = ''

    # def button_click(self, button_name):
    #         log.info('Click the button "%s" on the page' % (button_name)):
    #         element = find_elements(self.app.driver, self.xpath_button_by_name1 % button_name)
    #         if element:
    #             element.click()
    #             # print("\n The button text %s is displayed on the page" % button_name)
    #         else:
    #             raise Exception("\n The button text %s is NOT displayed on the page" % button_name)

    # def button_present_on_page(self, button_text):
    #         log.info('Verify the text "%s" is present on the page' % (button_text)):
    #         # if is_not:
    #         #     element = find_elements(self.app.driver,"//*[text()[contains(.,\"%s\")]]" % button_text)
    #         #     if element:
    #         #         element[0].click()
    #         #         print( "\n The text %s is displayed on the page" % button_text)
    #         #     else:
    #         #         raise Exception("\n The text %s is NOT displayed on the page" % button_text)
    #         # if not is_not:
    #         #     element =find_elements(self.app.driver,"//*[contains(text(),'%s')]" % button_text)
    #         #     if not element:
    #         #         print( "\n The text %s is NOT displayed on the page (as expected!)" % button_text)
    #         #     else:
    #         #         raise Exception("\n The text %s IS displayed on the page (but it must not!)" % button_text)
    #         btn = find_elements(self.app.driver, "//button[contains(@class, '%s')][contains(., 'Create Case')]" % button_text)
    #         print (len(btn))
    #         assert len(btn) > 0, 'Button Add Another section has not been found on the page'
    #         btn[0].click()
    #         time.sleep(2)

    def click_btn(self, btn_name):
        """
        click on element with text if its displayed
        """
        log.info('Click button "%s"' % (btn_name))
        target = [btn for btn in find_elements(self.app.driver, self.xpath_button_by_name % btn_name)
                  if btn.is_displayed()]
        if btn_name == 'Add Another':
            target = [btn for btn in find_elements(self.app.driver, self.xpath_button_by_name % btn_name) if
                      btn.is_displayed()]
            log.info('Button {0} has been displayed'.format(btn_name))
        if not target:
            log.critical('Button {0} has not been found'.format(btn_name))
            assert False, ('Button {0} has not been found'.format(btn_name))
        else:
            try:
                target[0].click()
            except:
                JS_tricks.element_to_the_middle(self.app.driver, target[0])
                time.sleep(2)
                JS_tricks.mouse_click_element(self.app.driver, target[0])
                log.info('Button {0} has been found & clicked'.format(btn_name))
            finally:
                time.sleep(1.5)
    time.sleep(2)

    def create_new_case_button(self, btn_name='Create New Case'):
        """
        click on element with text if its displayed
        """
        self.click_btn(btn_name)

    def click_link(self, link_text):
        """
            Verify current URL contains "link_text"
        """
        log.info('Click on "%s" link' % (link_text))
        time.sleep(2)
        link = find_elements(self.app.driver, '//*[text()="%s"]' % link_text)
        if link:
            link[0].click()
            time.sleep(2)
            try:
                WebDriverWait(self.app.driver, 5).until(EC.alert_is_present(),
                                                        'Waiting for alert with confirmation')
                alert = self.app.driver.switch_to.alert
                alert.accept()
                log.info("alert accepted")
                time.sleep(2)
            except TimeoutException:
                log.warn("no alert")
        else:
            assert False, ('Link not found "%s"!' % link_text)
        time.sleep(3)

    def click_main_nav_button(self, name):
            log.info('Click main navigation button "%s"' % (name))
            if 'oncology' in self.app.driver.current_url:
                try:
                    main_menu = find_element(self.app.driver, "//span[@class='account-link']")
                    # ActionChains(context.browser).move_to_element(main_menu).perform()
                    main_menu.click()
                    time.sleep(2)
                    button = find_element(self.app.driver, "//ul[@class='user-menu']//a[contains(., '%s')]" % name)
                    print('==', button)
                    button.click()
                except:

                    assert False, 'Button {} has not been found'.format(name)
            else:
                icons_meaning = {'Help': 'fa-question-circle',
                                 'My Account': 'fa-cog',
                                 'Sign out': 'fa-cog',
                                 'Similar Patients': 'fa-users',
                                 'CT Pre-screening': 'fa-flask',
                                 }

                # context.browser.implicitly_wait(4)
                try:
                    button = find_elements(self.app.driver, "//li[@role = 'presentation']/a[contains(., '%s')]" % name)
                    button[0].click()
                except Exception as e:
                    print("did not found button, cause of \n {0}".format(e))
                    if name in icons_meaning.keys():
                        if name == 'Help':
                            icon = find_elements(self.app.driver, "//i[contains(@class, '%s')]" % icons_meaning[name])
                            if not icon:
                                # assert False,('Not able to navigate to [Help]')
                                assert False, 'Not able to navigate to [Help]'
                            else:
                                icon[0].click()
                                time.sleep(2)
                        else:
                            try:
                                find_element(self.app.driver,
                                             "//i[contains(@class, '%s')]" % icons_meaning[name]).click()
                                time.sleep(2)
                                find_element(self.app.driver,
                                             "//li[@role = 'presentation']/a[contains(., '%s')]" % name).click()
                            except Exception as e:
                                # assert False,('Not able to navigate to [%s].\n Error is:\n%s ' % (name, e))
                                assert False, 'Not able to navigate to [{0}].\n Error is:\n{1} '.format(name, e)
                    else:
                        # assert False,('Button %s has not been found' % name)
                        assert False, 'Button {0} has not been found'.format(name)

            time.sleep(2)

    def switch_to_new_window_and_verify_title(self, win_title):
        """
        Switch to new window and verify title
        """
        log.info('Switch to new window and verify title "%s"' % (win_title))
        self.window_before = self.app.driver.window_handles[0]
        self.app.driver.switch_to_window(self.app.driver.window_handles[-1])
        time.sleep(3)
        current_title = str(self.app.driver.title.encode('ascii', 'ignore').decode("utf-8"))
        if current_title != win_title:
            assert False, (
                    'Redirection went wrong. {' + win_title + '} not reached. Current window is {' + current_title + '}')

    def default_window_switch(self):
        self.app.driver.switch_to_window(self.window_before)
        time.sleep(3)

    def refresh_page(self):
        self.app.driver.set_page_load_timeout(10)
        self.app.driver.refresh()
        log.info("Refreshing the page")
        time.sleep(3)

    def hide_header(self):
        if "oncology" in self.app.driver.current_url:
            header = find_element(self.app.driver, "//div[contains(@class,'ant-layout-header')]")
            self.app.driver.execute_script("arguments[0].style.display='none'", header)
        else:
            header = find_element(self.app.driver, "//nav[contains(@class, 'navbar-fixed-top')]")
            self.app.driver.execute_script("arguments[0].style.display='none'", header)

    def hide_footer(self):
        footer = find_element(self.app.driver, "//div[@class='antd-pro-footer-toolbar-toolbar']")
        self.app.driver.execute_script("arguments[0].style.display='none'", footer)
        time.sleep(2)

    def show_footer(self):
        footer = find_element(self.app.driver, "//div[@class='antd-pro-footer-toolbar-toolbar']")
        self.app.driver.execute_script("arguments[0].style.display='block'", footer)

    def click_button_for_section(self, button, section):
        """
        eg. click "button" for "section"
        """
        log.info('Click %s button for %s section' % (button, section))
        self.app.driver.implicitly_wait(10)
        if 'oncology' in self.app.driver.current_url:
            element = find_elements(self.app.driver,
                                    "//div[@data-qa-key][.//span[contains(text(),'%s')]]//button[.//*[text()='%s']]" % (
                                        section, button))
        else:
            element = find_elements(self.app.driver,
                                    "//div[contains(@class, 'base-panel')][.//*[text()='%s']]//button[contains(., '%s')][not(@disabled)]" % (
                                        section, button))

        if not element:
            log.error('Button {0} is disabled')
            assert False, ('Button {0} is disabled'.format(button))
        elif element:
            JS_tricks.element_to_the_middle(self.app.driver, element[0])
            element[0].click()
            log.info('Button {' + button + '} clicked')
            time.sleep(1.5)
        else:
            log.error('Button {1} has not been found')
            assert False, ('Button {0} has not been found'.format(button))

    def browser_back(self):
            '''
            :purpose: Go back to the previous page
            '''
            log.info('Go back to previous page by clicking on Browser back')
            self.app.driver.back()
            time.sleep(2)
            log.info('Clicked on Browser back')

    def enter_date_in_calendar(self, calendar_field, date):
        """
        :purpose: Enter given "date" into calendar field "calendar_field"
        :parameter: date is passed from test file and calendar_field is the locator which is passed from page file
        """
        log.info('Enter date "%s" in calender field"%s"' % (date,calendar_field))
        input_before = WebDriverWait(self.app.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@data-qa-key='%s']" % calendar_field)))
        assert len(input_before) > 0, 'Input field before has not been found for calendar {0}'.format(
            calendar_field)
        print(input_before)
        input_before[0].click()
        # time.sleep(3)
        input_after = WebDriverWait(self.app.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH,"//input[@class='ant-calendar-input ']")))
            # find_elements(self.app.driver, "//input[@class='ant-calendar-input ']")
        assert len(input_before) > 0, 'Input field after has not been found for calendar {0}'.format(calendar_field)
        val = input_after[0].get_attribute('value')
        assert len(val) == 0, 'You are trying to put value in non-empty field'
        if date == 'today':
            today_btn = find_elements(self.app.driver, "//*[contains(@class, 'calendar-today-btn ')]")
            assert len(today_btn) > 0, 'Today link has not been found'
            today_btn[0].click()
        else:
            input_after[0].send_keys(date)
            time.sleep(1)
            input_after[0].send_keys(Keys.RETURN)
            log.info('date "%s" is entered in Calendar field "%s"' % (date,calendar_field))
        time.sleep(1)

    def enter_meeting_date(self,date='Oct 20, 2021'):
        self.enter_date_in_calendar('createCase_meetingDate', date)

    # purpose-select option from dropdown field
    # ddname is the locator of dropdown field
    # option_name is option which needs to be selected and it is passed from test file
    def select_option_from_dd(self, ddname, option_name,i=0):
            log.info('Dropdown "%s" - select option "%s"' % (ddname, option_name))
            try:
                val = find_elements(self.app.driver,"//*[@id='%s']|//div[@class='%s']|//*[@data-qa-key='%s']" % (ddname, ddname,ddname))
                val[i].click()
            except:
                log.error("unable to look for the dropdown name")
            option = find_elements(self.app.driver,
                                   "//div[contains(@class,'ant-select-dropdown')]//li[text()='%s']|//li[@data-qa-key='%s']" % (option_name,option_name))
            assert len(option) > 0, 'Option %s has not been found' % option_name
            time.sleep(2)
            option[0].click()
            log.info('Clicked on option "%s"' % (option_name))
            time.sleep(3)

    def remove_option_from_dropdown(self, ddname, option_name):
            log.info('Dropdown "%s" - remove option "%s"' % (ddname, option_name))
            x = find_elements(self.app.driver, "//*[@data-qa-key='%s']" % (ddname))
            assert len(x) > 0, 'X has not been found for option {0}'.format(option_name)
            x[0].click()
            time.sleep(1)

    def scroll_to(self, key):
            log.info('Scroll to "%s"' % (key))
            # field = find_elements(self.app.driver, "//*[@data-qa-key='%s']" % key)
            # JS_tricks.inner_scroll_to_element(self.app.driver, field)
            elem = find_element(self.app.driver, "//*[contains(@data-qa-key,'%s')]" % key)
            # JS_tricks.inner_scroll_to_element(self.app.driver, elem)
            JS_tricks.element_to_the_middle(self.app.driver, elem)

    def scroll_to_section(self, text):
            log.info('Scroll to "%s"' % (text))
            element = find_elements(self.app.driver, "//*[text()[contains(.,\"%s\")]]" % text)
            if element:
                print("\n The text %s is displayed on the page" % text)
                # JS_tricks.element_to_the_middle(self.app.driver, element)
                JS_tricks.inner_scroll_to_element(self.app.driver, element)
            else:
                raise Exception("\n The text %s is NOT displayed on the page" % text)
            # element = find_elements(self.app.driver, "//*[text()[contains(.,'%s')]]" % text)
            # field = find_elements(self.app.driver, "//*[@data-qa-key='%s']" % key)
            # JS_tricks.inner_scroll_to_element(self.app.driver, field)
            # elem = find_element(self.app.driver, "//*[contains(@data-qa-key,'%s')]" % text)
            # JS_tricks.inner_scroll_to_element(self.app.driver, elem)

    def click_dropdown(self, idVal, option_name):

        text_val = find_element(self.app.driver, "//*[@id='%s']" % idVal)

        if not text_val:
            log.error('Search field has not been found')
            assert False, 'Search field has not been found'
        else:
            # action = ActionChains(self.app.driver).move_to_element(text_val).click().send_keys(what) \
            #     .send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
            action = ActionChains(self.app.driver).move_to_element(text_val).click().perform()
            time.sleep(5)

        option = find_elements(self.app.driver,
                               "//div[contains(@class,'ant-select-dropdown')][not(contains(@class,'hidden'))]//li[text()='%s']" % option_name)
        assert len(option) > 0, 'Option %s has not been found' % option_name

        option[0].click()

    def click_dropdown_primary_site(self,param= 'Lung'):
        self.click_dropdown("createCase_diagnosis.primarySite", param)

    def click_dropdown_diagnosis_stage(self,param = 'IVB'):
        self.click_dropdown("createCase_diagnosis.stage", param)

    def click_dropdown_diagnosis_hist(self,param = 'Adenocarcinoma in situ'):
        self.click_dropdown("createCase_diagnosis.histology", param)

    def save_case(self,param = 'Save and Close'):
        self.click_btn(param)

    def load_more_btn(self, param='Load More'):
        self.click_btn(param)

    def navigate_to(self, service_name):

        log.info("Navigate to service '%s' " % service_name)
        links = find_elements(self.app.driver, "//div[text()='%s']" % service_name)

        assert len(links) > 0, "Service '%s' has not been found"
        links[0].click()

    def click_dropdown_tableau(self, text):
        element = find_elements(self.app.driver, "//*[contains(text(),'%s')]" % text)
        if not element:
            log.error('Search field has not been found')
            assert False, 'Search field has not been found'
        else:
            # action = ActionChains(self.app.driver).move_to_element(text_val).click().perform()
            element[0].click()
            time.sleep(2)

    def click_tab(self, idVal):
        # click_tab = find_element(self.app.driver, "//*[@id='%s']" % idVal).click()
        # click_tab = find_elements(self.app.driver, "//*[contains(text(),'%s')] % idVal")
        value = find_elements(self.app.driver,"//span[@class='tabLabel' and contains(text(),'%s')]" % idVal)

        value[0].click()

    def click_text(self, textVal):
        # click_tab = find_element(self.app.driver, "//*[@id='%s']" % idVal).click()
        # click_tab = find_elements(self.app.driver, "//*[contains(text(),'%s')] % idVal")
        value = find_element(self.app.driver,
                              "//span[contains(text(),'%s')]" % textVal)

        value.click()
        # find_txt = find_element(self.app.driver, "//*[contains(text(),12)]").send_keys("20")
        # # find_txt.clear()
        # # time.sleep(5)
        # # find_txt.send_keys("20")
        # time.sleep(5)

    def click_text(self, textVal):
        value = find_element(self.app.driver,
                             "//span[contains(text(),'%s')]" % textVal)

        value.click()
        time.sleep(5)
        # text_val = find_elements(self.app.driver, "//*[@id='popup_1']")
        elem =find_element(self.app.driver, "//*[contains(text(),12)]")
        # time.sleep(5)
        # elem.send_keys('20')
        # text_val = find_elements(self.app.driver, self.xpath_textfield_val % idVal)
        # if not text_val:
        #     log.error('Search field has not been found')
        #     assert False, 'Search field has not been found'
        # else:
        #     if len(text_val) > 0:
        #         text_val[0].click()
        #         text_val[0].clear()
        #         text_val[0].send_keys("20")

        #         # text_val[0].send_keys(Keys.RETURN)x
        #         time.sleep(2)
        # elem.clear()
        ActionChains(self.app.driver).move_to_element(elem).click().send_keys('20')
        # action = ActionChains(self.app.driver).move_to_element(elem).click().perform()
        time.sleep(5)

    # purpose - to click on button which is displayed on the page
    # button_name is name of button which user wants to click, it can be pass from test file
    #expected_text is expected text after clicking on the button,it can be pass from test file
    def click_button(self, button_name,expected_text):
        button = find_elements(self.app.driver, self.button_xpath %(button_name,button_name))
        if button :
            log.info('The button %s is displayed on the page', format(button_name))
            try:
                button[0].click()
            except:
                JS_tricks.element_to_the_middle(self.app.driver, button[0])
                JS_tricks.mouse_click_element(self.app.driver, button[0])
                log.info('Button %s has been found & clicked', format(button_name))
            finally:
                WebDriverWait(self.app.driver, 40).until(EC.presence_of_all_elements_located((By.XPATH,self.xpath_contains %expected_text)))
            self.app.verification.text_present_on_page(page_text=expected_text)
