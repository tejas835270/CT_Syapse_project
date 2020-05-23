import time
from qa_automation_drt_haw.settings import Config
import pytest


from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password
user_first_last_name = pytest.data.get_user('portal_chronicle')['full_name']

patient = pytest.data.get_patient_first_last_name('patient_genomic_alterations')
PDS_service_name= pytest.data.get_service_name('PDS')

#  below are the data which comes from fixture_data.json file to fill the fields of vital status
fields_data1 = pytest.data.get_data('Chronicle_genomic_alterations_data1')
fields_data2 =pytest.data.get_data('Chronicle_genomic_alterations_data2')
fields_data3 =pytest.data.get_data('Chronicle_genomic_alterations_data3')
biomarkers_values1=pytest.data.get_data('genomic_alterations_biomarkers_value1')
biomarkers_values2=pytest.data.get_data('genomic_alterations_biomarkers_value2')
biomarkers_values3=pytest.data.get_data('genomic_alterations_biomarkers_value3')
biomarkers1=pytest.data.get_Biomarkers_data('genomic_alterations_biomarkers_value1')
biomarkers2=pytest.data.get_Biomarkers_data('genomic_alterations_biomarkers_value2')
biomarkers3=pytest.data.get_Biomarkers_data('genomic_alterations_biomarkers_value3')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    log.info(biomarkers_values1)
    log.info(biomarkers1)
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()


@pytest.mark.p1
def test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Genomic Alterations - Fill up all the fields and Save
    """
    log.info("Test Started- to  Fill up all the fields and Save in Genomic Alterations")
    # clear data before starting the test-if there is any
    app_test.chronicle_genomic_alterations.remove_all_sections_from_Geonomic_alterations()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle.click_Add_Another()
    app_test.chronicle_genomic_alterations.fill_out_the_fields_for_Geonomic_alterations(dict=fields_data1)
    app_test.chronicle_genomic_alterations.select_biomarkers(values=biomarkers1)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    time.sleep(2)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.chronicle_genomic_alterations.values_verification_for_Geonomic_alterations(dict=fields_data1)
    app_test.chronicle_genomic_alterations.verify_biomarkers_values(dict=biomarkers_values1)
    log.info("Test Passed- all the fields are saved and verified successfully")


@pytest.mark.p2
def test_change_all_fields_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Genomic Alterations - Change all field values and Save
    """
    log.info("Test Started- to Change all field values and Save in Genomic Alterations and verify")
    # run "test_fill_up_all_fields_save" - as this test is dependent on "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()

    app_test.chronicle_genomic_alterations.remove_data_from_all_fields(biomarker_value=biomarkers1)
    app_test.chronicle_genomic_alterations.fill_out_the_fields_for_Geonomic_alterations(dict=fields_data2)
    app_test.chronicle_genomic_alterations.select_biomarkers(values=biomarkers2)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    time.sleep(2)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.chronicle_genomic_alterations.values_verification_for_Geonomic_alterations(dict=fields_data2)
    app_test.chronicle_genomic_alterations.verify_biomarkers_values(dict=biomarkers_values2)
    log.info("Test Passed- all the fields are changed and verified successfully")


@pytest.mark.p3
def test_add_another_section(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Genomic Alterations - Add Another section
    """
    log.info("Test Started- to Add Another section in Genomic Alterations and verify")
    # run "test_fill_up_all_fields_save" - as this test is dependent on "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle.click_Add_Another_for_section(section_name=app_test.chronicle_genomic_alterations.Section)
    app_test.chronicle_genomic_alterations.fill_out_the_fields_for_Geonomic_alterations(dict=fields_data3,section_name=app_test.chronicle_genomic_alterations.section_name2)
    app_test.chronicle_genomic_alterations.select_biomarkers(values=biomarkers3,field_name=app_test.chronicle_genomic_alterations.field_name2)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    time.sleep(2)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.chronicle_genomic_alterations.values_verification_for_Geonomic_alterations(dict=fields_data3,section=app_test.chronicle_genomic_alterations.section_name2_for_verification)
    app_test.chronicle_genomic_alterations.verify_biomarkers_values(dict=biomarkers_values3,section=app_test.chronicle_genomic_alterations.section_name2_for_verification)

    log.info("Test Passed- one more section is added and verified successfully")

@pytest.mark.p3
def test_change_all_fields_not_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Genomic Alterations - Change all field values without saving
    """
    log.info("Test Started- to Change all field values in Genomic Alterations and dont save and verify")
    # run "test_fill_up_all_fields_save" - as this test is dependent on "test_fill_up_all_fields_save"
    test_fill_up_all_fields_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_genomic_alterations.remove_data_from_all_fields(biomarker_value=biomarkers1)
    app_test.chronicle_genomic_alterations.fill_out_the_fields_for_Geonomic_alterations(dict=fields_data2)
    app_test.chronicle_genomic_alterations.select_biomarkers(values=biomarkers2)

    app_test.navigation.refresh_page()
    time.sleep(2)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.chronicle_genomic_alterations.values_verification_for_Geonomic_alterations(dict=fields_data1)
    app_test.chronicle_genomic_alterations.verify_biomarkers_values(dict=biomarkers_values1)

    log.info("Test Passed- all the fields are not changed")




@pytest.mark.p3
def test_remove_section_save(app_test, pick_patient_for_chronicle, test_info):
    """
    Chronicle - Genomic Alterations - Remove section and Save
    """
    log.info("Test Started- to Remove section and Save")
    # run "test_add_another_section" to make this test independent
    test_add_another_section(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle.remove_section(app_test.chronicle_genomic_alterations.section1_remove_link)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()

    app_test.navigation.refresh_page()
    time.sleep(2)
    app_test.chronicle_genomic_alterations.chronicle_tab_Genomic_Alterations()

    app_test.chronicle_genomic_alterations.values_verification_for_Geonomic_alterations(dict=fields_data3)
    app_test.chronicle_genomic_alterations.verify_biomarkers_values(dict=biomarkers_values3)

    app_test.chronicle_genomic_alterations.verify_section_is_displayed()

    log.info("Test Passed- section is removed and verified successfully")














