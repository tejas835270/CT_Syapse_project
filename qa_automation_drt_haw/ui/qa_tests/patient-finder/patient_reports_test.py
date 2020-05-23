import pytest
import time
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password

# todo: text will be changed
@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    log.info("Opening application")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()

@pytest.mark.p4
@pytest.mark.p3
def test_verify_mdx_global_none_text_is_not_Present_on_Page(app_test, test_info):
    pytest.log_test = 'Verify the global.noneGiven text is not present on the mdx patient report page'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-236'
    log.info("\n Test Started - to verify global.nonGiven text is not present on the mdx report page")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(app_test.portal.mdx_service_name)
    app_test.verification.search_box()
    app_test.finder.search_mdx_patien()
    app_test.mdx.verify_global_none_text_is_not_present(app_test.mdx.global_none_given)
    log.info("\n Test Ended")