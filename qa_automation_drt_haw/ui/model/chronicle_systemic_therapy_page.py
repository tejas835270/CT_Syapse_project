import time
import datetime
import os
import pytest

from selenium.webdriver.common.keys import Keys



from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from qa_automation_drt_haw.ui.ui_utils import JS_tricks
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements

class Chronicle_Systemic_Therapy:

#field_locators is dictionary where key represents field name and value represents locators
    field_locators = {'Regimen': 'regimen',
                      'Start Date': 'regimenStartDate',
                      'End Date': 'regimenEndDate',
                      'Agent/drug': 'agentOrDrug',
                      'Purpose of Treatment': 'purposeOfTreatment',
                      'Timing of chemotherapy related to other treatments': 'relativeChemoTiming',
                      'Best response': 'bestResponse',
                      'Last best response date': 'lastBestResponseDate',
                      'Reason for treatment change/stop': 'reasonForTreatmentChange',
                      'Date of progression/recurrence': 'dateOfProgressionOrRecurrence',
                      'Time to progression/recurrence': 'timeToProgressionOrRecurrence',
                      'Toxi-category': 'toxiCategory',
                      'CTCAE': 'ctcae',
                      'Treatment/Summary complete?': 'treatmentSummaryComplete'
                      }
# below variable are created to store locators of section_name
    section='systemicTherapy'
    section1_locator= section+"__0__"
    section2_locator= section+"__1__"
    section1_locator_for_verification=section+"__0"
    section2_locator_for_verification = section+"__1"
    agentOrDrug1_locator =section1_locator+'agentOrDrug__1'
    agentOrDrug2_locator = section1_locator+'agentOrDrug__2'

#systemic Therapy tab_name
    systemicTherapy_tabname="Systemic Therapy"

    # to initialize
    def __init__(self, app):
        self.app = app

    # use of below method is to navigate to [Systemic_Therapy] tab which comes under [Patient Data Entry]
    def chronicle_tab_Systemic_Therapy(self):
        self.app.chronicle.chronicle_tab(self.systemicTherapy_tabname)

    # use of below method is to verify vocab for [Systemic_Therapy] tab where dict is dictionary which is passed in test file , section is defined at the top
    def verify_vocab_for_Systemic_Therapy(self,dict,section=section1_locator):
        self.app.chronicle.verify_vocab_for(section_name=section, data=dict)

    #use of below method is to click on add another button for agentOrDrug
    def agentOrDrug_add_another(self):
        self.app.chronicle.click_btn_for_section(button='Add Another', section=self.section1_locator_for_verification)

    #use of below method is to select value for agentOrDrug1
    def select_value_for_agentOrDrug1(self,values='lenvatinib'):
        self.app.chronicle.biomarker_field_input('Vocab', self.agentOrDrug1_locator,values)

    #use of below method is to select value for agentOrDrug2
    def select_value_for_agentOrDrug2(self, values='Zometa'):
        self.app.chronicle.biomarker_field_input('Vocab', self.agentOrDrug2_locator, values)

    # use of below method is to fill the Systemic_Therapy fields where dict is dictionary which is passed in test file , section is defined at the top
    def Systemic_Therapy_fill_out_the_fields(self,dict,section_name=section1_locator):
        '''
        purpose - Fill up all the fields in Systemic Therapy-section 1 and Save'''
        dict1 = self.app.chronicle.create_dict_for_locators_value(data=dict,field_locator=self.field_locators)
        log.info(dict1)
        self.app.chronicle.fill_out_the_fields(tab_name=self.systemicTherapy_tabname, section_name = section_name , data=dict1)

    # use of below method is to verify the values of Systemic_Therapy fields where dict is dictionary which is passed in test file , section is defined at the top
    def Systemic_Therapy_values_verification(self,dict,section=section1_locator_for_verification):
        '''
                purpose - Verify all the fields value in Systemic Therapy'''
        self.app.chronicle.chronicle_tab_values_verification(self.systemicTherapy_tabname, section=section, data=dict)

    # use of below method is to click on add another by giving section name and role
    def click_add_button_for_section_and_role(self, section=section, role='section'):
        self.app.chronicle.click_button_for_section_and_role(button='Add Another', section=section , role=role)

    # use of below method is to remove all sections from Systematic_therapy , save and then verify
    def remove_all_sections_from_Systematic_therapy(self):
        """
            Chronicle - Systematic_therapy - Remove all sections
        """
        # app.navigation.refresh_page()
        log.info("clear data before starting the test-if there is any")
        self.chronicle_tab_Systemic_Therapy()
        self.app.navigation.hide_header()
        self.app.navigation.hide_footer()
        self.app.chronicle.remove_all_sections()
        self.chronicle_tab_Systemic_Therapy()
        if self.app.chronicle.verify_text_present_on_page("No Systemic Therapies"):
            log.info("All sections has been removed from Systematic therapy")
            assert True, 'All sections has not been removed from Systematic therapy'
        else:
            log.info("All sections has not been removed from Systematic therapy")


    # use of below method is to remove all the data from fields of Systematic_therapy and dont click save button , just clear the fields
    #field_locator is dictionary of fields name and locator pairs , section_name is locator of section ,both are defined at the top
    def remove_data_from_all_fields(self , field_locator= field_locators,section_name = section2_locator):
        log.info("clear field data before changing it")
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name+field_locator["Regimen"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name+field_locator["Purpose of Treatment"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name+field_locator["Timing of chemotherapy related to other treatments"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name+field_locator["Best response"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name+field_locator["Reason for treatment change/stop"]).replace(" ", ""))
        self.app.chronicle.remove_date_from_calendar_field_if_present((section_name+field_locator["Start Date"]).replace(" ", ""))
        self.app.chronicle.remove_date_from_calendar_field_if_present((section_name+field_locator["End Date"]).replace(" ", ""))
        self.app.chronicle.remove_date_from_calendar_field_if_present((section_name+field_locator["Last best response date"]).replace(" ", ""))
        self.app.chronicle.remove_date_from_calendar_field_if_present((section_name+field_locator["Date of progression/recurrence"]).replace(" ", ""))
        self.app.chronicle.remove_date_from_calendar_field_if_present((section_name+field_locator["Time to progression/recurrence"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Toxi-category"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["CTCAE"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Treatment/Summary complete?"]).replace(" ", ""))

        log.info("cleared....")


