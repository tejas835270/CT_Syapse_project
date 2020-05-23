import pytest
from qa_automation_drt_haw.settings import Config
import time

from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.portal_2_roles_username
psw = Config.portal_2_roles_password
PDS_service_name= pytest.data.get_service_name('PDS')
patient1 =pytest.data.get_patient('patients_for_finder_test')['Patient1']
patient2 =pytest.data.get_patient('patients_for_finder_test')['Patient2']
patient3 =pytest.data.get_patient('patients_for_finder_test')['Patient3']
patient4 =pytest.data.get_patient('patients_for_finder_test')['Patient4']
patient5 =pytest.data.get_patient('patients_for_finder_test')['Patient5']
patient6 =pytest.data.get_patient('patients_for_finder_test')['Patient6']
patient7 =pytest.data.get_patient('patients_for_finder_test')['Patient7']
patient8 =pytest.data.get_patient('patients_for_finder_test')['Patient8']
patient9 =pytest.data.get_patient('patients_for_finder_test')['Patient9']

pytestmark=pytest.mark.skip(reason="Need to make them data independent using api strategy, currently skipping as “chronicle-service” is on low priority")

#todo: text will be changed
@pytest.fixture(scope="function")
def patient_search_default_page(app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to(PDS_service_name)
    app_test.finder.verify_Please_search_text_present()
    yield
    app_test.driver.close()

@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_search_3chars(app_test, patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - 3 chars search'
        log.info("Test Started-Patient finder search - 3 chars search")
        app_test.chronicle.verify_url_contains_oncology()
        app_test.verification.search_box()
        app_test.finder.search(patient1)
        log.info("Test Passed for Patient search using 3 chars search \n")
#
# #todo: enable this test after https://syapse.atlassian.net/browse/AP-38190 is resolved
@pytest.mark.skip(reason="flaky test")
@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_korean_fnamelname(app_test, patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - korean firstname lastname'
        log.info("Test Started-Patient finder search - korean firstname lastname")
        app_test.finder.find_and_pick_patient(patient2)
        app_test.navigation.browser_back()
        log.info("Test Passed for Patient search using korean firstname lastname \n ")

@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_search_using_fname(app_test, patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - using firstname'
        log.info("Test Started-Patient finder search - using firstname")
        app_test.finder.find_and_pick_patient(patient3)
        app_test.navigation.browser_back()
        log.info("Test Passed for Patient search using firstname \n")
#
@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_search_mrn(app_test, patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - using mrn'
        log.info("Test Started-Patient finder search - using mrn")
        app_test.finder.find_and_pick_patient(patient4)
        app_test.navigation.browser_back()
        log.info("Test Passed for Patient search using mrn \n")

@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_search_lname(app_test, patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - using lastname'
        log.info("Test Started-Patient finder search - using lastname")
        app_test.finder.find_and_pick_patient(patient5)
        app_test.navigation.browser_back()
        log.info("Test Passed for Patient search using lastname \n")

@pytest.mark.skip(reason="flaky test")
@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_search_pagination( app_test, patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - check pagination'
        log.info("Test Started-Patient finder search - check pagination")
        app_test.finder.search(patient6)
        app_test.verification.scroll_to_bottom_of_page()
        app_test.verification.click_nxt_pagenum(3)
        time.sleep(2)
        log.info("Test Passed for pagination \n")

@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_search_fnamelname(app_test,patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - search using fname lname'
        log.info("Test Started-Patient finder search - using fname lname")
        app_test.finder.find_and_pick_patient(patient7)
        app_test.navigation.browser_back()
        log.info("Test Passed for Patient search using fname lname \n")

@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_search_nomatch(app_test,patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - no match'
        log.info("Test Started-Patient finder search - no match")
        app_test.finder.search(patient8)
        app_test.finder.verify_text_No_Results_found()
        app_test.finder.verify_text_search_did_not_match()
        log.info("Test Passed for Patient search-no match \n")

@pytest.mark.p4
@pytest.mark.p0
def test_patient_finder_search_case_Sensitivity(app_test, patient_search_default_page,test_info):
        pytest.log_test = 'Patient finder search - search using case sensitivity'
        log.info("Test Started-Patient finder search - search using case sensitivity")
        app_test.finder.find_and_pick_patient(patient9)
        app_test.navigation.browser_back()
        log.info("Test Passed for Patient search using case sensitivity \n")