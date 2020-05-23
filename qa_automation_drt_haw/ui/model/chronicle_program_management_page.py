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


class chronicle_Program_Management:

    '''field_locators is dictionary where key represents field name and value represents locators'''
    field_locators ={
        "Subject ID":"subjectId",
        "Consent Status": "consentStatus",
        "Did NGS test results impact treatment planning for the patient?": "didNgsImpactTreatment__0",
        "NGS test results impact - Other":"ngsTestResultsImpactOther",
        "Are there additional areas impacted by NGS test results?": "ngsOtherImpact",
        "Additional areas impacted by NGS test results - Other": "additionalAreasImpactedByNGSTestResultsOther",
        "Are there any issues and concerns raised?": "issuesAndConcerns",
        "Comments": "programComment"
    }

    # below variable are created to store locators of section_name
    section='programManagement'
    section_=section+'__'

    # below variable are created to store locators of multipledidNgsImpactTreatment fields
    didNgsImpactTreatment='programManagement__didNgsImpactTreatment'
    didNgsImpactTreatment_dd0 =didNgsImpactTreatment+'__0'
    didNgsImpactTreatment_dd1 =didNgsImpactTreatment+'__1'
    didNgsImpactTreatment_dd2 =didNgsImpactTreatment+'__2'
    didNgsImpactTreatment_dd3 =didNgsImpactTreatment+'__3'
    #section1_locator=
    #section1_locator_for_verification=


    # Program Management tab_name
    Program_Management_tabname="Program Management"

    # below is the data which comes from fixture_data.json file
    # fields_data1 = pytest.data.get_data('Chronicle_programManagement_no_data')

    # to initialize
    def __init__(self, app):
        self.app = app

    # use of below method is to navigate to [Program_Management] tab which comes under [Patient Data Entry]
    def chronicle_tab_Program_Management(self):
        self.app.chronicle.chronicle_tab(self.Program_Management_tabname)

    # use of below method is to fill the Program_Management fields where dict is dictionary which is passed in test file , section is defined at the top
    def Program_Management_fill_out_the_fields(self, dict, section_name=section_):
        '''
        purpose - Fill up all the fields in Systemic Therapy-section 1 and Save'''
        dict1 = self.app.chronicle.create_dict_for_locators_value(data=dict, field_locator=self.field_locators)
        log.info(dict1)
        self.app.chronicle.fill_out_the_fields(tab_name=self.Program_Management_tabname, section_name=section_name,data=dict1)

    # use of below method is to verify the values of Program_Management fields where dict is dictionary which is passed in test file , section is defined at the top
    def Program_Management_values_verification(self, dict, section=section):
        '''
                purpose - Verify all the fields value in Systemic Therapy'''
        self.app.chronicle.chronicle_tab_values_verification(self.Program_Management_tabname, section=section, data=dict)

    # use of below method is to click add another for [Did NGS test results impact treatment planning for the patient?] field
    def add_another_for_didNgsImpactTreatment(self):
        #self.app.chronicle.add_another_section(type='field')
        btn = find_elements(self.app.driver, "//div[@data-qa-key='add-another-didNgsImpactTreatment']//button[contains(@class, 'field')][contains(., 'Add Another')]")
        if len(btn) > 0:
            JS_tricks.inner_scroll_to_element(self.app.driver, btn[0])
            log.info('Button Add Another section has been found on the page')
            assert True, 'Button Add Another has not been found on the page'
            btn[0].click()
            time.sleep(2)
        else:
            log.error('Button Add Another has not been found on the page')

    # use of below method is to select option in multiple didNgsImpactTreatment dropdowns where ddname locators defined at the top and data is given from test file
    def select_dd_option_didNgsImpactTreatment(self,value,ddname=didNgsImpactTreatment_dd1):
        self.app.chronicle.select_option_from_dd(ddname=ddname,option_name= value)


    # use of below method is to remove all the existing data from all fields of Program_Management and save
    # field_locator is dictionary of fields name and locator pairs , section_name is locator of section ,both are defined at the top
    def remove_all_existing_data(self, field_locator= field_locators, section_name = section_):
        log.info("clear data from all the fields if there is any before starting test ")
        self.chronicle_tab_Program_Management()
        self.remove_data_from_fields_before_changing()
        self.app.navigation.show_footer()
        self.app.chronicle.click_on_save()
        #self.app.chronicle_program_management.chronicle_tab_Program_Management()
        # self.Program_Management_values_verification(self.fields_data1)
        log.info("cleared....")

    # use of below method is to remove all the existing data from all fields of Program_Management and donot save
    #field_locator is dictionary of fields name and locator pairs , section_name is locator of section ,both are defined at the top
    def remove_data_from_fields_before_changing(self, field_locator=field_locators, section_name=section_):
        log.info("clear data from all the fields before changing them  ")
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["Subject ID"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Consent Status"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Are there additional areas impacted by NGS test results?"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Did NGS test results impact treatment planning for the patient?"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Are there any issues and concerns raised?"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["Comments"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["Additional areas impacted by NGS test results - Other"]).replace(" ",                                                                                                 ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["NGS test results impact - Other"]).replace(" ", ""))
        if self.didNgsImpactTreatment_dd0:
            self.app.chronicle.remove_option_from_dropdown_if_data_present(self.didNgsImpactTreatment_dd0)
        if self.didNgsImpactTreatment_dd3:
            self.app.chronicle.remove_additional_field(self.app.chronicle_program_management.didNgsImpactTreatment_dd3)
        else:
            log.info("not present , no need to remove it")
        if self.didNgsImpactTreatment_dd2:
            self.app.chronicle.remove_additional_field(self.app.chronicle_program_management.didNgsImpactTreatment_dd2)
        else:
            log.info("not present , no need to remove it")
        if self.didNgsImpactTreatment_dd1:
            self.app.chronicle.remove_additional_field(self.app.chronicle_program_management.didNgsImpactTreatment_dd1)
        else:
            log.info("not present , no need to remove it")

        # self.app.chronicle_program_management.chronicle_tab_Program_Management()
        # self.Program_Management_values_verification(self.fields_data1)
        log.info("cleared....")






