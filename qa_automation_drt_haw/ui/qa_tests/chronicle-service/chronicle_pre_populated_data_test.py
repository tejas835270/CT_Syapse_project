import time
from qa_automation_drt_haw.settings import Config
import pytest

from allure_commons import fixture

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
PDS_service_name= pytest.data.get_service_name('PDS')
data_Only_Alive = pytest.data.get_data('Chronicle_Vital_Status_Alive_Only')

#data for dates - stored in fixture_data.json
date_data1 = pytest.data.get_data('date5')
date_data2 = pytest.data.get_data('date6')

#data for verification
fields_data1 = pytest.data.get_data('Chronicle_Vital_Status_data10')
fields_data2 = pytest.data.get_data('Chronicle_Vital_Status_no_data')
fields_data3 = pytest.data.get_data('Chronicle_Cancer_Diagnosis_data1')
tooltip_text = pytest.data.get_data('tooltip_text')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def login_as_chronicle_user(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    # app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()

#     todo start all test from finder

@pytest.mark.p3
def test_vital_status_alive(app_test, login_as_chronicle_user, test_info):
    """
    Chronicle - Verify Pre-populated information for Vital Status - Alive
    """
    log.info("Test Started- to Verify Pre-populated information for Vital Status - Alive")
    patient = pytest.data.get_patient_first_last_name('patient_info')
    app_test.finder.find_and_pick_patient(patient)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle.Click_select_from_existing_data()
    app_test.chronicle.verify_prepopulated_data(data=data_Only_Alive)
    app_test.chronicle.open_patient_finder()
    log.info("Test Passed- Pre-populated information for Vital Status - Alive is verified successfully")

@pytest.mark.p1
def test_vital_status_deceased_select_and_save(app_test, login_as_chronicle_user, test_info):
    """
    Chronicle - Verify Pre-populated information for Vital Status - Deceased - Select option and Save
    """
    log.info("Test Started- to Verify Pre-populated information for Vital Status - Deceased - Select option and Save")
    #app_test.chronicle.open_patient_finder()
    patient = pytest.data.get_patient_first_last_name('patient_prep_data_deceased')
    patient_data = pytest.data.get_patient('patient_prep_data_deceased')['prep_data']
    app_test.finder.find_and_pick_patient(patient)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.Click_select_from_existing_data()
    app_test.chronicle.verify_prepopulated_data(data=patient_data)
    app_test.chronicle.choose_option_from_prep_info(data=patient_data)
    app_test.chronicle.Click_Use_this_result()
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=patient_data)
    log.info("Test Passed-Pre-populated information for Vital Status - Deceased is saved and verified successfully")

@pytest.mark.p3
def test_vital_status_modify_and_save(app_test,login_as_chronicle_user, test_info):
    """
    Chronicle - Vital Status - Modify pre-populated information and Save
    """
    log.info("Test Started- to Modify pre-populated information and Save")
    #to make test independent - existing data should be selected
    test_vital_status_deceased_select_and_save(app_test, login_as_chronicle_user, test_info)
    patient = pytest.data.get_patient_first_last_name('patient_prep_data_deceased')
    patient_data = pytest.data.get_patient('patient_prep_data_deceased')['prep_data']
    #app_test.finder.find_and_pick_patient(patient)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_patient_status.clear_dateOfLastContact()
    app_test.chronicle_patient_status.enter_date_into_dateOfLastContact(date=date_data1)
    app_test.chronicle_patient_status.clear_dateOfDeath()
    app_test.chronicle.enter_date_into_calendar(calendar_field=app_test.chronicle_patient_status.Date_of_death,date=date_data2)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    # todo expected result
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data1)
    app_test.chronicle.open_patient_finder()
    log.info("Test Passed- pre-populated information modified and Saved successfully")


@pytest.mark.p2
def test_vital_status_select_and_cancel(app_test, login_as_chronicle_user, test_info):
    """
    Chronicle - Pre-population for Vital Status - Select option and Cancel
    """
    log.info("Test Started- Pre-population for Vital Status - Select option and Cancel")
    patient = pytest.data.get_patient_first_last_name('patient_prep_data_alive')
    patient_data = pytest.data.get_patient('patient_prep_data_alive')['prep_data']
    app_test.finder.find_and_pick_patient(patient)
    time.sleep(5)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()

    app_test.chronicle_patient_status.verify_Use_this_result_is_disable()
    app_test.chronicle.Click_select_from_existing_data()
    app_test.chronicle.choose_option_from_prep_info(data=patient_data)
    app_test.chronicle.click_on_cancel()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data2)
    log.info("Test Passed- Pre-population for Vital Status is selected and Cancelled successfully")


@pytest.mark.p3
def test_cancer_no_data(app_test, login_as_chronicle_user, test_info):
    """
    Chronicle - Cancer Diagnosis - No pre-populated data
    """
    log.info("Test Started- Cancer Diagnosis - No pre-populated data")
    patient = pytest.data.get_patient_first_last_name('patient_prep_data_deceased')
    app_test.finder.find_and_pick_patient(patient)
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_patient_status.click_add_another_for_Cancer_Diagnosis()
    app_test.chronicle.verify_tooltip_for_text(what_for=app_test.chronicle_patient_status.select_from_existing_data, tooltip_text=tooltip_text)
    app_test.chronicle.open_patient_finder()
    log.info("Test Passed- Cancer Diagnosis - No pre-populated data")


@pytest.mark.p3
def test_cancer_select_save(app_test, login_as_chronicle_user, test_info):
    """
    Chronicle - Cancer Diagnosis - Verify Pre-populated information - Select option and Save
    """
    log.info("Test Started- to Verify Pre-populated information - Select option and Save")
    patient = pytest.data.get_patient('patient_prep_data_cancer')['first_name']
    patient_data = pytest.data.get_patient('patient_prep_data_cancer')['prep_data']
    patient_diagnosis = pytest.data.get_patient('patient_prep_data_cancer')['cancer_diagnosis']

    app_test.finder.find_and_pick_patient(patient)
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_cancer_diagnosis.chronicle_tab_Cancer_Diagnosis()
    app_test.chronicle_cancer_diagnosis.click_Add_Another_for_Cancer_Diagnosis()
    app_test.chronicle.Click_select_from_existing_data()


    app_test.chronicle.verify_prepopulated_data(data=patient_data)
    app_test.chronicle.choose_option_from_prep_info(data=patient_data)
    app_test.chronicle.Click_Use_this_result()

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=patient_diagnosis)
    app_test.chronicle.open_patient_finder()
    log.info("Test passed- Pre-populated information is Selected and Saved successfully")


@pytest.mark.p3
def test_cancer_modify_save(app_test, login_as_chronicle_user, test_info):
    """
    Chronicle - Cancer Diagnosis - Modify pre-populated information and Save
    """
    log.info("Test Started- to Modify pre-populated information and Save ")
    # to make test independent - existing data should be selected
    test_cancer_select_save(app_test, login_as_chronicle_user, test_info)
    patient = pytest.data.get_patient('patient_prep_data_cancer')['first_name']

    app_test.finder.find_and_pick_patient(patient)
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()

    app_test.chronicle_cancer_diagnosis.remove_data_from_all_fields()
    app_test.chronicle_cancer_diagnosis.fill_out_the_fields_for_Cancer_Diagnosis(dict=fields_data3)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_cancer_diagnosis.values_verification_for_Cancer_Diagnosis(dict=fields_data3)

    log.info("Test Passed- pre-populated information is modified and Saved successfully ")
