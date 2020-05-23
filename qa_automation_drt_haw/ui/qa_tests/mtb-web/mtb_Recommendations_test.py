import pytest

from qa_automation_drt_haw.settings import Config
from qa_automation_drt_haw.ui.ui_utils.Logs import log

#pick up credentials from setting.py file
username = Config.mtb_testing_only_username
psw = Config.mtb_testing_only_password

#  below are the data which comes from fixture_data.json file to fill the fields on [create new case] page
meeting_date= pytest.data.get_mtb_create_case_data('Meeting_Date')
notes_data1=pytest.data.get_mtb_create_case_data('notes_data1')
notes_data2=pytest.data.get_mtb_create_case_data('notes_data2')
description_data1=pytest.data.get_mtb_create_case_data('description_data1')
description_data2=pytest.data.get_mtb_create_case_data('description_data2')
text_with_more_than_200_character= pytest.data.get_mtb_create_case_data('text_with_more_than_200_character')
text_with_200_character= pytest.data.get_mtb_create_case_data('text_with_200_character')

#pick up dropdown value fron vocab Recommendation_type.csv
type_options=pytest.data.retrive_data_from_csv_to_list(data_file='Recommendation_type.csv')

@pytest.fixture(scope="function")
def test_launch_mtb(app_test):
    app_test.portal.login(username, psw)
    app_test.portal.navigate_to_mtb_service()


@pytest.mark.p4
@pytest.mark.p1
def test_recommendation_fields_and_default_state(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38053"
        pytest.log_test = 'Verify recommendation fields and default state'
        log.info("\n Test Started- to Verify recommendation fields and default state")
        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()

        app_test.mtb_create_case_page.verify_none_provided_text()
        app_test.verification.verify_button_is_present(app_test.mtb_create_case_page.add_recommendation_text)
        app_test.navigation.click_button(button_name=app_test.mtb_create_case_page.add_recommendation_text,expected_text=app_test.mtb_create_case_page.recommendation_type)

        app_test.mtb_create_case_page.verify_recommendations_fields()
        log.info("Test passed-recommendation fields and default state are correct")

@pytest.mark.p4
@pytest.mark.p2
def test_recommendations_error_messages(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38052"
        pytest.log_test = 'Verify app_testropriate error message is displayed when required fields are missing'
        log.info("\n Test Started- to Verify app_testropriate error message is displayed when required fields are missing")

        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()

        app_test.mtb_create_case_page.scroll_to_recommendations()
        app_test.navigation.click_button(app_test.mtb_create_case_page.add_recommendation_text,app_test.mtb_create_case_page.recommendation_type)
        #case 1:
        app_test.mtb_create_case_page.enter_data_in_recommendations_notes(what=notes_data1)
        app_test.navigation.click_button(app_test.mtb_create_case_page.save,app_test.mtb_create_case_page.add_recommendation_text)
        app_test.verification.text_present_on_page(page_text=app_test.mtb_create_case_page.type_required_error)
        app_test.verification.text_present_on_page(page_text=app_test.mtb_create_case_page.description_required_error)

        # case 2:
        app_test.mtb_create_case_page.select_option_from_recommendation_type(option_name=type_options[1])
        app_test.navigation.click_button(app_test.mtb_create_case_page.save, app_test.mtb_create_case_page.add_recommendation_text)
        app_test.verification.text_present_on_page(page_text=app_test.mtb_create_case_page.description_required_error)

        # case 3:
        app_test.navigation.click_btn(app_test.mtb_create_case_page.remove)
        app_test.navigation.click_button(app_test.mtb_create_case_page.add_recommendation_text,app_test.mtb_create_case_page.recommendation_type)
        app_test.mtb_create_case_page.enter_data_in_recommendations_description(what=description_data1)
        app_test.navigation.click_button(app_test.mtb_create_case_page.save, app_test.mtb_create_case_page.add_recommendation_text)
        app_test.verification.text_present_on_page(page_text=app_test.mtb_create_case_page.type_required_error)
        log.info("app_testropriate error message is displayed when required fields are missing")

@pytest.mark.p4
@pytest.mark.p3
def test_recommendation_type_dd_options(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38054"
        pytest.log_test = 'Verify dropdown options for recommendation type'
        log.info("\n Test Started- to Verify dropdown options for recommendation type")

        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()

        app_test.mtb_create_case_page.scroll_to_recommendations()
        app_test.navigation.click_button(app_test.mtb_create_case_page.add_recommendation_text,app_test.mtb_create_case_page.recommendation_type)
        app_test.verification.verify_dd_default_value(dd_name=app_test.mtb_create_case_page.recommendation_type_class,expected_option=type_options[0])
        app_test.verification.verify_dd_values(dd_class=app_test.mtb_create_case_page.recommendation_type_class,data=type_options)
        log.info("Test passed- dropdown options for recommendation type are correct")


@pytest.mark.p3
def test_200_character_limit_of_Recommendation_Description(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38055"
        pytest.log_test = 'Verify user can enter a description between 0 and 200 characters, inclusively'
        log.info("\n Test Started- to Verify user can enter a description between 0 and 200 characters, inclusively")

        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()

        app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
        app_test.mtb_create_case_page.scroll_to_recommendations()
        app_test.navigation.click_button(app_test.mtb_create_case_page.add_recommendation_text,app_test.mtb_create_case_page.recommendation_type)
        app_test.mtb_create_case_page.select_option_from_recommendation_type(option_name=type_options[1])
        app_test.finder.text_field_enter(what=text_with_more_than_200_character, idVal=app_test.mtb_create_case_page.description_id)
        app_test.verification.verify_textarea_value(expected_text=text_with_200_character, idVal=app_test.mtb_create_case_page.description_id)
        app_test.mtb_create_case_page.click_on_save_and_close()

        # verify that case saved successfully with 200 character limit of description
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        app_test.verification.verify_textarea_value(expected_text=text_with_200_character, idVal=app_test.mtb_create_case_page.description_id)
        log.info("Test passed- user can enter up to 200 chars in Recommendation_Description and successfully save MTB case")


@pytest.mark.p3
def test_200_character_limit_of_notes(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38056"
        pytest.log_test = 'Verify notes is a free text field with 200 char limit'
        log.info("\n Test Started- to verify notes is a free text field with 200 char limit")

        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()

        app_test.mtb_create_case_page.scroll_to_recommendations()
        app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
        app_test.navigation.click_button(app_test.mtb_create_case_page.add_recommendation_text,app_test.mtb_create_case_page.recommendation_type)
        app_test.mtb_create_case_page.select_option_from_recommendation_type(option_name=type_options[1])
        app_test.mtb_create_case_page.enter_data_in_recommendations_description(what=text_with_200_character)
        app_test.mtb_create_case_page.enter_data_in_recommendations_notes(what=text_with_more_than_200_character)
        app_test.mtb_create_case_page.click_on_save_and_close()
        # verify that case saved successfully with 200 character limit of notes
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        # app_test.mtb_create_case_page.click_on_to_enable_text(app_test.mtb_create_case_page.notes_)
        app_test.verification.verify_textarea_value(expected_text=text_with_200_character, idVal=app_test.mtb_create_case_page.notes_id_verify)
        log.info("Test passed-  notes is a free text field with 200 char limit")


@pytest.mark.p2
def test_mtb_create_case_without_recommendation(app_test,test_launch_mtb,test_info):
        log.info("\n Test Started- to Verify 'Recommendations summary' field is optional to create MTB case")

        app_test.mtb_case_management_page.verify_create_new_case_text_present_on_page()
        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()

        app_test.mtb_create_case_page.enter_meeting_date(date=meeting_date)
        app_test.mtb_create_case_page.click_on_save_and_close()
        # verify case id is created on mtb case management screen and its data
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        log.info("Test Passed - MTB case is created successfully (without recommendations summary)")
        log.info('-----END-----')

@pytest.mark.p1
def test_add_one_recommendation(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38057 - scenario-1"
        pytest.log_test = 'Verify user can add 1 recommendations for a given MTB case'
        log.info("\n Test Started- to Verify user can add one recommendation")

        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()

        app_test.mtb_create_case_page.scroll_to_recommendations()
        app_test.mtb_create_case_page.fill_out_Recommendations(type_data=type_options[1],description_data=description_data1,notes_data=notes_data1)
        app_test.mtb_create_case_page.click_on_save_and_close()
        # verify that case is created succcessfully
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        app_test.mtb_create_case_page.Verify_values_for_Recommendations(type_data=type_options[1],description_data=description_data1,notes_data=notes_data1)
        log.info("Test passed- user successfully added 1 recommendation for a given MTB case")

@pytest.mark.p3
def test_add_more_recommendations(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38057 - Scenario-2"
        pytest.log_test = 'Verify user can add 1 or more recommendations for a given MTB case'
        log.info("Test Started- to Verify user can add 1 or more recommendations for a given MTB case")

        app_test.mtb_case_management_page.click_on_create_new_case_button()
        app_test.verification.search_box()
        app_test.finder.search_specific_patient()
        case_id = app_test.mtb_create_case_page.pick_up_case_ID()
        case_url = app_test.mtb_create_case_page.get_case_url()
        app_test.mtb_create_case_page.scroll_to_recommendations()

        #add more recommendations
        app_test.mtb_create_case_page.fill_out_Recommendations(type_data=type_options[1],description_data=description_data1,notes_data=notes_data1)
        app_test.mtb_create_case_page.fill_out_Recommendations(type_data=app_test.mtb_create_case_page.treatment_1, description_data=description_data2,notes_data=notes_data2,i=1)
        app_test.mtb_create_case_page.fill_out_Recommendations(type_data=app_test.mtb_create_case_page.genetic_2,description_data=description_data1,notes_data=notes_data1, i=2)
        app_test.mtb_create_case_page.fill_out_Recommendations(type_data=app_test.mtb_create_case_page.molecular_3,description_data=description_data2,notes_data=notes_data2, i=3)
        app_test.mtb_create_case_page.fill_out_Recommendations(type_data=app_test.mtb_create_case_page.other_4,description_data=description_data1, notes_data=notes_data1,i=4)
        app_test.mtb_create_case_page.click_on_save_and_close()

        # verify that case has been save with correct data
        app_test.mtb_case_management_page.navigate_to_case(case_url, case_id)
        app_test.mtb_create_case_page.Verify_values_for_Recommendations(type_data=type_options[1], description_data=description_data1,notes_data=notes_data1)
        app_test.mtb_create_case_page.Verify_values_for_Recommendations(type_data=type_options[2], description_data=description_data2,notes_data=notes_data2,i=1)
        app_test.mtb_create_case_page.Verify_values_for_Recommendations(type_data=type_options[3],description_data=description_data1,notes_data=notes_data1, i=2)
        app_test.mtb_create_case_page.Verify_values_for_Recommendations(type_data=type_options[4],description_data=description_data2, notes_data=notes_data2,i=3)
        app_test.mtb_create_case_page.Verify_values_for_Recommendations(type_data=type_options[5],description_data=description_data1,notes_data=notes_data1, i=4)
        log.info("Test passed- user successfully added 1 recommendation for a given MTB case")

@pytest.mark.p2
def test_user_can_delete_recommendations(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38058"
        pytest.log_test = 'Verify user can delete recommendation(s)'
        log.info("\n Test Started- to Verify user can delete recommendation(s)")

        #first run "test_add_more_recommendations" test to add multiple recommendations
        test_add_more_recommendations(app_test, test_launch_mtb, test_info)

        # scenario 1 -Click 'Remove' button for one recommendation and 'Save'. Recommendation should be successfully deleted
        app_test.mtb_create_case_page.scroll_to_recommendations()
        app_test.mtb_create_case_page.verify_one_recommendation_is_removed()

        # scenario 2- Verify user cannot delete "Description" for a recommendation. Required field UI validation error should be thrown
        app_test.mtb.clear_input_field_using_backspace(field_name=app_test.mtb_create_case_page.description_id)
        app_test.verification.text_present_on_page(page_text=app_test.mtb_create_case_page.description_required_error)


        # scenario 3-Verify user cannot delete "Type" for a recommendation. Required field UI validation error should be thrown
        app_test.mtb_create_case_page.select_option_from_recommendation_type(option_name=type_options[0])
        app_test.verification.text_present_on_page(page_text=app_test.mtb_create_case_page.type_required_error)

        #scenario 4 :-Click 'Remove' button for all the remaining recommendations and 'Save'. Verify no recommendations are available for this MTB case, and that the "Recommendations" section now displays the default state
        app_test.mtb_create_case_page.remove_all_recommendations()
        app_test.mtb_create_case_page.save_case()
        app_test.mtb_create_case_page.verify_none_provided_text()
        app_test.verification.verify_button_is_present(app_test.mtb_create_case_page.add_recommendation_text)

        log.info("Test passed- user can delete recommendation(s) for a given MTB case")

@pytest.mark.p2
def test_user_can_edit_recommendation(app_test, test_launch_mtb,test_info):
        pytest.log_link = "https://syapse.atlassian.net/browse/AP-38059"
        pytest.log_test = 'Verify user can edit recommendation(s)'
        log.info("\n Test Started- to Verify user can edit recommendation(s)")

        #first run "test_add_more_recommendations" test to add multiple recommendations
        test_add_more_recommendations(app_test, test_launch_mtb, test_info)

        #edit 1st row of the recommendation
        app_test.mtb_create_case_page.scroll_to_recommendations()
        app_test.mtb_create_case_page.select_option_from_recommendation_type(option_name=type_options[2])
        app_test.mtb_create_case_page.edit_data_in_recommendations_notes(what=notes_data2)
        app_test.mtb_create_case_page.enter_data_in_recommendations_description(what=description_data2)
        app_test.mtb_create_case_page.save_case()
        app_test.mtb_create_case_page.Verify_values_for_Recommendations(type_data=type_options[2],description_data=description_data2,notes_data=notes_data2)
        log.info("Test passed- user can edit recommendation for a given MTB case")