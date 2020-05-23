import time
import pytest
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
user_first_last_name = pytest.data.get_user('portal_chronicle')['full_name']

patient = pytest.data.get_patient_first_last_name('patient_status')
PDS_service_name= pytest.data.get_service_name('PDS')
patient_without_vital_status=pytest.data.get_patient_first_name('patient_without_vital_status')

#  below are the data which comes from fixture_data.json file to fill the fields of vital status
fields_data1 = pytest.data.get_data('Chronicle_Vital_Status_no_data')
fields_data2 = pytest.data.get_data('Chronicle_Vital_Status_data')
fields_data3 = pytest.data.get_data('Chronicle_Vital_Status_data8')
fields_data4=pytest.data.get_data('Chronicle_Vital_Status_data9')
fields_no_data= pytest.data.get_data('Chronicle_Vital_Status_no_data2')
date1 = pytest.data.get_data('date4')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()

@pytest.mark.p4
@pytest.mark.p1
def test_no_vital_status_error_msg(app_test, test_info):
    # This test requires patient does not have data for 'vital status' field
    """
    Chronicle - Verify Error message if Vital status is not selected
    """
    log.info("Test Started- to Verify Error message if Vital status is not selected")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient_without_vital_status)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.enter_date_into_dateOfLastContact(date1)
    app_test.chronicle.click_on_save()
    app_test.chronicle_patient_status.verify_error_msg()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data1)
    log.info("Test Passed- Error message if Vital status is not selected is displayed")


@pytest.mark.p2
def test_vital_status_deceased(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Save Vital status - Deceased
    """
    log.info("Test Started- to  Save Vital status - Deceased")
    #clear- if there is existing data clear it
    app_test.chronicle_patient_status.clear_data_from_patient_status()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    time.sleep(5)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data2)
    log.info("Test Passed- Vital status with Deceased is saved and verified successfully")

@pytest.mark.p1
def test_vital_status_fill_up_all_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Vital Status - Fill up all the fields and Save
    """
    log.info("Test Started- to  Fill up all the fields and Save in Vital Status")
    # clear- if there is existing data clear it
    app_test.chronicle_patient_status.clear_data_from_patient_status()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_patient_status.fill_out_the_fields_for_Vital_Status(dict=fields_data3)
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    time.sleep(3)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data3)
    log.info("Test Passed- all the fields are Saved and verified successfully")

@pytest.mark.p3
def test_vital_status_change_all_not_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Vital Status - Change all fields without saving
    """
    log.info("Test Started- to  Change all fields without saving and verify ")
    # run "test_vital_status_fill_up_all_save" to make this test independent
    test_vital_status_fill_up_all_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.remove_data_from_patient_status()
    app_test.chronicle_patient_status.fill_out_the_fields_for_Vital_Status(dict=fields_data4)

    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data3)
    log.info("Test Passed - all fields without saving are not changed ")



@pytest.mark.p2
def test_vital_status_change_all_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Vital Status - Change all fields and Save
    """
    log.info("Test Started- to  Change all fields and Save and verify ")
    # run below test to make it independent
    test_vital_status_fill_up_all_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Deceased_radiobutton()

    app_test.chronicle_patient_status.remove_data_from_patient_status()
    app_test.chronicle_patient_status.fill_out_the_fields_for_Vital_Status(dict=fields_data4)
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()

    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data4)
    log.info('Test Started- all fields are changed and verified successfully')

#@pytest.mark.skip(reason='flaky')
@pytest.mark.p3
def test_vital_status_delete_all_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Vital Status - Delete info from all fields and Save
    """
    log.info('Test Started- to Delete info from all fields and Save')
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.clear_data_from_patient_status()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_no_data)
    log.info('Test Started- info from all fields deleted successfully')


