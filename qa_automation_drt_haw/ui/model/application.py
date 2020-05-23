
import os

from selenium import webdriver

from qa_automation_drt_haw.ui.model.chronicle_cancer_diagnosis_page import Chronicle_Cancer_Diagnosis
from qa_automation_drt_haw.ui.model.chronicle_genomic_alterations_page import Chronicle_Genomic_Alterations
from qa_automation_drt_haw.ui.model.chronicle_patient_status_page import Chronicle_Patient_Status
from qa_automation_drt_haw.ui.model.chronicle_program_management_page import chronicle_Program_Management
from qa_automation_drt_haw.ui.model.chronicle_surgery_and_radiation_page import Chronicle_Surgery_And_Radiation
from qa_automation_drt_haw.ui.model.chronicle_systemic_therapy_page import Chronicle_Systemic_Therapy
from qa_automation_drt_haw.ui.model.cohort_builder_page import Cohort_Builder_page
from qa_automation_drt_haw.ui.model.mdx import MDX
from qa_automation_drt_haw.ui.model.program_insights_page import Program_Insights_page
from qa_automation_drt_haw.ui.model.nmr_page import nmr_page
from qa_automation_drt_haw.ui.model.bti_page import bti_page

from qa_automation_drt_haw.ui.model.session import Session
from qa_automation_drt_haw.ui.model.admin import Admin
from qa_automation_drt_haw.ui.model.chronicle import Chronicle
from qa_automation_drt_haw.ui.model.navigation import GeneralNavigation
from qa_automation_drt_haw.ui.model.care_dashboard import CareDashboard
from qa_automation_drt_haw.ui.model.verification import GeneralVerification
from qa_automation_drt_haw.ui.model.portal import Portal
from qa_automation_drt_haw.ui.model.finder import Finder
from qa_automation_drt_haw.ui.model.mtb import MTB
from decouple import config

from qa_automation_drt_haw.ui.model.mtb_case_management_page import Mtb_Case_Management_page
from qa_automation_drt_haw.ui.model.mtb_create_case_page import Mtb_Create_Case_page



# URL = 'https://portal-web.dev.syapse.com/'



class Application:
    URL = 'https://portal.%s.syapse.com/'
    SQA_URL = 'https://portal-%s.syapse.com/'

    def __init__(self, env, browser):
        self.env = env
        self.session = Session(self)
        self.admin = Admin(self)
        self.chronicle = Chronicle(self)
        self.navigation = GeneralNavigation(self)
        self.care_dashboard = CareDashboard(self)
        self.verification = GeneralVerification(self)
        self.portal = Portal(self)
        self.finder = Finder(self)
        self.mtb = MTB(self)
        self.mtb_case_management_page = Mtb_Case_Management_page(self)
        self.mtb_create_case_page = Mtb_Create_Case_page(self)
        self.program_insights_page = Program_Insights_page(self)
        self.cohort_builder_page = Cohort_Builder_page(self)
        self.nmr_page = nmr_page(self)
        self.bti_page = bti_page(self)
        self.chronicle_patient_status = Chronicle_Patient_Status(self)
        self.chronicle_cancer_diagnosis = Chronicle_Cancer_Diagnosis(self)
        self.chronicle_genomic_alterations = Chronicle_Genomic_Alterations(self)
        self.chronicle_systemic_therapy = Chronicle_Systemic_Therapy(self)
        self.chronicle_surgery_and_radiation = Chronicle_Surgery_And_Radiation(self)
        self.chronicle_program_management = chronicle_Program_Management(self)
        self.mdx = MDX(self)

        # set up driver
        self.driver = self.set_up_driver(browser)

        self.base_url = self.URL % env
        self.sqa_base_url = self.SQA_URL % env


    def set_up_driver(self, browser):
        if browser == 'chrome':

            chrome_profile = webdriver.ChromeOptions()

            chrome_profile.add_argument('--dns-prefetch-disable')
# The env var is set in the docker image
            if os.environ.get("IS_DOCKER") or os.environ.get('JENKINS_URL'):
               chrome_profile.add_argument('--headless')
            # chrome_profile.add_argument('--headless')
            chrome_profile.add_argument('--no-sandbox')
            chrome_profile.add_argument('--disable-gpu')
            chrome_profile.add_argument('--window-size=1600,1200')
            chrome_profile.add_argument('--no-cache')
            chrome_profile.add_argument('--disable-dev-shm-usage')
            var = os.getenv('ROOT_DIR') + "/temp_download"
            prefs = {"download.default_directory": "%s" % var}
            chrome_profile.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(options=chrome_profile)
            driver.implicitly_wait(20)
            driver.set_window_size(1600, 1200)
            # driver.maximize_window()
        elif browser == 'firefox':
            driver = webdriver.Firefox()
        else:
            print("Driver has not set up")
        return driver


    def open_home_page(self):
        self.driver.implicitly_wait(20)
        if self.env  == "dev":
            self.driver.get(self.base_url)
        elif self.env == "stg":
            self.driver.get(self.base_url)
        elif self.env == "sqa":
            self.driver.get(self.sqa_base_url)


    def destroy(self):
        self.driver.quit()

