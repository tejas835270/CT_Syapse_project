
from qa_automation_drt_haw.settings import Config
import pytest
import time
from qa_automation_drt_haw.qa_utils.backend_data import *

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password
meeting_date = pytest.data.get_mtb_create_case_data('Meeting_Date')
Primary_Oncologist_data = pytest.data.get_mtb_create_case_data('Primary_Oncologist')
Diagnosis_Date = pytest.data.get_mtb_create_case_data('Diagnosis_Date')
histology_data = pytest.data.get_mtb_create_case_data('Histology')
Recommendations_Summary= pytest.data.get_mtb_create_case_data('Recommendations_Summary')
meeting_notes = pytest.data.get_mtb_create_case_data('random_meeting_notes')
disallowed_characters = pytest.data.get_mtb_create_case_data('disallowed_characters')
patient_name = pytest.data.get_mtb_create_case_data('patient_name')
special_chars_list = pytest.data.get_mtb_create_case_data('Special_chars')
patient_search = Config.patient_search_multiple_results
case_Narrative_data = pytest.data.get_mtb_create_case_data('case_Narrative')
Recommendation_notes_single_line = pytest.data.get_mtb_create_case_data('Recommendation_notes_single_line')
Recommendation_notes_multi_line = pytest.data.get_mtb_create_case_data('Recommendation_notes_multi_line')
patient_with_report = Config.auto_report_patient_mrn
# pick up dropdown value fron vocab csv
primary_site_csv = pytest.data.retrive_data_from_csv(data_file='Data_vocab/Primary_Site.csv')
stage_group_csv = pytest.data.retrive_data_from_csv(data_file='Data_vocab/StageGroup.csv')

#todo: text will be changed
@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    log.info("Opening application")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()


@pytest.mark.p0
def test_mtb_create_case_button_exists(app_test, test_launch_mtb,test_info):
    pytest.log_test = 'Verify Create Case button exists and is clickable'
    log.info("\n Test Started - to Verify Create Case button exists and it is clickable")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.navigation.browser_back()
    log.info("\n Test Ended")


@pytest.mark.p1
def test_mtb_create_case_with_meetingDate(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'create case with meeting date and check case mgmt screen'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to create case with meeting date and check case mgmt screen")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.enter_diagnosis_date(date=Diagnosis_Date)
    app_test.mtb_create_case_page.select_option_from_Primary_Site(option_name=primary_site_csv[3][0])
    app_test.mtb_create_case_page.select_option_from_Stage_Group_dd(option_name=stage_group_csv[15][0])
    app_test.mtb_create_case_page.select_option_from_Histology(option_name=histology_data)
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_create_case_page.click_on_save_and_close()
    # verify that case is created succcessfully with correct data
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    app_test.mtb_create_case_page.mtb_case_values_verification(meeting_date=meeting_date, diagnosis_date=Diagnosis_Date,
                                                          primary_oncologist_data=Primary_Oncologist_data,
                                                          primary_sites=primary_site_csv[3][0],
                                                          stage_group_option=stage_group_csv[15][0],
                                                          histology_data=histology_data)
    log.info("\n Test Ended")


@pytest.mark.p2
def test_mtb_create_case_without_meetingDate(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'create case without meeting date and check case mgmt screen'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to create case without meeting date")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.enter_diagnosis_date(date=Diagnosis_Date)
    app_test.mtb_create_case_page.select_option_from_Primary_Site(option_name=primary_site_csv[3][0])
    app_test.mtb_create_case_page.select_option_from_Stage_Group_dd(option_name=stage_group_csv[15][0])
    app_test.mtb_create_case_page.select_option_from_Histology(option_name=histology_data)
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_create_case_page.click_on_save_and_close()
    # verify that case is created succcessfully with correct data
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    app_test.mtb_create_case_page.mtb_case_values_verification(diagnosis_date=Diagnosis_Date,
                                                          primary_oncologist_data=Primary_Oncologist_data,
                                                          primary_sites=primary_site_csv[3][0],
                                                          stage_group_option=stage_group_csv[15][0],
                                                          histology_data=histology_data)

    log.info("\n Test Ended")


@pytest.mark.p1
def test_mtb_click_cancel_button(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'click cancel button without adding entries any fields'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to verify cancle button")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.click_on_Cancel_button()
    #app_test.mtb_create_case_page.verify_user_clicks_on_continue()
    app_test.mtb_case_management_page.verify_current_url_contains_mtb()
    app_test.mtb_case_management_page.verify_Molecular_Tumor_Board_text_present_on_page()
    log.info("\n Test Ended")


@pytest.mark.p2
def test_mtb_create_case_without_site(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'create case without primary site'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to create case without primary site")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.enter_diagnosis_date(date=Diagnosis_Date)
    app_test.mtb_create_case_page.select_option_from_Stage_Group_dd(option_name=stage_group_csv[15][0])
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_create_case_page.click_on_save_and_close()
    app_test.mtb_case_management_page.verify_current_url_contains_mtb()
    app_test.mtb_case_management_page.verify_Molecular_Tumor_Board_text_present_on_page()

    # verify that case is created succcessfully with correct data
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    app_test.mtb_create_case_page.mtb_case_values_verification(meeting_date=meeting_date, diagnosis_date=Diagnosis_Date,
                                                          primary_oncologist_data=Primary_Oncologist_data,
                                                          stage_group_option=stage_group_csv[15][0],
                                                          histology_data=histology_data)
    log.info("\n Test Ended")


@pytest.mark.p2
def test_mtb_create_case_without_site_histology(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'create case without histology field value'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to create case without histology field value")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.enter_diagnosis_date(date=Diagnosis_Date)
    app_test.mtb_create_case_page.select_option_from_Stage_Group_dd(option_name=stage_group_csv[15][0])
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_create_case_page.click_on_save_and_close()
    app_test.mtb_case_management_page.verify_current_url_contains_mtb()
    app_test.mtb_case_management_page.verify_Molecular_Tumor_Board_text_present_on_page()
    # verify that case is created succcessfully with correct data
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    app_test.mtb_create_case_page.mtb_case_values_verification(meeting_date=meeting_date, diagnosis_date=Diagnosis_Date,
                                                          primary_oncologist_data=Primary_Oncologist_data,
                                                          stage_group_option=stage_group_csv[15][0] )

    log.info("\n Test Ended")

#TODO : Once pagination is avialable in SQA, need to uncomment p4

#@pytest.mark.p4
@pytest.mark.p2
def test_verify_error_msg_in_case_narrative_field(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify the error message, when special characters like ` ~  are entered in Case narrative field'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-507'
    log.info("\n Test Started - to verify_error_message_on_special_characters_in_case_narrative_field")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.enter_text_in_caseNarrative(disallowed_characters)
    app_test.mtb_create_case_page.verify_error_message(app_test.mtb_create_case_page.caseNarrative_field_error)
    log.info("\n Test Ended")

#TODO : Once pagination is avialable in SQA, need to uncomment p4

#@pytest.mark.p4
@pytest.mark.p2
def test_verify_error_msg_in_meeting_notes(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify the error message, when special characters like ` ~  are entered in meeting notes field'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-439'
    log.info("\n Test Started - to verify_error_message_on_special_characters_in_meeting_notes")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.open_new_meeting_notes()
    app_test.mtb_create_case_page.enter_meeting_notes(disallowed_characters)
    app_test.mtb_create_case_page.verify_error_message(app_test.mtb_create_case_page.meeting_notes_field_error)
    log.info("\n Test Ended")


@pytest.mark.p2
def test_verify_meeting_notes_when_reopened(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify the text gets saved in meeting notes when case is saved and meeting drawer is opened again'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-502'
    log.info("\n Test Started - to verify_meeting_notes_when_reopened")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.open_new_meeting_notes()
    app_test.mtb_create_case_page.enter_meeting_notes(meeting_notes)
    app_test.navigation.refresh_page()
    app_test.mtb_create_case_page.open_new_meeting_notes()
    app_test.mtb_create_case_page.verify_entered_meeting_notes('Empty')
    app_test.mtb_create_case_page.enter_meeting_notes(meeting_notes)
    app_test.mtb_create_case_page.save_case()
    app_test.navigation.refresh_page()
    app_test.mtb_create_case_page.open_existing_meeting_notes()
    app_test.mtb_create_case_page.verify_entered_meeting_notes(meeting_notes)
    log.info("\n Test Ended")

#TODO : Once pagination is avialable in SQA, need to uncomment p4

#@pytest.mark.p4
@pytest.mark.p2
def test_verify_scroll_working_in_mtb_case(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify the Scrolling down is working within a case after clicking on ‘Add’ links'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-590'
    log.info("\n Test Started - to verify_scroll_working_in_mtb_case")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.navigate_to_caseID('any')
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_case_management_page.verify_recommendations_summary_text_is_dispalyed()
    app_test.verification.scroll_to_top_of_page()
    app_test.mtb_case_management_page.verify_mtb_case_management_text_is_dispalyed()
    app_test.mtb_create_case_page.open_option_list_for_Histology()
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_case_management_page.verify_recommendations_summary_text_is_dispalyed()
    app_test.navigation.refresh_page()
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_case_management_page.verify_recommendations_summary_text_is_dispalyed()
    log.info("\n Test Ended")


@pytest.mark.p3
@pytest.mark.p4
def test_mtb_popup_appears_when_back_button_isclicked(app_test, test_launch_mtb, test_info):
    pytest.log_test = ' Verify a popup appears when the back button is clicked ' \
                      'when modifications are made and the case is not saved'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-448'
    log.info("Test Started")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.navigation.click_text(app_test.mtb_create_case_page.mtb_case_management)
    app_test.verification.verify_cancel_button_popup_is_displayed()
    log.info('Test Ended')

@pytest.mark.p2
@pytest.mark.p4
def test_verify_error_message_when_2_characters_entered_patient_search(app_test, test_launch_mtb, test_info):
    pytest.log_test = ' Verify error message appears when less than 3 characters are ' \
                      'entered in the search field of the patient finder'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-627'
    log.info("Test Started")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.find_only_patient_name(patient_name)
    app_test.verification.text_present_on_page(app_test.mtb_create_case_page.search_error)



@pytest.mark.p3
@pytest.mark.p4
@pytest.mark.parametrize(argnames="Special_Chars", argvalues=list(special_chars_list))
def test_verify_error_message_when_special_characters_entered_in_search_box(app_test, test_launch_mtb, Special_Chars,
                                                                            test_info):
    pytest.log_test = ' Verify error message appears when special characters like `~ @#$^ {} | ' \
                      'are entered in search box of patient finder page'
    pytest.log_link = ['https://syapse.atlassian.net/browse/BUMP-629',
                       'https://syapse.atlassian.net/browse/BUMP-633']
    log.info("Test Started")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.find_only_patient_name(patient_name + Special_Chars)
    app_test.mtb_create_case_page.verify_special_char_error_message_is_displayed()
    log.info("Test Ended")


@pytest.mark.p0
@pytest.mark.p4
def test_verify_mrn_digit_count(app_test, test_launch_mtb, test_info):
    pytest.log_test = ' Verify the MRN format of patients in patient search'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-635'
    log.info("Test Started")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.show_searched_patient()
    mrn_len = app_test.finder.find_last_4_digits_from_MRN()
    mrn = len(str(mrn_len))
    if mrn <= 3:
        log.info("MRN number should be atleast of 4 digits")
        assert False, "MRN is not a valid MRN"
    else:
        log.info("MRN is a Valid MRN")
        assert True, "MRN is a valid MRN"


@pytest.mark.p4
@pytest.mark.p3
def test_verify_patient_sex_value(app_test, test_launch_mtb, test_info):
    pytest.log_test = ' Verify the sex value of the patient in patient search'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-636'
    log.info("Test Started")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.show_searched_patient()
    app_test.mtb_create_case_page.verify_sex_value()

@pytest.mark.p4
@pytest.mark.p0
def test_verify_dark_mode_button_availability_on_mtb_pages(app_test, test_launch_mtb,
                                                              test_info):
    pytest.log_test = "Verify whether dark mode button's availability on mtb pages"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-144"
    log.info(
        "\n Test Started - to verify_dark_mode_button_availability_on_mtb_pages")
    app_test.mtb_case_management_page.verify_dark_button_is_available()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.mtb_case_management_page.verify_dark_button_is_available()
    app_test.finder.search_specific_patient()
    app_test.mtb_case_management_page.verify_dark_button_is_available()
    app_test.mtb_case_management_page.click_on_MTB_case_management()
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.verify_dark_button_is_available()
    app_test.portal.click_syapse_logo()
    app_test.portal.verify_portal_home_screen()
    app_test.mtb_case_management_page.verify_dark_button_is_not_available()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_dark_mode_activation_on_mtb_pages(app_test, test_launch_mtb,
                                                           test_info):
    pytest.log_test = "Verify whether dark mode style is activated on mtb pages"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-144"
    log.info(
        "\n Test Started - to verify_dark_mode_activation_on_mtb_pages")
    app_test.mtb_case_management_page.verify_dark_button_is_available()
    app_test.mtb_case_management_page.activate_dark_mode()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_activated()
    app_test.mtb_case_management_page.deactivate_dark_mode()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_deactivated()
    app_test.finder.search_specific_patient()
    app_test.mtb_case_management_page.activate_dark_mode()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_activated()
    app_test.mtb_case_management_page.deactivate_dark_mode()
    app_test.mtb_case_management_page.click_on_MTB_case_management()
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.activate_dark_mode()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_activated()
    app_test.portal.click_syapse_logo()
    app_test.portal.verify_portal_home_screen()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_deactivated()
    app_test.portal.navigate_to_mtb_service()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_deactivated()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_dark_mode_deactivation_on_mtb_pages(app_test, test_launch_mtb,
                                                           test_info):
    pytest.log_test = "Verify whether dark mode style is activated on mtb pages"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-144"
    log.info(
        "\n Test Started - to verify_dark_mode_deactivation_on_mtb_pages")
    app_test.mtb_case_management_page.verify_dark_button_is_available()
    app_test.mtb_case_management_page.activate_dark_mode()
    app_test.mtb_case_management_page.deactivate_dark_mode()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_deactivated()
    app_test.finder.search_specific_patient()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_deactivated()
    app_test.mtb_case_management_page.click_on_MTB_case_management()
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_deactivated()
    app_test.portal.click_syapse_logo()
    app_test.portal.verify_portal_home_screen()
    app_test.mtb_case_management_page.verify_dark_mode_style_is_deactivated()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p3
def test_verify_no_of_patient_in_search_results(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify the number of patients in search result on each page'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-317'
    log.info("\n Test Started - to check No of patients in search result")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    # patient is searche as using api we will get only 1 value and to test this functionality we should have
    # more than 10 patient results
    patient_search = get_patient_last_name_with_max_count()
    app_test.finder.find_only_patient_name(patient_search)
    count = app_test.finder.get_patient_count_on_current_page()
    for num in range(4):
        if count >= 10:
            app_test.finder.open_and_verify_patient_next_page()
            if app_test.finder.get_patient_count_on_current_page() >= 10:
                log.info("Current page also contains 10 patients")
            assert True, "Next pages Contains 10 patients"
        else:
            log.error("More than 10 patients are present")
            assert False, "More than 10 patients are present"

    log.info("\n Test Ended")

# Todo Validated against Recommendation Summary and Meeting Notes fields
@pytest.mark.p4
@pytest.mark.p3
def test_verify_lines_are_preserved_in_text_boxes(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify the new lines are preseverd in text boxes in MTB'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-651'
    log.info("\n Test Started - to verify new lines are preserved in text boxes")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.enter_text_in_caseNarrative(what=case_Narrative_data)
    app_test.mtb_create_case_page.enter_text_in_recommendationsSummary(what=Recommendations_Summary)
    app_test.mtb_create_case_page.open_new_meeting_notes()
    app_test.mtb_create_case_page.enter_meeting_notes(meeting_notes)
    app_test.mtb_create_case_page.close_meeting_notes()
    app_test.mtb_create_case_page.verify_entered_Recommendation_summary(Recommendations_Summary)
    app_test.mtb_create_case_page.open_existing_meeting_notes()
    app_test.mtb_create_case_page.verify_entered_meeting_notes(meeting_notes)

    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p3
def test_verify_primary_oncologist_accepts_100_chars(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Primary oncologist Text box area should be limited to 100 characters length'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-405'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to verify the count of primary oncologist field accepts")
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.verify_no_characters_in_primary_oncologist(Primary_Oncologist_data)
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p3
@pytest.mark.parametrize(argnames="Notes",
                         argvalues=(Recommendation_notes_single_line, Recommendation_notes_multi_line))
def test_verify_recommendation_notes_height_increases_as_text_increased(app_test, test_launch_mtb, Notes, test_info):
    pytest.log_test = 'Verify recommendation Notes increases in height when more character are entered'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-400'
    log.info("\n Test Started - to verify the recommendation notes increases in height")
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.navigation.click_btn(app_test.mtb_create_case_page.add_recommendation_text)
    app_test.mtb_create_case_page.enter_text_in_recommendation_notes_and_verify_field_height_increases(Notes)
    log.info("\n Test Ended")

# Todo test this test case with a patient having reports associated with it.
#TODO : Skipped in SQA as need to work on data in SQA

@pytest.mark.p2
# @pytest.mark.p4
def test_verify_refresh_button_is_visible(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify the refresh button is visible on page'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-652'
    log.info("\n Test Started - to verify the visibility of refresh button on page")
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.find_and_pick_patient(patient_with_report)
    app_test.mtb_create_case_page.verify_refresh_button_is_displayed()

# Todo test this test case with a patient having reports associated with it.
# Todo Validation is made based on the total reports present on the page for the patient in case
#TODO : Skipped in SQA as need to work on data in SQA

@pytest.mark.p2
# @pytest.mark.p4
def test_verify_total_no_of_reports_for_patient(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify all the reports associated with patients are displayed on page'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-74'
    log.info("\n Test Started - to Verify all the reports associated with patients are displayed on page")
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.find_and_pick_patient(patient_with_report)
    app_test.mtb_create_case_page.verify_refresh_button_is_displayed()
    app_test.mtb_create_case_page.verify_total_reports()

# Todo test this test case with a patient having reports associated with it.
#TODO : Skipped in SQA as need to work on data in SQA

@pytest.mark.p2
def test_verify_success_msg_on_report_load(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify all success message when reports are loaded successfully'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-139'
    log.info("\n Test Started - to Verify success message when reports are loaded successfully")
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.find_and_pick_patient(patient_with_report)
    app_test.mtb_create_case_page.verify_refresh_button_is_displayed()
    app_test.mtb_create_case_page.verify_success_message_on_report_load_is_displayed()

@pytest.mark.p4
@pytest.mark.p3
def test_verify_page_tile_component_for_portal(app_test,test_info):
    pytest.log_test = 'Verify page tile component in Portal'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-48'
    log.info("\n Test Started - to Verify page tile component of Portal UI")
    app_test.portal.login(username, psw)
    app_test.portal.verify_page_tile_welcome_text_height()


@pytest.mark.p4
@pytest.mark.p3
def test_verify_page_tile_component_for_MTB(app_test,test_launch_mtb,test_info):
    pytest.log_test = 'Verify page tile component in MTB '
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-48'
    log.info("\n Test Started - to Verify page tile component of MTB UI")
    app_test.mtb_create_case_page.verify_page_tile_Molecular_Tumor_Board_text_height()