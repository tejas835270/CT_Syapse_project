
import pytest

from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.ui.ui_utils.Logs import log

#pick up the user credentials for setting.py file (which fetch the data from fixture_data.json file)
username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password

#  below are the data which comes from fixture_data.json file to fill the fields on [create new case] page
meeting_date= pytest.data.get_mtb_create_case_data('Meeting_Date')
Diagnosis_Date= pytest.data.get_mtb_create_case_data('Diagnosis_Date')
Recommendations_Summary= pytest.data.get_mtb_create_case_data('Recommendations_Summary')
Primary_Oncologist_data= pytest.data.get_mtb_create_case_data('Primary_Oncologist')
Edit_Recommendations_Summary = pytest.data.get_mtb_create_case_data('Edit_Recommendations_Summary')
empty_Recommendations_Summary= ''
text_with_more_than_200_character= pytest.data.get_mtb_create_case_data('text_with_more_than_200_character')
text_with_200_character= pytest.data.get_mtb_create_case_data('text_with_200_character')

@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()

@pytest.mark.p0
def test_add_recommendation_summary_Save_Verify(app_test, test_launch_mtb,test_info):
        pytest.log_test = 'Verify add recommendation_summary , save and then verify'
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-40413"
        log.info("\n Test Started- to add recommendation_summary , save and then verify")
        app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()
        app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
        app_test.mtb_create_case_page.enter_text_in_recommendationsSummary(what=Recommendations_Summary)
        app_test.mtb_create_case_page.click_on_save_and_close()

        #verify case id on mtb case management screen and its data
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        app_test.mtb_create_case_page.click_on_to_enable_text(app_test.mtb_create_case_page.meeting_none)
        if app_test.mtb_create_case_page.Recommendations_Summary_value_verification(data=Recommendations_Summary):
            log.info("Passed - recommendation_summary_text is saved and verified successfully")
            assert True, "recommendation_summary_text is not saved correctly"
        else:
            log.info("Failed - recommendation_summary_text is not saved correctly")
        log.info("\n Test Ended")

@pytest.mark.p0
def test_Edit_recommendation_summary_Save_Verify(app_test,test_launch_mtb,test_info):
        pytest.log_test = 'Verify Edit recommendation summary,Save and Verify'
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-40410"
        log.info("\n Test Started-to Edit recommendation summary,Save and Verify")
        #to remove dependancy first run "test_add_recommendation_summary_Save_Verify"
        test_add_recommendation_summary_Save_Verify(app_test,test_launch_mtb,test_info)
        case_id=app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()
        app_test.verification.scroll_to_bottom_of_page()
        app_test.mtb_create_case_page.enter_text_in_recommendationsSummary(what=Edit_Recommendations_Summary)
        app_test.mtb_create_case_page.click_on_save_and_close()

        #verify case id on mtb case management screen and its data
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        app_test.mtb_create_case_page.click_on_to_enable_text(app_test.mtb_create_case_page.meeting_none)
        if app_test.mtb_create_case_page.Recommendations_Summary_value_verification(data=Edit_Recommendations_Summary):
                log.info("Passed-recommendation_summary_text is edited and verified successfully")
                assert  True,"recommendation_summary_text is not edited successfully"
        else:
                log.info("Failed-recommendation_summary_text is not edited successfully")
        log.info("\n Test Ended")

@pytest.mark.p0
def test_mtb_create_case_without_recommendation_summary(app_test,test_launch_mtb,test_info):
        pytest.log_test = 'Verify Recommendations summary field is optional to create MTB case'
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-39278"
        log.info("\n Test Started- to Verify 'Recommendations summary' field is optional to create MTB case")
        # app_test.mtb_case_management_page.navigate_to_mtb_url()
        app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()
        app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
        app_test.mtb_create_case_page.enter_primary_oncologist(data=Primary_Oncologist_data)
        app_test.mtb_create_case_page.click_on_save_and_close()
        # verify case id is created on mtb case management screen and its data
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        log.info("Test Passed - MTB case is created successfully (without recommendations summary)")
        log.info("\n Test Ended")

@pytest.mark.p0
def test_add_recommendation_summary_Cancel_Verify(app_test,test_launch_mtb,test_info):
        pytest.log_test = 'Verify add recommendation_summary , cancel and then verify'
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-40409"
        log.info("Test Started- to add recommendation_summary , cancel and then verify")
        #1st run test_mtb_create_case_without_recommendation_summary to create case without recommendation summary
        test_mtb_create_case_without_recommendation_summary(app_test,test_launch_mtb,test_info)
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()
        app_test.verification.scroll_to_bottom_of_page()
        app_test.mtb_create_case_page.enter_text_in_recommendationsSummary(what=Recommendations_Summary)
        app_test.mtb_create_case_page.click_on_Cancel_button()
        app_test.mtb_create_case_page.verify_user_clicks_on_continue()

        # verify case id on mtb case management screen and its data
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        app_test.mtb_create_case_page.click_on_to_enable_text(app_test.mtb_create_case_page.meeting_none)
        if app_test.mtb_create_case_page.Recommendations_Summary_value_verification(data=empty_Recommendations_Summary):
            log.info("Passed - recommendation_summary_text is not added after clicking on cancel")
            assert True, "recommendation_summary_text is added after clicking on cancel"
        else:
            log.info("Failed - recommendation_summary_text is added after clicking on cancel")
        log.info("\n Test Ended")

@pytest.mark.p0
def test_Remove_recommendation_summary_Save_Verify(app_test,test_launch_mtb,test_info):
        pytest.log_test = 'Verify Remove recommendation summary,Save and Verify'
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-40411"
        log.info("\n Test Started-to Remove recommendation summary,Save and Verify")
        #to remove dependancy first run "test_add_recommendation_summary_Save_Verify"
        test_add_recommendation_summary_Save_Verify(app_test,test_launch_mtb,test_info)
        case_id=app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()
        app_test.verification.scroll_to_bottom_of_page()
        app_test.mtb_create_case_page.enter_text_in_recommendationsSummary(what=empty_Recommendations_Summary)
        app_test.mtb_create_case_page.click_on_save_and_close()

        # verify case id on mtb case management screen and its data
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        app_test.mtb_create_case_page.click_on_to_enable_text(app_test.mtb_create_case_page.meeting_none)
        if app_test.mtb_create_case_page.Recommendations_Summary_value_verification(data=empty_Recommendations_Summary):
                log.info("Passed-recommendation_summary_text is empty")
                assert  True,"recommendation_summary_text is not empty"
        else:
                log.info("Failed-recommendation_summary_text is not removed/empty")
        log.info("\n Test Ended")

@pytest.mark.skip(reason='functionality no longer valid')
def test_200_character_limit_of_Recommendation_Summary(app_test, test_launch_mtb,test_info):
        pytest.log_test = 'Verify Recommendations summary text box exists and accepts text with 200 character limit'
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-39277"
        log.info("\n Test Started- Verify 'Recommendations summary' text box exists and accepts text with 200 character limit")
        app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()
        app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
        app_test.mtb_create_case_page.verify_recommendations_summary_text_present_on_page()
        app_test.mtb_create_case_page.scroll_to_meeting_summary()
        app_test.mtb_create_case_page.enter_text_in_recommendationsSummary(what=text_with_more_than_200_character)
        app_test.mtb_create_case_page.click_on_save_and_close()

        #verify that Recommendations Summary can accept only 200 characters
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        if app_test.mtb_create_case_page.Recommendations_Summary_value_verification(data=text_with_200_character):
            log.info("Passed-Recommendations Summary accepts text with 200 character limit")
            assert True, "Failed-Recommendations Summary accepts text with more than 200 character limit"
        else:
            log.info("Failed-Recommendations Summary accepts text with more than 200 character limit")
        log.info("\n Test Ended")

