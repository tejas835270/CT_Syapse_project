import time
from qa_automation_drt_haw.settings import Config
import pytest


from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_elements

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
user_first_last_name = pytest.data.get_user('portal_chronicle')['full_name']

patient = pytest.data.get_patient_first_last_name('patient_radiation')
PDS_service_name= pytest.data.get_service_name('PDS')

#patient does not have data for 'vital status' field
patient_without_vital_status=pytest.data.get_patient_first_name('patient_without_vital_status')

#  below are the data which comes from fixture_data.json file to fill the fields of Radiation Therapy
fields_data1 = pytest.data.get_data('Chronicle_Radiation_data1')
fields_data2 = pytest.data.get_data('Chronicle_Radiation_data_to_modify')
fields_data3 = pytest.data.get_data('Chronicle_Radiation_data3')
empty_fields= pytest.data.get_data('Chronicle_Radiation_no_data')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()

# This test requires patient does not have data for 'vital status' field - hence did below changes
@pytest.mark.p4
@pytest.mark.p3
def test_save_without_vital_status(app_test,test_info):
    """
    Chronicle - Radiation - Fill up all the fields and Save - without Vital Status
    """
    log.info("Test Started- to  Fill up all the fields and Save - without Vital Status")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient_without_vital_status)
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle.click_Add_Another_for_section(section_name=app_test.chronicle_surgery_and_radiation.radiation_section)
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_Radiation(dict=fields_data1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.verify_text_No_Radiation_Therapies()
    log.info("Test passed- data is not saved if all the fields are filled without Vital Status")



@pytest.mark.p1
def test_fill_up_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Radiation - Fill up all the fields and Save - with Vital Status
    """
    log.info("Test Started- to  Fill up all the fields and Save - with Vital Status")
    # clear data before starting the test-if there is any
    app_test.chronicle_surgery_and_radiation.remove_all_sections_from_RadiationTherapy()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle.click_Add_Another_for_section(section_name=app_test.chronicle_surgery_and_radiation.radiation_section)
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_Radiation(dict=fields_data1)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data1,section=app_test.chronicle_surgery_and_radiation.radiation_section1_for_verification)
    log.info("Test passed- all the fields are filled with Vital Status and Saved successfully- ")


@pytest.mark.p2
def test_change_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Surgery and Radiation - Change all field values and Save
    """
    log.info("Test Started- to Change all field values and Save")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_surgery_and_radiation.remove_all_fields_data_from_radiation()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_Radiation(dict=fields_data2)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data2,section=app_test.chronicle_surgery_and_radiation.radiation_section1_for_verification)

    log.info("Test passed- all field values are changed and verified successfully")


@pytest.mark.p3
def test_change_all_fields_no_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Surgery and Radiation - Change all field values without saving
    """
    log.info("Test Started- to Change all field values without saving")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_surgery_and_radiation.remove_all_fields_data_from_radiation()
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_Radiation(dict=fields_data2)

    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data1,section=app_test.chronicle_surgery_and_radiation.radiation_section1_for_verification)

    log.info("Test passed- all field values are not changed without saving")

@pytest.mark.p3
def test_add_section(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Radiation - Add section
    """
    log.info("Test Started- to Add section")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.click_Add_Another_for_section(section_name=app_test.chronicle_surgery_and_radiation.radiation_section)
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_Radiation(dict=fields_data3,section_name=app_test.chronicle_surgery_and_radiation.radiation_section2_locator)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data3,section=app_test.chronicle_surgery_and_radiation.radiation_section2_for_verification)

    log.info("Test passed- one more section added and verified successfully")

@pytest.mark.p3
def test_remove_section(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Radiation - Remove Radiation section
    """
    log.info("Test Started- to Remove Radiation section")
    # to remove dependancy first run "test_add_section"
    test_add_section(app_test, pick_patient_for_chronicle, test_info)
    #app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.remove_section(app_test.chronicle_surgery_and_radiation.radiation_remove_link1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()

    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data3,section=app_test.chronicle_surgery_and_radiation.radiation_section1_for_verification)
    app_test.chronicle_surgery_and_radiation.verify_section_is_displayed(section_name=app_test.chronicle_surgery_and_radiation.radiation_section2_for_verification)
    log.info("Test passed- Radiation section is removed and verified successfully")



@pytest.mark.p3
def test_add_few_sections(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Radiation - Add few sections
    """
    log.info("Test Started- to Add few sections")
    # clear data before starting the test-if there is any
    app_test.chronicle_surgery_and_radiation.remove_all_sections_from_RadiationTherapy()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.click_Add_Another_for_section(section_name=app_test.chronicle_surgery_and_radiation.radiation_section)
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_Radiation(dict=fields_data1)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.hide_footer()

    app_test.chronicle.click_Add_Another_for_section(section_name=app_test.chronicle_surgery_and_radiation.radiation_section)
    app_test.chronicle_surgery_and_radiation.fill_out_the_fields_for_Radiation(dict=fields_data3,section_name=app_test.chronicle_surgery_and_radiation.radiation_section2_locator)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()

    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()

    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data1,section=app_test.chronicle_surgery_and_radiation.radiation_section1_for_verification)
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=fields_data3,section=app_test.chronicle_surgery_and_radiation.radiation_section2_for_verification)

    log.info("Test Started- few sections are added successfully")

@pytest.mark.p3
def test_remove_all_sections_from_Radiation_Therapy(app_test, pick_patient_for_chronicle, test_info):
    """
        Chronicle - Surgery and Radiation - Remove all sections if there
    """
    log.info("Test Started- to Remove all sections if there")
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.remove_all_sections_from_RadiationTherapy()
    log.info("Test passed-all sections are removed successfully")


#@pytest.mark.skip(reason='flaky')
@pytest.mark.p3
def test_empty_section(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Surgery and Radiation - Empty section
    """
    log.info("Test Started- to Empty section")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_surgery_and_radiation.remove_all_fields_data_from_radiation()

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_surgery_and_radiation.chronicle_tab_Surgery_and_Radiation()
    app_test.chronicle_surgery_and_radiation.values_verification_for_SurgeryandRadiation(dict=empty_fields,section=app_test.chronicle_surgery_and_radiation.radiation_section1_for_verification)
    log.info("Test passed- section is empty")










