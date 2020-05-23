import time
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements

from qa_automation_drt_haw.ui.ui_utils.Logs import log


class bti_page():

    # title of page
    title = 'Workbook: Biomarker Testing Insights'


    # to initialize
    def __init__(self, app):
        self.app = app

    # purpose- to verify the title of Cohort Builder page when login with user having single org access
    def verify_bti_title(self):
        self.app.verification.go_next_tab_verify_title(self.title)

