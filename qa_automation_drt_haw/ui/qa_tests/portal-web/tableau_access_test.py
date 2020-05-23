import pytest
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.ui.ui_utils.Logs import log

username = Config.tableau_executive_only_username
psw =Config.tableau_executive_only_password
username1 = Config.mtb_testing_only_username
suborg_cohortbuilder_username = Config.tableau_executive_only_username

# --------------------------------------------------
# ----------- LOGIN --------------------------------
# --------------------------------------------------

pytestmark=pytest.mark.skip(reason="testcase failing due to known bug :- AP-40627-tableau portal links are not working in dev environment")


# 'https://syapse.atlassian.net/browse/AP-37913'
@pytest.mark.skip(reason="testcase failing due to known bug :- AP-40627-tableau portal links are not working in dev environment")

@pytest.mark.p1
def test_tableau_org_exec_only(app_test, test_info):
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-37917'
    log.info("Test Started to verify tableau access for org_exec_only")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_Program_Insights()
    app_test.program_insights_page.verify_program_insights_title()
    app_test.program_insights_page.verify_url_contains_ProgramInsights()
    log.info("Test Passed")

#As per Soumya's comment, "clinicalanalyst" is changed to  "cohortbuilder"
@pytest.mark.skip(reason="testcase failing due to known bug :- AP-40627-tableau portal links are not working in dev environment")
@pytest.mark.p2
def test_tableau_org_cohortbuilder_only(app_test, test_info):
    log.info("Test Started for org_clinicalanalyst_only")
    app_test.portal.login(username1, psw)
    app_test.portal.navigate_to_Cohort_Builder()
    app_test.cohort_builder_page.verify_cohort_builder_title()
    app_test.cohort_builder_page.verify_url_contains_PatientCohortBuilder()
    log.info("Test Ended")

#parent org = Integration2
#sub-org=SomethingClinic
@pytest.mark.p2
def test_tableau_suborg_cohortbuilder_only(app_test, test_info):
    log.info("Test Started for suborg_clinicalanalyst_only")
    app_test.portal.login(suborg_cohortbuilder_username, psw)
    app_test.portal.navigate_to_Cohort_Builder()
    app_test.cohort_builder_page.verify_cohort_builder_title_for_suborg()
    app_test.cohort_builder_page.verify_url_contains_PatientCohortBuilderSomethingClinic()
    log.info("Test Ended")

