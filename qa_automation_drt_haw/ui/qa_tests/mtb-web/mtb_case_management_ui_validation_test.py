import pytest
from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.ui.ui_utils.Logs import log

#pick up credentials from setting.py file
username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password

#pick up environment independent data from fixure_data.json file
meeting_date= pytest.data.get_mtb_create_case_data('Meeting_Date')
Primary_Oncologist_data=pytest.data.get_mtb_create_case_data('Primary_Oncologist')
Diagnosis_Date= pytest.data.get_mtb_create_case_data('Diagnosis_Date')
histology_data = pytest.data.get_mtb_create_case_data('Histology')
Recommendations_Summary_with_special_characters= pytest.data.get_mtb_create_case_data('Recommendations_Summary_with_special_characters')

#pick up dropdown value fron vocab csv
primary_site_csv=pytest.data.retrive_data_from_csv(data_file='Data_vocab/Primary_Site.csv')
stage_group_csv=pytest.data.retrive_data_from_csv(data_file='Data_vocab/StageGroup.csv')

@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    log.info("Opening application")
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()


@pytest.mark.p0
def test_mtb_create_case_with_all_diagnosis_field(app_test, test_launch_mtb, test_info):

    pytest.log_test = 'Verify user can create case by providing values for all diagnosis fields (histology, ' \
                      'site and stage)'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-38773'
    log.info("\n Test Started - to Verify user can create case by providing values for all diagnosis fields (histology,site and stage)")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.enter_diagnosis_date(date=Diagnosis_Date)
    app_test.mtb_create_case_page.select_option_from_Primary_Site(option_name=primary_site_csv[3][0])
    app_test.mtb_create_case_page.select_option_from_Stage_Group_dd(option_name=stage_group_csv[15][0])
    app_test.mtb_create_case_page.select_option_from_Histology(option_name=histology_data)
    app_test.mtb_create_case_page.click_on_save_and_close()

    # verify that case is created succcessfully
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test_mtb_verify_cancel(app_test, test_launch_mtb, test_info):

    pytest.log_test = 'Verify cancel confirmation pop up for new case'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39148'
    log.info("\n Test Started - to Verify cancel confirmation pop up for new case")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.click_on_Cancel_button()
    app_test.verification.scroll_to_top_of_page()
    app_test.mtb_case_management_page.verify_current_url_contains_mtb()
    app_test.mtb_case_management_page.verify_mtb_case_management_text_present_on_page()

    if app_test.verification.verify_cancel_button_popup_is_displayed():
        log.info('Popup is Displayed when clicked on Cancel button')
        app_test.mtb_create_case_page.verify_user_clicks_on_cancel()
        app_test.mtb_create_case_page.click_on_Cancel_button()
        app_test.mtb_create_case_page.verify_user_clicks_on_continue()
    else:
        log.error('Cancel Popup is not present')
        assert False, 'Cancel Popup is not present'
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test_mtb_verify_CaseID_shown_before_case_saved(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify that case ID is shown even before case is saved'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39268'
    log.info("\n Test Started - to Verify that case ID is shown even before case is saved")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    mrn_case_id = app_test.verification.verify_case_id_is_displayed_with_middle_digits_mrn()
    if mrn_case_id:
        log.info('Case ID is present in Case Management Screen with expected MRN Number')
    else:
        log.error('Case ID is present in Case Management Screen with incorrect MRN Number')
        assert False, 'Case ID is present in Case Management Screen with incorrect MRN Number'
    log.info("\n Test Ended")

@pytest.mark.p0
def test_mtb_verify_saving_case_saves_case_id_and_associates_mtb_case(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify that saving create case, saves the case ID and associates it to the MTB case'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39270'
    log.info("\n Test Started - to Verify that saving create case, saves the case ID and associates it to the MTB case")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.click_on_save_and_close()
    app_test.mtb_case_management_page.verify_Molecular_Tumor_Board_text_present_on_page()

    # verify that case is created succcessfully with correct case id
    app_test.mtb_case_management_page.navigate_to_case(case_url,case_id)
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test_mtb_verify_case_id_format(app_test, test_launch_mtb, test_info):
    pytest.log_test = 'Verify case ID format'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39271'
    log.info("\n Test Started - to Verify case ID format")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    mrn = app_test.finder.pick_patient_mrn()
    mrn_last_4_digits = str(mrn[-4:])

    #if env is dev then search and pick up patient by mrn which is received through api
    if app_test.env=='dev':
        app_test.finder.find_and_pick_patient(mrn)
    # if env is sqa then click on first patient from the available list
    elif app_test.env == "sqa":
        app_test.finder.finder_pick_value(mrn)

    app_test.mtb_case_management_page.verify_mtb_case_management_text_present_on_page()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    mrn_in_case_id=str(case_id[-4:])
    print(mrn_in_case_id,mrn_last_4_digits)

    #verify the last 4 digit of case id is equal to last 4 digit of mrn
    if mrn_last_4_digits == mrn_in_case_id:
        log.info('last 4 digit of mrn is present in the Case ID')
        assert True, "Case ID is in Wrong Format"
    else:
        log.error('last 4 digit of mrn is not present in the Case ID')
        assert False, "Case ID is in correct Format"
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test_mtb_verify_vertical_scroll_for_large_recommendation_summary(app_test, test_launch_mtb,test_info):

    pytest.log_test = 'Verify vertical scroll is available for large recommendation summary'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39279'
    log.info("\n Test Started - to Verify vertical scroll is available for large recommendation summary")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.verification.scroll_to_bottom_of_page()
    app_test.mtb_create_case_page.click_on_to_enable_text(ele_xpath=app_test.mtb_create_case_page.meeting_none)
    app_test.verification.verify_scroll_for_recommdations_summary()
    log.info("\n Test Ended")

@pytest.mark.p2
def test_mtb_verify_recommendation_summary_text_box_allows_special_characters(app_test, test_launch_mtb,test_info):

    pytest.log_test = 'Verify recommendation summary text box allows special characters'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39280'
    log.info("\n Test Started - to Verify recommendation summary text box allows special characters")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.verification.scroll_to_bottom_of_page()

    #enter special characters in summary field
    app_test.mtb_create_case_page.enter_text_in_recommendationsSummary(what=Recommendations_Summary_with_special_characters)

    if not app_test.mtb.verify_error_msg():
        log.info('recommendation summary Text field allows special characters " - ( ) (") , . " ')
    else:
        print("Special Characters are not allowed")
        log.error('recommendation summary Text field does not allows special characters like  @ # ^ ~ `')
    app_test.navigation.save_case()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test_verify_that_user_navigates_to_consolidated_create_case_page(app_test, test_launch_mtb,test_info):
    pytest.log_test = 'Verify that user navigates to a consolidated create case page'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39311'
    log.info("\n Test Started - to Verify that user navigates to a consolidated create case page")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.verification.verify_case_id_DOB_are_present_on_MTB_page()
    app_test.verification.all_field_text_present_on_case_creation_page()
    log.info("\n Test Ended")

@pytest.mark.p4
@pytest.mark.p2
def test__verify_that_user_with_MTB_editor_role_can_access_MTB_from_portal(app_test,test_info):
    pytest.log_test = 'Verify that user with MTB editor role can access MTB from portal'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39394'
    log.info("\n Test Started - to Verify that user with MTB editor role can access MTB from porta")
    app_test.portal.login(username, psw)
    app_test.verification.verify_contents_of_MTB_module('Prepare and present cases for molecular tumor board review.')
    app_test.portal.navigate_to_mtb_service()
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    log.info("\n Test Ended")

@pytest.mark.p2
def test_mtb_verify_links_to_create_or_edit_case_forms(app_test, test_launch_mtb,test_info):
    pytest.log_test = 'Verify links to create/edit case forms'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39619'
    log.info("\n Test Started - to Verify links to create/edit case forms")
    # For Create New Case Option
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    app_test.mtb_case_management_page.verify_mtb_case_management_text_present_on_page()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.click_on_save_and_close()

    # For Edit Case Option
    log.info("Verify the case is created by reopening it")
    app_test.mtb_case_management_page.navigate_to_case(case_url,case_id)
    app_test.verification.verify_prepopulated_fileds_in_cases()
    log.info("\n Test Ended")


@pytest.mark.p2
def test_mtb_verify_case_narrative_field_is_optional(app_test, test_launch_mtb,test_info):
    pytest.log_test = 'Verify case narrative field is optional to create a case'
    pytest.log_link = 'https://syapse.atlassian.net/browse/AP-39718'
    log.info("\n Test Started - to Verify case narrative field is optional to create a case")
    app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
    app_test.mtb_case_management_page.click_on_create_new_case_button()
    app_test.verification.search_box()
    app_test.finder.search_specific_patient()
    case_id = app_test.mtb_create_case_page.pick_up_case_ID()
    case_url = app_test.mtb_create_case_page.get_case_url()
    app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
    app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
    app_test.mtb_create_case_page.click_on_save_and_close()

    #verify case is created successfully
    app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
    log.info("\n Test Ended")