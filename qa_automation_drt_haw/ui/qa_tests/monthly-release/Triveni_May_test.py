import pytest
import time
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password
patient_name = pytest.data.get_mtb_create_case_data('patient_name')
acceptable_special_chars = pytest.data.get_mtb_create_case_data('acceptable_special_chars')

# todo: text will be changed
@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    log.info("Opening application")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()


@pytest.mark.p4
@pytest.mark.p0
def test_verify_attachment_download_functionality(app_test, test_launch_mtb,test_info):
    pytest.log_test = "Verify the downloaded file name is same as the file name attached in the attachment component"
    pytest.log_link = ["https://syapse.atlassian.net/browse/BUMP-738"]

    log.info("\n Test Started - to Verify the downloaded file name is same as the file name attached in the attachment component")
    case_url = Config.case_url_with_attachments
    app_test.mtb_case_management_page.navigate_to_case(case_url)
    app_test.mtb_case_management_page.verify_availability_of_attachments()
    app_test.mtb_case_management_page.verify_downloaded_attachments_name()
    log.info("\n Test Ended")

@pytest.mark.p3
@pytest.mark.p4
@pytest.mark.parametrize(argnames="Special_Chars", argvalues=list(acceptable_special_chars))
def test_verify__no_error_message_when_acceptable_special_characters_entered_in_search_box(app_test, test_launch_mtb, Special_Chars,
                                                                            test_info):
    pytest.log_test = " Verify no error message appears when special characters like ('-) are entered in search box of patient finder page"
    pytest.log_link = ['https://syapse.atlassian.net/browse/BUMP-633']
    log.info("Test Started- to Verify no error message appears when special characters like ('-) are entered in search box of patient finder page")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.mtb_create_case_page.verify_no_error_message_is_displayed_for_acceptable_special_chars(name=patient_name + Special_Chars)
    log.info("Test Ended")
