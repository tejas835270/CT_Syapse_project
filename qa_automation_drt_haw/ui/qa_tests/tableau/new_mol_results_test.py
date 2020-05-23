import pytest
from qa_automation_drt_haw.settings import Config
import os

#select the cohort_builder test-data file as per the environment
if os.getenv('ENV') == 'sqa':
    test_data = pytest.data.retrive_data_from_csv(data_file='sqa_tableau_nmr.csv')
else:
    test_data = []

pytestmark = pytest.mark.skipif(os.getenv('ENV') == 'dev', reason='AP-40724-cohort builder link is not working in dev environment')


@pytest.mark.parametrize(argnames=("sr,username,password,org,date"),argvalues=test_data,ids=["test-"+str(i[0]) for i in test_data])
@pytest.mark.p2
@pytest.mark.p4
def test_validate_tableau_url_new_molecular_results(app_test,sr,username,password,org,date, test_info):
    user = getattr(Config, username)
    pwd = getattr(Config, password)
    app_test.portal.login(user, pwd)
    app_test.portal.navigate_to_New_Molecular_Result()
    app_test.nmr_page.verify_nmr_title()
    app_test.verification.go_next_tab_verify_url(org)
    app_test.verification.verify_no_error_in_page(app_test.cohort_builder_page.resource_not_found_error)
    app_test.navigation.click_dropdown_tableau(app_test.cohort_builder_page.none)
    app_test.verification.select_all_checkbox_in_dashboard()
    app_test.navigation.click_button(button_name=app_test.cohort_builder_page.apply_btn,expected_text=date)
    app_test.verification.text_present_on_page(app_test.nmr_page.new_molecular_results_tab)