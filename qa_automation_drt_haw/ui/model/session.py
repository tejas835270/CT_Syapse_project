import time


from selenium.webdriver.common.keys import Keys

from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import react_loadmask


class Session:

    xpath_username = "//input[@name = 'username']"
    xpath_password = "//input[@name = 'password']"

    def __init__(self, app):
        self.app = app

    def login(self, username, psw):
        time.sleep(3)
        input_username = self.app.driver.find_element_by_xpath(self.xpath_username)
        input_username.send_keys(username, Keys.ENTER)
        time.sleep(2)

        input_psw = self.app.driver.find_element_by_xpath(self.xpath_password)
        input_psw.send_keys(psw, Keys.ENTER)
        time.sleep(3)

        react_loadmask(self.app.driver)
        time.sleep(3)


    def logout(self):
        pass

    def reset_psw(self,username, psw):
        pass



    def verify_user_is_logged(self, where):
        """
        :param where: "in"\"out" - to verify login\logout
        """
        # log.info('Am I %s'%where)
        if where == 'in':
            if 'logout' in self.app.driver.current_url or not self.app.driver.find_elements_by_xpath(
                    "//*[text() = 'Sign out' or text() = 'Sign Out' or text() = 'Please choose an interface']"):
                assert False, 'Looks we have not been logged in.'
        elif where == 'out':
            if not self.app.driver.find_elements_by_xpath("//button[text() = 'Sign in']"):
                assert False, 'We are not on login page. User might be in the system'
        else:
            assert 'Unknown parameter given - "{0}". Expected: "in" or "out"'.format(where)


