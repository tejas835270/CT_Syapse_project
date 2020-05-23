import os
import pytest
from qa_automation_drt_haw.settings import Config

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password
invalid_username = pytest.data.get_user('invalid_user_data')['invalid_username']
invalid_pwd = pytest.data.get_user('invalid_user_data')['invalid_pwd']


# --------------------------------------------------
# ----------- LOGIN --------------------------------
# --------------------------------------------------

@pytest.mark.p4
@pytest.mark.p0
def test_login_with_valid_credentials(app_test, test_info):
    pytest.log_test = 'Verify login is successful with valid credentials'
    log.info("\n Test Started - to verify login is successful with valid credentials ")
    app_test.portal.login(username, psw)
    app_test.portal.verify_url_contains_portal()
    app_test.portal.logout()
    log.info("\n Test Ended")
    # todo header verification

@pytest.mark.p4
@pytest.mark.p2
def test_login_with_invalid_username(app_test, test_info):
    pytest.log_test = 'Verify user can not login with invalid username'
    log.info("\n Test Started - to Verify user can not login with invalid username")
    app_test.portal.login(invalid_username, psw)
    app_test.portal.verify_invalid_credentials_error()
    app_test.portal.verify_url_contains_auth0()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test_login_with_invalid_psw(app_test, test_info):
    pytest.log_test = 'Verify user can not login with invalid password'
    log.info("\n Test Started - to Verify user can not login with invalid password ")
    app_test.navigation.refresh_page()
    app_test.portal.login(username, invalid_pwd)
    app_test.portal.verify_invalid_credentials_error()
    app_test.portal.verify_url_contains_auth0()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test_login_with_empty_psw(app_test, test_info):
    pytest.log_test = 'Verify user can not login with empty password'
    log.info("\n Test Started - to Verify user can not login with empty password")
    app_test.navigation.refresh_page()
    app_test.portal.login(username, '')
    app_test.portal.verify_pwd_blank_error()
    app_test.portal.verify_url_contains_auth0()
    log.info("\n Test Ended")


@pytest.mark.p4
@pytest.mark.p0
def test_logout(app_test, test_info):
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-37909'
    pytest.log_test = 'Verify that user is successfully logout from the application'
    log.info("\n Test Started - to Verify that user is successfully logout from the application")
    app_test.portal.login(username, psw)
    app_test.portal.logout()
    app_test.portal.verify_url_contains_auth0()
    log.info("\n Test Ended")

@pytest.mark.p2
def test_user_info(app_test, test_info):
    pytest.log_test = 'Verify user information(fname and lname) is correct'
    log.info("\n Test Started - to Verify user information(fname and lname) is correct")
    app_test.portal.login(username, psw)
    user_full_name=app_test.finder.find_user_full_name(username, psw)
    app_test.portal.verify_user_info_present(user_full_name)
    app_test.portal.logout()
    log.info("\n Test Ended")


# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------
@pytest.mark.p1
def test_user_two_roles(app_test, test_info):
    pytest.log_test = 'Verify user roles'
    log.info("\n Test Started - to Verify user roles")
    app_test.portal.login(username, psw)
    expected_user_roles = pytest.data.get_user('portal_2_roles')['roles']
    expected_user_services = [x['service_name'] for x in expected_user_roles]
    app_test.portal.verify_service_is_enabled_for_user(services=expected_user_services, enabled=True)
    app_test.portal.logout()
    log.info("\n Test Ended")


@pytest.mark.p4
#'https://syapse.atlassian.net/browse/AP-37917'
@pytest.mark.p0
def test_navigation(app_test, test_info):
    pytest.log_test = 'Verify the service navigation'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-37913'
    log.info("\n Test Started - to Verify the navigation to services")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_Patient_Data_Entry()
    app_test.chronicle.verify_url_contains_oncology()
    # todo more verification that user on the chronicle page
    app_test.portal.click_syapse_logo()
    app_test.portal.navigate_to_mtb_service()
    app_test.mtb.verify_url_contains_mtb()
    # todo more verification that user on the mtb page
    app_test.navigation.browser_back() # change when logo will work
    app_test.portal.verify_url_contains_portal()
    app_test.portal.logout()
    log.info("\n Test Ended")

@pytest.mark.p1
def test_user_one_roles(app_test, test_info):
    pytest.log_test = 'Verify user has only one role i.e portal_chronicle'
    log.info("\n Test Started - to Verify user has only one role i.e portal_chronicle")
    username = Config.portal_chronicle_username
    psw = Config.portal_chronicle_password
    app_test.portal.login(username, psw)
    expected_user_roles = pytest.data.get_user('portal_chronicle')['roles']
    expected_user_services = [x['service_name'] for x in expected_user_roles]
    app_test.portal.verify_service_is_enabled_for_user(services=expected_user_services, enabled=True)
    app_test.portal.logout()
    log.info("\n Test Ended")

@pytest.mark.p0
def test_user_no_roles(app_test, test_info):
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-37916'
    pytest.log_test = 'Verify user has no roles'
    log.info("\n Test Started - to Verify user has no roles")
    username = Config.portal_no_roles_username
    psw = Config.portal_no_roles_password
    app_test.portal.login(username, psw)
    app_test.portal.verify_service_is_enabled_for_user(services=[], enabled=True)
    app_test.portal.logout()
    log.info("\n Test Ended")

# TODO help link - not implemented
@pytest.mark.p4
@pytest.mark.p0
def test_verify_Precision_Medicine_Impact_tile_IsPresent(app_test, test_info):
    pytest.log_test = 'Verify Precision Medicine Impact tile is present on the Portal Page'
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-579'
    log.info("Test Started")
    username = Config.mtb_testing_only_username
    psw = Config.mtb_testing_only_password
    app_test.portal.login(username, psw)
    app_test.portal.verify_Application_tile_IsPresent(app_test.portal.tile_text)
    log.info("Test Ended")

@pytest.mark.p4
@pytest.mark.p0
def test_verify_Precision_Medicine_Impact_tile_Description(app_test, test_info):
    pytest.log_test = 'Verify description of Precision Medicine Impact tile' \
                      'It should be "Understand follow through for tumor board interventions and germline counseling" '
    pytest.log_link = 'https://syapse.atlassian.net/browse/BUMP-580'
    log.info("Test Started")
    username = Config.mtb_testing_only_username
    psw = Config.mtb_testing_only_password
    app_test.portal.login(username, psw)
    app_test.portal.verify_Application_description(app_test.portal.tile_text, app_test.portal.tile_description)
    log.info("Test Ended")
