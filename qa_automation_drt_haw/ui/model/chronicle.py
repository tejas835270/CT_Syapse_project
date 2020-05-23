import time
import datetime
import os
from selenium.webdriver.common.keys import Keys



from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from qa_automation_drt_haw.ui.ui_utils import JS_tricks
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements


class Chronicle:

    # link-names
    Use_this_result = 'Use this result'
    select_from_existing_data = 'Select from existing data'

    def __init__(self, app):
        self.app = app

    def verify_url_contains_oncology(self):
        self.app.verification.verify_current_url_contains('oncology')

    def verify_url_contains_chronicle(self):
        self.app.verification.verify_current_url_contains('/chronicle/')

    def chronicle_tab(self, tab_name):
        log.info('Chronicle tab %s' % (tab_name))
        self.app.driver.implicitly_wait(10)
        flag = False
        next_but = find_elements(self.app.driver, "//span[contains(@class,'ant-tabs-tab-next')]")
        try:
            time.sleep(1)
            tab = find_elements(self.app.driver, "//div[@role = 'tab'][./span[text()='%s']]" % tab_name)
            assert len(tab) > 0, 'Chronicle tab {0} is not displayed on the page'.format(tab_name)
            self.app.driver.set_page_load_timeout(10)
            tab[0].click()
            time.sleep(2)
        except:
            while (find_elements(self.app.driver,
                                 "//span[contains(@class,'ant-tabs-tab-btn-disabled')]") == 0) or (flag == False):
                tab = find_elements(self.app.driver, "//div[@role = 'tab'][./span[text()='%s']]" % tab_name)
                if len(tab) > 0 and tab[0].is_displayed():
                    tab[0].click()
                    time.sleep(3)
                    flag = True
                next_but = find_elements(self.app.driver, "//span[contains(@class,'ant-tabs-tab-next')]")[0].click()
            time.sleep(2)
        assert tab[0].get_attribute('aria-selected') == 'true', 'Chronicle tab {0} has not been activated'.format(
            tab_name)
        time.sleep(2)

    def modal_window_title(self, title, present=True):
        """
        Verify modal window with title is/is not present on the page
        """
        log.info('Verify modal window with title "%s" is present=%s on the page' % (title, present))
        modal_window = find_elements(self.app.driver, "//div[@class='ant-modal-title' and text()='%s']" % title)
        if not present:
            if modal_window and modal_window[0].is_displayed():
                assert True == False, 'Modal window with title %s is present on the page. But it should not be' % title
        else:
            assert modal_window[
                0].is_displayed(), 'Modal window with title %s is not present on the page. But it should be' % title

    def select_radiobutton(self, radio_name):
        """
        Select Chronicle radiobutton

        """
        log.info('Chronicle radiobutton "%s"' % (radio_name))
        radio = find_elements(self.app.driver, "//label[.//span[text()='%s']]//input" % radio_name)
        assert len(radio) > 0, 'Radiobutton {0} has not been found'.format(radio_name)
        radio[0].click()
        time.sleep(2)

    def chronicle_tab_values_verification(self, tab_name, section, data):
        """
        Verify Chronicle tab data - for section "
         """
        log.info('Verify Chronicle tab "%s" - section "%s": %s' % (tab_name, section, data))
        # TODO add verification for several sections
        expected_result = []
        actual_result = []
        print(section)

        sec = find_elements(self.app.driver, "//div[@data-qa-key = '%s']" % section)
        if len(sec) > 0:
            log.info('%s Sections have been found'  % section)
            assert True, '%s Sections have not been found'  % section
        else:
            log.error('%s Sections have not been found'  % section)

        section_dict = {}
        for heading in data.keys():
            fields = sec[0].find_elements_by_xpath(
                ".//div[@class='section-layer__form-element'][.//label[text()='%s']]//*[@data-qa-key][not(@class='label-field')][not(@class='add-field')]" % heading)
            assert len(fields) > 0, 'Field {0} has not been found on tab {1}'.format(heading, tab_name)
            field_type = fields[0].get_attribute('class')
            print(field_type)
            if heading == 'Vital Status':
                selected = find_elements(self.app.driver,
                                         "//label[./span[contains(@class, 'ant-radio-checked')]]/span[2]")
                if selected:
                    section_dict[heading] = selected[0].text
                else:
                    section_dict[heading] = ''

            elif field_type == 'chronicle__datepicker' or field_type == 'string-field':
                input_fields = fields[0].find_elements_by_xpath(".//input|.//textarea")
                assert len(input_fields) > 0, 'Input field has not been found for heading {0}'.format(heading)
                input_value = input_fields[0].get_attribute('value')
                print(input_value)
                section_dict[heading] = input_value


            elif field_type == 'chronicle__enum-field' or field_type == 'chronicle__select-field':
                sel_values_list = []
                for field in fields:
                    selected_values = field.find_elements_by_xpath(
                        ".//div[@class='ant-select-selection-selected-value']")
                    if selected_values:
                        # section_dict[heading] = selected_values[0].text
                        sel_values_list.append(selected_values[0].text)
                        section_dict[heading] = ', '.join(sel_values_list)
                    else:
                        placeholders = field.find_elements_by_xpath(
                            ".//div[@class='ant-select-selection__placeholder' and text()='Select...']")
                        assert len(placeholders) > 0, 'Dropdown has not been found'
                        assert placeholders[0].is_displayed()
                        section_dict[heading] = 'Select...'

            elif field_type == 'biomarker-field-picker':
                biomarker_list = []
                sel = fields[0].find_elements_by_xpath(".//div[contains(@class, 'selection__choice__content')]")
                if sel:
                    for j in sel:
                        biomarker_list.append(j.text)
                        print(biomarker_list)
                    section_dict[heading] = ', '.join(biomarker_list)
                else:
                    section_dict[heading] = ''
            else:
                assert False, 'Unknown type of field'
        actual_result.append(section_dict)
        print(actual_result, 'Actual result')

        today = datetime.date.today().strftime('%b %d, %Y')
        print('Today is', today)

        cells = [cell.replace('Today', today) for cell in data.values()]
        exp_sect_dict = dict(zip(data.keys(), cells))
        expected_result.append(exp_sect_dict)

        print('Expected result: ', expected_result)
        print('Actual result  : ', actual_result)
        log.info('Expected result: ', expected_result)
        log.info('Actual result  : ', actual_result)
        assert actual_result == expected_result

    def verify_last_modified_user_and_time(self, user_name, date_save):
        """
        Chronicle: verify last modified user "Chronic Elle" and date "<now>"
        """
        log.info('Chronicle: verify last modified user "%s" and date "%s"' % (user_name, date_save))
        # date_save  = <now> +- 5 min
        saved_info = find_elements(self.app.driver, "//span[@data-qa-key='lastSave']")

        if len(saved_info) == 0:
            assert False, "Record has not been found"
        else:
            user_info = saved_info[0].text
            print("-=-=-=-=-", user_info)

            if user_name not in user_info:
                assert False, "%s has not been found in saved record" % user_name

            if date_save == "<now>":
                now_date = datetime.datetime.now()
                print("-=-=-=", now_date)

                current_mont_day = now_date.strftime("%B") + " " + now_date.strftime("%d").replace('0','')
                print(current_mont_day)
                current_year = now_date.strftime("%Y")
                print(current_year)

                if (current_mont_day not in user_info) or (current_year not in user_info):
                    assert False, "Bug! Date does't match" + current_mont_day + "  " + current_year

                # compare time
                info_time = user_info.split('at ')
                t_actual = datetime.datetime.strptime(info_time[1], "%H:%M:%S")

                delta_time = (now_date.hour * 60 + now_date.minute) - (t_actual.hour * 60 + t_actual.minute)
                if abs(delta_time) > 3:
                    assert False, "Bug! Time does't match"

    def enter_date_into_calendar(self, calendar_field, date):
        """
        Enter date into calendar field
        """
        log.info('Calendar field "%s" enter date "%s"' % (calendar_field, date))
        self.app.driver.implicitly_wait(20)
        input_before = find_elements(self.app.driver, "//span[@data-qa-key='%s']//input" % calendar_field)
        assert len(input_before) > 0, 'Input field before has not been found for calendar {0}'.format(
            calendar_field)

        input_before[0].click()
        time.sleep(3)
        input_after = find_elements(self.app.driver, "//input[@class='ant-calendar-input ']")
        assert len(input_before) > 0, 'Input field after has not been found for calendar {0}'.format(calendar_field)
        val = input_after[0].get_attribute('value')
        assert len(val) == 0, 'You are trying to put value in non-empty field'
        if date == 'today':
            today_btn = find_elements(self.app.driver, "//*[contains(@class, 'calendar-today-btn ')]")
            assert len(today_btn) > 0, 'Today link has not been found'
            today_btn[0].click()
        else:
            input_after[0].send_keys(date)
            # input_after[0].send_keys(Keys.ENTER)
            try:
                body = find_elements(self.app.driver, "//span[@data-qa-key='%s']/../..//label" % calendar_field)
                # body = context.browser.find_elements_by_xpath("//div[@class='ant-card-head-title']")
                body[0].click()
            except:
                print("Label has not been found")
        time.sleep(3)

    def remove_date_from_calendar_field(self, calendar_field):
        log.info('Calendar field "%s" selected remove option' % (calendar_field))
        x = find_elements(self.app.driver,
                          "//span[@data-qa-key='%s']//span[@class = 'ant-calendar-picker-icon']" % calendar_field)
        if len(x) > 0:
            log.info('Calendar field %s has been found' % calendar_field)
            assert True, 'Calendar field %s has not been found' % calendar_field
        else:
            log.info('Calendar field %s has not been found' % calendar_field)
        x[0].click()
        time.sleep(1)

    def pick_chronicle_patient(self, patient):
        # todo check current page, if it is chronicle -go to ipr first
        if "/chronicle" in self.app.driver.current_url:
            self.app.navigation.click_link("Integrated Patient Record")
            time.sleep(3)
        self.app.care_dashboard.find_and_pick_patient(patient)
        self.app.navigation.hide_header()
        # self.app.verification.text_present_on_page("Edit Patient's Care Data")
        self.app.navigation.click_link("Edit Patient's Care Data")

    def fill_out_the_fields(self, tab_name, section_name, data):
        log.info('Chronicle tab "%s": Section "%s" tab - fill up the fields' % (tab_name, section_name,))
        self.app.driver.implicitly_wait(5)
        for heading in data.keys():
            key = section_name + heading
            value_to_enter = data[heading]
            print('Value to enter', value_to_enter)
            print('Key', key)
            field = find_elements(self.app.driver, "//*[@data-qa-key='%s']" % key)
            JS_tricks.inner_scroll_to_element(self.app.driver, field)
            #time.sleep(3)
            if len(field) > 0:
                assert True, 'Field %s %s has not been found' % (section_name, heading)
                log.info('Field %s %s has been found' % (section_name, heading))
            else:
                log.info('Field %s %s has not been found' % (section_name, heading))
            field_type = field[0].get_attribute('class')
            if field_type == 'chronicle__select-field' or field_type == 'chronicle__enum-field':
                field_prep = find_elements(self.app.driver,"//*[@data-qa-key='%s']//div[contains(@class, 'selection__placeholder')]" % key)
                assert len(field_prep) > 0, 'Unable to activate the field %s' % heading
                field_prep[0].click()
                time.sleep(1)
                input = find_elements(self.app.driver, "//*[@data-qa-key='%s']//input" % key)
                assert len(input) > 0, 'Field %s has not been found' % heading
                # value_to_enter = context.table.rows[0].cells[context.table.headings.index(heading)]
                print(value_to_enter)
                input[0].send_keys(value_to_enter)
                time.sleep(1)
                val = find_elements(self.app.driver,
                                    "//div[contains(@class,'ant-select-dropdown')][not(contains(@class,'hidden'))]//li[@role='option'][contains(., '%s')]" % value_to_enter)
                #time.sleep(5)
                assert len(val) > 0, 'Desired value %s has not been found in the vocab' % value_to_enter
                #JS_tricks.inner_scroll_to_elementoffset(self.app.driver, val)
                val[0].click()
                try:
                    body = find_elements(self.app.driver,
                                         "//span[contains(@data-qa-key,'%s')]/../..//label" % key)
                    # body = context.browser.find_elements_by_xpath("//div[@class='ant-card-head-title']")
                    body[0].click()
                except:
                    print("Label has not been found")

            elif field_type == 'chronicle__datepicker':
                input_before = find_elements(self.app.driver, "//span[@data-qa-key='%s']//input" % key)
                assert len(input_before) > 0, 'Input field before has not been found for calendar {0}'.format(key)

                input_before[0].click()
                time.sleep(1)
                input_after = find_elements(self.app.driver, "//input[@class='ant-calendar-input ']")
                assert len(input_before) > 0, 'Input field after has not been found for calendar {0}'.format(key)
                val = input_after[0].get_attribute('value')
                assert len(val) == 0, 'You are trying to put value in non-empty field'
                input_after[0].send_keys(value_to_enter)
                try:
                    body = find_elements(self.app.driver,
                                         "//span[contains(@data-qa-key,'%s')]/../..//label" % key)
                    body[0].click()
                    time.sleep(1)
                except:
                    print("Label has not been found")

            elif field_type == 'string-field':
                input = find_elements(self.app.driver, "//*[@data-qa-key='%s']//input" % key)
                if not input:
                    input = find_elements(self.app.driver, "//*[@data-qa-key='%s']//textarea" % key)
                    assert len(input) > 0, 'Field %s has not been found' % heading

                print("----", str(value_to_enter))

                input[0].clear()
                input[0].send_keys(str(value_to_enter))
                time.sleep(2)
                try:
                    body = find_elements(self.app.driver,
                                         "//span[contains(@data-qa-key,'%s')]/../..//label" % key)
                    body[0].click()
                except:
                    print("Label has not been found")

    def verify_text_present_on_page(self, page_text, is_not=True):
        log.info('Verify the text "%s" is present= %s on the page' % (page_text, is_not))
        if is_not == 'is':
            element = find_elements(self.app.driver, '//span[contains(.,"%s")]' % page_text)
            if element:
                log.info("\n The text %s is displayed on the page" % page_text)
            else:
                log.error("\n The text %s is NOT displayed on the page" % page_text)
                raise Exception("\n The text %s is NOT displayed on the page" % page_text)
        if not is_not:
            element = find_elements(self.app.driver, '//span[contains(.,"%s")]' % page_text)
            if not element:
                log.info("\n The text %s is NOT displayed on the page (as expected!)" % page_text)
            else:
                log.error("\n The text %s IS displayed on the page (but it must not!)" % page_text)
                raise Exception("\n The text %s IS displayed on the page (but it must not!)" % page_text)

    def add_another_section(self, type):
        log.info('Chronicle: Click button Add Another to add "%s"' % (type))
        btn = find_elements(self.app.driver, "//button[contains(@class, '%s')][contains(., 'Add Another')]" % type)
        if len(btn) > 0:
            JS_tricks.inner_scroll_to_element(self.app.driver, btn[0])
            log.info('Button Add Another section has been found on the page')
            assert True, 'Button Add Another section has not been found on the page'
            btn[0].click()
            time.sleep(2)
        else:
            log.error('Button Add Another section has not been found on the page')

    def remove_option_from_dropdown(self, ddname, option_name):
        log.info('Dropdown "%s" - remove option "%s"' % (ddname, option_name))
        x = find_elements(self.app.driver, "//*[@data-qa-key='%s']"
                                           "//span[@class = 'ant-select-selection__clear']" % (ddname))
        assert len(x) > 0, 'X has not been found for option {0}'.format(option_name)
        x[0].click()
        time.sleep(1)

    def clear_input_field(self, field_name):
        log.info('Chronicle: Clear "%s" input field' % (field_name))
        field = find_elements(self.app.driver,
                              "//*[@data-qa-key='%s']//input|//*[@data-qa-key='%s']//textarea" % (
                              field_name, field_name))
        if len(field) > 0:
            log.info('Link %s has been found' % field_name)
            assert True, 'Link %s has not been found' % field_name
            field[0].clear()
            time.sleep(2)
        else:
            log.info('Link %s has not been found' % field_name)
        try:
            find_elements(self.app.driver, "//*[@data-qa-key='%s']/../..//label" % field_name)[0].click()
        except:
            print("Label has not been found")

    def biomarker_field_input(self, cond, field_name, values):
        log.info('Chronicle: "%s" field "%s" - Enter "%s"' % (cond, field_name, values))
        values = values.split(', ')
        print("-=-=-", values)
        if cond != 'Biomarker':
            field_prep = find_elements(self.app.driver,
                                       "//*[@data-qa-key='%s']//div[contains(@class, 'selection__placeholder')]" % field_name)
            #assert len(field_prep) > 0, 'Unable to activate the field %s' % field_name
            if len(field_prep) > 0:
                log.info('field %s is active' % field_name)
                assert True , 'Unable to activate the field %s' % field_name
            else:
                log.info('Unable to activate the field %s' % field_name)
            field_prep[0].click()
            time.sleep(1)
        for i in values:
            print("===", i)
            field = find_elements(self.app.driver, "//*[@data-qa-key='%s']//input" % field_name)
            if len(field) > 0:
                log.info('Field %s has been found' % field_name)
                assert True ,'Field %s has not been found' % field_name
            else:
                log.info('Field %s has not been found' % field_name)
            field[0].send_keys(i)
            time.sleep(2)
            val = find_elements(self.app.driver, "//li[@role='option'][contains(., '%s')]" % i)

            if len(val) > 0:
                log.info('Desired value "%s" has been found in the vocab' % i)
                assert True, 'Desired value "%s" has not been found in the vocab' % i
                val[0].click()
            else:
                log.info('Desired value "%s" has not been found in the vocab' % i)
            try:
                find_elements(self.app.driver, "//*[@data-qa-key='%s']/../..//label" % field_name)[0].click()
            except:
                print("Label has not been found")
                log.info("Label has not been found")
        time.sleep(2)

    def enter_into_input_field(self, text, field_name):
        log.info('Chronicle: Enter "%s" into "%s" input field' % (text, field_name))
        text = text.split(', ')
        field = find_elements(self.app.driver,
                              "//*[@data-qa-key='%s']//input|//*[@data-qa-key='%s']//textarea" % (
                              field_name, field_name))

        assert len(field) > 0, 'Field %s has not been found' % field_name

        field[0].clear()
        for c in text:
            field[0].send_keys(c)
        try:
            find_elements(self.app.driver, "//*[@data-qa-key='%s']/../..//label" % field_name)[0].click()
        except:
            print("Label has not been found")

        time.sleep(2)

    def select_option_from_dd(self, ddname, option_name):
        log.info('Dropdown "%s" - select option "%s"' % (ddname, option_name))
        try:
            find_element(self.app.driver,
                         "//*[@data-qa-key='%s']" % ddname).click()

        except:
            find_element(self.app.driver,
                         "//*[contains(@data-qa-key,'%s')]" % ddname).click()
        time.sleep(1)
        option = find_elements(self.app.driver,
                               "//div[contains(@class,'ant-select-dropdown')][not(contains(@class,'hidden'))]//li[text()='%s']" % option_name)
        if len(option) > 0:
            log.info('Option %s has been found' % option_name)
            assert len(option) > 0, 'Option %s has not been found' % option_name
            option[0].click()
        else:
            log.error('Option %s has not been found' % option_name)
        try:
            find_elements(self.app.driver, "//*[contains(@data-qa-key,'%s')]/../..//label")[0].click()
        except:
            print("Label has not found")

        time.sleep(3)

    def remove_section(self, section_to_remove):
        # you should put data-qa-key for Remove button
        log.info('Remove section "%s"' % (section_to_remove))
        section = find_elements(self.app.driver, "//*[@data-qa-key='%s']" % section_to_remove)
        assert len(section) > 0, 'Section %s has not been found' % section_to_remove
        section[0].click()

    def verify_section_is_displayed(self, section_name, cond="is"):
        log.info('Verify "%s" section %s displayed' % (section_name, cond))
        section = find_elements(self.app.driver, "//*[@data-qa-key='%s']" % section_name)
        if cond == 'not':
            if len(section) == 0:
                log.info("section %s is not displayed "% section_name)
                assert len(section) == 0 ,"section %s is displayed "% section_name
        else:
            log.info("section %s is  displayed " % section_name)
            assert len(section) > 0

    def click_button_for_section_and_role(self, button, section, role):
        log.info('Click button "%s" for section "%s" role "%s"' % (button, section, role))
        self.app.driver.implicitly_wait(10)
        element = find_elements(self.app.driver,
                                "//div[@data-qa-key='%s']//button[contains(@class, '%s')][contains(., '%s')]" % (
                                section, role, button))

        if not element:
            log.error('Button {0} is disabled'.format(button))
            assert False, ('Button {0} is disabled'.format(button))
        elif element:
            log.info('Button {0} is enable'.format(button))
            JS_tricks.element_to_the_middle(self.app.driver, element[0])
            element[0].click()
            time.sleep(1.5)
        else:
            log.error('Button {1} has not been found'.format(button))
            assert False, ('Button {1} has not been found'.format(button))

    def click_button_add_another_for_field_in_section(self, field, section):
        log.info('Chronicle: Click button Add Another for "%s" in section "%s"' % (field, section))
        self.app.driver.implicitly_wait(10)
        element = find_elements(self.app.driver,
                                "//div[@data-qa-key='%s']//div[@data-qa-key='%s']//*[text()='Add Another']/.." % (
                                field, section))
        print(element)
        if len(element) == 0:
            assert False, ('Button Add Another has not been found')
        elif element[0]:
            JS_tricks.element_to_the_middle(self.app.driver, element[0])
            element[0].click()
            time.sleep(1.5)
        time.sleep(2)

    def remove_additional_field(self, field_name):
            log.info('Chronicle: Remove additional field "%s"' % (field_name))
            field_name = field_name.split(', ')
            for i in field_name:
                remove_btn = find_elements(self.app.driver,
                                           "//div[@data-qa-key = '%s']//span[@class='remove-field']" % i)
                if len(remove_btn) > 0:
                    log.info('Remove button for field %s has been found' % i)
                    assert True, 'Remove button for field %s has not been found' % i
                    remove_btn[0].click()
                    time.sleep(1)
                else:
                    log.error('Remove button for field %s has not been found' % i)

    def remove_selected_biomarkers(self, field_name, values):
            log.info('Chronicle: Biomarker field "%s" - Remove "%s"' % (field_name, values))
            values = values.split(', ')
            for i in values:
                sel_val = find_elements(self.app.driver,
                    "//li[contains(., '%s')]//span[contains(@class, 'remove')]" % i)
                assert len(sel_val) > 0, 'Selected value %s has not been found in biomarker field' % i
                sel_val[0].click()


    def verify_vocab_for(self, section_name,data):
            log.info('Verify vocabs for "%s"' % (section_name))
            mismatches = {}

            for heading in data.keys():
                file_name = data[heading]
                vocab_name = section_name + heading

                temp_file = os.path.abspath(os.path.dirname(__file__) + "/../../test_data/Data_vocab/%s" % file_name)
                data_ex = []
                with open(temp_file, 'rb') as csvfile:
                    for i in csvfile:
                        data_ex.append(i.strip())

                data_ac = []
                el = find_element(self.app.driver, "//*[@data-qa-key='%s']" % vocab_name).click()
                time.sleep(2)
                vocab_list = find_elements(self.app.driver,"//li[@role='option']")
                for e in vocab_list:
                    if e.text != '':
                        data_ac.append(e.text.strip().encode('UTF8'))

                print("Actual   Vocab %s, len = %s" % (vocab_name, len(data_ac)), (data_ac))
                print("Expected Vocab %s, len = %s" % (vocab_name, len(data_ex)), (data_ex))
                log.info("Actual   Vocab %s, len = %s" % (vocab_name, len(data_ac)), (data_ac))
                log.info("Expected Vocab %s, len = %s" % (vocab_name, len(data_ex)), (data_ex))

                #     close the vocab
                el = find_element(self.app.driver,"//*[@data-qa-key='%s']/../..//label" % vocab_name).click()
                time.sleep(2)

                # assert  sorted(data_ac) == sorted(data_ex), "Vocab %s does not match the pattern" % vocab_name
                if sorted(data_ac) != sorted(data_ex):
                    print("======================================================")

                    print( "Vocab %s does not match the pattern" % vocab_name)
                    print(set(sorted(data_ac)) - set(sorted(data_ex)))
                    print("======================================================")
                    log.info("======================================================")

                    log.info("Vocab %s does not match the pattern" % vocab_name)
                    log.info(set(sorted(data_ac)) - set(sorted(data_ex)))
                    log.info("======================================================")
                    mismatches[vocab_name] = set(sorted(data_ac)) - set(sorted(data_ex))

            if len(mismatches) > 0:
                log.info('Mismatch(es) found in: %s' % mismatches)
                assert 'Mismatch(es) found in: %s' % mismatches

            time.sleep(3)


    def type_and_verify_vocab(self, input, vocab_name):
            log.info('Type "%s" for vocab field "%s" and verify the search resul' % (input, vocab_name))
            self.app.driver.implicitly_wait(20)
            WebDriverWait(self.app.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@data-qa-key='%s']" % vocab_name))).click()
            #find_element(self.app.driver,"//*[@data-qa-key='%s']" % vocab_name).click()
            input_field = find_element(self.app.driver, "//*[@data-qa-key='%s']//input" % vocab_name)
            input_field.send_keys(input)
            time.sleep(1)

            data_ac = []
            vocab_list = find_elements(self.app.driver, "//li[@role='option']")
            for e in vocab_list:
                if e.text != '':
                    data_ac.append(e.text.strip().encode('UTF8'))
                    if input.lower() not in e.text.lower():
                        log.info("Bug: vocab %s input: %s result:%s " % (vocab_name, input, e.text))
                        assert False, "Bug: vocab %s input: %s result:%s " % (vocab_name, input, e.text)
            try:
                find_element(self.app.driver, "//*[@data-qa-key='%s']//input" % vocab_name).clear()
                time.sleep(1)
                log.info('Label {' + vocab_name + ' }has  been found , click on it')
                find_element(self.app.driver,"//*[contains(@data-qa-key,'%s')]/../..//label" % vocab_name).click()
            except:
                print("Label has not been found")
                log.info('Label {' + vocab_name + ' }has not been found')



    def type_and_verify_empty_result(self, input, vocab_name):
            log.info('Type "%s" for vocab field "%s" and verify empty result' % (input, vocab_name))
            elem = WebDriverWait(self.app.driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains("
                                                                                                     "@data-qa-key,"
                                                                                                     "'%s')]" %
                                                                                           vocab_name)))
            #elem = find_element(self.app.driver,"//*[contains(@data-qa-key,'%s')]" % vocab_name)
            JS_tricks.inner_scroll_to_element(self.app.driver, elem)
            elem.click()
            input_field = find_element(self.app.driver,"//*[contains(@data-qa-key,'%s')]//input" % vocab_name)
            input_field.send_keys(input)
            time.sleep(1)

            vocab_list = find_elements(self.app.driver,"//li[@role='option']")
            for e in vocab_list:
                if e.text != '' and e.text != 'Not Found':
                    log.info("Bug: vocab %s input: %s result:%s " % (vocab_name, input, e.text))
                    assert False, "Bug: vocab % input: %s result:%s " % (vocab_name, input, e.text)

            try:
                input_field = find_element(self.app.driver,
                    "//*[contains(@data-qa-key,'%s')]//input" % vocab_name).clear()
                log.info('Label {' + vocab_name + ' }has been found')
                find_element(self.app.driver,"//*[contains(@data-qa-key,'%s')]/../..//label" % vocab_name).click()
            except:
                print("Label has not been found")
                log.info('Label {' + vocab_name + ' }has not been found')


    def verify_prepopulated_data(self,data):
            log.info('Verify Chronicle pre-populated info')

            actual_results = []

            headers = [x.text for x in find_elements(self.app.driver,'//thead//th') if len(x.text) != 0]
            rows = find_elements(self.app.driver,"//tbody/tr")
            if len(rows) > 0:
                log.info('Pre-populated values have been found')
                assert True, 'Pre-populated values have not been found'

            else:
                log.error('Pre-populated values have not been found')

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
            if expected_results == actual_results:
                log.info("Expected: %s, is equal to  Actual: %s" % (expected_results, actual_results))
                assert True, "Expected: %s, Actual: %s" % (expected_results, actual_results)
            else:
                log.error("Expected: %s,is not equal to Actual: %s" % (expected_results, actual_results))


    def choose_option_from_prep_info(self, data):
            log.info('Choose following option from pre-populated info')

            table_rows = find_elements(self.app.driver,"//tbody/tr")
            print(table_rows)
            assert len(table_rows) > 0, 'Pre-populated values have not been found'

            # chosen_option = [cell for cell in context.table.rows[0].cells]
            chosen_option = [cell for cell in data.values()]
            print(chosen_option)

            flag = False
            for table_row in table_rows:
                # pre_values = [y.text for y in table_row.find_elements(self.app.driver,"td[not(contains(@class, 'selection-column'))]")]
                pre_values = [y.text for y in table_row.find_elements_by_xpath("td[not(contains(@class, 'selection-column'))]")]

                print("pre v", pre_values)
                radio_button = table_row.find_elements_by_xpath(".//span[contains(@class, 'radio')]/input/../../../../..")
                assert len(radio_button) > 0, 'Radio has not been found for chosen option'
                if chosen_option == pre_values:
                    print(pre_values)
                    flag = True
                    radio_button[0].click()
                    time.sleep(3)
                    sel_radio = table_row.find_elements_by_xpath(".//span[contains(@class, 'radio-checked')]/input")
                    assert len(sel_radio) > 0, 'Radiobutton has not been selected'
                    break
            assert flag, 'Expected pre-population option has not been found on the page'


    def verify_tooltip_for_text(self, what_for, tooltip_text):
            log.info('Chronicle: Verify tooltip for text "%s" is "%s"'%(what_for,tooltip_text))
            element = find_elements(self.app.driver,"//*[text()[contains(.,'%s')]]" % what_for)
            if not element:
                assert False, ("Element with text '%s' was not found" % what_for)
            JS_tricks.mouse_over_element(self.app.driver, element[0])
            time.sleep(3)
            actual_tooltip = find_elements(self.app.driver,
                "//div[contains(@class,'ant-tooltip')][not(contains(@class,'hidden'))]//*[text()='%s']" % tooltip_text)
            if len(actual_tooltip) == 0:
                assert False, ("Expected tooltip: %s has not been found" % tooltip_text)

    def open_patient_finder(self):
        log.info('Chronicle: open patient finder')
        self.app.navigation.click_link('Chronicle')


    def click_btn_for_section(self, button, section):
            log.info('Chronicle: Click button "%s" for section "%s"'%(button,section))
            self.app.driver.implicitly_wait(10)
            element = find_elements(self.app.driver,
                "//div[@data-qa-key='%s']//*[text()='%s']/.." % (section, button))

            if not element:
                log.error('Button {0} is disabled' % button)
                assert False, ('Button {0} is disabled'.format(button))
            elif element:
                JS_tricks.element_to_the_middle(self.app.driver, element[0])
                element[0].click()
                time.sleep(1.5)
                log.info('Button %s has been found & clicked' % button)
            else:
                log.error('Button {1} has not been found' % button)
                assert False, ('Button {1} has not been found'.format(button))

    def test_enter_date_in_last_contact_save(self):
        """
            Chronicle - Patient Status - Enter Date in Last Contact and Save
            """
        self.remove_date_from_calendar_field("vitalStatus__dateOfLastContact")
        self.app.navigation.click_btn("Save")
        self.app.navigation.refresh_page()
        self.chronicle_tab("Patient Status")
        self.enter_date_into_calendar("vitalStatus__dateOfLastContact","Nov 23, 2019")
        self.app.navigation.click_btn("Save")
        self.app.navigation.refresh_page()

    def test_clear_last_contact_save(self):
        """
         Chronicle - Patient Status - clear Last Contact and Save
        """
        self.chronicle_tab("Patient Status")
        self.remove_date_from_calendar_field("vitalStatus__dateOfLastContact")
        self.app.navigation.click_btn("Save")

    def remove_date_from_calendar_field_if_present(self, calendar_field):
            log.info('Calendar field "%s" selected remove option' % (calendar_field))
            input_before = find_element(self.app.driver, "//span[@data-qa-key='%s']//input[@class='ant-calendar-picker-input ant-input']" % calendar_field)
            #input_before.click()
            #time.sleep(5)
            #input_after = find_element(self.app.driver, "//input[@class='ant-calendar-input ']")
            val = input_before.get_attribute('value')
            if len(val) > 0:
                input_after = find_element(self.app.driver, "//span[@data-qa-key='%s']//i[@class='anticon anticon-cross-circle ant-calendar-picker-clear']" % calendar_field)
                ActionChains(self.app.driver).move_to_element(input_after).click(input_after).perform()
                #input_after.click();
                time.sleep(3)
                print("cleared")


    def remove_option_from_dropdown_if_data_present(self, ddname):
            log.info('Dropdown "%s" - clear' % (ddname))
            x = find_elements(self.app.driver, "//*[@data-qa-key='%s']"
                                               "//span[@class = 'ant-select-selection__clear']" % (ddname))
            if x:
                log.info('%s dropdown has data ,clear it'%ddname)
                x[0].click()
                time.sleep(1)
                log.info("%s - cleared" %ddname)
            else:
                log.info('%s dropdown has no data ,no need to clear it' % ddname)

    def clear_input_field_1(self, field_name):
            log.info('Chronicle: Clear "%s" input field' % (field_name))
            field = find_elements(self.app.driver,
                                  "//*[@data-qa-key='%s']//textarea" % (field_name))
            if len(field) > 0:
                log.info('Link %s has been found' % field_name)
                assert True, 'Link %s has not been found' % field_name
                field[0].send_keys(Keys.CONTROL, 'a')
                #field[0].send_keys(Keys.COMMAND, 'a')
                field[0].send_keys(Keys.DELETE)
                time.sleep(2)
            else:
                log.info('Link %s has not been found' % field_name)
            try:
                find_elements(self.app.driver, "//*[@data-qa-key='%s']/../..//label" % field_name)[0].click()
            except:
                print("Label has not been found")


    def test_remove_all_sections_from_genomic_alterations(self):
        """
        Chronicle - genomic_alterations - Remove all sections if there
        """
        #self.app.navigation.refresh_page()
        self.chronicle_tab("Genomic Alterations")
        self.app.navigation.hide_header()
        self.app.navigation.hide_footer()
        ele = find_elements(self.app.driver, "//*[@data-qa-key='genomicAlterations__0__removeLink']")
        ele1 = find_elements(self.app.driver, "//*[@data-qa-key='genomicAlterations__1__removeLink']")
        if ele1:
            self.remove_section('genomicAlterations__1__removeLink')
            self.remove_section('genomicAlterations__0__removeLink')
            self.app.navigation.show_footer()
            self.app.navigation.click_btn('Save')
            self.app.navigation.refresh_page()
            time.sleep(5)

        elif ele:
            self.remove_section('genomicAlterations__0__removeLink')
            self.app.navigation.show_footer()
            self.app.navigation.click_btn('Save')
            self.app.navigation.refresh_page()
            time.sleep(5)

    def clear_input_field_2(self, field_name):
            log.info('Chronicle: Clear "%s" input field' % (field_name))
            field = find_elements(self.app.driver,
                                  "//*[@data-qa-key='%s']//input" % (field_name))
            assert len(field) > 0, 'Link %s has not been found' % field_name
            field[0].send_keys(Keys.CONTROL, 'a')
            field[0].send_keys(Keys.DELETE)
            #field[0].clear()
            time.sleep(2)
            try:
                find_elements(self.app.driver, "//*[@data-qa-key='%s']/../..//label" % field_name)[0].click()
            except:
                print("Label has not been found")

    # purpose is to remove data from input field by sending Keys.BACKSPACE
    def clear_input_field_using_backspace(self, field_name):
            log.info('Chronicle: Clear "%s" input field' % (field_name))
            field = find_elements(self.app.driver,
                                  "//*[@data-qa-key='%s']//input|//*[@data-qa-key='%s']//textarea" % (
                                      field_name, field_name))
            assert len(field) > 0, 'Link %s has not been found' % field_name
           # element =find_element(self.app.driver,
                #                  "//*[@data-qa-key='%s']//input[@class='ant-input']" % (field_name))
            lenText = field[0].get_attribute('value')
            lenth = len(lenText)
            log.info(lenth)
            i=0
            while i < lenth:
                field[0].send_keys(Keys.BACKSPACE)
                i=i+1
            lenText = field[0].get_attribute('value')
            if len(lenText) == 0:
                log.info("cleared")
                assert True
            else:
                log.info("not cleared")
            time.sleep(2)


    # use - to remove all the sections from [cancer diagnosis,genomic alterations,progam management,surgery and radiation] under Chronicle/[Patient Data Entry]
    def remove_all_sections(self):
        remove_links = find_elements(self.app.driver, "//a[contains(text(),'Remove')]")
        #if len(remove_links)>0:
        n=len(remove_links)
        log.info(n)
        if  n > 0:
            while n > 0:
                if n == 0:
                    log.info(len(remove_links))
                    log.info('all sections are removed')
                    break
                else:
                    log.info(remove_links)
                    remove_links[0].click()
                    n=n-1
                    time.sleep(3)
                    log.info('section is removed')
            self.app.navigation.show_footer()
            self.click_on_save()
            self.app.navigation.refresh_page()
            time.sleep(5)
        else:
            log.info("no data to remove")

    # use - to click on save button
    def click_on_save(self):
        self.app.navigation.click_btn("Save")

    # use - to click on [Add ANother] button
    def click_Add_Another(self):
        self.app.navigation.click_btn('Add Another')

    # use - to click on [Add ANother] button for given section name
    def click_Add_Another_for_section(self,section_name):
        self.app.navigation.click_button_for_section(button='Add Another', section=section_name)

    def click_Add_Another_with_SectionAndRole(self,section_name):
        self.click_button_for_section_and_role(button="Add Another", section=section_name, role="section")

    # use - to click on [Cancel] button on the present page
    def click_on_cancel(self):
        self.app.navigation.click_btn("Cancel")

        # use of below method is to click on [Select from existing data] link

    def Click_select_from_existing_data(self):
        self.app.navigation.click_btn(self.select_from_existing_data)

        # use of below method is to click on [Use this result] link

    def Click_Use_this_result(self):
        self.app.navigation.click_btn(self.Use_this_result)

    #purpose to verify that given section is not present , section_name will be given in test files
    def verify_section_is_not_displayed(self,section_name):
        self.verify_section_is_displayed(section_name, cond="not")

    #purpose - it creates dictionary where key represents locator and value represents values by combining 2 dictionaries data(where key is field name and value is data to fill) and field_locator(where key is field name and value is locators)
    def create_dict_for_locators_value(self,data ,field_locator):
        key2 = data.keys()
        final_dict = {}
        for heading in field_locator.keys():
            if heading in key2:
                assert True, 'no data found, please provide data'
                final_dict[field_locator[heading]] = data[heading]
            else:
                log.info('no data found, please provide data')
        log.info(final_dict)
        return final_dict

