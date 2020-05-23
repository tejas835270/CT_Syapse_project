import time
from qa_automation_drt_haw.settings import Config
import pytest


from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_elements

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
user_first_last_name = pytest.data.get_user('portal_chronicle')['full_name']

patient = pytest.data.get_patient_first_last_name('patient_with_deceased_status')
PDS_service_name= pytest.data.get_service_name('PDS')

#patient does not have data for 'vital status' field
patient_without_vital_status=pytest.data.get_patient_first_name('patient_without_vital_status')

# below are the data which comes from fixture_data.json file to fill the all fields of disease Status
fields_data1 = pytest.data.get_data('Chronicle_Disease_Status_data1')
fields_data2 = pytest.data.get_data('Chronicle_Disease_Status_data2')
fields_data3 = pytest.data.get_data('Chronicle_Disease_Status_data3')
fields_data4 = pytest.data.get_data('Chronicle_Disease_Status_data4')
fields_data5 = pytest.data.get_data('Chronicle_Disease_Status_data5')
fields_no_data = pytest.data.get_data('Chronicle_Disease_Status_no_data')

# below are the data which comes from fixture_data.json file to verify multiple Distant_metastasis fields value
Distant_metastasis_data1=pytest.data.get_data('Distant_metastasis_data1')
Distant_metastasis_data2=pytest.data.get_data('Distant_metastasis_data2')
Distant_metastasis_data3=pytest.data.get_data('Distant_metastasis_data3')
Distant_metastasis_custom_values=pytest.data.get_data('Distant_metastasis_custom_value')

# below are the data which comes from fixture_data.json file to verify multiple Extent_of_disease fields value
Extent_of_disease_data1=pytest.data.get_data('Extent_of_disease_data1')
Extent_of_disease_data2=pytest.data.get_data('Extent_of_disease_data2')
Extent_of_disease_data3=pytest.data.get_data('Extent_of_disease_data3')
Extent_of_disease_data4=pytest.data.get_data('Extent_of_disease_data4')
#Distant_metastasis_custom_values=pytest.data.get_data('Distant_metastasis_custom_value')

# below are the data which comes from fixture_data.json file to enter value in Distant_metastasis fields
value1=pytest.data.get_data('Distant_metastasis_value1')
value2=pytest.data.get_data('Distant_metastasis_value2')
value3=pytest.data.get_data('Distant_metastasis_value3')
value4=pytest.data.get_data('Distant_metastasis_value4')
custom_value1=pytest.data.get_data('Distant_metastasis_custom_value1')
custom_value2=pytest.data.get_data('Distant_metastasis_custom_value2')

# below are the data which comes from fixture_data.json file to enter value in Extent_of_disease fields
Extent_of_disease_value1=pytest.data.get_data('Extent_of_disease_value1')
Extent_of_disease_value2=pytest.data.get_data('Extent_of_disease_value2')
Extent_of_disease_value3=pytest.data.get_data('Extent_of_disease_value3')

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
def test_save_without_vital_status(app_test, test_info):
    """
    Chronicle - Disease status - Fill up all without selecting Vital status
    """
    log.info("Test Started- Fill up all without selecting Vital status")
    # This test requires patient does not have data for 'vital status' field
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient_without_vital_status)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.click_Add_Another()
    app_test.chronicle_patient_status.fill_out_the_fields_for_Disease_Status(dict=fields_data1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    time.sleep(2)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.verify_text_No_Disease_status_present()
    log.info("Test Passed- if all the fields without Vital Status are filled , Saved and then values are not saved ")

@pytest.mark.p3
def test_fill_up_all_fields_no_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Disease status - Fill up all fields without saving
    """
    log.info("Test Started- Fill up all fields without saving")
    # clear data before starting the test-if there is any
    app_test.chronicle_patient_status.remove_all_sections_from_Disease_Status()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Deceased_radiobutton()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.click_Add_Another()
    app_test.chronicle_patient_status.fill_out_the_fields_for_Disease_Status(dict=fields_data2)
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.verify_text_No_Disease_status_present()
    log.info("Test passed- all fields are not saved without saving")



@pytest.mark.p1
def test_fill_up_all_fields_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Disease status - Fill up all fields without saving
    """
    log.info("Test Started- Fill up all fields and save")
    # clear data before starting the test-if there is any
    app_test.chronicle_patient_status.remove_all_sections_from_Disease_Status()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Deceased_radiobutton()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.click_Add_Another()
    app_test.chronicle_patient_status.fill_out_the_fields_for_Disease_Status(dict=fields_data2)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data2,section=app_test.chronicle_patient_status.disease_section1_for_verification)
    log.info("Test passed- all fields are saved and verified successfully")

@pytest.mark.p3
def test_add_section(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease status - Add Another section
    """
    log.info("Test Started- to Add Another section")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.click_Add_Another_with_SectionAndRole(section_name=app_test.chronicle_patient_status.disease_section)
    app_test.chronicle_patient_status.fill_out_the_fields_for_Disease_Status(dict=fields_data3,section_name=app_test.chronicle_patient_status.disease_section2)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data3,
                                                                                section=app_test.chronicle_patient_status.disease_section2_for_verification)
    log.info("Test passed -Another section is added and verified successfully")


@pytest.mark.p2
def test_change_all_fields_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease status - Change values in the fields and Save
    """
    log.info("Test Started- to Change values in the fields and Save")
    # to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_patient_status.remove_data_from_Disease_Statusfields()

    app_test.chronicle_patient_status.fill_out_the_fields_for_Disease_Status(dict=fields_data4)
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=Extent_of_disease_value3,
                                                                                        field_name=app_test.chronicle_patient_status.Extent_of_disease_locator_0)
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=value2,field_name=app_test.chronicle_patient_status.Distant_metastasis_locator_0)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data5,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)
    log.info("Test passed- values in the fields are changed and verified successfully")


@pytest.mark.p3
def test_remove_section(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease status - Remove section and Save
    """
    log.info("Test Started- to  Remove section and Save")
    # to remove dependancy first run "test_add_section"
    test_add_section(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.remove_section(app_test.chronicle_patient_status.diseaseStatus_removelink1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_data3,section=app_test.chronicle_patient_status.disease_section1_for_verification)

    app_test.chronicle.verify_section_is_not_displayed(section_name=app_test.chronicle_patient_status.disease_section2_for_verification)
    log.info("Test passed- section is removed successfully")

@pytest.mark.p3
def test_add_multiple_distant_metastasis_and_recurrence_sites(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease Status - Distant metastasis or recurrence sites - Add multiple values
    """
    log.info("Test Started- to Add multiple values for Distant metastasis or recurrence sites")
    # clear data before starting the test-if there is any
    app_test.chronicle_patient_status.remove_all_sections_from_Disease_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.click_Add_Another()
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=value1, field_name=app_test.chronicle_patient_status.Distant_metastasis_locator0)
    app_test.chronicle_patient_status.click_Add_Another_for_distantMetastasis()
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=value2, field_name=app_test.chronicle_patient_status.Distant_metastasis_locator1)
    app_test.chronicle_patient_status.click_Add_Another_for_distantMetastasis()
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=value3,
                                                                                        field_name=app_test.chronicle_patient_status.Distant_metastasis_locator2)
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Distant_metastasis_data1,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Distant_metastasis_data1,section=app_test.chronicle_patient_status.disease_section1_for_verification)

    log.info("Test passed- multiple values for Distant metastasis or recurrence sites are added and verified successfully")


@pytest.mark.p3
def test_remove_multiple_distant_metastasis_and_recurrence_sites(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease Status - Distant metastasis or recurrence sites - Remove few values and Save
    """
    log.info("Test Started- to Remove few values from Distant metastasis or recurrence sites and Save")
    # to remove dependancy first run "test_add_multiple_distant_metastasis_and_recurrence_sites"
    test_add_multiple_distant_metastasis_and_recurrence_sites(app_test, pick_patient_for_chronicle, test_info)
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.remove_additional_field(app_test.chronicle_patient_status.Distant_metastasis_locator)
    app_test.chronicle.remove_additional_field(app_test.chronicle_patient_status.Distant_metastasis_locator1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Distant_metastasis_data2,section=app_test.chronicle_patient_status.disease_section1_for_verification)

    log.info("Test passed- few values from Distant metastasis or recurrence sites are removed and verified successfully")



@pytest.mark.p3
def test_enter_custom_value_distant_metastasis_and_recurrence_sites(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease Status - Distant metastasis or recurrence sites - Enter custom value
    """
    log.info("Test Started- to Enter custom value for Distant metastasis or recurrence sites and Save")
    # clear data before starting the test-if there is any
    app_test.chronicle_patient_status.remove_all_sections_from_Disease_Status()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle.click_Add_Another()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()

    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=custom_value1,
                                                                                        field_name=app_test.chronicle_patient_status.Distant_metastasis_locator0)
    app_test.chronicle_patient_status.click_Add_Another_for_distantMetastasis()
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=custom_value2,
                                                                                        field_name=app_test.chronicle_patient_status.Distant_metastasis_locator1)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Distant_metastasis_custom_values,section=app_test.chronicle_patient_status.disease_section1_for_verification)

    log.info("Test passed- custom value for Distant metastasis or recurrence sites are saved and verified successfully")


@pytest.mark.p3
def test_change_and_remove_custom_value_distant_metastasis_and_recurrence_sites(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease Status - Distant metastasis or recurrence sites - Change and Remove custom value
    """
    log.info("Test Started- to Change and Remove custom value for Distant metastasis or recurrence sites and Save")
    # to remove dependancy first run "test_enter_custom_value_distant_metastasis_and_recurrence_sites"
    test_enter_custom_value_distant_metastasis_and_recurrence_sites(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.remove_additional_field(app_test.chronicle_patient_status.Distant_metastasis_locator)
    app_test.chronicle.remove_option_from_dropdown_if_data_present(app_test.chronicle_patient_status.Distant_metastasis_locator)
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=value4,
                                                                                        field_name=app_test.chronicle_patient_status.Distant_metastasis_locator)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Distant_metastasis_data3,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)
    log.info("Test Started-custom value for Distant metastasis or recurrence sites are changed and removed successfully")

@pytest.mark.p3
def test_extent_of_disease_add_multiple_values(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease Status - Extent of Disease - Add multiple values (AP-27577)
    """
    log.info("Test Started- to Add multiple values for Extent of Disease")
    # clear data before starting the test-if there is any
    app_test.chronicle_patient_status.remove_all_sections_from_Disease_Status()

    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.click_Add_Another()

    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=Extent_of_disease_value1,
                                                                                        field_name=app_test.chronicle_patient_status.Extent_of_disease_locator0)
    app_test.chronicle_patient_status.click_Add_Another_for_Extent_of_disease()
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=Extent_of_disease_value2,
                                                                                        field_name=app_test.chronicle_patient_status.Extent_of_disease_locator1)
    app_test.chronicle_patient_status.click_Add_Another_for_Extent_of_disease()
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=Extent_of_disease_value3,
                                                                                        field_name=app_test.chronicle_patient_status.Extent_of_disease_locator2)

    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Extent_of_disease_data1,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Extent_of_disease_data1,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)
    log.info("Test passed- multiple values for Extent of Disease are added and verified successfully")


@pytest.mark.p3
def test_extent_of_disease_change_values(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease Status - Extent of Disease - Change value in additional fields (AP-27577)
    """
    log.info("Test Started- to Change value in additional fields for Extent of Disease")
    # to remove dependancy first run "test_extent_of_disease_add_multiple_values"
    test_extent_of_disease_add_multiple_values(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.remove_option_from_dropdown_if_data_present(app_test.chronicle_patient_status.Extent_of_disease_locator1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Extent_of_disease_data2,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)

    app_test.navigation.hide_footer()
    app_test.chronicle_patient_status.select_value_for_Distant_metastasis_and_Extent_disease(data=Extent_of_disease_value1,
                                                                                        field_name=app_test.chronicle_patient_status.Extent_of_disease_locator1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Extent_of_disease_data3,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)
    log.info("Test passed- additional fields for Extent of Disease are changed successfully")


@pytest.mark.p3
def test_extent_of_disease_remove_values_and_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease Status - Extent of disease - Remove few values and Save (AP-27577)
    """
    log.info("Test Started- Remove few values and Save for Extent of Disease")
    # to remove dependancy first run "test_extent_of_disease_add_multiple_values"
    test_extent_of_disease_add_multiple_values(app_test, pick_patient_for_chronicle, test_info)

    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle.remove_additional_field(app_test.chronicle_patient_status.Extent_of_disease_locator_0)
    app_test.chronicle.remove_additional_field(app_test.chronicle_patient_status.Extent_of_disease_locator_0)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=Extent_of_disease_data4,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)

    log.info("Test Started- few values are removed and Saved successfully for Extent of Disease")

# TODO fix - comment field
#@pytest.mark.skip(reason='flaky')
@pytest.mark.p3
def test_disease_status_empty_section(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Disease status - Empty section
    """
    log.info("Test Started- Empty section")
    #to remove dependancy first run "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.navigation.hide_footer()
    app_test.navigation.hide_header()
    app_test.chronicle_patient_status.remove_data_from_Disease_Statusfields()
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.values_verification_for_VitalandDisease_Status(dict=fields_no_data,
                                                                                section=app_test.chronicle_patient_status.disease_section1_for_verification)
    log.info("Test passed - all fields are empty")












