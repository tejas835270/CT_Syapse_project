import time
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements

from qa_automation_drt_haw.ui.ui_utils.Logs import log


class nmr_page():

    # title of page
    title='Workbook: New Molecular Results'

    new_molecular_results_tab='New Molecular Results'

    # to initialize
    def __init__(self, app):
        self.app = app

    # purpose- to verify the title of Cohort Builder page when login with user having single org access
    def verify_nmr_title(self):
        self.app.verification.go_next_tab_verify_title(self.title)
