import time
import datetime
import os

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from qa_automation_drt_haw.ui.ui_utils import JS_tricks
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import *
from qa_automation_drt_haw.ui.model.verification import GeneralVerification as GV

class Mtb_Create_Case_page:
    # locators element present on [create new case] page
    xpath_textfield_val = "//input[@id='%s']"
    xpath_textarea_val = "//textarea[@id='%s']"
    xpath_textarea_data_key = "//textarea[@data-qa-key='%s']"
    continue_popup_locator = "//button[@data-qa-key='continue']"
    select_btn_field = "//*[contains(text(),'Select')]"
    value_field = "//*[@data-row-key='%s']"
    xpath_data_test = "//span[@data-test='%s']"
    case_id_locator = "//div[@class='mtb-case-header']//div[@class='ant-card-head-title']"
    Meeting_Date = 'createCase_meetingDate'
    Diagnosis_Date = 'createCase_diagnosisDate'
    Primary_Oncologist = 'createCase_mtbMeetingInfo.primaryOncologist'
    primary_oncologist_before_textbox = "//*[@data-qa-key='createCase_physician_display']"
    Primary_Site = 'createCase_diagnosis.primarySite'
    Meeting_summary = 'meeting_summary'
    Recommendations_Summary = 'createCase_recommendationsSummary'
    primary_site_class = 'ant-modal dropdown-modal primarySiteModal'
    histology_class = 'ant-modal dropdown-modal histologyModal'
    primary_site_data_test = 'primarySitesButton'
    histology_data_test = 'histologiesButton'
    caseNarrative_field = 'createCase_caseNarrative'
    stage_group_field = 'createCase_diagnosis.stage'
    cancel_btn_on_popup_locator = "//button[@data-qa-key='cancel']"
    oncologist_none = "//textarea[@data-qa-key='createCase_physician_view']"
    caseNarrative_none = "//*[@class='case-narrative']//textarea|//div[@data-qa-key='case_narrative_display']"
    meeting_none = "//*[@class='meeting-summary']//textarea|//div[@data-qa-key='meeting_summary_display']"
    special_char_error = "//*[contains(text(),'The field must not contain the following special characters: ~ ` @ # $ ^ { } |')]"
    sex_value = "//*[@id=\"id-1-1\"]//tr[%s]/td[%s]"
    caseNarrative_field_error = '''//div[contains(text(),"Case Narrative must not contain the following special characters: ~ `")]'''
    meeting_notes_field_error = '''//div[contains(text(),"Meeting Notes must not contain the following special characters: ~ `")]'''
    meeting_notes_button = '''//ul[@data-qa-key='meta']//span[contains(text(),'Meeting Notes')]'''
    meeting_notes_close = '''//ul[@data-qa-key='meta']//span[contains(text(),'Close Meeting Notes')]'''
    meeting_notes_none = "//div[@class='meeting-notes']//textarea"
    meeting_notes_text_area = "createCase_meetingNotes.note"  # "//div[@class='meeting-notes']//textarea[@data-qa-key='meeting_notes_edit']"
    meeting_notes_display_area = "//div[@data-qa-key='meeting_notes_display']/."
    meeting_notes_view = "//*[@data-qa-key='meeting_notes_view']"
    case_narrative='createCase_caseNarrative'
    primary_Sites_Value='primarySitesValue'
    histologies_Value='histologiesValue'
    stage_group="//div[@data-qa-key='createCase_cancerStagingGroups']//div[@class='ant-select-selection-selected-value']"
    notes_ = "//*[@data-qa-key='Recommendation_0']//textarea|//*[@data-qa-key='editableTable_notes_edit']|//*[@data-qa-key='editableTable_notes_view']"
    notes_display="//*[@data-qa-key='editableTable_notes_display']"
    notes_edit="editableTable_notes_edit"
    cases_table = "//tbody/tr"
    current_page_number = "//li[contains(@class,'ant-pagination-item-active')]"
    next_page_btn = "//i[contains(@class,'anticon-right')]"
    previous_page_btn = "//i[contains(@class,'anticon-left')]"
    meeting_date_header = "//th[contains(@class,'sort-meeting-date')]"
    case_id_header = "//th[contains(@class,'sort-case-id')]"
    diagnosis_header = "//th[contains(@class,'sort-diagnosis')]"
    sorting_enabled = "//i[contains(@class,' on')]"
    current_sorting_applied = ""
    save_success_notification = "//div[contains(@class,'notification-topRight')]//i[contains(@class,'notice-icon-success')]"
    report_success_msg = "//i[@class='anticon anticon-check-circle']"
    recommendation_remove_xpath="//*[@data-qa-key='editableTable_remove_btn']"
    total_recommendation="//*[contains(@data-qa-key,'Recommendation_')]"
    none_provided = "//div[@class='case-narrative']//*[contains(text(),'None provided')]"
    xpath_cases_table = "//td[@class='data-qa-key-sort-case-id ant-table-column-has-actions ant-table-column-has-sorters']"
    primary_onco = 'createCase_mtbMeetingInfo.primaryOncologist'
    recommendation_notes = "//div[@class='ant-form-item-control']//span[@class='ant-form-item-children']"
    recommendation_text_area_data_key = 'editableTable_notes_edit'
    auto_reports = '//div[@class=\'outer-row\']'
    refresh_icon = '//*[@class=\'anticon anticon-sync auto-populated-sync-icon\']'
    recommendation_summary_field = '//div[@data-qa-key=\'meeting_summary_display\']/.'
    MTB_page_component = "//header[@class='ant-layout-header' and @data-qa-key='syapsePageTitle']"
    # locators of element present under recommendations section on [create new case] page
    recommendation_type_class='data-qa-key-recs-type ant-select ant-select-enabled'
    description_id='recommendationDescription'
    notes_id_edit = "editableTable_notes_edit"
    notes_id_verify = "editableTable_notes_display"
    add_recommendation='editable_footer_add'
    save_and_close_data_qa_key='caseform_footer_save_and_close_btn'
    save_data_qa_key='caseform_footer_save_btn'
    treatment_1='treatment_1'
    genetic_2='genetic_2'
    molecular_3='molecular_3'
    other_4='other_4'


    # expected text which should be present on [create new case] page
    cancel_btn = 'Cancel'
    Recommendations_Summary_text = 'Recommendations Summary'
    Recommendations_text = 'Recommendations'
    none_provided_text = 'None provided'
    add_recommendation_text = 'Add Recommendation'
    recommendation_type = 'Recommendation Type'
    description = 'Description'
    relevant_biomarkers = 'Relevant Biomarkers'
    notes = 'Notes'
    remove = 'Remove'
    add_link = 'Add'
    mtb_case_management = 'MTB Case Management'
    SaveAndClose = "Save and Close"
    save = 'Save'
    case_updated = 'Case Updated Successfully'
    close_meeting_notes = "Close Meeting Notes"
    open_meeting_notes = "Open Meeting Notes"
    search_error = 'Search must be at least 3 characters'
    meeting_notes_updated_text = "Last updated by"
    # error messages
    description_required_error = 'Description is required'
    type_required_error = 'Recommendation Type is required'

    # TO initialize
    def __init__(self, app):
        self.app = app

    # purpose-pick and store the case id in case_id parameter from [create case] page
    def pick_up_case_ID(self):
        log.info('pick up the case id which is present at the top on [create new case] page')
        element = find_element(self.app.driver, "//div[@class='mtb-case-header']//div[@class='ant-card-head-title']")
        if element:
            assert True, ('Element not found')
        value = element.text
        case_id = value[5:20]
        log.info('picked up the case id- %s' % case_id)
        return case_id

    # purpose-verify the header_mrn on the [create case] page
    # where data for param is passsed from test file
    def verify_mrn_present_in_deidentified_header(self, param):
        log.info('verify the last 4 digit of mrn are present into the case id')
        self.app.verification.verify_partial_text(param)

    # purpose-Enter date in [meeting_date] field on [create case] page
    # where date is passsed from test file and Meeting_Date is the locator of [meeting_date] field which is defined at the top
    def enter_meeting_date(self, date):
        self.app.navigation.enter_date_in_calendar(self.Meeting_Date, date)

    # purpose-Enter date in [diagnosis_date] field on [create case] page
    # where date is passsed from test file and Diagnosis_Date is the locator of [diagnosis_date] field which is defined at the top
    def enter_diagnosis_date(self, date):
        self.app.navigation.enter_date_in_calendar(self.Diagnosis_Date, date)

    # purpose-Enter data in [primary_oncologist] field on [create case] page
    # where 'data' is passsed from test file and Primary_Oncologist is the locator of [Primary_Oncologist] field which is defined at the top
    def enter_primary_oncologist(self, data):
        try:
            self.click_on_to_enable_text(ele_xpath=self.oncologist_none)
            self.text_area_enter(data, self.Primary_Oncologist)
        except:
            self.text_area_enter(data, self.Primary_Oncologist)

    # purpose-select data from [Stage_Group] dropdown on [create case] page
    # where 'option_name' is passsed from test file and diagnosis_stage is the locator of [diagnosis_stage] d/d which is defined at the top
    def select_option_from_Stage_Group_dd(self, option_name):
        self.app.navigation.select_option_from_dd(self.stage_group_field, option_name)
        time.sleep(1)

    # purpose-to scroll to [Meeting_summary] field on [create case] page
    # Meeting_summary is the locator which is defined at the top
    def scroll_to_meeting_summary(self):
        self.app.navigation.scroll_to(self.Meeting_summary)

    # purpose-to enter data(what) in the textarea field(idVal)
    # idVal is locator which is defined at the top
    # what is data , passed from test file
    def text_area_enter(self, what, idVal):
        log.info('Enter some data in text field "%s"' % (idVal))
        text_val = find_elements(self.app.driver, self.xpath_textarea_val % idVal)
        if not text_val:
            log.error('Search field has not been found')
            assert False, ('Search field has not been found')
        else:
            # text_val[0].clear()
            self.app.mtb.clear_input_field_using_backspace(field_name=idVal)
            text_val[0].send_keys(what)
            log.info('data is entered in text field "%s"' % (idVal))

    # purpose-Enter data in [recommendationsSummary] field on [create case] page
    # where data for 'what' is passsed from test file and Recommendations_Summary is the locator of [Recommendations_Summary] field which is defined at the top
    def enter_text_in_recommendationsSummary(self, what):
        try:
            WebDriverWait(self.app.driver, 3).until(EC.presence_of_element_located, self.meeting_none)
            self.click_on_to_enable_text(ele_xpath=self.meeting_none)
            self.text_area_enter(what, self.Recommendations_Summary)
        except:
            self.text_area_enter(what, self.Recommendations_Summary)

    # purpose-Enter data in [case Narrative] field on [create case] page
    # where data for 'what' is passsed from test file and caseNarrative_field is the locator of [Recommendations_Summary] field which is defined at the top
    def enter_text_in_caseNarrative(self, what):
        try:
            WebDriverWait(self.app.driver, 3).until(EC.presence_of_element_located, self.caseNarrative_none)
            self.click_on_to_enable_text(ele_xpath=self.caseNarrative_none)
            self.text_area_enter(what, self.caseNarrative_field)
        except:
            self.text_area_enter(what, self.caseNarrative_field)

    def enter_text_in_recommendation_notes_and_verify_field_height_increases(self, what):
        """
        This function enters the text in the Recommendation Notes
        It verify the field height if is single line
        When text gets entered, it will verify if the field height get increased
        If more than 5 new lines are entered in text box,scroll bar will be visible
        """
        try:
            notes = find_elements(self.app.driver, self.recommendation_notes)
            if len(notes) > 0:
                ActionChains(self.app.driver).double_click(notes[9]).click(notes[9]).perform()
                text = find_element(self.app.driver,
                                    self.xpath_textarea_data_key % self.recommendation_text_area_data_key)
                log.info("Initially the field is empty so it is a single line height")
                text.send_keys(what)
                text_after_value = text.text
                if '\n' in text_after_value:
                    log.info("Recommendation Notes Field Height has Increased")
                    count = text_after_value.count('\n')
                    if int(count) == 6: log.info("Scroll bar is available")
                else:
                    log.info("Recommendation Notes Field is still single line height")
            outside = find_elements(self.app.driver, "//div[@class='ant-card-body']")
            outside[0].click()
        except:
            self.text_area_enter(what, self.recommendation_notes)

    # purpose- to click on [save and close] button
    def click_on_save_and_close(self):
        self.app.navigation.click_btn("Save and Close")

    def save_case(self):
        '''
        :purpose: This method is used to click on save button and stay on case page itself.
        :return: Nothing
        '''
        self.app.navigation.click_btn("Save")
        log.info("Clicked on Save")
        self.verify_success_notification_after_case_saved()

    # purpose-to verify the data of [recommendationsSummary] field on [create case] page
    # where data for 'data' is passsed from test file and Recommendations_Summary is the locator of [Recommendations_Summary] field which is defined at the top
    def Recommendations_Summary_value_verification(self, data, field_name=Recommendations_Summary):
        self.app.verification.verify_textarea_value(expected_text=data, idVal=field_name)
        return True

    # purpose- to click on [cancel] button where cancel_btn is the button name which is defined at the top
    def click_on_Cancel_button(self):
        self.app.navigation.click_btn(self.cancel_btn)

    # purpose- to click on [continue] button on popup which displays after clicking on [cancel] button and to verify that [mtb] page is displayed
    # continue_popup_locator is the locator of continue button which is defined at the top
    def verify_user_clicks_on_continue(self):
        continue_popup = WebDriverWait(self.app.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.continue_popup_locator)))
        if continue_popup:
            assert True,'continue button is not present on popup'
            log.info("continue button is present on popup")
            self.app.driver.execute_script("arguments[0].click();", continue_popup)
            log.info("continue button is clicked")
        else:
            log.error("continue button is not present on popup")
        self.app.mtb_case_management_page.verify_Molecular_Tumor_Board_text_present_on_page()
        assert True, 'User is on User Case Management Screen'
        log.info("User is on User Case Management Screen")

    # purpose - to verify that 'Recommendations Summary' text is present on [create new case] page
    # param is the expected text defined at the top
    def verify_recommendations_summary_text_present_on_page(self, text=Recommendations_Summary_text):
        self.app.verification.text_present_on_page(text)

    # purpose- to click on [cancel] button on popup which displays after clicking on [cancel] button and to verify that [mtb] page is displayed
    # cancel_btn_on_popup_locator is the locator of cancel button which is defined at the top
    def verify_user_clicks_on_cancel(self):
        cancel_popup = WebDriverWait(self.app.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.cancel_btn_on_popup_locator)))
        if cancel_popup:
            assert True,'cancel button is not present on popup'
            log.info("cancel button is present on popup")
            self.app.driver.execute_script("arguments[0].click();", cancel_popup)
            log.info("cancel button is clicked")
        else:
            log.error("cancel button is not present on popup")
        text = str(self.app.verification.text_present_on_page(self.app.mtb_case_management_page.mtb_case_management_text))
        if text.find(self.app.mtb_case_management_page.mtb_case_management_text):
            assert True, 'User is on Create Case form page '
            print("User is on same page")
            log.info("User is on same page")

    # purpose- to click on [add] link
    # field_name is name of field for which user want to click [add] link
    # btn_text is the button text
    def click_on_add_or_change_link(self, field_name, btn_text):
        log.info('Click on "%s" link for field "%s"' % (btn_text, field_name))
        element = find_elements(self.app.driver,
                                "//a[@data-test='%s' and contains(text(),'%s')]" % (field_name, btn_text))
        if len(element) > 0:
            assert True, ('%s link has not been found for field %s' % (btn_text, field_name))
            try:
                element[0].click()
                log.info('Clicked on "%s" link for field "%s"' % (btn_text, field_name))
            except:
                JS_tricks.element_to_the_middle(self.app.driver, element[0])
                JS_tricks.mouse_click_element(self.app.driver, element[0])
                log.info('Add/change link %s has been found & clicked' % btn_text)
        else:
            raise Exception('\n %s link has not been found for field %s' % (btn_text, field_name))

    # purpose-select the value for [Primary_Site] or Histology type fields
    # where class_name is the field's class name for which user want select value
    # option_name is option which user want to select
    def select_option_from_PrimarySite_or_Histology(self, class_name, option_name):
        log.info('select option "%s" from the drop-down' % option_name)
        self.app.driver.implicitly_wait(5)
        field_prep = find_elements(self.app.driver, "//div[@class='%s']//textarea" % class_name)
        value_to_enter = option_name
        assert len(field_prep) > 0, 'Unable to activate the field %s' % class_name
        field_prep[0].send_keys(value_to_enter)
        vals = find_elements(self.app.driver, self.value_field % value_to_enter)
        if len(vals) > 0:
            log.info('Desired value "%s" has been found in the vocab' % value_to_enter)
            assert True, 'Desired value "%s" has not been found in the vocab' % value_to_enter
        else:
            log.error('Desired value %s has not been found in the vocab' % value_to_enter)
        vals[0].click()
        log.info('Clicked on option "%s"' % value_to_enter)
        select_btn = find_elements(self.app.driver, self.select_btn_field)
        try:
            JS_tricks.element_to_the_middle(self.app.driver, select_btn[0])
            JS_tricks.mouse_click_element(self.app.driver, select_btn[0])
            log.info('Clicked on select button')
        except:
            log.error('"%s" button is not clickable' % select_btn[0])
            raise Exception('\n %s not clickable' % select_btn[0])
        time.sleep(1)

    # purpose-select the value for [Primary_Site] field
    # It calls 2 methods  "click_on_add_or_change_link" and "select_option_from_PrimarySite_or_Histology" which are defined above with description
    def select_option_from_Primary_Site(self, option_name):
        self.click_on_add_or_change_link(field_name=self.primary_site_data_test, btn_text=self.add_link)
        self.select_option_from_PrimarySite_or_Histology(class_name=self.primary_site_class, option_name=option_name)

    # purpose-select the value for [Histology] field
    # It calls 2 methods  "click_on_add_or_change_link" and "select_option_from_PrimarySite_or_Histology" which are defined above with description
    def select_option_from_Histology(self, option_name):
        self.click_on_add_or_change_link(field_name=self.histology_data_test, btn_text=self.add_link)
        self.select_option_from_PrimarySite_or_Histology(class_name=self.histology_class, option_name=option_name)

    # purpose-if text box is not present then click on [none provided] text to see the textbox
    # ele_xpath is the locator of element which contains "none provided" for the particular field
    def click_on_to_enable_text(self, ele_xpath):
        element = find_element(self.app.driver, ele_xpath)
        if element:
            self.app.driver.execute_script("arguments[0].click();", element)
            ActionChains(self.app.driver).move_to_element(element).click(element)

    def verify_special_char_error_message_is_displayed(self):
        """
        This function validate whether a error message is displayed when special characters are entered
        in patient search box.
        If error message is displayed for special characters like ~`@#$^{}|  which are disallowed then,
        this function will get passed as the validation is only done on verify the error message.
        If there is no error message for special character like ~`@#$^{}| then this function will get failed

        """
        try:
            error = WebDriverWait(self.app.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.special_char_error)))
            if error.is_displayed():
                log.info("Error message is displayed")
                assert True, "Error message is displayed"
        except:
            log.info("Error message is not displayed with the given special character")
            raise Exception("BUG ....!!!!!  No error Message against this special Characters")

    def verify_no_error_message_is_displayed_for_acceptable_special_chars(self, name):
        """
        :purpose-This function validate the error message is not displayed when "'-" these special characters are entered
        in patient search box.
        :param:name is value which contains special character
        """
        log.info("Enter patient name with accepatable special characters in the search box")
        self.app.finder.find_only_patient_name(name)
        log.info("Verify that Error message is not displayed for acceptable ('-) special characters")
        try:
            error = WebDriverWait(self.app.driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, self.special_char_error)))
            if error:
                log.info("Error message is not displayed for acceptable ('-) special characters")
                assert True, "Error message is displayed for acceptable ('-) special characters"
            else:
                log.error("Error message is displayed for acceptable ('-) special characters")
                assert False, "Error message is not displayed for acceptable ('-) special characters"
        except:
            raise Exception("BUG ....!!!!!  Error message is not displayed for acceptable ('-) special characters")

    def verify_sex_value(self, tr_row=1, td_col=3):
        """
        This function validates the Sex of Patients.
        tr_row : Specify the row number in which Patient Sex element is present
        td_col : Specify the Column in which Patient Sex element is present(If later DOB element is shifted to 2rd or 4th column,change this value accordingly
        It should match with the Sex value returned from API for thr patient
        """
        from qa_automation_drt_haw.ui.model.finder import Finder
        sex = find_element(self.app.driver, self.sex_value % (tr_row, td_col))
        patient_sex_value = Finder.get_patient_Sex_Value(self.app.finder)
        sex_text = sex.text
        if sex_text in str(patient_sex_value):
            log.info("Sex is displayed correctly")
        else:
            log.info("Sex value is displayed wrong")
            assert False, "Sex value is displayed wrong"

    def enter_meeting_notes(self, what):
        '''
        purpose: Method is used to enter the text in meeting notes
        :param what: Text to be entered
        :return: Nothing
        '''
        try:
            self.click_on_to_enable_text(ele_xpath=self.meeting_notes_none)
            self.text_area_enter(what, self.meeting_notes_text_area)
        except:
            self.text_area_enter(what, self.meeting_notes_text_area)

    def verify_entered_meeting_notes(self, text_to_validate):
        '''
        purpose: Method is used to verify the text in meeting notes
        :param text_to_validate: Expected text to be validated
        :return: Nothing
        '''
        ele_xpath = self.xpath_textarea_val % self.meeting_notes_text_area
        val = self.retrieve_entered_text(ele_xpath)
        if text_to_validate == 'Empty':
            assert val == "" , 'Expected value in meeting note is not empty'
        else:
            assert val == text_to_validate, "Expected value in meeting note does not match actual"



    def verify_entered_case_narrative(self, text_to_validate):
            '''
            purpose: Method is used to verify the text in meeting notes
            :param text_to_validate: Expected text to be validated
            :return: Nothing
            '''
            display_text = find_elements(self.app.driver, "//div[@data-qa-key='case_narrative_display']/.")
            if len(display_text) > 0:
                ActionChains(self.app.driver).double_click(display_text[0]).perform()
            time.sleep(2)
            ele_xpath = self.xpath_textarea_val % self.case_narrative
            print('meet note %s'%ele_xpath)
            val = self.retrieve_entered_text(ele_xpath)
            if text_to_validate == 'Empty':
                assert val == "", 'Expected value in meeting note is not empty'
            else:
                assert val == text_to_validate, 'Expected value in meeting note does not match actual'

    def verify_entered_Recommendation_summary(self, text_to_validate):
        '''
                purpose: Method is used to verify the text in Recommendation summary
                :param text_to_validate: Expected text to be validated
                :return: Nothing
                '''
        try:
            display_text = find_elements(self.app.driver, self.recommendation_summary_field)
            if len(display_text) > 0:
                action = ActionChains(self.app.driver).double_click(display_text[0]).perform()
        except:
            log.error('Unable to open the meeting notes to edit')
        ele_xpath = self.xpath_textarea_val % self.Recommendations_Summary
        self.click_on_to_enable_text(ele_xpath)
        val = self.retrieve_entered_text(ele_xpath)
        print(val)
        if text_to_validate == 'Empty':
            assert val == "", 'Expected value in meeting note is not empty'
        else:
            if '\n' in str(val):
                log.info("New line is present in the text,It should be displayed on the Next line")
                assert True, "New line is present in the text,so Lines are preseved"
            else:
                log.info("The Text is a Single Line text so no line is preserved")
            # assert val == text_to_validate, 'Expected value in meeting note does not match actual'

    def retrieve_entered_text(self, locator_value, mode=By.XPATH):
        '''
        :purpose: Method is used to retrieve the text from given element
        :param locator_value: This contains the value required for locator
        :param mode: Mode to locate element. Such By.CSS,BY.ID etc. Default is BY.XPATH
        :return: The retrieved text
        '''
        text_field = find_elements(self.app.driver, locator_value, mode)
        # print('field - %s' % text_field)
        if len(text_field) > 0:
            temp = text_field[0].get_attribute('value')
            log.info("Fetched the text entered from given element")
        else:
            temp = None
            log.warning("Given element is not found")
        return temp

    def verify_error_message(self, error_element):

        '''
        Purpose: This method is used to verify the error message
        :param error_element: Error element to be verified.
        :return: None
        '''
        element = find_element(self.app.driver, error_element)
        if element:
            assert True, "Error message is received"
        else:
            assert False, "Expected error message is not received"

    def open_new_meeting_notes(self):
        '''
        purpose: This method opens the meetings note to add new meeting notes
        :return: nothing
        '''
        WebDriverWait(self.app.driver, 10).until(EC.element_to_be_clickable, self.meeting_notes_button)
        element = find_element(self.app.driver, self.meeting_notes_button)
        action = ActionChains(self.app.driver).move_to_element(element).click().perform()

        WebDriverWait(self.app.driver, 8).until(EC.presence_of_element_located, self.meeting_notes_none)
        self.click_on_to_enable_text(ele_xpath=self.meeting_notes_none)

    def open_existing_meeting_notes(self):
        '''
        purpose: This method opens the meetings note to edit meeting notes
        :return: nothing
        '''
        WebDriverWait(self.app.driver, 10).until(EC.element_to_be_clickable, self.meeting_notes_button)
        element = find_element(self.app.driver, self.meeting_notes_button)
        action = ActionChains(self.app.driver).move_to_element(element).click().perform()
        time.sleep(0.5)
        try:
            display_text = find_elements(self.app.driver, self.meeting_notes_display_area)
            if len(display_text) > 0:
                action = ActionChains(self.app.driver).double_click(display_text[0]).perform()
        except:
            log.error('Unable to open the meeting notes to edit')

    def close_meeting_notes(self):
        '''
        Purpose: This method is used to close the meeting notes.
        :return:
        '''
        element = get_element_after_wait(self.app.driver,locator=self.meeting_notes_close,timeout=10)
        if element is not None:
            action_click(self.app.driver,element)
        else:
            log.error("Close Meeting Notes button is not available to click")

    def open_option_list_for_Histology(self):
        '''
        Purpose: This method open the add link for Histology field
        :return: nothing
        '''
        self.click_on_add_or_change_link(field_name=self.histology_data_test, btn_text=self.add_link)

    def get_case_url(self):
        '''
        Purpose: Fetched the url of case created in mtb
        :return: case web url
        '''
        return get_current_url(self.app.driver)

    # purpose-to scroll to [Recommendations] section on [create new case] page
    # Recommendations_text is the section which is defined at the top
    def scroll_to_recommendations(self):
        self.app.navigation.scroll_to_section(self.Recommendations_text)

    # purpose - to verify that 'None provided' is displayed under [Recommendations] section as the default state
    # none_provided_text is the expected text declared at the top
    def verify_none_provided_text(self):
        self.app.verification.text_present_on_page(self.none_provided_text)

    # purpose - to verify column headers of [Recommendations] section
    # none_provided_text is the expected text declared at the top
    def verify_recommendations_fields(self):
        self.app.verification.verify_column_header_on_table(self.recommendation_type)
        self.app.verification.verify_column_header_on_table(self.description)
        self.app.verification.verify_column_header_on_table(self.relevant_biomarkers)
        self.app.verification.verify_column_header_on_table(self.notes)
        self.app.verification.verify_button_on_page(self.remove)

    # purpose-Enter data in [recommendations_description] field on [create case] page
    # where data for 'what' is passsed from test file and description_id is the locator of [recommendations_description] field which is defined at the top
    def enter_data_in_recommendations_description(self, what, i=0):
        self.app.finder.text_area_enter(what, self.description_id, i=i)

    # purpose-Enter data in [recommendations_notes] field on [create case] page
    # where data for 'what' is passsed from test file and notes_id is the locator of [recommendations_notes] field which is defined at the top
    def enter_data_in_recommendations_notes(self, what, i=0):
        WebDriverWait(self.app.driver, 3).until(EC.presence_of_element_located, self.notes_)
        self.click_on_to_enable_text(ele_xpath=self.notes_)
        self.app.finder.text_area_enter(what, self.notes_id_edit,i=i)

    def edit_data_in_recommendations_notes(self, what, i=0):
        '''
        :purpose: enter data for the recommendation notes field
        :param what: data for 'what' is passsed from test file
        :param i: it is index value , by default it is 0
        '''
        WebDriverWait(self.app.driver, 3).until(EC.presence_of_element_located, self.notes_display)
        self.click_on_to_enable_text(ele_xpath=self.notes_display)
        self.app.mtb.clear_input_field_using_backspace(field_name=self.notes_edit)
        self.app.finder.text_area_enter(what, self.notes_id_edit)

    # purpose-select option in [recommendation_type] field on [create case] page.
    # ddname is the locator of [recommendation_type] field i.e 'recommendation_type_class'
    # option_name is option which needs to be selected and it is passed from test file
    def select_option_from_recommendation_type(self, option_name, ddname=recommendation_type_class, i=0):
        self.app.navigation.select_option_from_dd(option_name=option_name, ddname=ddname, i=i)

    # purpose-fill out all the fields of recommendations
    # data for type_data,notes_data,description_data are passsed from test file and bydefault is empty for these fields
    def fill_out_Recommendations(self, type_data='', notes_data='', description_data='', i=0,j=0):
        self.app.navigation.click_button(self.add_recommendation, self.recommendation_type)
        self.select_option_from_recommendation_type(option_name=type_data, i=i)
        self.enter_data_in_recommendations_notes(what=notes_data, i=j)
        self.enter_data_in_recommendations_description(what=description_data, i=i)

    # purpose-verify the values for recommendations fields
    # data for type_data,notes_data,description_data are passsed from test file and bydefault is empty for these fields
    def Verify_values_for_Recommendations(self, type_data='', notes_data='', description_data='', i=0):
        log.info("Verify the values of recommendation fields")
        self.app.verification.verify_dd_default_value(expected_option=type_data, dd_name=self.recommendation_type_class, i=i)
        self.app.verification.verify_textarea_value(expected_text=description_data, idVal=self.description_id, i=i)
        self.app.verification.verify_textarea_value(expected_text=notes_data, idVal=self.notes_id_verify, i=i)
        log.info("all the values of recommendation fields are as expected")

    def remove_all_recommendations(self):
        '''
        #purpose-to remove all the recommendations
        '''
        log.info("Removing all the recommendations")
        recommendation_remove_xpath=find_elements(self.app.driver,self.recommendation_remove_xpath)
        n = len(recommendation_remove_xpath)
        if n>0 :
            while  n > 0 :
                self.app.navigation.click_btn(self.remove)
                n = n - 1
                log.info('recommendation %s is removed' %n)
            log.info("All recommendations are removed")

    def verify_one_recommendation_is_removed(self):
        '''
        #purpose-to verify the one recommendation is removed from the available list
        '''
        log.info("Removing one recommendation from the available list")
        recommendations=find_elements(self.app.driver,self.total_recommendation)
        # get total recommendations count before removing
        before_length = len(recommendations)
        print(before_length)

        #remove one recommendation
        self.app.navigation.click_btn(self.remove)

        recommendations = find_elements(self.app.driver, self.total_recommendation)
        # get the total recommendations count after removing 1
        after_length = len(recommendations)
        print(after_length)

        if before_length-1 == after_length:
            log.info('one recommendation is removed sucessfully out of %s' %before_length )
            assert True,'one recommendation is not removed out of %s'  %before_length
        else:
            log.error('one recommendation is not removed out of %s'  %before_length)
            assert False,'one recommendation is removed sucessfully out of %s'  %before_length


    # purpose-verify the values for all the mtb fields
    # data for all the parameters will be passed from test file and initial values are empty for these parameters
    def mtb_case_values_verification(self, meeting_date='', diagnosis_date='', primary_oncologist_data='',
                                     primary_sites='', stage_group_option='', histology_data='',
                                     recommendation_summary_data='', case_narrative_data=''):
        self.app.verification.verify_calender_value(calendar_field=self.Meeting_Date, expected_date=meeting_date)
        self.app.verification.verify_calender_value(calendar_field=self.Diagnosis_Date, expected_date=diagnosis_date)
        self.click_on_to_enable_text(self.primary_oncologist_before_textbox)
        self.app.verification.verify_textarea_value(idVal=self.Primary_Oncologist,expected_text=primary_oncologist_data)
        primary_site_ele = find_elements(self.app.driver, self.xpath_data_test % self.primary_Sites_Value)
        histology_ele = find_elements(self.app.driver, self.xpath_data_test % self.histologies_Value)
        if len(primary_site_ele) > 0:
            self.app.verification.verify_textarea_value(idVal=self.primary_Sites_Value, expected_text=primary_sites)
        if len(histology_ele) > 0:
            self.app.verification.verify_textarea_value(idVal=self.histologies_Value, expected_text=histology_data)
        self.app.verification.verify_dd_default_value(expected_option=stage_group_option, dd_xpath=self.stage_group)
        self.click_on_to_enable_text(self.meeting_none)
        self.Recommendations_Summary_value_verification(data=recommendation_summary_data)
        # self.app.verification.verify_textarea_value(idVal=self.Recommendations_Summary,expected_text=recommendation_summary_data)
        self.click_on_to_enable_text(ele_xpath=self.caseNarrative_none)
        self.app.verification.verify_textarea_value(idVal=self.case_narrative, expected_text=case_narrative_data)

    def get_cases_count_on_current_page(self):
        '''
        Purpose: To get the current count of cases from molecular tumor board page
        :return: count of cases
        '''
        cases = find_elements(self.app.driver, self.cases_table)
        if len(cases)>0:
            count = len(cases)
            log.info("In MTB '%s' cases are available" % count)
            return count
        else:
            log.warning("In MTB, cases are not obtained")

    def verify_no_of_cases_on_MTB_page(self, max_count=25, exact_count=None):
        '''
        Purpose: To verify if required cases are available on the given page
        :param max_count: Max count of possible cases (It is an optional parameter, having default value of 25)
        :param exact_count: On a given page, if exact cases count needs to be verified. Need to pass this parameter.
        :return:
        '''

        count = self.get_cases_count_on_current_page()
        page_num = self.get_current_page_number()
        if exact_count is None:
            if count > 0 and count <= max_count:
                log.info(" %s Cases are available in given page - %s" % (count,page_num))
            if count <= 0 or count > max_count:
                log.error("Cases are not available")
        else:
            if count == exact_count:
                log.info(" %s Cases are available in given page - %s" % (count,page_num))
            else:
                log.error("Actual Cases %s does not match the expected count %s" % (count, exact_count))

    def get_current_page_number(self):
        '''
        Purpose: To fetch the current page number
        :return: The number of current page
        '''

        page_num = find_elements(self.app.driver,self.current_page_number)
        if len(page_num) > 0:
            val = page_num[0].get_attribute('title')
            log.info('Current page number is %s' % val)
            return val
        else:
            log.error("Unable to get current page number")
            return None

    def goto_next_page(self,no_of_times=1):
        '''
        Purpose: To naviagate to next page
        :param no_of_times: Next page will be opened as per this parameter. By Default value is 1
        :return: Page number after opening new page
        '''
        next_page_num = ""
        for num in range(no_of_times):
            cur_page_num = self.get_current_page_number()
            next_button = find_elements(self.app.driver,self.next_page_btn)
            if len(next_button) > 0:
                log.info("Navigate to next page")
                # next_button[0].click()
                action_click(self.app.driver, next_button[0])
                next_page_num = self.get_current_page_number()
                if int(next_page_num) == int(cur_page_num) + 1:
                    log.info("Navigation to page num '%s' is successful."% next_page_num)
                else:
                    log.error("Navigation to page num '%s' is unsuccessful."% (int(cur_page_num) + 1))
                    next_page_num = 0

        return int(next_page_num)

    def open_and_verify_next_page(self,no_of_times=1):
        '''
        Purpose: This method is used to open the next page and verify if it is opened
        :param no_of_times: No of times next page to be opened. Default value is 1.
        :return: nothing
        '''
        assert self.goto_next_page(no_of_times=no_of_times) != 0, "Error encountered while navigation amongst the " \
                                                                  "pages "

    def goto_previous_page(self,no_of_times=1):
        '''
        Purpose: To naviagate to previous page
        :param no_of_times: Next page will be opened as per this parameter. By Default value is 1
        :return: Page number after opening new page
        '''
        previous_page_num = ""
        for num in range(no_of_times):
            cur_page_num = self.get_current_page_number()
            previous_button = find_elements(self.app.driver,self.previous_page_btn)
            if len(previous_button) > 0:
                log.info("Navigate to previous page")
                previous_button[0].click()
                previous_page_num = self.get_current_page_number()
                if int(previous_page_num) == int(cur_page_num) - 1:
                    log.info("Navigation to page num '%s' is successful."% previous_page_num)
                else:
                    log.error("Navigation to page num '%s' is unsuccessful."% (int(cur_page_num) - 1))
                    previous_page_num = 0

        return int(previous_page_num)

    def open_and_verify_previous_page(self, no_of_times=1):
        '''
        Purpose: This method is used to open the previous page and verify if it is opened
        :param no_of_times: No of times previous page to be opened. Default value is 1.
        :return: nothing
        '''
        assert self.goto_previous_page(no_of_times=no_of_times) != 0, "Error encountered while navigation amongst " \
                                                                      "the pages "

    def check_meeting_date_sorting(self):
        '''
        Purpose: To check if sorting is applied
        :return: Which sorting is applied (<col_name>_ascending or <col_name>_descending)
        '''
        element_locator = self.meeting_date_header + self.sorting_enabled
        val = self.check_sorting("meeting_date",element_locator)
        if val is not False:
            return val
        else:
            return None


    def check_case_id_sorting(self):
        '''
        Purpose: To check if sorting is applied
        :return: Which sorting is applied (ascending or descending)
        '''

        element_locator = self.case_id_header + self.sorting_enabled
        val = self.check_sorting("case_id", element_locator)
        if val is not False:
            return val
        else:
            return None


    def check_diagnosis_sorting(self):
        '''
        Purpose: To check if sorting is applied
        :return: Which sorting is applied (ascending or descending)
        '''

        element_locator = self.diagnosis_header + self.sorting_enabled
        val = self.check_sorting("diagnosis",element_locator)
        if val is not False:
            return val
        else:
            return None


    def check_sorting(self,col_header_name,sorting_element_locator):
        '''
        Purpose: This is a generic method which is used to check the existing sorting on given column
        :param col_header_name: Column name on which sorting needs to be verified
        :param sorting_element_locator: Locator of sorting element next to the column name
        :return: If sorting exists then returns (<col_name>_ascending or <col_name>_descending) or returns False
        '''
        element = find_elements(self.app.driver, sorting_element_locator)
        if len(element) > 0:
            val = element[0].get_attribute('class')
            if 'caret-up' in str(val).lower():
                sorting = col_header_name + "_ascending"
            elif 'caret-down' in str(val).lower():
                sorting = col_header_name + "_descending"
            log.info("Applied sorting is as %s"%sorting)
        else:
            sorting = False
            log.info("Sorting is not available for header %s" % col_header_name)
        return sorting

    def get_current_sorting_applied(self):
        '''
        Purpose: Out of all the available columns in mtb page, check the existing sort applied
        :return: If sorting exists then returns (<col_name>_ascending or <col_name>_descending) or returns None
        '''
        if self.check_meeting_date_sorting() is not None:
            sorting = self.check_meeting_date_sorting()
        elif self.check_case_id_sorting() is not None:
            sorting = self.check_case_id_sorting()
        elif self.check_diagnosis_sorting() is not None:
            sorting = self.check_diagnosis_sorting()
        else:
            log.error("Default Sorting is not applied")
            sorting = None
        return sorting

    def store_applied_sorting(self):
        '''
        Purpose: To store the current sorting applied on mtb page in the class member
        :return: Nothing
        '''
        self.current_sorting_applied = self.get_current_sorting_applied()
        log.info("Stored the current sorting in class member variable")

    def verify_sorting_applied(self,sorting_value=None):
        '''
        Purpose: This method is used to verify if correct sorting is applied on case pages
        :param sorting_value: Sorting value should be in format "<col_name>_ascending" or "<col_name>_descending"
        :return: Nothing
        '''
        if sorting_value is None:
            sorting_value = self.current_sorting_applied
        val = self.get_current_sorting_applied()

        assert val == sorting_value,"Expected sorting value '%s' does not match actual value '%s'"%(sorting_value,val)
        log.info("Sorting is verified successfully.Expected sorting value '%s' matches actual value '%s'"%(sorting_value,val))

    def apply_meeting_date_sort(self,sort_type='descending'):
        '''
        Purpose: To apply sorting on meeting date col
        :param sort_type: Type of sorting 'ascending' or 'descending'
        :return: None
        '''
        self.apply_sort(self.meeting_date_header,sort_type=sort_type)

    def apply_case_id_sort(self, sort_type='descending'):
        '''
        Purpose: To apply sorting on case id col
        :param sort_type: Type of sorting 'ascending' or 'descending'
        :return: None
        '''
        self.apply_sort(self.case_id_header, sort_type=sort_type)

    def apply_diagnosis_sort(self, sort_type='descending'):
        '''
        Purpose: To apply sorting on diagnosis col
        :param sort_type: Type of sorting 'ascending' or 'descending'
        :return: None
        '''
        self.apply_sort(self.diagnosis_header, sort_type=sort_type)


    def apply_sort(self,col_header_locator,sort_type='descending'):
        '''
        Purpose: This method is used to apply the sorting on given column
        :param col_header_locator: locator of the column header
        :param sort_type: Type of sorting 'ascending' or 'descending'
        :return: Nothing
        '''
        global sort_locator
        if str(sort_type).lower() == 'descending':
            sort_locator = col_header_locator + "//i[contains(@class,'caret-down')]"
        elif str(sort_type).lower() == 'ascending':
            sort_locator = col_header_locator + "//i[contains(@class,'caret-up')]"
        else:
            log.error("Invalid value for sorting '%s'" % sort_type)

        element = find_elements(self.app.driver, sort_locator)
        if len(element) > 0:
            if ' on' not in element[0].get_attribute('class'):
                element[0].click()
                if get_element_after_wait(self.app.driver,locator=self.meeting_date_header,timeout=5) is not None:
                    log.info("sorting is applied")

    def double_navigate_to_right(self):
        '''
        Purpose: This method is used to navigate +5 pages on right in mtb page
        :return: None
        '''
        locator = "//i[contains(@class,'double-right')]//.."
        current_page_num = self.get_current_page_number()
        log.info(current_page_num)
        element = find_elements(self.app.driver,locator)
        if len(element) > 0:
            element[0].click()
            new_page_num = self.get_current_page_number()
            log.info(new_page_num)
            assert int(current_page_num) + 5 == int(new_page_num), "Unable to navigate to 5 pages to right after clicking on '...'"

    def double_navigate_to_left(self):
        '''
        Purpose: This method is used to navigate +5 pages on left in mtb page
        :return: None
        '''
        locator = "//i[contains(@class,'double-left')]//.."
        current_page_num = self.get_current_page_number()
        log.info(current_page_num)
        if int(current_page_num) > 5:

            element = find_elements(self.app.driver,locator)
            if len(element) > 0:
                element[0].click()
                new_page_num = self.get_current_page_number()
                log.info(new_page_num)
                assert int(current_page_num) - 5 == int(new_page_num), "Unable to navigate to 5 pages to left after clicking on '...'"

    def  verify_no_characters_in_primary_oncologist(self, text_to_validate):
        """
        This function counts the no of characters in primary oncologist field
        It validates the actual and retrived value
        """
        ele_xpath = self.xpath_textarea_val % self.primary_onco
        val = self.retrieve_entered_text(ele_xpath)
        if text_to_validate == 'Empty':
            assert val == "", 'Expected value in meeting note is not empty'
        else:
            log.error("More than 100 characters are entered")
            assert val == text_to_validate, 'Expected value in meeting note does not match actual'

    def verify_refresh_button_is_displayed(self):
        """
        This functions verifies whether the refresh button is visible on case page
        """
        try:
            refersh_icon = find_element(self.app.driver,self.refresh_icon)
            if refersh_icon.is_displayed():
                log.info("Refresh Button is visible on page")
            else:
                log.warn("Patient donot have any reports and so Refresh icon is not visible")
        except NoSuchElementException:
            log.info("Patient donot have any reports and so Refresh icon is not visible")

    def verify_total_reports(self):
        """
        This function fetches the total no of reports for the patients from the case form
        """
        try:
            reports = find_elements(self.app.driver,self.auto_reports)
            total_reports = len(reports)
            log.info("Total reports are %s", total_reports)
            return total_reports
        except:
            log.error("No Reports are Available for Patient")
            assert False,"No Reports are Available for Patient"

    def verify_success_message_on_report_load_is_displayed(self):
        """
        This function verifies the Success Message when refresh button is clicked and reports are updated
        """
        try:
            refersh_icon = find_element(self.app.driver, self.refresh_icon)
            action_click(self.app.driver,refersh_icon)
            print("Refresh button is clicked")
            log.info("Refresh button is clicked")
            msg = WebDriverWait(self.app.driver, 3).until(EC.presence_of_element_located,
                                                        self.report_success_msg)
            if msg:
                log.info("Report Success message displayed")
                print("Report Success message displayed")
            else:
                log.error("No popup is displayed")
                assert False, "Report success message is not displayed"
        except:
            log.error("Report success message is not displayed")
            assert False, "Report success message is not displayed"

    def verify_success_notification_after_case_saved(self):
        '''
        Purpose: To verify the success notification is received after save button is clicked in a case
        :return: Nothing
        '''
        log.info("Waiting for success notification")
        element = get_element_after_wait(self.app.driver,self.save_success_notification, timeout=15, pollFrequency=0.25)
        log.info(element)
        assert element != None, "Success notification after case is saved not received"
        log.info("Success notification is received")

    def verify_inital_height_of_meting_notes(self):
        """
        This function verifies the intial height of meeting notes before clicking on the element to active text area
        Returns True if height is 31px else Returns False
        """
        notes_text_box = find_element(self.app.driver,self.meeting_notes_view)
        inital_height = notes_text_box.size['height']
        if inital_height == 31:
            log.info("Inital Height is %s" %inital_height)
            assert True,"Inital Height is %s" %inital_height
        else:
            log.error("Initial height is not matching the criteria")
            assert False,"Initial height is not matching the criteria"

    def verify_page_tile_Molecular_Tumor_Board_text_height(self):
        """
        This function verifies the Height of the page component named 'Molecular Tumor Board'
        """
        height = find_element(self.app.driver,self.MTB_page_component)
        height_value= height.size['height']
        try:
            if height_value == 76:
                log.info("Molecular Tumor Board Component size is %s",height_value)
            else:
                log.error("Molecular Tumor Board Component size is changed and retrieved value is %s",height_value)
                assert False,"Page component size is changed"
        except:
            log.error("Molecular Tumor Board Component size is changed and retrieved value is %s", height_value)
            assert False, "Page component size is changed"

    def get_max_height_of_meeting_notes_text_area(self):
        """
        This function gets the max height of the meeting notes text area field.
        So that the text can be entered and be visible after decreasing window size
        """
        self.click_on_to_enable_text(ele_xpath=self.meeting_notes_none)
        notes_text_box = find_element(self.app.driver,self.xpath_textarea_val % self.meeting_notes_text_area)
        height = notes_text_box.size['height']
        log.info("Text area Height after click is %s",height)
        return height

    def verify_scroll_in_meeting_notes(self):
        """
        This function verify the scroll bar gets activate in meeting note text area field when max height of text area
        field is reached.
        Technically after 11 rows in text area the scroll will get activate
        """
        ele_xpath = self.xpath_textarea_val % self.meeting_notes_text_area
        val = self.retrieve_entered_text(ele_xpath)
        lines = val.count('\n')
        if lines == 11:
            log.info("Scroll is displayed")
            assert True,"Scroll is displayed"
        elif lines < 11:
            print("Scroll is not displayed as it has only % s" %lines)
            assert False,"Scroll is not displayed as it has only %s" %lines

    def verify_none_provided_text_is_absent(self):
        """
        This function verifies the placeholder is present on the fields.
        Return False If the element is present on the page
        Returns True if NoSuchElementException error is thrown saying element is not present on page
        """
        try:
            none_place_holder = find_element(self.app.driver,self.none_provided)
            if none_place_holder:
                log.error("None provided placeholder is present on the page")
                assert False,"None provided placeholder is present on the page"
        except NoSuchElementException:
            log.info("None Provided placeholder is absent on the fields")
            return True

    def verification_in_zoom_mode(self,zoom_percent):
        """
        This function zooms the browser window and performs validation on meeting notes functionality
        :param zoom_percent : Pass the zoom % inorder to zoom the page to e.g 0.9 refers 90% 1.5 refers 150%
        """
        # self.app.driver.execute_script("document.body.style.zoom='%s'" %zoom)
        log.info("Zoom is %s percent " %zoom_percent)
        self.open_existing_meeting_notes()
        height_before_zoom = self.get_max_height_of_meeting_notes_text_area()
        log.info("Height before zoom is %s" % height_before_zoom)
        self.app.driver.execute_script("document.body.style.transform = 'scale(%s)';" %zoom_percent)
        height_after_zoom = self.get_max_height_of_meeting_notes_text_area()
        log.info("Height after zoom is %s " % height_after_zoom)
        if height_after_zoom == height_before_zoom:
            self.verify_scroll_in_meeting_notes()
            GV.text_present_on_page(self.app.verification,self.meeting_notes_updated_text)
        else:
            log.error("Meeting Notes text area height is changed")
            assert False,"Meeting Notes text area height is changed"

    def retrive_case_id(self):
        """
        This function retrives the 1st Case ID from the Case Management Table
        """
        element = find_elements(self.app.driver,
                                self.xpath_cases_table)
        if len(element) > 0:
            val = element[0].text
            log.info("Case Id is :- %s" % val)
            return val

    def apply_meeting_date_asc_sort(self, sort_type='ascending'):
        '''
        Purpose: To apply sorting on meeting date col
        :param sort_type: Type of sorting 'ascending''
        :return: None
        '''
        self.apply_sort(self.meeting_date_header, sort_type=sort_type)


    def verify_cases_sorted_on_meeting_date(self):
        """
        This function verifies the cases are sorted as per the sorting.
        The most recent/latest Case Id are displayed by default.
        When sorting applied the cases with older date/no meeting dates should be displayed first
        The Case ids retrived are then verified against the case ids fetched from Database
        """
        from qa_automation_drt_haw.qa_utils import backend_data as DB
        ui_desc_case_id = self.retrive_case_id()
        log.info("Case ID from UI is :- %s" % ui_desc_case_id)
        db_desc_case_id = DB.get_case_id_when_meeting_date_desc_sorted()
        log.info("Case ID from Database is :- %s " % db_desc_case_id)
        if ui_desc_case_id == db_desc_case_id:
            log.info("Default sort Case IDs are matched")
            assert True,"Default sort Case Ids are matched"
        else:
            log.error("Mismatch in Case Ids with Default Sort")
            assert False,"Default Sorting Case Ids are not matching"
        self.apply_meeting_date_asc_sort()
        ui_asc_case_id = self.retrive_case_id()
        log.info("Case ID from UI after ascending Sort is :- %s" % ui_asc_case_id)
        db_asc_caseId = DB.get_case_id_when_meeting_date_asc_sorted()
        log.info("Case ID from Database after ascending sort is :- %s" % db_asc_caseId)
        if ui_asc_case_id == db_asc_caseId:
            log.info("Ascending case IDs matched")
            assert True,"Ascending case IDs matched"
        else:
            log.error("Ascending case Ids are not matched")
            assert False,"Ascending case IDs are not matched"
