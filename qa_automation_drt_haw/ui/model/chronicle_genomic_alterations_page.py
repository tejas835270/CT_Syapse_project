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


class Chronicle_Genomic_Alterations:

    # field_locators is dictionary where key represents  field name and value represents locators
    field_locators = {
        'Report Result Date': 'reportResultDate',
        'Specimen Collection Date': 'specimenCollectionDate',
        'Sample Type': 'sampleType',
        'Test Name': 'testName',
        'Test Type': 'testType',
        'Biomarkers': 'biomarkers',
        'Comments': 'alterationComment'

    }

    # below are locators of element  present on [patient status] tab
    section_name1_for_verification = "genomicAlterations__0"
    section_name2_for_verification = "genomicAlterations__1"
    section_name1 = section_name1_for_verification+"__"
    section_name2 = section_name2_for_verification+'__'
    field_name = (section_name1 + field_locators["Biomarkers"]).replace(" ", "")
    field_name2 = (section_name2 + field_locators["Biomarkers"]).replace(" ", "")

    #section remove links
    section1_remove_link=section_name1+'removeLink'

    #tab-name
    Genomic_tab_name="Genomic Alterations"
    Section= 'Genomic Alteration'

    # below is the data which comes from fixture_data.json file
    # fields_data1 = pytest.data.get_data('Chronicle_Vital_Status_data6')

    # to initialize
    def __init__(self, app):
        self.app = app

    # use of below method is to navigate to [Genomic Alterations] tab which comes under [Patient Data Entry]
    #Genomic_tab_name stores the tab name
    def chronicle_tab_Genomic_Alterations(self):
        self.app.chronicle.chronicle_tab(self.Genomic_tab_name)

    # use of below method is to verify vocab for [Genomic Alterations] tab where dict is dictionary which is passed in test file , section is defined at the top
    def verify_vocab_for_genomicAlterations(self,dict,section=section_name1):
        self.app.chronicle.verify_vocab_for(section_name=section,data=dict)

     # use of below method is to fill the [Genomic Alterations] fields where dict is dictionary which is passed in test file , section is defined at the top
    def fill_out_the_fields_for_Geonomic_alterations(self, dict, section_name=section_name1):
        '''purpose - Fill up all the fields in [Genomic Alterations]-section 1 and Save'''
        dict1 = self.app.chronicle.create_dict_for_locators_value(data=dict, field_locator=self.field_locators)
        log.info(dict1)
        self.app.chronicle.fill_out_the_fields(tab_name=self.Genomic_tab_name, section_name=section_name, data=dict1)

    # to select values in biomarkers where values given in test file and field_name is given at the top
    def select_biomarkers(self,values,field_name=field_name):
        self.app.chronicle.biomarker_field_input(cond='Biomarker', field_name=field_name, values=values)

    # use of below method is to verify the biomarker fields where dict is dictionary which is passed in test file , section is defined at the top
    def verify_biomarkers_values(self,dict, section = section_name1_for_verification):
        self.app.chronicle.chronicle_tab_values_verification(tab_name=self.Genomic_tab_name, section=section, data=dict)


    # use of below method is to verify the values of [Genomic Alterations] fields where dict is dictionary which is passed in test file , section is defined at the top
    def values_verification_for_Geonomic_alterations(self, dict, section=section_name1_for_verification):
        '''purpose - Verify all the fields value in Systemic Therapy'''
        self.app.chronicle.chronicle_tab_values_verification(tab_name=self.Genomic_tab_name, section=section, data=dict)

    #use of below method is to verify given section is displayed where section_name is setion's locator defined at the top
    def verify_section_is_displayed(self,section_name = section_name2_for_verification):
        self.app.chronicle.verify_section_is_displayed( section_name=section_name , cond='not')

    # use of below method is to remove all the existing sections from Geonomic_alterations
    def remove_all_sections_from_Geonomic_alterations(self):
        """
            Chronicle - Systematic_therapy - Remove all sections
        """
        # app.navigation.refresh_page()
        log.info("clear data before starting the test-if there is any")
        self.chronicle_tab_Genomic_Alterations()
        self.app.navigation.hide_header()
        self.app.navigation.hide_footer()
        self.app.chronicle.remove_all_sections()
        self.chronicle_tab_Genomic_Alterations()
        if self.app.chronicle.verify_text_present_on_page("No Genomic Alterations"):
            log.info("All sections has been removed from Genomic Alterations")
            assert True, 'All sections has not been removed from Genomic Alterations'
        else:
            log.info("All sections has not been removed from Genomic Alterations")

    # use of below method is to clear all the data from [geonomic alterations] fields and do not save
    #field_locator is dictionary of fields name and locator pairs , section_name is locator of section ,both are defined at the top
    def remove_data_from_all_fields(self, biomarker_value,field_locator=field_locators, section_name=section_name1):
        log.info("clear field data before changing it")
        self.app.chronicle.remove_date_from_calendar_field( (section_name + field_locator["Report Result Date"]).replace(" ", ""))
        self.app.chronicle.remove_date_from_calendar_field( (section_name + field_locator["Specimen Collection Date"]).replace(" ", ""))
        self.app.chronicle.remove_option_from_dropdown_if_data_present((section_name + field_locator["Sample Type"]).replace(" ", ""))
        self.app.chronicle.clear_input_field((section_name + field_locator["Test Name"]).replace(" ", ""))
        self.app.chronicle.clear_input_field((section_name + field_locator["Test Type"]).replace(" ", ""))
        self.app.chronicle.clear_input_field((section_name + field_locator["Comments"]).replace(" ", ""))
        self.app.chronicle.remove_selected_biomarkers(field_name=self.field_name,values=biomarker_value)
        # self.values_verification_for_VitalandDisease_Status(self.fields_data1)
        log.info("cleared....")
