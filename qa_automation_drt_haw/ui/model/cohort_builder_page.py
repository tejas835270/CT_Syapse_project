import time
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements

from qa_automation_drt_haw.ui.ui_utils.Logs import log

class Cohort_Builder_page():

    # title of page
    title='Workbook: Cohort Builder'
    
    # for multi-org user url should contain below text
    url_contains_for_multi_org = 'CohortBuilderSomethingClinic'

    # title of page for multi-org user
    title_for_sub_org = 'Workbook: Cohort Builder Something Clinic'

    #Expected messages on UI
    resource_not_found_error='Resource Not Found'
    none="(None)"
    apply_btn="Apply"
    new_molecular_results_tab='New Molecular Results'

    # to initialize
    def __init__(self, app):
        self.app = app

    # purpose- to verify the title of Cohort Builder page when login with user having single org access
    def     verify_cohort_builder_title(self):
        self.app.verification.go_next_tab_verify_title(self.title)

    # purpose- to verify the title of Cohort Builder page when login with user having multi-org access
    def verify_cohort_builder_title_for_suborg(self):
        self.app.verification.go_next_tab_verify_title(self.title_for_sub_org)

    # purpose- to verify the url content when login with user having multi-org access
    # parent org = Integration2
    # sub-org=SomethingClinic
    def verify_url_contains_PatientCohortBuilderSomethingClinic(self):
        self.app.verification.go_next_tab_verify_url_and_close(self.url_contains_for_multi_org)