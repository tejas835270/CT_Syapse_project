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


class Chronicle_Cancer_Diagnosis:

    # field_locators is dictionary where key represents field name and value represents locators
    field_locators = {
                        'Diagnosis Date': 'diagnosisDate',
                        'Primary Site': 'primarySite',
                        'Histology': 'histology',
                        'Tumor type (Oncotree)': 'tumorType',
                        'Tumor size (mm)': 'tumorSize',
                        'cT': 'cT',
                        'cN': 'cN',
                        'cM': 'cM',
                        'Clinical stage group': 'cStageGroup',
                        'pT': 'pT',
                        'pN': 'pN',
                        'pM': 'pM',
                        'Pathologic stage group': 'pStageGroup',
                        'AJCC staging version': 'ajccStagingVersion',
                        'Distant metastasis or recurrence sites': 'distantMetastasis',
                        'Comments': 'diagnosisComment',
                      }

    # section-names and locators
    section_0 = 'cancerDiagnoses__0'
    section_1_locator = section_0+"__"
    section_2_locator_for_verification = 'cancerDiagnoses__1'
    section_2_locator = section_2_locator_for_verification+'__'


    # below variable are created to store locators of elements which are required to enter values
    DiagnosisDate_locator=(section_1_locator + field_locators["Diagnosis Date"]).replace(" ", "")
    primarySite_locator=(section_1_locator + field_locators["Primary Site"]).replace(" ", "")
    histology_locator=(section_1_locator + field_locators["Histology"]).replace(" ", "")
    tumorType_locator=(section_1_locator + field_locators["Tumor type (Oncotree)"]).replace(" ", "")
    tumorSize_locator=(section_1_locator + field_locators["Tumor size (mm)"]).replace(" ", "")

    cT_locator=(section_1_locator + field_locators["cT"]).replace(" ", "")
    cN_locator=(section_1_locator + field_locators["cN"]).replace(" ", "")
    cM_locator = (section_1_locator + field_locators["cM"]).replace(" ", "")
    cStageGroup_locator=(section_1_locator + field_locators["Clinical stage group"]).replace(" ", "")
    pT_locator= (section_1_locator + field_locators["pT"]).replace(" ", "")
    pN_locator=(section_1_locator + field_locators["pN"]).replace(" ", "")
    pM_locator=(section_1_locator + field_locators["pM"]).replace(" ", "")
    pStageGroup_locator=(section_1_locator + field_locators["Pathologic stage group"]).replace(" ", "")
    AJCS_staging_locator=(section_1_locator + field_locators["AJCC staging version"]).replace(" ", "")
    distantMetastasis_locator='cancerDiagnoses__0__distantMetastasis__0'
    Comments_locator=(section_1_locator + field_locators["Comments"]).replace(" ", "")

    # below are locators of  Distant_metastasis fields
    distantMetastasis_locator0 = 'cancerDiagnoses__0__distantMetastasis'
    Distant_metastasis_locator1 = distantMetastasis_locator0+'__1'
    Distant_metastasis_locator2 = distantMetastasis_locator0+'__2'

    #button types
    section_type='section'
    field_type='field'
    vocab='Vocab'

    # below variable stores UI text data
    #tab-name
    CancerDiagnosis_tab_name="Cancer Diagnosis"

    #add-another button name
    Add_another_button_name="Add Another"

    #when there is no data or sections then below text should be present
    No_Cancer_Diagnosis_text="No Cancer Diagnoses"

    # below is the data which comes from fixture_data.json file
    # fields_data1 = pytest.data.get_data('Chronicle_Vital_Status_no_data')

    #to initialize
    def __init__(self, app):
        self.app = app

    # use of below method is to navigate to [Cancer_Diagnosis] tab which comes under [Patient Data Entry]
    def chronicle_tab_Cancer_Diagnosis(self):
        self.app.chronicle.chronicle_tab(self.CancerDiagnosis_tab_name)

    # use of below method is to click add another button for [Cancer_Diagnosis]
    def click_Add_Another_for_Cancer_Diagnosis(self):
        self.app.navigation.click_button_for_section(self.Add_another_button_name, self.CancerDiagnosis_tab_name)

    # use of below method is to verify vocabulary for [Cancer_Diagnosis] fields , where dict is data dictionary which is passed from test file ,section is sections's locator defined at the top
    def verify_vocab_for_cancerDiagnoses(self,dict,section=section_1_locator):
        self.app.chronicle.verify_vocab_for(section_name=section, data=dict)

    # use of below method is type and verify the vocabulary DATA for [primarySite] field , where input is data which can be passed from test file currently given default value as 'br'
    # primarySite_locator is the locator of [primarySite] field
    def primarySite_type_and_verify_vocab(self,input='br'):
        self.app.chronicle.type_and_verify_vocab(input, self.primarySite_locator)

    # use of below method is type and verify the non vocabulary data for [primarySite] field , where input is data which can be passed from test file currently given default value as 'www'
    # primarySite_locator is the locator of [primarySite] field
    def primarySite_type_and_verify_empty_result(self,input='www'):
        self.app.chronicle.type_and_verify_empty_result(input,self.primarySite_locator)

    # use of below method is type and verify the vocabulary data for [histology] field , where input is data which can be passed from test file currently given default value as 'fibro'
    # histology_locator is the locator of [histology] field
    def histology_type_and_verify_vocab(self,input='fibro'):
        self.app.chronicle.type_and_verify_vocab(input, self.histology_locator)

    # use of below method is type and verify the NON vocabulary data for [histology] field , where input is data which can be passed from test file currently given default value as '111'
    # histology_locator is the locator of [histology] field
    def histology_type_and_verify_empty_result(self,input='111'):
        self.app.chronicle.type_and_verify_empty_result(input, self.histology_locator)

    # use of below method is type and verify the vocabulary data for [tumorType] field , where input is data which can be passed from test file currently given default value as 'basa'
    # tumorType_locator is the locator of [tumorType] field
    def tumorType_type_and_verify_vocab(self, input='basa'):
        self.app.chronicle.type_and_verify_vocab(input, self.tumorType_locator)

    # use of below method is type and verify the non vocabulary data for [tumorType] field , where input is data which can be passed from test file currently given default value as 'five'
    # tumorType_locator is the locator of [tumorType] field
    def tumorType_type_and_verify_empty_result(self, input='five'):
        self.app.chronicle.type_and_verify_empty_result(input, self.tumorType_locator)

    # use of below method is type and verify the vocabulary data for [cT] field , where input is data which can be passed from test file currently given default value as 'nos'
    # cT_locator is the locator of [cT] field
    def cT_type_and_verify_vocab(self, input='nos'):
        self.app.chronicle.type_and_verify_vocab(input, self.cT_locator)

    # use of below method is type and verify the non vocabulary data for [cT] field , where input is data which can be passed from test file currently given default value as 'cM'
    # cT_locator is the locator of [cT] field
    def cT_type_and_verify_empty_result(self, input='cM'):
        self.app.chronicle.type_and_verify_empty_result(input, self.cT_locator)

    # use of below method is type and verify the vocabulary data for [cN] field , where input is data which can be passed from test file currently given default value as 'n0'
    # cN_locator is the locator of [cN] field
    def cN_type_and_verify_vocab(self, input='n0'):
        self.app.chronicle.type_and_verify_vocab(input, self.cN_locator)

    # use of below method is type and verify the non vocabulary data for [cN] field , where input is data which can be passed from test file currently given default value as 'cM'
    # cN_locator is the locator of [cN] field
    def cN_type_and_verify_empty_result(self, input='cM'):
        self.app.chronicle.type_and_verify_empty_result(input,self.cN_locator)

    # use of below method is type and verify the vocabulary data for [cM] field , where input is data which can be passed from test file currently given default value as 'm1'
    # cM_locator is the locator of [cM] field
    def cM_type_and_verify_vocab(self, input='m1'):
        self.app.chronicle.type_and_verify_vocab(input, self.cM_locator)

    # use of below method is type and verify the non vocabulary data for [cM] field , where input is data which can be passed from test file currently given default value as 'n0'
    # cM_locator is the locator of [cM] field
    def cM_type_and_verify_empty_result(self, input='n0'):
        self.app.chronicle.type_and_verify_empty_result(input, self.cM_locator)

    # use of below method is type and verify the vocabulary data for [cStageGroup] field , where input is data which can be passed from test file currently given default value as 'IIA'
    # cStageGroup_locator is the locator of [cStageGroup] field
    def cStageGroup_type_and_verify_vocab(self, input='IIA'):
        self.app.chronicle.type_and_verify_vocab(input,self.cStageGroup_locator)

    # use of below method is type and verify the NON vocabulary data for [cStageGroup] field , where input is data which can be passed from test file currently given default value as '0N'
    # cStageGroup_locator is the locator of [cStageGroup] field
    def cStageGroup_type_and_verify_empty_result(self, input='0n'):
        self.app.chronicle.type_and_verify_empty_result(input, self.cStageGroup_locator)

    # use of below method is type and verify the vocabulary data for [pT] field , where input is data which can be passed from test file currently given default value as 'T0'
    # pT_locator is the locator of [pT] field
    def pT_type_and_verify_vocab(self, input='T0'):
        self.app.chronicle.type_and_verify_vocab(input, self.pT_locator)

    # use of below method is type and verify the NON vocabulary data for [pT] field , where input is data which can be passed from test file currently given default value as 'M0'
    # pT_locator is the locator of [pT] field
    def pT_type_and_verify_empty_result(self, input='M0'):
        self.app.chronicle.type_and_verify_empty_result(input, self.pT_locator)

    # use of below method is type and verify the vocabulary data for [pN] field , where input is data which can be passed from test file currently given default value as 'n0'
    # pN_locator is the locator of [pN] field
    def pN_type_and_verify_vocab(self, input='n0'):
        self.app.chronicle.type_and_verify_vocab(input, self.pN_locator)

    # use of below method is type and verify the NON vocabulary data for [pN] field , where input is data which can be passed from test file currently given default value as 'M0'
    # pN_locator is the locator of [pN] field
    def pN_type_and_verify_empty_result(self, input='M0'):
        self.app.chronicle.type_and_verify_empty_result(input, self.pN_locator)

    # use of below method is type and verify the vocabulary data for [pM] field , where input is data which can be passed from test file currently given default value as 'm1'
    # pM_locator is the locator of [pM] field
    def pM_type_and_verify_vocab(self, input='m1'):
        self.app.chronicle.type_and_verify_vocab(input, self.pM_locator)

    # use of below method is type and verify the NON vocabulary data for [pM] field , where input is data which can be passed from test file currently given default value as 'N0'
    # pM_locator is the locator of [pM] field
    def pM_type_and_verify_empty_result(self, input='n0'):
        self.app.chronicle.type_and_verify_empty_result(input, self.pM_locator)

    # use of below method is type and verify the vocabulary data for [pStageGroup] field , where input is data which can be passed from test file currently given default value as 'II'
    # pStageGroup_locator is the locator of [pStageGroup] field
    def pStageGroup_type_and_verify_vocab(self, input='II'):
        self.app.chronicle.type_and_verify_vocab(input, self.pStageGroup_locator)

    # use of below method is type and verify the non vocabulary data for [pStageGroup] field , where input is data which can be passed from test file currently given default value as 'n0'
    # pStageGroup_locator is the locator of [pStageGroup] field
    def pStageGroup_type_and_verify_empty_result(self, input='n0'):
        self.app.chronicle.type_and_verify_empty_result(input, self.pStageGroup_locator)

    # use of below method is type and verify the vocabulary data for [distantMetastasis] field , where input is data which can be passed from test file currently given default value as 'nodes'
    # distantMetastasis_locator0 is the locator of [distantMetastasis] field
    def distantMetastasis_type_and_verify_vocab(self, input='nodes'):
        self.app.chronicle.type_and_verify_vocab(input, self.distantMetastasis_locator0)

    # use of below method is to fill the Cancer_Diagnosisfields where dict is dictionary which is passed in test file , section is defined at the top
    def fill_out_the_fields_for_Cancer_Diagnosis(self, dict, section_name=section_1_locator):
        '''
        purpose - Fill up all the fields in Systemic Therapy-section 1 and Save'''
        dict1 = self.app.chronicle.create_dict_for_locators_value(data=dict, field_locator=self.field_locators)
        log.info(dict1)
        self.app.chronicle.fill_out_the_fields(tab_name=self.CancerDiagnosis_tab_name, section_name=section_name,
                                               data=dict1)

    # use of below method is to verify the values of Cancer_Diagnosis fields where dict is dictionary which is passed in test file , section is defined at the top
    def values_verification_for_Cancer_Diagnosis(self, dict, section=section_0):
        '''purpose - Verify all the fields value in Systemic Therapy'''
        self.app.chronicle.chronicle_tab_values_verification(tab_name=self.CancerDiagnosis_tab_name,section=section,data=dict)

    # use of below method is to remove all the data from fields of Cancer Diagnosis and dont click save button , just clear the fields
    def remove_data_from_all_fields(self):
        log.info("clear field data before changing it")
        self.app.chronicle.remove_date_from_calendar_field_if_present(self.DiagnosisDate_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.primarySite_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.histology_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.tumorType_locator)
        self.app.chronicle.clear_input_field(self.tumorSize_locator)
        #clinical stage
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.cT_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.cN_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.cM_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.cStageGroup_locator)
        #Pathologic stage
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.pT_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.pN_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.pM_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.pStageGroup_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.AJCS_staging_locator)
        self.app.chronicle.remove_option_from_dropdown_if_data_present(self.distantMetastasis_locator)
        self.app.chronicle.clear_input_field(self.Comments_locator)
        #self.values_verification_for_Cancer_Diagnosis(dict=fields_data1)
        log.info("cleared....")

    # use of below method is to verify that 'No Cancer Diagnoses' text is present when there is no data under Disease_Status
    # No_Cancer_Diagnosis_text variable stores the expected text 'No Cancer Diagnoses'
    def verify_text_No_Cancer_Diagnosis_present(self):
        if self.app.chronicle.verify_text_present_on_page(self.No_Cancer_Diagnosis_text):
            return True
        else:
            return False

    # use of below method is to remove all sections from Cancer_Diagnosis , save and then verify
    def remove_all_sections_from_Cancer_Diagnosis(self):
        """
            Chronicle - Cancer_Diagnosis - Remove all sections
        """
        log.info("clear data before starting the test-if there is any")
        self.chronicle_tab_Cancer_Diagnosis()
        self.app.navigation.hide_header()
        self.app.navigation.hide_footer()
        self.app.chronicle.remove_all_sections()
        self.chronicle_tab_Cancer_Diagnosis()
        if self.verify_text_No_Cancer_Diagnosis_present():
            log.info("All sections has been removed from Cancer_Diagnosis")
            assert True, 'All sections has not been removed from Cancer_Diagnosis'
        else:
            log.info("All sections has not been removed from Cancer_Diagnosis")

