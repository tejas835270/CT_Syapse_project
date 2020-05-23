import pytest
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
user_first_last_name = pytest.data.get_user('portal_chronicle')['full_name']

patient = pytest.data.get_patient_first_last_name('patient_program_management')
PDS_service_name= pytest.data.get_service_name('PDS')

#patient does not have data for 'vital status' field
patient_without_vital_status=pytest.data.get_patient_first_name('patient_without_vital_status')

# below are the data which comes from fixture_data.json file to fill the all fields of program management
fields_data1 = pytest.data.get_data('Chronicle_programManagement_data1')
fields_no_data = pytest.data.get_data('Chronicle_programManagement_no_data')
data_Only_Alive = pytest.data.get_data('Chronicle_Vital_Status_Alive_Only')
fields_data2 = pytest.data.get_data('Chronicle_programManagement_data_to_fill_all_fields')
fields_data3 = pytest.data.get_data('Chronicle_programManagement_data_to_change_all_fields')
fields_data4 = pytest.data.get_data('Chronicle_programManagement_data_with_multiple_didNgsImpactTreatment')
fields_data5 = pytest.data.get_data('Chronicle_programManagement_data_toChange_multiple_didNgsImpactTreatment')
fields_data6 = pytest.data.get_data('Chronicle_programManagement_data_remove_multiple_didNgsImpactTreatment')


#to verify data only for didNgsImpactTreatment field
didNgsImpactTreatment__data_verification1 = pytest.data.get_data('programManagement__didNgsImpactTreatment_data_verification1')
didNgsImpactTreatment__data_verification2 = pytest.data.get_data('programManagement__didNgsImpactTreatment_data_verification2')
didNgsImpactTreatment__data_verification3 = pytest.data.get_data('programManagement__didNgsImpactTreatment_data_verification3')

#to enter data only for didNgsImpactTreatment field
didNgsImpactTreatment__data1=pytest.data.get_data('programManagement__didNgsImpactTreatment__data1')
didNgsImpactTreatment__data2=pytest.data.get_data('programManagement__didNgsImpactTreatment__data2')
didNgsImpactTreatment__data3=pytest.data.get_data('programManagement__didNgsImpactTreatment__data3')
didNgsImpactTreatment__data4=pytest.data.get_data('programManagement__didNgsImpactTreatment__data4')
didNgsImpactTreatment__data5=pytest.data.get_data('programManagement__didNgsImpactTreatment__data5')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()


# This test requires patient does not have data for 'vital status' field (i.e. patient_without_vital_status-Jones)
@pytest.mark.p4
@pytest.mark.p3
def test_save_without_vital_status(app_test,test_info):
    """
    Chronicle - Program Management  - Fill up all the fields and Save - without Vital Status
    """
    log.info("Test Started- to Fill up all the fields  without Vital Status, Save and verify values ")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient_without_vital_status)
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_program_management.Program_Management_fill_out_the_fields(dict=fields_data1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_no_data)
    log.info("Test Passed- if all the fields without Vital Status are filled , Saved and then values are not saved ")

@pytest.mark.p3
def test_fields_not_required_for_saving(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Program Management - Verify filling up the fields is not required for saving the form
    """
    log.info("Test Started- to  Verify filling up the fields is not required for saving the form ")
    # clear data before starting the test-if there is any
    app_test.chronicle_program_management.remove_all_existing_data()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_no_data)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=data_Only_Alive)
    log.info("Test Passed- the form is saved without filling up the fields ")

@pytest.mark.p1
def test_fill_up_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Program Management  - Fill up all the fields and Save - with Vital Status
    """
    log.info("Test Started- Fill up all the fields and Save - with Vital Status")
    # clear data before starting the test-if there is any
    app_test.chronicle_program_management.remove_all_existing_data()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_program_management.Program_Management_fill_out_the_fields(dict=fields_data2)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()

    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_data2)

    log.info("Test passed- all the fields are filled and Saved successfully with Vital Status")



@pytest.mark.p2
def test_change_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Program Management - Change all field values and Save
    """
    log.info("Test Started- to Change all field values and Save")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test,pick_patient_for_chronicle,test_info)
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_program_management.remove_data_from_fields_before_changing()
    app_test.chronicle_program_management.Program_Management_fill_out_the_fields(dict=fields_data3)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()

    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_data3)

    log.info("Test passed- all field values are changed and verified successfully")

@pytest.mark.p3
def test_change_all_fields_no_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Program Management - Change all field values without saving
    """
    log.info("Test Started- to Change all field values  without saving")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_program_management.remove_data_from_fields_before_changing()
    app_test.chronicle_program_management.Program_Management_fill_out_the_fields(dict=fields_data3)

    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_data2)

    log.info("Test Passed- all field values are not changed without saving")

@pytest.mark.p3
def test_ngs_add_multiple_values(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Program Management - NGS test result - Add multiple values
    """
    log.info("Test Started- for NGS test result - Add multiple values")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_program_management.add_another_for_didNgsImpactTreatment()
    app_test.chronicle_program_management.select_dd_option_didNgsImpactTreatment(value=didNgsImpactTreatment__data1)

    app_test.chronicle_program_management.add_another_for_didNgsImpactTreatment()
    app_test.chronicle_program_management.select_dd_option_didNgsImpactTreatment(ddname=app_test.chronicle_program_management.didNgsImpactTreatment_dd2,value=didNgsImpactTreatment__data2)

    app_test.chronicle_program_management.add_another_for_didNgsImpactTreatment()
    app_test.chronicle_program_management.select_dd_option_didNgsImpactTreatment(ddname=app_test.chronicle_program_management.didNgsImpactTreatment_dd3, value=didNgsImpactTreatment__data3)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()

    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_data4)

    log.info("Test Passed -multiple values added successfully for for NGS test result")


@pytest.mark.p3
def test_ngs_change_multiple_values(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Program Management - NGS test result - Change multiple values
    """
    log.info("Test Started- for NGS test result - Change multiple values")
    # to remove dependancy first run "test_ngs_add_multiple_values"
    test_ngs_add_multiple_values(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_program_management.select_dd_option_didNgsImpactTreatment(ddname=app_test.chronicle_program_management.didNgsImpactTreatment_dd0,value=didNgsImpactTreatment__data4)
    app_test.chronicle_program_management.select_dd_option_didNgsImpactTreatment(ddname=app_test.chronicle_program_management.didNgsImpactTreatment_dd2, value=didNgsImpactTreatment__data5)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()

    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()

    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_data5)
    log.info("Test Passed -multiple values changed successfully for for NGS test result")

@pytest.mark.p3
def test_ngs_remove_multiple_values_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Program Management - NGS test result - Remove few values
    """
    log.info("Test Started- for NGS test result - Remove few values")
    # to remove dependancy first run "test_ngs_change_multiple_values"
    test_ngs_add_multiple_values(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle.remove_additional_field(app_test.chronicle_program_management.didNgsImpactTreatment_dd0)
    app_test.chronicle_program_management.Program_Management_values_verification(dict=didNgsImpactTreatment__data_verification1)

    app_test.chronicle.remove_additional_field(app_test.chronicle_program_management.didNgsImpactTreatment_dd0)
    app_test.chronicle_program_management.Program_Management_values_verification(dict=didNgsImpactTreatment__data_verification2)

    app_test.chronicle.remove_additional_field(app_test.chronicle_program_management.didNgsImpactTreatment_dd1)
    app_test.chronicle_program_management.Program_Management_values_verification(dict=didNgsImpactTreatment__data_verification3)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_data6)

    log.info("Test Passed-ew values for NGS test result are removed and verified successfully")


#@pytest.mark.skip(reason='flaky')
@pytest.mark.p3
def test_remove_all_fields(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Program Management - Remove all the fields
    """
    log.info("Test Started- to Remove all the fields from Program Management")
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_program_management.remove_data_from_fields_before_changing()

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_program_management.chronicle_tab_Program_Management()
    app_test.chronicle_program_management.Program_Management_values_verification(dict=fields_no_data)

    log.info("Test Passed-  all the fields from Program Management are removed and verified successfully")


