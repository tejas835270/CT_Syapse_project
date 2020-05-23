import time
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements

from qa_automation_drt_haw.ui.ui_utils.Logs import log

class Program_Insights_page():

    # title of Program_Insights_page
    title='Workbook: Program Insights'

    #url should contain below text
    url_contains = 'ProgramInsights'
    Date = 'Last 12 months'
    text = 'Years'

    # to initialize
    def __init__(self, app):
        self.app = app

    # purpose- to verify the title of program_insights page when login with user having single org access
    def verify_program_insights_title(self):
        self.app.verification.go_next_tab_verify_title(self.title)

    # purpose- to verify the url content when login with user having single org access
    def verify_url_contains_ProgramInsights(self):
        self.app.verification.go_next_tab_verify_url_and_close(self.url_contains)