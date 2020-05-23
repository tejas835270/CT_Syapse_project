import time
from qa_automation_drt_haw.ui.ui_utils.Logs import log

from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements


class Admin:

    xpath_interface = "//section[.//h4[text() = '%s']]//span[text() = 'Enter']"
    xpath_admin_page_content = "//div[@id = 'admin-page-content']//*[@class = '%s']"
    xpath_page_title = "//h3[text() = '%s']"
    xpath_section_text = "//div[./h3[text() = '%s']]//div[@class = 'section-body']"

    def __init__(self, app):
        self.app = app
        # self.driver = app.driver


    def choose_interface(self, interface):
        log.info('Choose interface "%s"'%interface)
        self.app.driver.implicitly_wait(25)
        btn = find_elements(self.app.driver, self.xpath_interface % interface)
        if btn:
            btn[0].click()
            time.sleep(3)
        else:
           assert False, (
                'Seems that you have entered not valid variable (not "Content", "Care" or "Admin"). Or it might be a bug')
        time.sleep(2)


# ------------verification  -------------
    def verify_admin_landing_page(self):
        """
        verifies landing page welcome msgs and icons

        """
        log.info('Admin interface landing page')
        self.app.driver.implicitly_wait(5)

        for what, dom_class in [('icon', 'home-logo'), ('title', 'home-msg')]:
            if not find_element(self.app.driver,self.xpath_admin_page_content%dom_class):
                assert False, "Admin landing page {0} is missing".format(what)

        for title, info in [('Organization and user accounts',
                             'Manage profile information for healthcare organizations and their employees deployed on the Syapse Precision Medicine Platform.'),
                            ('User activity and record history',
                             'In User Activity, view login attempts for a specific user or for all users in their organization. Access Record History to view details of all changes to to records in your Syapse application.')]:

            if not find_element(self.app.driver, self.xpath_page_title % title):
                assert False, 'Admin landing page title has not been found - "%s"'.format(title)

            section_text = \
                find_elements(self.app.driver, self.xpath_section_text % title)[
                0].text
            diff = list(set(info.split()) - set(section_text.split()))
            if diff:
                assert False, 'Admin landing page description for title "{0}" does not match expected one.\nDifference: {1}'.format(
                    title, diff)


    def verify_admin_interface_menu_works(self):
        """
        Admin interface menu links should work
        will iterate trough all items (except django leading) and verify that they work (by href navigation and title)
        """
        from fuzzywuzzy import fuzz

        log.info('Admin interface menu links should work')
        sections = [section.text.strip() for section in find_elements(self.app.driver, "//div[contains(@class, 'nav-section-title')]")]
        print(sections)
        for section in sections:
            links = [(x.text, x.get_attribute('href')) for x in find_elements(self.app.driver,
                    "//div[div[contains(@class, 'nav-section-title')][contains(., '%s')]]//a[@class = 'admin-link']" % section) if x.get_attribute('target') == '']
            print(links)
            for link, href in links:
                find_element(self.app.driver,"//div[div[contains(@class, 'nav-section-title')][contains(., '%s')]]//a[@class = 'admin-link'][text() = '%s']" % (section, link)).click()
                time.sleep(2)
                if fuzz.partial_ratio(href, self.app.driver.current_url) < 97:
                    assert False, '{0} has not been navigated to {1}. Landed at {2}'.format(link, href, self.app.driver.current_url)

