#The tests here are added to test the UI functionality of tableau views, in order to make life simpler for the Symphony team
# The idea is to run these tests ONLY against SQA env for now

import pytest
from qa_automation_drt_haw.settings import Config
import os

if os.getenv('ENV') == 'sqa':
    test_data = pytest.data.retrive_data_from_csv(data_file='sqa_tableau_bti.csv')
else:
    test_data = []

pytestmark = pytest.mark.skipif(os.getenv('ENV') == 'dev', reason='AP-40724-cohort builder link is not working in dev environment')

@pytest.mark.parametrize(argnames=("sr,username,password,org,patient_count"),argvalues=test_data,ids=["test-"+str(i[0]) for i in test_data])
@pytest.mark.p2
@pytest.mark.p4
def test_validate_bti(app_test,sr,username,password,org,patient_count, test_info):
    user = getattr(Config, username)
    pwd = getattr(Config, password)
    app_test.portal.login(user, pwd)
    app_test.portal.navigate_to_BTI()
    app_test.bti_page.verify_bti_title()
    app_test.verification.verify_no_error_in_page(app_test.cohort_builder_page.resource_not_found_error)
    app_test.verification.go_next_tab_verify_url(org)
    # app_test.verification.text_present_on_page(patient_count)