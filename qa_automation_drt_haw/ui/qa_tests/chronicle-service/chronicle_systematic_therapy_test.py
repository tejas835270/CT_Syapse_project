import time
from qa_automation_drt_haw.settings import Config
import pytest


from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_elements

username = Config.portal_chronicle_username
psw = Config.portal_chronicle_password

patient = pytest.data.get_patient_first_last_name('patient_systematic_therapy')
PDS_service_name= pytest.data.get_service_name('PDS')
fields_data = pytest.data.get_data('Chronicle_Systemic_Therapy_data')
fields_data2 = pytest.data.get_data('Chronicle_Systemic_Therapy1_data')
fields_data3 = pytest.data.get_data('Chronicle_Systemic_Therapy1_data_changes')
fields_data4 = pytest.data.get_data('Chronicle_Systemic_Therapy_no_data')
fields_data5 = pytest.data.get_data('only_regiment_agent_value')

pytestmark=pytest.mark.skip(reason="currently not required due to low priority")

@pytest.fixture(scope="function")
def pick_patient_for_chronicle(request, app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.find_and_pick_patient(patient)
    yield
    app_test.driver.close()


@pytest.mark.p1
def test_fill_up_all_and_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Systemic Therapy - Fill up all the fields and Save
    """
    log.info("Test Started- to Fill up all the fields, Save and verify values ")
    # clear data before starting the test-if there is any
    log.info(app_test.chronicle_systemic_therapy.section1_locator)
    app_test.chronicle_systemic_therapy.remove_all_sections_from_Systematic_therapy()
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.chronicle.click_Add_Another()

    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_systemic_therapy.Systemic_Therapy_fill_out_the_fields(dict=fields_data)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.chronicle_systemic_therapy.Systemic_Therapy_values_verification(dict=fields_data)
    log.info("Test Passed - all the fields value saved and verified successfully")


@pytest.mark.p3
def test_add_another(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Systemic Therapy - Add Another
    """
    log.info("Test Started- to add another section , fill the fields and verify values")
    # to remove dependancy first run "test_fill_up_all_and_save"
    test_fill_up_all_and_save(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_systemic_therapy.click_add_button_for_section_and_role()
    app_test.chronicle_systemic_therapy.Systemic_Therapy_fill_out_the_fields(dict=fields_data2,section_name=app_test.chronicle_systemic_therapy.section2_locator)

    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.chronicle_systemic_therapy.Systemic_Therapy_values_verification(dict=fields_data)
    app_test.chronicle_systemic_therapy.Systemic_Therapy_values_verification(dict=fields_data2,section=app_test.chronicle_systemic_therapy.section2_locator_for_verification)
    log.info("Test Passed - another section is added and verified successfully")

@pytest.mark.p2
def test_change_all_save(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Systemic Therapy - Change all values in the fields and Save
    """
    log.info("Test Started to test - to Change all values in the fields and Save")
    # to remove dependancy first run "test_add_another"
    test_add_another(app_test, pick_patient_for_chronicle, test_info)
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    # remove existing data from field before changing them
    #time.sleep(5)
    app_test.chronicle_systemic_therapy.remove_data_from_all_fields()
    app_test.chronicle_systemic_therapy.Systemic_Therapy_fill_out_the_fields(dict=fields_data3,section_name=app_test.chronicle_systemic_therapy.section2_locator)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.chronicle_systemic_therapy.Systemic_Therapy_values_verification(dict=fields_data3,section=app_test.chronicle_systemic_therapy.section2_locator_for_verification)
    log.info("Test Passed")

@pytest.mark.p2
def test_drugs_add_another(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Systemic Therapy - Anti-cancer agents/drugs - Add Another field
    """
    # clear data before starting the test-if there is any
    app_test.chronicle_systemic_therapy.remove_all_sections_from_Systematic_therapy()
    log.info("Test Started to test -Systemic Therapy - Anti-cancer agents/drugs - Add Another field")
    #adding below step to make this Tc independent
    app_test.chronicle_patient_status.chronicle_tab_Patient_Status()
    app_test.chronicle_patient_status.select_Alive_radiobutton()
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.chronicle.click_Add_Another()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle_systemic_therapy.agentOrDrug_add_another()
    app_test.chronicle_systemic_therapy.select_value_for_agentOrDrug1()
    app_test.chronicle_systemic_therapy.agentOrDrug_add_another()
    app_test.chronicle_systemic_therapy.select_value_for_agentOrDrug2()
    log.info("Test Passed")


@pytest.mark.p3
def test_regiment_agent_value_not_in_vocab(app_test,pick_patient_for_chronicle,test_info):
    """
    Chronicle - Systemic Therapy - Regimen and Agent/drug -  enter in a value not in the vocab
    """
    # clear data before starting the test-if there is any
    app_test.chronicle_systemic_therapy.remove_all_sections_from_Systematic_therapy()
    log.info("Test Started to test - Systemic Therapy - Regimen and Agent/drug -  enter in a value not in the vocab")
    #app_test.navigation.refresh_page()
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.navigation.hide_header()
    app_test.navigation.hide_footer()
    app_test.chronicle.click_Add_Another()
    app_test.chronicle_systemic_therapy.Systemic_Therapy_fill_out_the_fields(dict=fields_data5)
    app_test.navigation.show_footer()
    app_test.chronicle.click_on_save()
    app_test.navigation.refresh_page()
    app_test.chronicle_systemic_therapy.chronicle_tab_Systemic_Therapy()
    app_test.chronicle_systemic_therapy.Systemic_Therapy_values_verification(dict=fields_data5)
    log.info("Test Passed- Regimen and Agent/drug value not in vocab saved and verified successfully")

