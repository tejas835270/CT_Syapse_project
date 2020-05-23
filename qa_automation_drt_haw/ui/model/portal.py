import time

from selenium.webdriver.common.keys import Keys
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import *
from qa_automation_drt_haw.ui.ui_utils.Logs import log

class Portal():
    xpath_auth_username = "//input[@name = 'email']"
    xpath_auth_password = "//input[@name = 'password']"
    xpath_login_btn = "//button[@type='submit']"
    xpath_welcome="//*[text()[contains(.,'Welcome!')]]"
    xpath_sign_out="//a[text()='Sign Out']"
    xpath_account_link="//span[@data-qa-key='account-link']"
    xpath_tile_text = "//*[contains(text(),'%s')]"
    xpath_tile_description = "//*[contains(text(),'%s')]"
    xpath_welcome_text_page_component = "//header[@class='ant-layout-header' and @data-qa-key='syapsePageTitle']"

    # Change Application related info like Application name and description which needs to be tested
    tile_text = 'Precision Medicine Impact'
    tile_description = 'Understand follow through for tumor board interventions and germline counseling'
    none_id="//*[contains(text(), '(None)')]"
    bti_id = "//*[contains(text(),'Cancer Dashboard')]"

    #available service names
    mtb_service_name='Molecular Tumor Board Manager'

    #available service names
    mtb_service_name='Molecular Tumor Board Manager'
    mdx_service_name='Patient Finder'

    def __init__(self, app):
        self.app = app

    #purpose: login to the portal
    #username and password will be passed from test file
    def login(self, username, password):
            log.info("Logging into Application")
            find_element(self.app.driver, self.xpath_auth_username).send_keys(username)
            find_element(self.app.driver, self.xpath_auth_password).send_keys(password)
            find_element(self.app.driver, self.xpath_login_btn).click()
            try:
                WebDriverWait(self.app.driver, 5).until(EC.visibility_of_element_located((By.XPATH, self.xpath_welcome)))
                log.info("login is successful with valid credentials")
            except:
                log.info("login is unsuccessful, please check entered username or password!")

    def clear_fields_and_login(self, username, password):
            log.info('Log in as "%s" with password "%s"' % (username, password))
            log.info("clear fields before login")
            username_field = find_element(self.app.driver, self.xpath_auth_username)
            pwd_field = find_element(self.app.driver, self.xpath_auth_password)
            username_field.send_keys(Keys.CONTROL, 'a')
            username_field.send_keys(Keys.DELETE)
            pwd_field.send_keys(Keys.CONTROL, 'a')
            pwd_field.send_keys(Keys.DELETE)
            find_element(self.app.driver, self.xpath_auth_username).send_keys(username)
            find_element(self.app.driver, self.xpath_auth_password).send_keys(password)
            find_element(self.app.driver, self.xpath_login_btn).click()
            time.sleep(2)

    def logout(self):
            '''
            :purpose: logout from the application by clicking on "sign out"
            :return: land to login page
            '''
            log.info('Logout from the application')
            find_element(self.app.driver, self.xpath_account_link).click()
            WebDriverWait(self.app.driver, 2).until(EC.visibility_of_element_located((By.XPATH, self.xpath_sign_out))).click()
            try:
                WebDriverWait(self.app.driver, 5).until(EC.visibility_of_element_located((By.XPATH, self.xpath_auth_username)))
                log.info("user successfully logged out from the application")
            except:
                log.info("user not logged out from the application")
                raise Exception("user not logged out from the application")

    def verify_service_is_enabled_for_user(self, services, enabled=True):
            '''
            :purpose:check the mentioned services are enabled as per user's roles
            :param Services: list of services
            '''
            log.info('Verify: service/s - %s is/are enable (%s)' % (services, enabled))
            actual_services = [x.text for x in find_elements(self.app.driver, "//a//div[@class='ant-card-head-title']")]
            print(actual_services)

            for s in services:
                print("--", s)
                if enabled:
                    log.info("service '%s' is enable and found" %s)
                    assert (s in actual_services), "Error: service '%s' has not been found" % (s)
                else:
                    log.info("Error: service '%s' has not been found" % (s))
                    assert (s not in actual_services), "Error: service '%s' has been found" % (s)

            if len(services) == 0:
                log.info("user has no roles/services")
                assert len(actual_services) == 0, "Error: service '%s' has been found; Expected: no available services" % actual_services

    def navigate_to_mtb_service(self, service_name=mtb_service_name):
            '''
            :purpose: to click on given service
            :param service_name: it is name of service where user wants to navigate
            :return: it will open given service page
            '''
            self.navigate_to_portal_service(service_name)
            if not self.app.mtb_case_management_page.verify_create_new_case_text_present_on_page():
                log.info("successfully navigated to %s service" %service_name )
            else:
                log.error("navigation falied to %s service" % service_name)

    def navigate_to(self, service_name):
            log.info('Navigate to service "%s"' % service_name)
            time.sleep(3)
            links = find_elements(self.app.driver, "//div[text()='%s']" % service_name)
            assert len(links) > 0, "Service '%s' has not been found"
            links[0].click()
            time.sleep(2)

    def click_syapse_logo(self):
            '''
            :purpose: to click on Syapse logo
            :return: navigate to the portal page
            '''
            log.info('Click Syapse logo')
            find_element(self.app.driver, "//span[@class='logo']").click()
            log.info('Clicked on Syapse logo and navigated to portal page')

    #purpose - to click/navigate to portal links
    #service_name is the service name which will be passed from page class file
    def navigate_to_portal_service(self, service_name):
            log.info('Navigate to service "%s"' % service_name)
            links = WebDriverWait(self.app.driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, "//div[text()='%s']" % service_name)))
            assert len(links) > 0, "Service '%s' has not been found"
            links[0].click()
            log.info("clicked on '%s' link" %service_name)
            time.sleep(2)

    def navigate_to_Program_Insights(self):
            log.info("Navigate to service 'Program Insights'")
            self.navigate_to_portal_service('Program Insights')
            log.info("clicked on 'Program Insights' link")

    # purpose - to navigate to [Cohort_Builder] link
    # none_id:- is the none element locator which is present on [Cohort_Builder] page
    def  navigate_to_Cohort_Builder(self):
            log.info("Navigate to service 'Cohort Builder'")
            self.navigate_to_portal_service("Cohort Builder")
            windows = self.app.driver.window_handles
            self.app.driver.switch_to.window(windows[1])
            WebDriverWait(self.app.driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH,self.none_id)))
            log.info("clicked on  'Cohort Builder' link")

    def  navigate_to_New_Molecular_Result(self):
            log.info("Navigate to service 'New Molecular Results'")
            self.navigate_to_portal_service("New Molecular Results")
            windows = self.app.driver.window_handles
            self.app.driver.switch_to.window(windows[1])
            WebDriverWait(self.app.driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH,self.none_id)))
            log.info("clicked on  'New Molecular Results' link")

    def  navigate_to_BTI(self):
            log.info("Navigate to service 'Biomarker Testing Insights'")
            self.navigate_to_portal_service("Biomarker Testing Insights")
            windows = self.app.driver.window_handles
            self.app.driver.switch_to.window(windows[1])
            WebDriverWait(self.app.driver, 30).until(EC.visibility_of_all_elements_located((By.XPATH,self.bti_id)))
            log.info("clicked on  'Biomarker Testing Insights' link")

    def navigate_to_Patient_Data_Entry(self):
            self.navigate_to_portal_service("Patient Data Entry")
            log.info("clicked on 'Patient Data Entry' link")
#
    def verify_url_contains_portal(self):
        '''
        :purpose: to check user has navigated successfully to portal page by checking the url
        '''
        log.info("Verify user has navigated successfully to portal page by checking the current url")
        if self.app.env  == "dev":
            self.app.verification.verify_current_url_contains(self.app.base_url)
        elif self.app.env == "sqa":
            self.app.verification.verify_current_url_contains(self.app.sqa_base_url)

    def verify_invalid_credentials_error(self):
        self.app.verification.text_present_on_page('Wrong email or password')

    def verify_url_contains_auth0(self):
        self.app.verification.verify_current_url_contains('auth0')

    def verify_pwd_blank_error(self):
        self.app.verification.text_present_on_page("Can't be blank")

    def verify_user_info_present(self,page_text):
        '''
        :param page_text: It stores user's full name
        :purpose: verify that user's full name is present on the portal page
        :return: user's full name is present or not
        '''
        log.info('Verify the user_full_name is present on the page')
        try:
            element = WebDriverWait(self.app.driver, 2).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[text()[contains(.,\"%s\")]]" % page_text)))
            if element:
                assert True, 'The user_full_name is displayed on the page'
                log.info(" The user_full_name is displayed on the page")
                print("\n The user_full_name is displayed on the page")
        except:
            log.error(" The user_full_name is NOT displayed on the page")
            assert False, 'The user_full_name  is not displayed on the page'

    def verify_Application_tile_IsPresent(self, service_name):
        """  Purpose : This method is useful to get the Tile of the particular application on portal
            :param service_name: Service name is a Tile name of any application under test
            :return: True or False
        """
        try:
            text = find_element(self.app.driver, self.xpath_tile_text % service_name)
            log.info('Application is on portal')
            assert True, "Application is on portal"
            return True
        except:
            log.info('Application is not on portal')
            raise Exception('Application is Not present on the Portal')

    def verify_Application_description(self, service_name, description):
        """  Purpose : This method is useful to get the description of the particular application on portal
            :param service_name: Service name is a Tile name of any application under test
            :param description: description is brief info about an application(what is use of an application).It is
            associated with the application name.
            :return: None
        """
        if self.verify_Application_tile_IsPresent(service_name):
            try:
                tile_description = find_element(self.app.driver, self.xpath_tile_description % description)
                log.info("Application Description is matching")
                assert True, "Application Description is matching"
            except:
                log.info("Application Description is not matching")
                raise Exception('!!!!....Application Description is not Matching...!!!')

    def verify_portal_home_screen(self):

        element = find_elements(self.app.driver,self.xpath_welcome)
        assert len(element) > 0, "Portal home page is not opened"


    def verify_page_tile_welcome_text_height(self):
        """
        This function verifies the height of the page component "Welcome Text"
        """
        height = find_element(self.app.driver,self.xpath_welcome_text_page_component)
        height_value= height.size['height']
        try:
            if height_value == 76:
                log.info("Welcome Text Component size is %s",height_value)
            else:
                log.error("Welcome Text Component size is changed and retrieved value is %s",height_value)
                assert False,"Welcome Text component size is changed"
        except:
            log.error("Welcome Text Component size is changed and retrieved value is %s", height_value)
            assert False, "Welcome Text component size is changed"