#The tests here are added to test the UI functionality of tableau views, in order to make life simpler for the Symphony team
# The idea is to run these tests ONLY against SQA env for now

import pytest
from qa_automation_drt_haw.settings import Config
import os

#select the cohort_builder test-data file as per the environment
if os.getenv('ENV') == 'dev':
    test_data = pytest.data.retrive_data_from_csv(data_file='dev_tableau_cohort_builder.csv')
elif os.getenv('ENV') == 'sqa':
    test_data = pytest.data.retrive_data_from_csv(data_file='sqa_tableau_cohort_builder.csv')

pytestmark = pytest.mark.skipif(os.getenv('ENV') == 'dev', reason='AP-40724-cohort builder link is not working in dev environment')

@pytest.mark.parametrize(argnames=("sr,username,password,org,patient_count"),argvalues=test_data,ids=["test-"+str(i[0]) for i in test_data])
@pytest.mark.p2
@pytest.mark.p4
def test_validate_tableau_url_cohort_builder(app_test,sr,username,password,org,patient_count, test_info):
    user = getattr(Config, username)
    pwd = getattr(Config, password)
    app_test.portal.login(user, pwd)
    app_test.portal.navigate_to_Cohort_Builder()
    app_test.cohort_builder_page.verify_cohort_builder_title()
    app_test.verification.go_next_tab_verify_url(org)
    app_test.verification.verify_no_error_in_page(app_test.cohort_builder_page.resource_not_found_error)
    app_test.navigation.click_dropdown_tableau(app_test.cohort_builder_page.none)
    app_test.verification.select_all_checkbox_in_dashboard()
    app_test.verification.sleep_time(2)
    app_test.navigation.click_button(button_name=app_test.cohort_builder_page.apply_btn,expected_text=patient_count)
    app_test.verification.text_present_on_page(patient_count)
    #todo - compare above count in Jeeves/newrelic


#testcase -1 : Aurora - Validate Cohort Builder url correct  for each org/sub_org
#TODO: Run the below test for every org/sub-org (JUST CHANGE THE `go_next_tab_verify_url` VALUE)
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_aurora_cohort_builder(app_test, test_info):
    app_test.portal.login(username_aurora, psw_aurora)
    app_test.navigation.navigate_to("Cohort Builder")
    app_test.verification.sleep_time(2)
    app_test.verification.go_next_tab_verify_title('Workbook: Cohort Builder')
    app_test.verification.sleep_time(1)
    app_test.verification.go_next_tab_verify_url('aurora-sqa/views/CohortBuilder/CohortBuilder?:embed=y#1')
    app_test.verification.sleep_time(2)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.navigation.click_dropdown_tableau("(None)")
    app_test.verification.select_all_checkbox_in_dashboard()
    app_test.verification.click_on_button("Apply")
    app_test.verification.sleep_time(15)
    app_test.verification.text_present_on_page('2,506 patients found')
    #todo - compare above count in Jeeves/newrelic

#testcase -2 : Aurora - Validate user can successfully navigate to 'NewMolecularResults' tab
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_aurora_new_molecular_results(app_test, test_info):
    app_test.portal.login(username_aurora, psw_aurora)
    app_test.navigation.navigate_to("Cohort Builder")
    app_test.verification.go_next_tab_verify_title('Workbook: Cohort Builder')
    #todo - compare above count in Jeeves/newrelic
    # app_test.navigation.click_tab("tableauTabbedNavigation_tab_1")
    app_test.navigation.click_tab("New Molecular Results")
    app_test.verification.sleep_time(5)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.go_next_tab_verify_url('aurora-sqa/views/CohortBuilder/NewMolecularResults?%3Aembed=y#1')
    app_test.verification.text_present_on_page('New Molecular Results')

#testcase -3 : Aurora - Validate Program Insights url correct  for each org/sub_org
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_aurora_program_insights(app_test, test_info):
    app_test.portal.login(username_aurora, psw_aurora)
    app_test.navigation.navigate_to("Program Insights")
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.go_next_tab_verify_url('aurora-sqa/views/ProgramInsights/Adoption?')
    app_test.navigation.click_dropdown_tableau("Last 12 months")
    app_test.verification.sleep_time(5)
    app_test.navigation.click_text('Years')
    app_test.verification.sleep_time(5)
    app_test.navigation.refresh_page()
    app_test.verification.sleep_time(3)
    # app_test.verification.text_present_on_page('Years')
    app_test.verification.go_next_tab_verify_title('Workbook: Program Insights')
    app_test.verification.verify_counts('1,351')

#testcase -4 : Aurora - Validate user can successfully navigate to 'TestFailure' tab
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_aurora_program_insights_test_failure(app_test, test_info):
    app_test.portal.login(username_aurora, psw_aurora)
    app_test.navigation.navigate_to("Program Insights")
    app_test.verification.sleep_time(4)
    app_test.verification.go_next_tab_verify_title('Workbook: Program Insights')
    app_test.verification.sleep_time(10)
    # app_test.navigation.click_tab("New Molecular Results")
    app_test.navigation.click_tab("Test Failure")
    app_test.verification.sleep_time(5)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.text_present_on_page('Test Failure')
    app_test.verification.go_next_tab_verify_url('aurora-sqa/views/ProgramInsights/TestFailure?%3Aembed=')

#testcase -5 : PMA - Validate Cohort Builder url correct  for each org/sub_org
#TODO: Run the below test for every org/sub-org (JUST CHANGE THE `go_next_tab_verify_url` VALUE)
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_pma_cohort_builder(app_test, test_info):
    app_test.portal.login(username_pma, psw_pma)
    app_test.navigation.navigate_to("Cohort Builder")
    app_test.verification.sleep_time(3)
    app_test.verification.go_next_tab_verify_title('Workbook: Cohort Builder')
    app_test.verification.sleep_time(6)
    app_test.verification.go_next_tab_verify_url('pma-sqa/views/CohortBuilder/CohortBuilder?:embed=y#1')
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.navigation.click_dropdown_tableau("(None)")
    app_test.verification.sleep_time(6)
    app_test.verification.select_all_checkbox_in_dashboard()
    app_test.verification.click_on_button("Apply")
    app_test.verification.sleep_time(120)
    app_test.verification.text_present_on_page('4,858 patients found')
    #todo - compare above count in Jeeves/newrelic

#testcase -6 : PMA - Validate user can successfully navigate to 'NewMolecularResults' tab
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_pma_new_molecular_results(app_test, test_info):
    app_test.portal.login(username_pma, psw_pma)
    app_test.navigation.navigate_to("Cohort Builder")
    app_test.verification.go_next_tab_verify_title('Workbook: Cohort Builder')
    #todo - compare above count in Jeeves/newrelic
    # app_test.navigation.click_tab("tableauTabbedNavigation_tab_1")
    app_test.navigation.click_tab("New Molecular Results")
    app_test.verification.sleep_time(5)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.go_next_tab_verify_url('pma-sqa/views/CohortBuilder/NewMolecularResults?%3Aembed=y#1')
    app_test.verification.text_present_on_page('New Molecular Results')


#testcase -7 : PMA - Validate user can successfully navigate to 'TestFailure' tab
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_pma_program_insights_test_failure(app_test, test_info):
    app_test.portal.login(username_pma, psw_pma)
    app_test.navigation.navigate_to("Program Insights")
    app_test.verification.go_next_tab_verify_title('Workbook: Program Insights')
    app_test.verification.sleep_time(10)
    # app_test.navigation.click_tab("New Molecular Results")
    app_test.navigation.click_tab("Test Failure")
    app_test.verification.sleep_time(5)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.text_present_on_page('Test Failure')
    app_test.verification.go_next_tab_verify_url('pma-sqa/views/ProgramInsights/TestFailure?%3Aembed=')

#testcase -8 : HFHS - Validate Cohort Builder url correct  for each org/sub_org
#TODO: Run the below test for every org/sub-org (JUST CHANGE THE `go_next_tab_verify_url` VALUE)
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_hfhs_cohort_builder(app_test, test_info):
    app_test.portal.login(username_hfhs_cohort, psw_hfhs_cohort)
    app_test.navigation.navigate_to("Cohort Builder")
    app_test.verification.go_next_tab_verify_title('Workbook: Cohort Builder')
    app_test.verification.go_next_tab_verify_url('hfhs-sqa/views/CohortBuilder/CohortBuilder?:embed=y#1')
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.navigation.click_dropdown_tableau("(None)")
    app_test.verification.sleep_time(6)
    app_test.verification.select_all_checkbox_in_dashboard()
    app_test.verification.click_on_button("Apply")
    app_test.verification.sleep_time(30)
    app_test.verification.text_present_on_page('672 patients found')
    #todo - compare above count in Jeeves/newrelic

#testcase -9 : HFHS - Validate user can successfully navigate to 'NewMolecularResults' tab
@pytest.mark.p2
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
def test_validate_tableau_url_hfhs_new_molecular_results(app_test, test_info):
    app_test.portal.login(username_hfhs_cohort, psw_hfhs_cohort)
    app_test.navigation.navigate_to("Cohort Builder")
    app_test.verification.go_next_tab_verify_title('Workbook: Cohort Builder')
    app_test.navigation.click_tab("New Molecular Results")
    app_test.verification.sleep_time(5)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.go_next_tab_verify_url('hfhs-sqa/views/CohortBuilder/NewMolecularResults?%3Aembed=y#1')
    app_test.verification.text_present_on_page('New Molecular Results')


#testcase -10 : hfhs - Validate user can successfully navigate to 'TestFailure' tab
@pytest.mark.p2
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
def test_validate_tableau_url_hfhs_program_insights_test_failure(app_test, test_info):
    app_test.portal.login(username_hfhs_cohort, psw_hfhs_cohort)
    app_test.navigation.navigate_to("Program Insights")
    app_test.verification.go_next_tab_verify_title('Workbook: Program Insights')
    app_test.verification.sleep_time(10)
    # app_test.navigation.click_tab("New Molecular Results")
    app_test.navigation.click_tab("Test Failure")
    app_test.verification.sleep_time(5)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.text_present_on_page('Test Failure')
    app_test.verification.go_next_tab_verify_url('hfhs-sqa/views/ProgramInsights/TestFailure?%3Aembed=')

#testcase -11 : PMA (CHI Mercy Health) - Validate Cohort Builder url correct  for each org/sub_org
#TODO: Run the below test for every org/sub-org (JUST CHANGE THE `go_next_tab_verify_url` VALUE)
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_chi_mercy_health_cohort_builder(app_test, test_info):
    app_test.portal.login(username_chi_mercy_health_cohort, psw_chi_mercy_health_cohort)
    app_test.navigation.navigate_to("Cohort Builder")
    app_test.verification.go_next_tab_verify_title('Workbook: Cohort Builder - CHI Mercy Health')
    app_test.verification.sleep_time(3)
    app_test.verification.go_next_tab_verify_url('pma-sqa/views/CohortBuilder-CHIMercyHealth/CohortBuilder?')
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.navigation.click_dropdown_tableau("(None)")
    app_test.verification.sleep_time(6)
    app_test.verification.select_all_checkbox_in_dashboard()
    app_test.verification.click_on_button("Apply")
    app_test.verification.sleep_time(30)
    app_test.verification.text_present_on_page('3 patients found')
    #todo - compare above count in Jeeves/newrelic

#testcase -12 : PMA (CHI Mercy Health) - Validate user can successfully navigate to 'NewMolecularResults' tab
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_chi_mercy_health_new_molecular_results(app_test, test_info):
    app_test.portal.login(username_chi_mercy_health_cohort, psw_chi_mercy_health_cohort)
    app_test.navigation.navigate_to("Cohort Builder")
    app_test.verification.go_next_tab_verify_title('Workbook: Cohort Builder - CHI Mercy Health')
    app_test.verification.sleep_time(3)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.text_present_on_page('Cohort Builder')
    app_test.navigation.click_tab("New Molecular Results")
    app_test.verification.sleep_time(5)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.go_next_tab_verify_url('pma-sqa/views/CohortBuilder-CHIMercyHealth/NewMolecularResults?%3Aembed=y#1')
    app_test.verification.text_present_on_page('New Molecular Results')


#testcase -13 : PMA (CHI Mercy Health) - Validate user can successfully navigate to 'TestFailure' tab
@pytest.mark.skip(reason="test maintenance is blocked deu to open ticket AP-40643")
@pytest.mark.p2
def test_validate_tableau_url_chi_mercy_health_program_insights_test_failure(app_test, test_info):
    app_test.portal.login(username_chi_mercy_health_cohort, psw_chi_mercy_health_cohort)
    app_test.navigation.navigate_to("Program Insights")
    app_test.verification.go_next_tab_verify_title('Workbook: Program Insights - CHI Mercy Health')
    app_test.verification.sleep_time(10)
    # app_test.navigation.click_tab("New Molecular Results")
    app_test.navigation.click_tab("Test Failure")
    app_test.verification.sleep_time(5)
    app_test.verification.verify_no_error_in_page('Resource Not Found')
    app_test.verification.text_present_on_page('Test Failure')
    app_test.verification.go_next_tab_verify_url('pma-sqa/views/ProgramInsights-CHIMercyHealth/TestFailure?%3Aembed=')




