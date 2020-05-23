import pytest
from qa_automation_drt_haw.settings import Config
import os

#select the cohort_builder test-data file as per the environment
if os.getenv('ENV') == 'sqa':
    test_data = pytest.data.retrive_data_from_csv(data_file='sqa_tableau_program_insights.csv')
else:
    test_data = []
pytestmark = pytest.mark.skipif(os.getenv('ENV') == 'dev', reason='AP-40724-cohort builder link is not working in dev environment')


@pytest.mark.parametrize(argnames=("sr,username,password,org,patient_count"),argvalues=test_data,ids=["test-"+str(i[0]) for i in test_data])
@pytest.mark.p2
@pytest.mark.p4
def test_validate_program_insights(app_test,sr,username,password,org,patient_count, test_info):
    user = getattr(Config, username)
    pwd = getattr(Config, password)
    app_test.portal.login(user, pwd)
    app_test.portal.navigate_to_Program_Insights()
    app_test.verification.verify_no_error_in_page(app_test.cohort_builder_page.resource_not_found_error)
    app_test.verification.go_next_tab_verify_url(org)
    app_test.navigation.click_dropdown_tableau(app_test.program_insights_page.Date)
    app_test.verification.sleep_time(5)
    app_test.navigation.click_text(app_test.program_insights_page.text)
    app_test.navigation.refresh_page()
    app_test.verification.sleep_time(3)
    app_test.program_insights_page.verify_program_insights_title()
    app_test.verification.verify_counts(patient_count)
