import pytest
import time
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password
Primary_Oncologist_data = pytest.data.get_mtb_create_case_data('Primary_Oncologist')
meeting_date = pytest.data.get_mtb_create_case_data('Meeting_Date')
meeting_notes = pytest.data.get_mtb_create_case_data('meeting_notes_11_rows')


# todo: text will be changed
@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    log.info("Opening application")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()


@pytest.mark.p3
@pytest.mark.parametrize(argnames='Zoom',argvalues={'1.2','0.5'})
def test_verify_meeting_note_height(app_test,test_launch_mtb,Zoom,test_info):
    pytest.log_test = 'Verify the initial meeting notes and after click on meeting notes height.Also verify the scroll ' \
                      'appears when max height of text box is reached and text overflows'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-726'
    log.info("\n Test Started - to Verify the initial meeting notes and after click on meeting notes height")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.navigation.click_btn(app_test.mtb_create_case_page.open_meeting_notes)
    app_test.mtb_create_case_page.verify_inital_height_of_meting_notes()
    app_test.mtb_create_case_page.get_max_height_of_meeting_notes_text_area()
    app_test.mtb_create_case_page.enter_meeting_notes(meeting_notes)
    app_test.mtb_create_case_page.click_on_save_and_close()
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    app_test.mtb_create_case_page.verification_in_zoom_mode(Zoom)
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p3
def test_verify_none_provided_text_is_present(app_test,test_launch_mtb,test_info):
    pytest.log_test = 'Verify None Provide text on place holder is absent on case form page'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-186'
    log.info("\n Test Started - to Verify None Provide text on place holder is absent on case form page")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    if app_test.mtb_create_case_page.verify_none_provided_text_is_absent():
        log.info("The field is editable and data can be entered in the fields")
        app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test_verify_sorting(app_test,test_launch_mtb,test_info):
    pytest.log_test = 'Verify cases are sorted in ascending order with no meeting date cases are at top'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-647'
    log.info("\n Test Started - to Verify cases are sorted in ascending order with no meeting date cases are at top")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_create_case_page.verify_cases_sorted_on_meeting_date()
    log.info("\n Test Ended")












