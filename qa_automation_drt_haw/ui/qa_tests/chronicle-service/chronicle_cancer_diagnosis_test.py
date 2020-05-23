import pytest
import time
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_elements

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
user_first_last_name = pytest.data.get_user('portal_chronicle')['full_name']

patient = pytest.data.get_patient_first_last_name('patient_cancer_diagnosis')
PDS_service_name= pytest.data.get_service_name('PDS')

#patient does not have data for 'vital status' field
patient_without_vital_status=pytest.data.get_patient_first_name('patient_without_vital_status')

#  below are the data which comes from fixture_data.json file to fill the fields of cancer Diagnosis
fields_data1 = pytest.data.get_data('Chronicle_Cancer_Diagnosis_data2')
fields_data2 = pytest.data.get_data('Chronicle_Cancer_Diagnosis_data3')
fields_data3 = pytest.data.get_data('Chronicle_Cancer_Diagnosis_data4')
fields_data4 = pytest.data.get_data('Chronicle_Cancer_Diagnosis_data5')

# below are the data which comes from fixture_data.json file to enter value in 'Distant metastasis or recurrence sites' fields
value1=pytest.data.get_data('Cancer_Diagnosis_Distant_metastasis_value1')
value2=pytest.data.get_data('Cancer_Diagnosis_Distant_metastasis_value2')
value3=pytest.data.get_data('Cancer_Diagnosis_Distant_metastasis_value3')

# below are the data which comes from fixture_data.json file to verify multiple Distant_metastasis fields value
Distant_metastasis_data1=pytest.data.get_data('Cancer_Diagnosis_Distant_metastasis_data1')
Distant_metastasis_data2=pytest.data.get_data('Cancer_Diagnosis_Distant_metastasis_data2')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()

@pytest.mark.p3
@pytest.mark.p4
def test_save_without_vital_status(app_test,test_info):
    """
    Chronicle - Cancer Diagnosis - Fill up all the fields without selecting Vital status
    """
    log.info("Test Started- to Fill up all the fields without selecting Vital status")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient_without_vital_status)
    app_test.chronicle.click_Add_Another()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_cancer_diagnosis.fill_out_the_fields_for_Cancer_Diagnosis(dict=fields_data1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_cancer_diagnosis.verify_text_No_Cancer_Diagnosis_present()
    log.info("Test passed- if all the fields without selecting Vital status filled then it will not save")

@pytest.mark.p3
def test_fill_up_all_fields_no_save(app_test, pick_patient_for_chronicle, test_info):
    """
     Chronicle - Cancer Diagnosis - Fill up all the fields without saving
    """
    log.info("Test Started- to Fill up all the fields without saving")
    #clear data before starting the test-if there is any
    app_test.chronicle_cancer_diagnosis.remove_all_sections_from_Cancer_Diagnosis()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_cancer_diagnosis.chronicle_tab_Cancer_Diagnosis()
    app_test.chronicle.click_Add_Another()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_cancer_diagnosis.fill_out_the_fields_for_Cancer_Diagnosis(dict=fields_data2)
    app_test.navigation.refresh_page()
    app_test.chronicle_cancer_diagnosis.verify_text_No_Cancer_Diagnosis_present()
    log.info("Test passed- all fields are not saved without saving")

@pytest.mark.p1
def test_fill_up_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
      Chronicle - Cancer Diagnosis - Fill up all the fields and Save
    """
    log.info("Test Started- to Fill up all the fields and Save")
    # clear data before starting the test
    app_test.chronicle_cancer_diagnosis.remove_all_sections_from_Cancer_Diagnosis()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_cancer_diagnosis.chronicle_tab_Cancer_Diagnosis()
    app_test.chronicle.click_Add_Another()

    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_cancer_diagnosis.fill_out_the_fields_for_Cancer_Diagnosis(dict=fields_data1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=fields_data1)
    log.info("Test passed- all the fields are Saved and verified successfully")

@pytest.mark.p3
def test_cancer_diagnosis_add_another(app_test,pick_patient_for_chronicle,test_info):
    """
      Chronicle - Cancer Diagnosis - Add Another
    """
    log.info("Test Started-  Add Another section in Cancer Diagnosis")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle.add_another_section(app_test.chronicle_cancer_diagnosis.section_type)
    app_test.chronicle_cancer_diagnosis.fill_out_the_fields_for_Cancer_Diagnosis(dict=fields_data3,section_name=app_test.chronicle_cancer_diagnosis.section_2_locator)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=fields_data1)
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=fields_data3,section=app_test.chronicle_cancer_diagnosis.section_2_locator_for_verification)
    log.info("Test passed- Another section in Cancer Diagnosis is added and verified successfully")

@pytest.mark.p2
def test_change_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
      Chronicle - Cancer Diagnosis - Change values in all the fields and Save,
      Verify changes in the first section do not affect second section
    """
    log.info("Test Started- to Verify that changes in the first section do not affect second section")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_cancer_diagnosis_add_another(app_test,pick_patient_for_chronicle,test_info)
    app_test.navigation.refresh_page()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_cancer_diagnosis.remove_data_from_all_fields()
    app_test.chronicle_cancer_diagnosis.fill_out_the_fields_for_Cancer_Diagnosis(dict=fields_data4)
    app_test.chronicle.biomarker_field_input(app_test.chronicle_cancer_diagnosis.vocab,
                                        field_name=app_test.chronicle_cancer_diagnosis.distantMetastasis_locator,
                                        values=value3)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=fields_data4)
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=Distant_metastasis_data2)

    # Verify changes in the first section do not affect second section
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=fields_data3,
                                                                            section=app_test.chronicle_cancer_diagnosis.section_2_locator_for_verification)
    log.info("Test passed- changes in the first section do not affect second section")

@pytest.mark.p3
def test_distant_metastasis_and_recurrence_sites_add_multiple(app_test, pick_patient_for_chronicle, test_info):
    """
     Chronicle - Cancer Diagnosis - Distant metastasis or recurrence sites - Add multiple values
    """
    log.info("Test Started- to  Add multiple values for Distant metastasis or recurrence sites ")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle.add_another_section(app_test.chronicle_cancer_diagnosis.field_type)
    app_test.chronicle.biomarker_field_input(app_test.chronicle_cancer_diagnosis.vocab,field_name=app_test.chronicle_cancer_diagnosis.Distant_metastasis_locator1,values=value1)

    app_test.chronicle.add_another_section(app_test.chronicle_cancer_diagnosis.field_type)
    app_test.chronicle.biomarker_field_input(app_test.chronicle_cancer_diagnosis.vocab,
                                        field_name=app_test.chronicle_cancer_diagnosis.Distant_metastasis_locator2,
                                        values=value2)

    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=Distant_metastasis_data1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=Distant_metastasis_data1)
    log.info("Test passed- multiple values for Distant metastasis or recurrence sites are added and verified successfully")











