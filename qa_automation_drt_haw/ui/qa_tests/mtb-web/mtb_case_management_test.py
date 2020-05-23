import pytest
import time
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password
meeting_date = pytest.data.get_mtb_create_case_data('Meeting_Date')
Primary_Oncologist_data = pytest.data.get_mtb_create_case_data('Primary_Oncologist')
Diagnosis_Date = pytest.data.get_mtb_create_case_data('Diagnosis_Date')
histology_data = pytest.data.get_mtb_create_case_data('Histology')
case_Narrative_data = pytest.data.get_mtb_create_case_data('case_Narrative')
Recommendations_Summary = pytest.data.get_mtb_create_case_data('Recommendations_Summary')
meeting_notes = pytest.data.get_mtb_create_case_data('random_meeting_notes')
# pick up dropdown value fron vocab csv
primary_site_csv = pytest.data.retrive_data_from_csv(data_file='Data_vocab/Primary_Site.csv')
stage_group_csv = pytest.data.retrive_data_from_csv(data_file='Data_vocab/StageGroup.csv')

# todo: text will be changed
@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    log.info("Opening application")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()


@pytest.mark.p4
@pytest.mark.p2
def test_user_choose_to_sort_meeting_date_in_ascending_order(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'check default sorting of meeting date'
    log.info("\n Test Started - to check default sorting of meeting date")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.meeting_date_ascending_sorting()
    log.info("\n Test Ended")


@pytest.mark.p1
def test_mtb_create_case_without_site(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'create case without primary site'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to create case without primary site")
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.enter_diagnosis_date(date=Diagnosis_Date)
    app_test.mtb_create_case_page.select_option_from_Stage_Group_dd(option_name=stage_group_csv[15][0])
    app_test.mtb_create_case_page.select_option_from_Histology(option_name=histology_data)
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_create_case_page.click_on_save_and_close()

    # verify that case is created succcessfully with correct data
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    app_test.mtb_create_case_page.mtb_case_values_verification(meeting_date=meeting_date, diagnosis_date=Diagnosis_Date,
                                                               primary_oncologist_data=Primary_Oncologist_data,
                                                               stage_group_option=stage_group_csv[15][0], histology_data=histology_data)
    log.info("\n Test Ended")


@pytest.mark.p1
def test_add_recommendation_summarytext_(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'create case by adding recommendation summary'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to create case by adding recommendation summary")
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.enter_diagnosis_date(date=Diagnosis_Date)
    app_test.mtb_create_case_page.enter_text_in_caseNarrative(what=case_Narrative_data)
    app_test.mtb_create_case_page.enter_text_in_recommendationsSummary(what=Recommendations_Summary)
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_create_case_page.click_on_save_and_close()

    # verify that case is created succcessfully with correct data
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    app_test.mtb_create_case_page.mtb_case_values_verification(meeting_date=meeting_date, diagnosis_date=Diagnosis_Date,
                                                          primary_oncologist_data=Primary_Oncologist_data,
                                                          recommendation_summary_data=Recommendations_Summary,
                                                          case_narrative_data=case_Narrative_data)

    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_add_verify_header_casemgmtscreen(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify headers in case mgmt screen'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to Verify headers in case mgmt screen")
    app_test.mtb_case_management_page.verify_all_column_header_on_table()
    log.info("\n Test Ended")


@pytest.mark.p4
@pytest.mark.p0
def test_cases_text_on_casemgmtscreen(app_test, test_launch_mtb, test_info):
    pytest.log_test = "Verify text 'Cases' exists in case mgmt screen"
    log.info("\n Test Started - to Verify text 'Cases' exists in case mgmt screen")
    app_test.mtb_case_management_page.verify_Cases_text_present_on_page()
    log.info("\n Test Ended")

@pytest.mark.p0
def test_mtb_text_on_casemgmtscreen(app_test, test_launch_mtb):
    pytest.log_test = 'Verify text mtb exist in case mgmt screen'
    log.info("\n Test started - to Verify text mtb exist in case mgmt screen")
    app_test.mtb_case_management_page.verify_Molecular_Tumor_Board_text_present_on_page()
    log.info("\n Test Ended")


@pytest.mark.p1
def test_verify_deidentified_header_mrn(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'create case by adding recommendation summary'
    # Navigate to mtb_url - to make tc independent
    log.info("\n Test Started - to verify deidentified_header_mrn")
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    mrn = app_test.finder.pick_patient_mrn()
    app_test.finder.find_and_pick_patient(mrn)
    last_4_digit_of_mrn = app_test.finder.find_last_4_digits_from_MRN()
    app_test.mtb_create_case_page.verify_mrn_present_in_deidentified_header(param=last_4_digit_of_mrn)
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p1
def test_user_navigates_to_Case_management_from_patient_finder(app_test,test_launch_mtb,test_info):
    pytest.log_test = 'Verify the user is able to navigate back to case management screens' \
                      ' from patient finder screen when clicked on MTB case management text'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-485'
    log.info('Test started ')
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.navigation.click_text(app_test.mtb_case_management_page.mtb_case_management_text)
    log.info('Test ended')

@pytest.mark.p3
@pytest.mark.p4
def test_user_navigates_portal_when_clicked_on_syapselogo(app_test,test_launch_mtb,test_info):
    pytest.log_test = 'Verify user navigates to Portal Page when clicked on Syapse Text from MTB Case Management page'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-628'
    log.info('Test started ')
    app_test.verification.text_present_on_page(app_test.mtb_case_management_page.Create_New_Case_text)
    app_test.portal.click_syapse_logo()
    app_test.portal.verify_url_contains_portal()


@pytest.mark.p4
@pytest.mark.p3
def test_verify_dob_format(app_test,test_launch_mtb,test_info):
    pytest.log_test = ' Verify the DOB format of the Patients from the search results'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-634'
    log.info("Test Started")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.show_searched_patient()
    app_test.mtb_case_management_page.verify_DOB_format()

@pytest.mark.p4
@pytest.mark.p0
def test_verify_cases_are_available_on_mtb_and_pagination_functionality(app_test, test_launch_mtb,
                                                                        test_info):
    pytest.log_test = 'Verify user has the ability to view cases on mtb and ' \
                      'navigate through different case pages'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-123'
    log.info(
        "\n Test Started - to verify_cases_are_available_on_mtb_and_pagination_functionality")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_create_case_page.verify_no_of_cases_on_MTB_page()
    app_test.mtb_create_case_page.store_applied_sorting()
    app_test.mtb_create_case_page.open_and_verify_next_page()
    app_test.mtb_create_case_page.verify_sorting_applied()
    app_test.mtb_create_case_page.apply_case_id_sort('ascending')
    app_test.mtb_create_case_page.store_applied_sorting()
    app_test.mtb_create_case_page.open_and_verify_next_page()
    app_test.mtb_create_case_page.verify_sorting_applied()
    app_test.mtb_create_case_page.apply_diagnosis_sort()
    app_test.mtb_create_case_page.store_applied_sorting()
    app_test.mtb_create_case_page.open_and_verify_next_page(2)
    app_test.mtb_create_case_page.open_and_verify_previous_page()
    app_test.mtb_create_case_page.verify_sorting_applied()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_navigation_to_next_or_previous_five_pages(app_test, test_launch_mtb,
                                              test_info):
    pytest.log_test = 'Verify user has the ability to navigate to next/previous five pages'
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-123"
    log.info(
        "\n Test Started - to verify_navigation_to_next_or_previous_five_pages")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_create_case_page.verify_no_of_cases_on_MTB_page()
    app_test.mtb_create_case_page.double_navigate_to_right()
    app_test.mtb_create_case_page.double_navigate_to_left()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_navigation_to_mtb_page_from_case_management_screen(app_test, test_launch_mtb,
                                                              test_info):
    pytest.log_test = "Verify user has the ability to navigate to mtb page from case management " \
                      "screen by clicking on 'MTB Case Management'"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-143"
    log.info(
        "\n Test Started - to verify_navigation_to_mtb_page_from_case_management_screen")
    app_test.mtb_case_management_page.navigate_to_caseID('any')
    app_test.mtb_case_management_page.verify_mtb_case_management_text_is_dispalyed()
    app_test.mtb_case_management_page.click_on_MTB_case_management()
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_behaviour_of_mtb_case_management_text_on_scrolling(app_test, test_launch_mtb,
                                                           test_info):
    pytest.log_test = "Verify MTB case management text is removed when scrolled down and appears back when scrolled up"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-143"
    log.info(
        "\n Test Started - to verify_behaviour_of_MTB_case_management_text_on_scrolling")
    app_test.mtb_case_management_page.navigate_to_caseID('any')
    app_test.mtb_case_management_page.verify_mtb_case_management_text_is_dispalyed()
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_case_management_page.verify_mtb_case_management_text_not_present_on_page()
    app_test.verification.scroll_to_top_of_page()
    app_test.mtb_case_management_page.verify_mtb_case_management_text_is_dispalyed()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_meeting_notes_after_sticky_patient_header(app_test, test_launch_mtb,
                                                              test_info):
    pytest.log_test = "Verify meeting notes is opened after scrolling down to the page'"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-142"

    log.info(
        "\n Test Started - to verify_meeting_notes_after_sticky_patient_header")
    app_test.mtb_case_management_page.navigate_to_caseID('any')
    app_test.mtb_case_management_page.verify_mtb_case_management_text_is_dispalyed()
    app_test.mtb_create_case_page.open_existing_meeting_notes()
    app_test.mtb_create_case_page.enter_meeting_notes(meeting_notes)
    app_test.mtb_create_case_page.close_meeting_notes()
    app_test.navigation.refresh_page()
    app_test.mtb_case_management_page.verify_mtb_case_management_text_is_dispalyed()
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_create_case_page.open_existing_meeting_notes()
    app_test.mtb_create_case_page.enter_meeting_notes(meeting_notes)
    app_test.mtb_create_case_page.close_meeting_notes()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_attachment_download_functionality(app_test, test_launch_mtb,
                                                              test_info):
    pytest.log_test = "Verify downloading functionality for the attachments"
    pytest.log_link = ["https://syapse.atlassian.net/browse/BUMP-116",
                       "https://syapse.atlassian.net/browse/BUMP-46",]

    log.info(
        "\n Test Started - to verify_attachment_download_functionality")
    case_url = Config.case_url_with_attachments
    app_test.mtb_case_management_page.navigate_to_case(case_url)
    app_test.mtb_case_management_page.verify_availability_of_attachments()
    app_test.mtb_case_management_page.verify_download_button_available_for_attachments()
    app_test.mtb_case_management_page.verify_attachments_got_downloaded()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_confirmation_requested_when_deleting_attachment(app_test, test_launch_mtb,
                                                              test_info):
    pytest.log_test = "Verify confirmation is requested when deleting the attachments"
    pytest.log_link = ["https://syapse.atlassian.net/browse/BUMP-46",
                       "https://syapse.atlassian.net/browse/BUMP-42"]
    log.info(
        "\n Test Started - to verify_confirmation_requested_when_deleting_attachment")
    case_url = Config.case_url_with_attachments
    app_test.mtb_case_management_page.navigate_to_case(case_url)
    app_test.mtb_case_management_page.verify_availability_of_attachments()
    app_test.mtb_case_management_page.verify_delete_button_available_for_attachments()
    app_test.mtb_case_management_page.verify_deletion_of_all_attachments()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_carousel_view_and_attachments_are_not_downloaded_by_clicking_on_file(app_test, test_launch_mtb,
                                                              test_info):
    pytest.log_test = "Verify confirmation is requested when deleting the attachments"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-42"
    log.info(
        "\n Test Started - to verify_attachments__are not_downloaded_by_clicking_on_file_name")
    case_url = Config.case_url_with_attachments
    app_test.mtb_case_management_page.navigate_to_case(case_url)
    app_test.mtb_case_management_page.verify_availability_of_attachments()
    app_test.mtb_case_management_page.check_whether_carousel_opens_on_clicking_attachment()
    app_test.mtb_case_management_page.verfify_files_are_not_downlaoded_after_clicking_on_file()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_dark_mode_button_when_meeting_notes_is_opened(app_test, test_launch_mtb,
                                                           test_info):
    pytest.log_test = "Verify whether dark mode button is available when meeting notes is opened"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-144"
    log.info(
        "\n Test Started - to verify_dark_mode_button_when_meeting_notes_is_opened")
    app_test.mtb_case_management_page.navigate_to_caseID('any')
    app_test.mtb_create_case_page.open_existing_meeting_notes()
    app_test.mtb_case_management_page.verify_dark_button_is_available()
    app_test.mtb_case_management_page.activate_dark_mode()
    app_test.mtb_create_case_page.close_meeting_notes()
    app_test.mtb_case_management_page.verify_dark_button_is_available()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_success_banner_is_provided_when_case_is_saved(app_test, test_launch_mtb,
                                                           test_info):
    pytest.log_test = "Verify case is saved success banner pops up"
    pytest.log_link = "https://syapse.atlassian.net/browse/BUMP-107"
    log.info(
        "\n Test Started - to verify_success_banner_is_provided_when_case_is_saved")
    app_test.mtb_case_management_page.navigate_to_caseID('any')
    app_test.mtb_create_case_page.save_case()
    log.info("\n Test Ended")