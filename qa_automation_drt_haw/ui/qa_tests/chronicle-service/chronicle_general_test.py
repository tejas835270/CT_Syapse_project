import pytest
import time
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
user_first_last_name = pytest.data.get_user('portal_chronicle')['full_name']

patient = pytest.data.get_patient_first_last_name('patient_info')
patient_info = pytest.data.get_patient('patient_info')['info']
PDS_service_name= pytest.data.get_service_name('PDS')


patient_with_deceased_status = pytest.data.get_patient_first_last_name('patient_with_deceased_status')
patient_with_deceased_status_info = pytest.data.get_patient('patient_with_deceased_status')['info']
fields_data1 = pytest.data.get_data('Chronicle_Vital_Status_data')
fields_data2 = pytest.data.get_data('Chronicle_Vital_Status_data2')
fields_data3 = pytest.data.get_data('Chronicle_Vital_Status_data3')
fields_data4 = pytest.data.get_data('Chronicle_Vital_Status_data4')
fields_data5 = pytest.data.get_data('Chronicle_Vital_Status_data5')
date = pytest.data.get_data('date1')
date2 = pytest.data.get_data('date2')
date3 = pytest.data.get_data('date3')

# TODO
# Chronicle - Vital Status - Exit without saving
# Chronicle - Cancer Diagnosis - Enter Date and Save  -- move ?


@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()

@pytest.mark.skip(reason="Need to make them data independent using api strategy, currently skipping as “chronicle-service” is on low priority")
@pytest.mark.p0
@pytest.mark.p4
def test_access_verification(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Access verification
    """
    log.info("Test Started- to verify access to Patient Data Entry")
    app_test.chronicle.verify_url_contains_chronicle()
    log.info("Test Passed-  Patient Data Entry Access is verified successfully")

@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p4
@pytest.mark.p3
def test_patient_demographic_info(app_test, pick_patient_for_chronicle,test_info):
    """
    Patient Details - Verify Patient Demographic Information
    """
    log.info("Test Started- to verify Patient Demographic Information")
    app_test.verification.patient_info(patient, patient_info)
    log.info("Test Passed- Patient Demographic Information is correct")

@pytest.mark.skip(reason="Need to make them data independent using api strategy, currently skipping as “chronicle-service” is on low priority")
@pytest.mark.p4
@pytest.mark.p0
def test_tab_navigation(app_test, pick_patient_for_chronicle,test_info):
    """
    Patient Details - Verify Tab navigation
    """
    log.info("Test Started- to Verify Tab navigations")
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.verification.patient_info(patient, patient_info)
    app_test.chronicle_cancer_diagnosis.chronicle_tab_Cancer_Diagnosis()
    app_test.verification.patient_info(patient, patient_info)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.verification.patient_info(patient, patient_info)
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.verification.patient_info(patient, patient_info)
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.verification.patient_info(patient, patient_info)
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.verification.patient_info(patient, patient_info)
    log.info("Test Passed- Tab navigations successful")

@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p2
def test_save_vital_status_alive(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Save Vital status - Alive
    """
    log.info("Test Started- to Save Vital status - Alive")
    # clear data before starting test
    app_test.chronicle_patient_status.clear_data_from_patient_status()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle.click_on_save()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data1)
    log.info("Test Passed- vital status data verification is successful")

@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p1
def test_display_last_modified_user_and_time(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Save Vital status - Display last modified user and date on form
    """
    log.info("Test Started-to Save Vital status - Display last modified user and date on form")
    app_test.chronicle_patient_status.clear_data_from_patient_status()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle.verify_last_modified_user_and_time(username, date)
    log.info("Test Passed- last modified user and date is verified")

@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p3
def test_change_vital_stutus_after_saving(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Vital Status - Verify user can change patient's vital status after saving
    """
    log.info("Test Started-to Verify user can change patient's vital status after saving")
    # clear data before starting test
    app_test.chronicle_patient_status.clear_data_from_patient_status()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Deceased_radiobutton()
    app_test.chronicle.click_on_save()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data2)
    log.info("Test Passed-can change patient's vital status after saving")


@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p3
def test_date_of_last_contact_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Vital Status - Date of Last Contact - Enter and Save
    """
    #app_test.navigation.refresh_page()
    log.info("Test Started-to Verify Date of Last Contact - Enter and Save")
    # clear data before starting test
    app_test.chronicle_patient_status.clear_data_from_patient_status()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.enter_date_into_dateOfLastContact(date=date2)
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    time.sleep(5)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data4)
    log.info("Test Passed -Date of Last Contact is saved and verified successfully")

@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p3
def test_change_date_of_last_contact_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Vital Status - Change Date of Last Contact and Save
    """
    log.info("Test Started-to change Date of Last Contact and Save")
    #run below test to make it independent
    test_date_of_last_contact_save(app_test,pick_patient_for_chronicle,test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.clear_dateOfLastContact()
    app_test.chronicle_patient_status.enter_date_into_dateOfLastContact(date=date3)
    app_test.chronicle.click_on_save()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data5)
    log.info("Test Passed -Date of Last Contact is changed and verified successfully")

@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p3
def test_remove_date_of_last_contact_save(app_test, pick_patient_for_chronicle,test_info):
    """
    Chronicle - Vital Status - Change Date of Last Contact and Save
    """
    log.info("Test Started-to remove Date of Last Contact and Save")
    test_date_of_last_contact_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.clear_dateOfLastContact()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data1)
    log.info("Test Passed -Date of Last Contact is removed and verified successfully")

@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p4
@pytest.mark.p3
def test_rediraction_back_to_portal(app_test, pick_patient_for_chronicle,test_info):
    """
    Chronicle - General - redirection back to the portal page
    """
    app_test.navigation.refresh_page()
    app_test.chronicle.open_patient_finder()
    # todo
    app_test.portal.click_syapse_logo()
    app_test.portal.verify_url_contains_portal()


@pytest.mark.skip(reason="currently not required due to low priority")
@pytest.mark.p3
def test_patient_demographic_info_deceased(app_test,pick_patient_for_chronicle,test_info):
    """
    Patient Details - Verify Patient Demographic Information with Deceased status
    """
    log.info("Test Started-to Verify Patient Demographic Information with Deceased status")
    app_test.chronicle.open_patient_finder()
    app_test.finder.find_and_pick_patient(patient_with_deceased_status)
    app_test.verification.patient_info(patient_with_deceased_status, patient_with_deceased_status_info)
    log.info("Test Passed-Patient Demographic Information with Deceased status is verified successfully")


