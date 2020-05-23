import time
import random
from datetime import datetime, timedelta
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements


class CareDashboard:
    xpath_search_field = "//form[contains(@class, 'search-bar')]//input"
    xpath_search_fields = "//div[@class='modal-content']//div[@class='search-bar-container']//input"

    xpath_search_results = "//div[@class = 'modal-content']//tbody//tr"

    xpath_patient_finder_update_button = "//div[@class = 'modal-content']//button[text()='Update']"
    xpath_next_page = "//div[@class = 'modal-content']//*[contains(@class,'glyphicon-chevron-right pagination-glyph-active')]"

    xpath_dob ="(//div[@class = 'modal-content']//tbody//tr//div[contains(text(), .)])[3]"


    def __init__(self, app, name=[], dob=''):
        self.app = app
        # self.app.driver = app.driver
        self.name = name
        self.dob = dob

    def header_search(self, what):
        search_field = find_elements(self.app.driver, self.xpath_search_field)
        if not search_field:
            assert False, ('Search field has not been found')
        else:
            search_field[0].clear()
            search_field[0].send_keys(what)
            search_field[0].submit()
            time.sleep(8)

    def finder_pick_value(self, value):
        time.sleep(8)
        if value == 'random':
            search_results =find_elements(self.app.driver, self.xpath_search_results)
            random.choice(search_results).click()
            choice =find_elements(
                self.app.driver,"//div[@class = 'modal-content']//tbody//tr[contains(@style, 'background')]")
            if choice:
                try:
                    self.name
                except AttributeError:
                    self.name = []
                name = find_element(
                    self.app.driver,"//div[@class = 'modal-content']//tbody//tr[contains(@style, 'background')]/td/div").text
                if name in self.name:
                    self.finder_pick_value(value)
                    # context.execute_steps(u'''Then Finder - pick value "{0}"'''.format(value))
                else:
                    self.name.append(name)
                    print("\nSelected value is", self.name)
                    time.sleep(1)
                    self.app.navigation.click_btn("Continue")
        else:
            search_fields = find_elements(self.app.driver, self.xpath_search_fields)
            update_buttons = find_elements(self.app.driver,self.xpath_patient_finder_update_button)
            while True:
                if search_fields and update_buttons:
                    if search_fields[0].get_attribute('value') == '':
                        print('here')
                        search_fields[0].send_keys(value)
                        update_buttons[0].click()
                time.sleep(6)
                search_results = [x for x in find_elements(self.app.driver, self.xpath_search_results) if all(word in x.text for word in value.split())]

                if search_results:
                    print("-" + search_results[0].text + "-")
                    dob = find_elements(self.app.driver,self.xpath_dob)
                    try:
                        print('dod = ', dob[0].text)
                        self.dob = datetime.strptime(dob[0].text, '%Y-%m-%d').strftime('%d %b %Y')
                    except:
                        pass
                    search_results[0].find_element_by_xpath('./td/div').click()
                    self.app.navigation.click_btn("Continue")
                    time.sleep(3)
                    break
                else:
                    next_pg =find_elements(self.app.driver, self.xpath_next_page)
                    if not next_pg:
                        assert False, ('Record "%s" has not been found' % value)
                    else:
                        next_pg[0].click()
                        time.sleep(4)
        time.sleep(8)


    def find_and_pick_patient(self, value):
        self.header_search(value)
        self.finder_pick_value(value)




