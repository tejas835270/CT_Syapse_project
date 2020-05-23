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


class Chronicle_Surgery_And_Radiation:

    # field_locators is dictionary where key represents field name and value represents locators
    #below field_locators are for 'Cancer surgery'
    field_locators = {'Cancer surgery date': 'cancerSurgeryDate',
                      'Cancer surgery type/name': 'cancerSurgeryName',
                      'Purpose of surgery': 'surgeryPurpose',
                      'Local treatment outcome': 'treatmentOutcome',
                      'Comments': 'surgeryComment',
                      }

    #below field_locators are for 'Radiation Therapy"'
    radiation_field_locators = {'RadOnc modality name': 'radOncModalityName',
                      'Purpose of radiation treatment': 'radiationPurpose',
                      'Region treated': 'regionTreated',
                      'RadOnc fraction': 'radOncFraction',
                      'RadOnc total dose administered': 'radOncTotalDoseAdmin',
                      'RadOnc start date': 'radOncStartDate',
                      'RadOnc end date': 'radOncEndDate',
                      'RadOnc site type': 'radOncSiteType',
                      'RadOnc body type': 'radOncBodyType',
                      'Comments': 'radiationComment'
                      }

    # below are locators of element of [cancerSurgery] present on [Surgery and Radiation] tab
    section='cancerSurgery'
    section1_locator_for_verification=section+"__0"
    section2_locator_for_verification = section+"__1"
    section3_locator_for_verification = section+"__2"
    section1_locator=section1_locator_for_verification+"__"
    section2_locator= section2_locator_for_verification+"__"
    section3_locator = section3_locator_for_verification+"__"


    # remove links for cancerSurgery
    remove_link1 = section2_locator+'removeLink'
    remove_link2= section3_locator+'removeLink'


    # below are element locators of [Radiation Therapy]
    radiation_section="Radiation Therapy"
    radiation_section1_for_verification = "radiationTherapy__0"
    radiation_section2_for_verification = "radiationTherapy__1"
    radiation_section1_locator=radiation_section1_for_verification+'__'
    radiation_section2_locator = radiation_section2_for_verification+"__"


    # remove links for [Radiation Therapy]
    radiation_remove_link1 = 'radiationTherapy__0__removeLink'

    #tab-name
    Surgery_and_Radiation_tab_name ="Surgery and Radiation"

    # to initialize
    def __init__(self, app):
        self.app = app

    # use of below method is to navigate to [Surgery and Radiation] tab which comes under [Patient Data Entry]
    def chronicle_tab_Surgery_and_Radiation(self):
        self.app.chronicle.chronicle_tab(self.Surgery_and_Radiation_tab_name)

    def click_Add_Another_for_Cancer_Surgery(self):
        self.app.chronicle.click_button_for_section_and_role(button='Add Another',section=self.section,role='button')

    # use of below method is to verify vocab for [Surgery_and_Radiation] tab where dict is dictionary which is passed in test file , section is defined at the top
    def verify_vocab_for_Surgery_and_Radiation(self,dict,section=section1_locator):
        self.app.chronicle.verify_vocab_for(section_name=section,data=dict)

    # use of below method is to fill the Surgery fields where dict is dictionary which is passed in test file , section is defined at the top
    def fill_out_the_fields_for_SurgeryandRadiation(self, dict, section_name=section1_locator):
        '''
        purpose - Fill up all the fields in SurgeryandRadiation-section 1 and Save'''
        dict1 = self.app.chronicle.create_dict_for_locators_value(data=dict,field_locator=self.field_locators)
        log.info(dict1)
        self.app.chronicle.fill_out_the_fields(tab_name=self.Surgery_and_Radiation_tab_name, section_name=section_name, data=dict1)

    # use of below method is to fill the Radiation fields where dict is dictionary which is passed in test file , section is defined at the top
    def fill_out_the_fields_for_Radiation(self, dict, section_name=radiation_section1_locator):
        dict1 = self.app.chronicle.create_dict_for_locators_value(data=dict, field_locator=self.radiation_field_locators)
        log.info(dict1)
        self.app.chronicle.fill_out_the_fields(tab_name=self.Surgery_and_Radiation_tab_name, section_name=section_name,data=dict1)

    # use of below method is to verify the values of SurgeryandRadiation fields where dict is dictionary which is passed in test file , section is defined at the top
    def values_verification_for_SurgeryandRadiation(self, dict, section=section1_locator_for_verification):
        '''
                purpose - Verify all the fields value in Systemic Therapy'''
        self.app.chronicle.chronicle_tab_values_verification(tab_name=self.Surgery_and_Radiation_tab_name, section=section, data=dict)

    # use of below method is to verify that 'No Cancer Surgeries' text is present when there is no data
    def verify_text_No_Cancer_Surgeries_present(self):
        self.app.chronicle.verify_text_present_on_page('No Cancer Surgeries')

    #use of below method is to verify given section is displayed
    #section_name is the locator of section defined at the top
    def verify_section_is_displayed(self,section_name = section2_locator_for_verification):
        self.app.chronicle.verify_section_is_displayed( section_name=section_name , cond='not')

    # use of below method is to remove all sections form Cancer Surgery and save
    def remove_all_sections_from_SurgeryOrCancerSurgery(self):
        """
            Chronicle - Remove all sections for surgery/Cancer Surgery section
        """
        # app.navigation.refresh_page()
        log.info("Remove all sections/data before starting the test-if there is any")
        self.chronicle_tab_Surgery_and_Radiation()
        self.app.navigation.hide_header()
        self.app.navigation.hide_footer()
        self.app.chronicle.remove_all_sections()
        self.chronicle_tab_Surgery_and_Radiation()
        if self.app.chronicle.verify_text_present_on_page("No Cancer Surgeries"):
            log.info("All sections has been removed from Cancer Surgery")
            assert True, 'All sections has not been removed from Cancer Surgery'
        else:
            log.info("All sections has not been removed from Cancer Surgery")

    # use of below method is to remove data from all fields from cancer surgery before changing them
    #field_locator is dictionary of fields name and locator pairs , section_name is locator of section ,both are defined at the top
    def remove_data_from_all_fields(self, field_locator=field_locators, section_name=section1_locator):

        log.info("clear field's data before changing it")
        self.app.chronicle.remove_date_from_calendar_field((section_name + field_locator["Cancer surgery date"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["Cancer surgery type/name"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Purpose of surgery"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Local treatment outcome"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["Comments"]).replace(" ", ""))
        log.info("cleared....")

    # use of below method is to verify that 'No Radiation Therapies' text is present when there is no data under Radiation Therapy
    def verify_text_No_Radiation_Therapies(self):
        if self.app.chronicle.verify_text_present_on_page("No Radiation Therapies"):
            return True

    # use of below method is to remove all sections form Radiation Therapy and save
    def remove_all_sections_from_RadiationTherapy(self):
        """
            Chronicle - Remove all sections for surgery/Cancer Surgery section
        """
        # app.navigation.refresh_page()
        log.info("Remove all sections/data before starting the test-if there is any")
        self.chronicle_tab_Surgery_and_Radiation()
        self.app.navigation.hide_header()
        self.app.navigation.hide_footer()
        self.app.chronicle.remove_all_sections()
        self.chronicle_tab_Surgery_and_Radiation()
        if self.verify_text_No_Radiation_Therapies():
            log.info("All sections has been removed from radiation Therapy")
            assert True, 'All sections has not been removed from radiation Therapy'
        else:
            log.info("All sections has not been removed from radiation Therapy")

    # use of below method is to remove data from all fields from Radiation therapybefore changing them
    #field_locator is dictionary of fields name and locator pairs , section_name is locator of section ,both are defined at the top
    def remove_all_fields_data_from_radiation(self, field_locator=radiation_field_locators, section_name=radiation_section1_locator):

        log.info("clear field's data before changing it")
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["RadOnc modality name"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Purpose of radiation treatment"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["Region treated"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["RadOnc fraction"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["RadOnc total dose administered"]).replace(" ", ""))
        self.app.chronicle.remove_date_from_calendar_field_if_present((section_name + field_locator["RadOnc start date"]).replace(" ", ""))
        self.app.chronicle.remove_date_from_calendar_field_if_present((section_name + field_locator["RadOnc end date"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["RadOnc site type"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["RadOnc body type"]).replace(" ", ""))
        self.app.chronicle.clear_input_field_using_backspace((section_name + field_locator["Comments"]).replace(" ", ""))
        log.info("cleared....")

