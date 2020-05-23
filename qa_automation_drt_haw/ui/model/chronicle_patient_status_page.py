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


class Chronicle_Patient_Status:

    # field_locators is dictionary where key represents  field name and value represents locators
    #below dictionary is for [vital status] section
    field_locators = {
        'Date of last contact': 'dateOfLastContact',
        'Date of death': 'dateOfDeath',
        'Cause of death': 'causeOfDeath',
        'Data Source': 'dataSource',
        'Comments': 'vitalComment'
    }
    # below are locators of element present under [vital status]section
    section = "vitalStatus"
    Date_of_last_contact = "vitalStatus__dateOfLastContact"
    Date_of_death = "vitalStatus__dateOfDeath"
    Cause_of_death = "vitalStatus__causeOfDeath"
    Data_Source = "vitalStatus__dataSource"
    Comments = "vitalStatus__vitalComment"
    vitalStatus__section_name = section+"__"

    # tab-name
    Patient_Status_tab_name = "Patient Status"
    Cancer_Diagnosis_tab_name="Cancer Diagnosis"

    # link-names
    Use_this_result = 'Use this result'
    select_from_existing_data = 'Select from existing data'

    # field_locators is dictionary where key represents  field name and value represents locators
    #below dictionary is for [Disease status] section
    Disease_field_locators = {
        'Disease status date': 'diseaseStatusDate',
        'Disease Status': 'diseaseStatus',
        'Extent of disease': 'extentOfDisease',
        'Distant metastasis or recurrence sites': 'distantMetastasis',
        'Comments': 'diseaseComment'
    }

    # below are locators of sections present under [Disease status]section
    disease_section="diseaseStatus"
    disease_section1_for_verification=disease_section+"__0"
    disease_section2_for_verification = disease_section+"__1"
    disease_section1 = disease_section1_for_verification+"__"
    disease_section2 = disease_section2_for_verification+"__"


    # below are locators of element present under [Disease status]section
    Disease_status_date_locator = (disease_section1 + Disease_field_locators["Disease status date"]).replace(" ", "")
    Disease_Status_locator =(disease_section1 + Disease_field_locators["Disease Status"]).replace(" ", "")
    Extent_of_disease_locator='diseaseStatus__0__extentOfDisease__0'
    Distant_metastasis_locator ='diseaseStatus__0__distantMetastasis__0'
    Comments_locator =(disease_section1 + Disease_field_locators["Comments"]).replace(" ", "")

    # below are locators of  Distant_metastasis fields
    Distant_metastasis_locator0 = 'diseaseStatus__0__distantMetastasis'
    Distant_metastasis_locator_0 = Distant_metastasis_locator0+'__0'
    Distant_metastasis_locator1=Distant_metastasis_locator0+'__1'
    Distant_metastasis_locator2=Distant_metastasis_locator0+'__2'
    Remove_Distant_metastasis_fields ='diseaseStatus__0__distantMetastasis__0, diseaseStatus__0__distantMetastasis__1'

    # below are locators of Extent of disease fields
    Extent_of_disease_locator0 ='diseaseStatus__0__extentOfDisease'
    Extent_of_disease_locator_0 =Extent_of_disease_locator0+'__0'
    Extent_of_disease_locator1 = Extent_of_disease_locator0+'__1'
    Extent_of_disease_locator2 = Extent_of_disease_locator0+'__2'


    # remove links of  diseaseStatus
    diseaseStatus_removelink1='diseaseStatus__0__removeLink'

    # locator of add another button of  Distant_metastasis
    Distant_metastasis_add_another='add-another-distantMetastasis'
    Extent_of_disease_add_another = 'add-another-extentOfDisease'

    #below variable stores UI text data
    No_Disease_status_text = 'No Disease status'
    Alive="Alive"
    Deceased='Deceased'
    error_msg_text='This field is required'

    # below is the data which comes from fixture_data.json file
   #fields_data1 = pytest.data.get_data('Chronicle_Vital_Status_no_data')

    # to initialize
    def __init__(self, app):
        self.app = app

    # use of below method is to navigate to [patient status] tab which comes under [Patient Data Entry]
    def chronicle_tab_Patient_Status(self):
        self.app.chronicle.chronicle_tab(self.Patient_Status_tab_name)

    # use of below method is to select  Alive radio button under vital status
    def select_Alive_radiobutton(self):
        self.app.chronicle.select_radiobutton(self.Alive)

    # use of below method is to select  Deceased radio button under vital status
    def select_Deceased_radiobutton(self):
        self.app.chronicle.select_radiobutton(self.Deceased)

    # use of below method is to verify that [Use this result] link is disable
    def verify_Use_this_result_is_disable(self):
        self.app.verification.button_is_disable(self.Use_this_result)

    # use of below method is to click add another button for [Cancer_Diagnosis]
    def click_add_another_for_Cancer_Diagnosis(self):
        self.app.navigation.click_button_for_section("Add Another", self.Cancer_Diagnosis_tab_name)

    #use of below method is to fill the vital status fields where dict is dictionary which is passed in test file , section is defined at the top
    def fill_out_the_fields_for_Vital_Status(self, dict, section_name=vitalStatus__section_name):
        '''
        purpose - Fill up all the fields in Systemic Therapy-section 1 and Save'''
        dict1 = self.app.chronicle.create_dict_for_locators_value(data=dict,field_locator=self.field_locators)
        log.info(dict1)
        self.app.chronicle.fill_out_the_fields(tab_name=self.Patient_Status_tab_name, section_name=section_name, data=dict1)

    # use of below method is to verify the values of vital status fields where dict is dictionary which is passed in test file , section is defined at the top
    def values_verification_for_VitalandDisease_Status(self, dict, section=section):
        '''
                purpose - Verify all the fields value in Systemic Therapy'''
        self.app.chronicle.chronicle_tab_values_verification(tab_name=self.Patient_Status_tab_name, section=section, data=dict)

    # use of below method is to enter date in dateOfLastContact field where calendar_field is locator of dateOfLastContact defined at the top, date is given in test file
    def enter_date_into_dateOfLastContact(self , date , calendar_field= Date_of_last_contact ):
        self.app.chronicle.enter_date_into_calendar(calendar_field, date)

    # use of below method is to clear date from dateOfLastContact field where calendar_field is locator of dateOfLastContact defined at the top
    def clear_dateOfLastContact(self , calendar_field=Date_of_last_contact):
        """Chronicle - Patient Status - clear Last Contact
               """
        self. app.chronicle.remove_date_from_calendar_field_if_present(calendar_field)

    # use of below method is to clear date from dateOfLastContact field where calendar_field is locator of dateOfLastContact defined at the top
    def clear_dateOfDeath(self , calendar_field=Date_of_death):
        """Chronicle - Patient Status - clear Date_of_death """
        self. app.chronicle.remove_date_from_calendar_field_if_present(calendar_field)

    # use of below method is to clear all the data from [vital status] fields and save it
    def clear_data_from_patient_status(self):
        """
         Chronicle - Patient Status - clear Last Contact and Save
        """
        log.info("clear all the fields")
        self.remove_data_from_patient_status()
        self.app.chronicle.click_on_save()
        #self.values_verification_for_VitalandDisease_Status(self.fields_data1)
        log.info("cleared")

    # use of below method is to clear all the data from [vital status] fields and dont save it
    # field locators are passed in below functions to remove values and they are defined at the top
    def remove_data_from_patient_status(self):
        """
         Chronicle - Patient Status - clear Last Contact and Save
        """
        log.info("clear all the field data before changing it")
        self.chronicle_tab_Patient_Status()
        self.app.chronicle.remove_date_from_calendar_field_if_present(self.Date_of_last_contact)
        self.app.chronicle.remove_date_from_calendar_field_if_present(self.Date_of_death)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.Data_Source)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.Cause_of_death)
        self.app.chronicle.clear_input_field_using_backspace(self.Comments)
        #self.values_verification_for_VitalandDisease_Status(self.fields_data1)
        log.info("cleared")

    # use of below method is to verify error message if Vital status is not selected
    #error_msg_text variable stores the expected error text
    def verify_error_msg(self):
        self.app.verification.text_present_on_page(page_text=self.error_msg_text)

    #Disease Status section

    # use of below method is to fill the Disease status fields where dict is dictionary which is passed in test file , section is defined at the top
    def fill_out_the_fields_for_Disease_Status(self, dict, section_name=disease_section1):
        dict1 = self.app.chronicle.create_dict_for_locators_value(data=dict, field_locator=self.Disease_field_locators)
        log.info(dict1)
        self.app.chronicle.fill_out_the_fields(tab_name=self.Cancer_Diagnosis_tab_name, section_name=section_name,data=dict1)

    # use of below method is to verify that 'No Disease status' text is present when there is no data under Disease_Status
    def verify_text_No_Disease_status_present(self):
        if self.app.chronicle.verify_text_present_on_page(self.No_Disease_status_text):
            return True

    # use of below method is to remove all sections from Disease_Status , save and then verify
    def remove_all_sections_from_Disease_Status(self):
        """
            Chronicle - Systematic_therapy - Remove all sections
        """
        # app.navigation.refresh_page()
        log.info("clear data before starting the test-if there is any")
        self.chronicle_tab_Patient_Status()
        self.app.navigation.hide_header()
        self.app.navigation.hide_footer()
        self.app.chronicle.remove_all_sections()
        self.chronicle_tab_Patient_Status()
        if self.verify_text_No_Disease_status_present:
            log.info("All sections has been removed from Disease_Status")
            assert True, 'All sections has not been removed from Disease_Status'
        else:
            log.info("All sections has not been removed from Disease_Status")

    # use of below method is to remove all the data from fields of Disease_Status and dont click save button , just clear the fields
    # field locators are passed in below function one by one to remove values and they are defined at the top
    def remove_data_from_Disease_Statusfields(self):
        log.info("clear field data before changing it")
        self.app.chronicle.remove_date_from_calendar_field_if_present(self.Disease_status_date_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.Disease_Status_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.Extent_of_disease_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.Distant_metastasis_locator)
        self.app.chronicle.clear_input_field_using_backspace(self.Comments_locator)
        if self.Distant_metastasis_locator2:
            self.app.chronicle.remove_additional_field(self.Distant_metastasis_locator2)
        if self.Distant_metastasis_locator1:
            self.app.chronicle.remove_additional_field(self.Distant_metastasis_locator1)
        if self.Extent_of_disease_locator1:
            self.app.chronicle.remove_additional_field(self.Extent_of_disease_locator1)
        if self.Extent_of_disease_locator2:
            self.app.chronicle.remove_additional_field(self.Extent_of_disease_locator2)
        log.info("cleared....")

    # use of below method is to select value for "Distant_metastasis and extent Of Disease" (biomarker_field)
    #data and field_name are passed from test file , field_name is defined at the top
    def select_value_for_Distant_metastasis_and_Extent_disease(self, data, field_name):
        self.app.chronicle.biomarker_field_input(cond="Vocab", field_name=field_name,values=data)

    # use of below method is to click [Add Another] button for Distant_metastasis (biomarker_field)
    # Distant_metastasis_add_another is field name and disease_section1_for_verification is section and they are defined at the top
    def click_Add_Another_for_distantMetastasis(self):
        self.app.chronicle.click_button_add_another_for_field_in_section(field=self.disease_section1_for_verification,section=self.Distant_metastasis_add_another)

    # use of below method is to click [Add Another] button for "extent Of Disease" (biomarker_field)
    # disease_section1_for_verification is field name and Extent_of_disease_add_another is section and they are defined at the top
    def click_Add_Another_for_Extent_of_disease(self):
        self.app.chronicle.click_button_add_another_for_field_in_section(field=self.disease_section1_for_verification,
                                                                         section=self.Extent_of_disease_add_another)






