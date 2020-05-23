import time
from qa_automation_drt_haw.settings import Config
import pytest


from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_elements

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
user_first_last_name = pytest.data.get_user('portal_chronicle')['full_name']

patient = pytest.data.get_patient_first_last_name('patient_surgery')
PDS_service_name= pytest.data.get_service_name('PDS')
fields_data1 = pytest.data.get_data('Chronicle_Cancer_Surgery1_data')
patient_without_vital_status=pytest.data.get_patient_first_name('patient_without_vital_status')
fields_data2 = pytest.data.get_data('Chronicle_Cancer_Surgery2_data')
fields_data3 =pytest.data.get_data('Chronicle_Cancer_Surgery3_data')
fields_data4=pytest.data.get_data('Chronicle_Cancer_Surgery4_data')
fields_data5=pytest.data.get_data('Chronicle_Cancer_Surgery5_data')
fields_data6=pytest.data.get_data('Chronicle_Cancer_Surgery_no_data')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()


@pytest.mark.p4
@pytest.mark.p3
def test_save_without_vital_status(app_test,test_info):
    """
    Chronicle - Surgery  - Fill up all the fields and Save - without Vital Status
    """
    log.info("Test Started- to Fill up all the fields without Vital Status and verify that data is not saved")
    # This test requires patient does not have data for 'vital status' field
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient_without_vital_status)
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_surgery_and_radiation.click_Add_Another_for_Cancer_Surgery()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_SurgeryandRadiation(dict=fields_data1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.verify_text_No_Cancer_Surgeries_present()
    log.info("Test Passed - data no saved (without Vital Status)")


@pytest.mark.p1
def test_fill_up_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Surgery  - Fill up all the fields and Save - with Vital Status
    """
    log.info("Test Started- to Fill up all the fields, Save and verify values ")
    # clear data before starting the test-if there is any
    app_test.chronicle_surgery_and_radiation.remove_all_sections_from_SurgeryOrCancerSurgery()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_surgery_and_radiation.click_Add_Another_for_Cancer_Surgery()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_SurgeryandRadiation(dict=fields_data2)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data2)
    log.info("Test Passed - all the fields value saved and verified successfully")



@pytest.mark.p2
def test_change_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Surgery - Change all field values and Save
    """
    log.info("Test Started to Change all field values and Save")
    # to make test independent run "test_fill_up_all_fields_save" to add data for change
    test_fill_up_all_fields_save(app_test,pick_patient_for_chronicle,test_info)
    #app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_surgery_and_radiation.remove_data_from_all_fields()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_SurgeryandRadiation(dict=fields_data3)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data3)
    log.info("Test Passed- all field values are changed and Saved successfully")


@pytest.mark.p3
def test_change_all_fields_no_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Surgery - Change all field values without saving
    """
    log.info("Test Started to Change all field values and no Save")
    # to make test independent run "test_fill_up_all_fields_save" to add data for no-change
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    #app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_surgery_and_radiation.remove_data_from_all_fields()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_SurgeryandRadiation(dict=fields_data3)
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data2)
    log.info("Test Passed- all field values are not changed")


@pytest.mark.p3
def test_add_few_sections(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Surgery - Add few sections
    """
    log.info("Test Started to Add few sections and Verify")
    # to make test independent run "test_fill_up_all_fields_save" to add 1st data
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    time.sleep(5)
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()

    app_test.chronicle_surgery_and_radiation.click_Add_Another_for_Cancer_Surgery()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_SurgeryandRadiation(dict=fields_data4, section_name=app_test.chronicle_surgery_and_radiation.section2_locator)
    app_test.chronicle_surgery_and_radiation.click_Add_Another_for_Cancer_Surgery()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_SurgeryandRadiation(dict=fields_data5, section_name=app_test.chronicle_surgery_and_radiation.section3_locator)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data4, section=app_test.chronicle_surgery_and_radiation.section2_locator_for_verification)
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data5, section=app_test.chronicle_surgery_and_radiation.section3_locator_for_verification)
    log.info("Test Passed - Added few sections and Verified successfully")


@pytest.mark.p3
def test_remove_sections(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Surgery - Remove Cancer Surgery section
    """
    log.info("Test Started to Remove Cancer Surgery section")
    test_add_few_sections(app_test, pick_patient_for_chronicle, test_info)
    #app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle.remove_section(app_test.chronicle_surgery_and_radiation.remove_link2)
    app_test.chronicle.remove_section(app_test.chronicle_surgery_and_radiation.remove_link1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data2)
    app_test.chronicle_surgery_and_radiation.verify_section_is_displayed()
    app_test.chronicle_surgery_and_radiation.verify_section_is_displayed(section_name=app_test.chronicle_surgery_and_radiation.section3_locator_for_verification)
    log.info("Test Passed - one section removed successfully")


#@pytest.mark.skip(reason='flaky')
@pytest.mark.p3
def test_empty_sections(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Surgery - Empty section
    """
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_surgery_and_radiation.remove_data_from_all_fields()
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data6)


@pytest.mark.p3
def test_remove_all_sections(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Surgery - Remove all sections
    """
    #app_test.navigation.refresh_page()
    log.info("Test Started- to remove all the sections from Cancer Surgery")
    app_test.chronicle_surgery_and_radiation.remove_all_sections_from_SurgeryOrCancerSurgery()
    log.info("Test Passed")

