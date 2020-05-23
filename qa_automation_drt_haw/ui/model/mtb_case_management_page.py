import time
from datetime import datetime
import os

from selenium.webdriver.common.keys import Keys

from qa_automation_drt_haw.ui.ui_utils import JS_tricks
from qa_automation_drt_haw.ui.ui_utils.Logs import log
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import find_element, find_elements
from qa_automation_drt_haw.ui.ui_utils.Selenium_tricks import *

class Mtb_Case_Management_page:
    mtb_url = 'https://mtb.%s.syapse.com/'
    xpath_dob = "//*[@id=\"id-1-1\"]//tr[%s]/td[%s]"

    # Expected title/header data which should be present on [mtb case management] page
    mtb_case_management_text='MTB Case Management'
    mtb_recommendation_summary = "Recommendations Summary"
    cases_text='Cases'
    Create_New_Case_text='Create New Case'
    attachment_items = "//span[@class='attachment_upload']//div[contains(@class,'ant-upload-list-item ')]"
    attachment_download_button = "//span[@class='attachment_upload']//img[contains(@class,'attachment-download')]"
    attachment_delete_button = "//span[@class='attachment_upload']//i[contains(@class,'delete')]"
    attachment_body_section = "//span[@class='attachment_upload']/.."
    carousel_view_for_attachment = "//div[contains(@class,'attachments-image-carousel')]"
    carousel_close_button = "//button[@class='ant-modal-close']"
    dark_mode_button = "//span[@id='dark-mode']"
    style_on_dark_mode = "//span[@id='dark-mode']//preceding-sibling::style"
    attachment_name_xpath="//a[@class='ant-upload-list-item-name ant-upload-list-item-name-icon-count-0']"

    if os.getenv('ROOT_DIR') is not None:
        attachment_download_folder = os.getenv('ROOT_DIR') + '/temp_download'
    else:
        log.error("Unable to get root folder directory.")

    #to initialize
    def __init__(self, app):
        self.app = app
        self.env = self.app.env

    # purpose- navigate to mtb url
    #mtb_url stores the mtb url
    def navigate_to_mtb_url(self):
        self.app.driver.implicitly_wait(15)
        self.app.driver.get(self.mtb_url % self.env)
        log.info("navigated to mtb url")
        self.app.driver.set_page_load_timeout(5)
        self.verify_create_new_case_text_present_on_page()


    def verify_all_column_header_on_table(self):
        '''
        :purpose: Verify the column headers on [mtb case management] page
        '''
        self.app.verification.verify_column_headers_on_table('Meeting Date')
        self.app.verification.verify_column_headers_on_table('Case ID')
        self.app.verification.verify_column_headers_on_table('Diagnosis')

    def meeting_date_ascending_sorting(self, sortfield='Sort'):
            '''
            :purpose: verify the default sorting
            :return: whether list is sorted ot not
            '''
            log.info('Verify Default "%s" is available for "meeting date" column on [mtb case management] page' % sortfield)
            sort_field = find_elements(self.app.driver, "//*[@title='%s']" % sortfield)
            assert len(sort_field) > 0, 'Sort field have not been found'
            table1 = find_element(self.app.driver, "//tbody/tr[1]/td[1]")
            table20 = find_element(self.app.driver, "//tbody/tr[20]/td[1]")
            before_sort_max = table1.text
            before_sort_min = table20.text

            sort_field[0].click()
            time.sleep(0.5)
            sort_field = find_elements(self.app.driver, "//*[@title='%s']" % sortfield)
            sort_field[0].click()
            time.sleep(0.5)
            table1 = find_element(self.app.driver, "//tbody/tr[1]/td[1]")
            table20 = find_element(self.app.driver, "//tbody/tr[20]/td[1]")
            after_sort_max = table20.text
            after_sort_min = table1.text
            print("Before sort Max", before_sort_max)
            print("Before Sort Min", before_sort_min)
            print("After Sort Max", after_sort_max)
            print("After Sort Min", after_sort_min)

            if before_sort_max == after_sort_min and before_sort_min == after_sort_max:
                log.info("Meeting date column is sorted in ascending order")
                assert True, "Meeting date column is sorted in ascending order"
            else:
                log.error("Meeting date column is not sorted")
                assert False, "Meeting date column is not sorted"

    # purpose- pick up the case id from [create new case]page
    def pick_case(self, patientName):
            log.info('Click case for patient "%s" ' % patientName)
            row_field = find_elements(self.app.driver, "//*[contains(text(),'%s')]" % patientName)
            assert len(row_field) > 0, 'Row field have not been found'
            row_field[0].click()
            time.sleep(3)

    def verify_current_url_contains_mtb(self):
        self.app.verification.verify_current_url_contains('mtb')

    def verify_Molecular_Tumor_Board_text_present_on_page(self, param='Molecular Tumor Board'):
        self.app.verification.text_present_on_page(param)

    #purpose - to verify that 'Create New Case' is diplayed on mtb page
    def verify_create_new_case_text_present_on_page(self, param=Create_New_Case_text):
        log.info('Verify that user is present on [mtb management page] by checking availability of "create new case" button')
        if self.app.verification.text_present_on_page(param):
            flag=True
        else:
            flag = False
        return flag

    def verify_Cases_text_present_on_page(self, param='Cases'):
        self.app.verification.text_present_on_page(param)

    # purpose - to click on 'Create New Case' button on mtb page
    #btn_name is the name of button declared at the top
    def click_on_create_new_case_button(self, btn_name=Create_New_Case_text):
        """
        click on element with text if its displayed
        """
        self.app.navigation.click_btn(btn_name)
        log.info("user will navigate to [search patient] page")

    # purpose - navigate to given 'case_id'
    #case_id is passed from test file
    def navigate_to_caseID(self, case_id):
        log.info('Navigation to the case - "%s"' %case_id)
        self.verify_create_new_case_text_present_on_page()
        self.app.driver.implicitly_wait(10)
        # This will select a specified case
        if case_id != 'any':
            element = find_elements(self.app.driver, "//td[contains(.,'%s')]" % case_id)
        # This will select the first available case
        else:
            element = find_elements(self.app.driver, "//table//tr[2]")

        next_page_btn = find_element(self.app.driver, "//i[contains(@class,'anticon-right')]")

        if element:
            log.info("The case id has been found on [mtb case management] page.")
            element[0].click()

        else:
            while next_page_btn.is_enabled:
                self.app.verification.scroll_to_bottom_of_page()
                next_page_btn.click()
                time.sleep(3)
                element = find_elements(self.app.driver, "//td[contains(.,'%s')]" % case_id)
                if element:
                    log.info("\nThe case is created successfully")

                    JS_tricks.inner_scroll_to_element(self.app.driver, element)
                    element[0].click()
                    break
                else:
                    log.info("The case is not present on the current page, please load more cases")
                    next_page_btn = find_element(self.app.driver, "//i[contains(@class,'anticon-right')]")
        self.verify_mtb_case_management_text_present_on_page()

    #purpose - to verify that 'MTB Case Management' text is present on [mtb case management] page
    #param is the expected text defined at the top
    def verify_mtb_case_management_text_present_on_page(self, param=mtb_case_management_text):
        self.app.verification.text_present_on_page(param)

    def verify_mtb_case_management_text_not_present_on_page(self, param=mtb_case_management_text):
        self.app.verification.text_present_on_page(param, False)
        log.info("'MTB case management' text is not available on page")


    def verify_mtb_case_management_text_is_dispalyed(self):
        '''
        :purpose: This method is used to check whether mtb_case_management_text is visible on page
        :return: Boolean value (True or False)
        '''
        element = find_element(self.app.driver, "//*[contains(text(),'%s')]"%self.mtb_case_management_text)

        if element.is_displayed():
            log.info('%s is displayed'% self.mtb_case_management_text)
            assert True, '%s is displayed'% self.mtb_case_management_text
        else:
            log.error('%s is not displayed' % self.mtb_case_management_text)
            assert False, '%s is not displayed' % self.mtb_case_management_text

    def verify_recommendations_summary_text_is_dispalyed(self):
        '''
        :purpose: This method is used to check whether mtb_recommendation_summary is visible on page
        :return: Boolean value (True or False)
        '''
        element = find_element(self.app.driver, "//*[contains(text(),'%s')]"%self.mtb_recommendation_summary)
        if element.is_displayed():
            log.info('%s is displayed'% self.mtb_recommendation_summary)
            assert True, '%s is displayed'% self.mtb_recommendation_summary
        else:
            log.error('%s is not displayed' % self.mtb_recommendation_summary)
            assert False, '%s is not displayed' % self.mtb_recommendation_summary


    def navigate_to_case(self,case_path,case_id=None):
        '''
        Purpose: Navigates to the created case by using case url.
        :param case_path: url for the required case
        :param case_id: case id (It is optional). If provided then case-id will be verified on case management screen
        :return: Nothing
        :note: To get case url, "mtb_create_case_page.get_case_url()" can be used in the test
        '''
        log.info("Opening the case using case url")
        go_to_page(self.app.driver,case_path)
        self.verify_mtb_case_management_text_present_on_page()
        if case_id is not None:
            log.info("Verifyin the case id '%s' on case management screen" % case_id)
            assert self.app.verification.verify_case_id_is_displayed_on_case_managment_screen() == case_id, "Unable to open Case id '%s'" % case_id

    def verify_DOB_format(self,tr_row=1,td_col=2):
        """
        This function validates the DOB format of the patients.
        tr_row : Specify the row number in which DOB element is present
        td_col : Specify the Column in which DOB element is present(If later DOB element is shifted to 3rd or 4th column,change this value accordingly
        Returns True if DOB is in MMM DD, YYYY Format else returns False
        """
        dob = find_element(self.app.driver, self.xpath_dob %(tr_row,td_col))
        dob_value = str(dob.text)
        try:
            if format(dob_value).__eq__(datetime.strptime(dob_value, "%b %d, %Y")):
                log.info("Patient DOB is in Valid Format i.e MMM DD, YYYY")
                assert True, "Patient DOB is Valid"
        except:
            log.info("Invalid DOB format")
            raise Exception("Invalid DOB format", "Valid Format is MMM DD, YYYY")


    def click_on_MTB_case_management(self):

        temp_element = get_element_after_wait(self.app.driver,self.app.mtb_create_case_page.meeting_notes_button,timeout=10)
        if temp_element is not None:
            element = find_elements(self.app.driver,"//span[contains(text(),'%s')]" % self.mtb_case_management_text)
            if len(element) > 0:
                # element[0].click
                print("hello")
                print(element[0].is_enabled())
                if element[0].is_enabled():
                    action_click(self.app.driver,element[0])
                    log.info("Clicked on MTB_case_management")
            else:
                log.error("MTB_case_management is not displayed.")
        else:
            log.error("MTB case did not load.")

    def get_attachents_count(self):
        '''
        Purpose: In a given case, to retrieve the count of attachment
        :return: The count of attachment
        '''

        element = find_elements(self.app.driver,self.attachment_items)
        if len(element) > 0:
            log.info("'%s' Attachments are available in the given case" % len(element))
            return len(element)
        else:
            log.info("Attachments are not available in the given case")
            return 0

    def verify_availability_of_attachments(self):
        '''
        Purpose: To verify non-zero attachment exists in the given case
        :return: Nothing
        '''
        log.info("Checking if attachments are available")
        assert self.get_attachents_count() != 0, "Attachments are not available"

    def verify_download_button_available_for_attachments(self):
        '''
        Purpose: To verify that download button is available for each attachment in the case
        :return: Nothing
        '''

        log.info("Checking if download button is available for each attachment")
        element = find_elements(self.app.driver, self.attachment_download_button)
        num = len(element)

        assert self.get_attachents_count() == num, "All attachments don't have download button"
        log.info("All '%s' attachments have the download button." % num)

    def verify_delete_button_available_for_attachments(self):
        '''
        Purpose: To verify that delete button is available for each attachment in the case
        :return: Nothing
        '''

        log.info("Checking if delete button is available for each attachment")
        element = find_elements(self.app.driver, self.attachment_delete_button)
        num = len(element)

        assert self.get_attachents_count() == num, "All attachments don't have delete button"
        log.info("All '%s' attachments have the delete button." % num)

    def download_attachments(self,max_files=2):
        '''
        Purpose: This method is used download the
        :param max_files: Provides count for maximum files to download. Default value is 2.
        :return: Count of attachments downloaded
        '''
        element = find_elements(self.app.driver, self.attachment_download_button)
        section_element = find_elements(self.app.driver,self.attachment_body_section)
        if len(element) > 0 and len(section_element) > 0:
            # Limiting to download the files up to 2
            if max_files >= len(element):
                count = len(element)
            else:
                log.warning("Available files to download are more than 2")
                count = max_files
            log.info("Downloading %s attachments into project-download folder"% count)
            JS_tricks.element_to_the_middle(self.app.driver,section_element[0])
            time.sleep(0.5)
            JS_tricks.inner_scroll_to_elementoffset(self.app.driver,section_element[0])
            file_count = 0
            for num in range(count):
                wait_counter = 0
                JS_tricks.element_to_the_middle(self.app.driver,element[num])
                time.sleep(0.5)
                action_click(self.app.driver, element[num])
                time.sleep(1)
                # Logic to wait till file gets downloaded
                file_count = file_count + 1
                while wait_counter <= 60 and file_count != len(os.listdir(self.attachment_download_folder)):
                    wait_counter = wait_counter + 1
                    time.sleep(1)
                log.info(os.listdir(self.attachment_download_folder))
            return count
        else:
            log.error("Unable to access attachments for downloading")
            return 0

    def verify_downloaded_attachments_name(self,max_files=2,download_path=None):
        '''
        Purpose: This method is used to verify the downloaded attachment name is the same as the attachment
        :param max_files: Provides count for maximum files "to pick up attachment name" and "to download". Default value is 2.
        :return: the downloaded attachment name is the same as the attachment or not
        '''
        element = WebDriverWait(self.app.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, self.attachment_name_xpath)))
        expected_file_list=[]
        i=0
        if len(element) > 0:
             #limiting to pick up file name up to 2(by-default0)
            if max_files >= len(element):
                count = len(element)
            else:
                log.warning("Available files to download are more than 2")
                count = max_files
            log.info("picking up the %s attachment names from UI and storing it in expected_file_list" % count)
            for i in range(count):
                # pick up the attachment names from UI
                element = find_elements(self.app.driver, self.attachment_name_xpath)
                file_name=element[i].text or element[i].get_attribute("download")
                only_file_name = file_name.split(".")[0]
                print(only_file_name)
                expected_file_list.append(only_file_name)

        expected_file_list=sorted(expected_file_list)
        log.info("expected_file_list=" + str(expected_file_list))

        # downloading the attachments
        self.download_attachments(max_files)

        # pick up the file names from downloaded folder
        log.info("picking up the downloaded attachment names from download folder and storing it in actual_file_list" )
        path = self.attachment_download_folder
        # list = os.listdir(path)
        list=[]
        for root, dirs, files in os.walk(path):
            for name in files:
                log.info(os.path.splitext(name)[0])
                list.append((os.path.splitext(name)[0]))

        actual_file_list = sorted(list)
        log.info("actual_file_list"+str(actual_file_list))

        if actual_file_list == expected_file_list :
            log.info("downloaded file names '%s' are matching the expected file names '%s'" %(actual_file_list,expected_file_list))
            assert True,"downloaded file names '%s' are not matching the expected file names '%s'" %(actual_file_list,expected_file_list)
        else:
            log.error("downloaded file names '%s' are not matching the expected file names '%s'" % (actual_file_list, expected_file_list))
            assert False ,"downloaded file names '%s' are matching the expected file names '%s'" %(actual_file_list,expected_file_list)

        self.remove_all_downloaded_files(path=path)

    def remove_all_downloaded_files(self, path):
        '''
        Purpose: This method is used to remove all downloaded files after verification
        '''
        # After verification removing all downloaded files
        filelist = os.listdir(path)
        for f in filelist:
            os.remove(os.path.join(path, f))
        os.rmdir(path)
        log.info("Attachments are removed from downloaded location")

    def verify_attachments_got_downloaded(self,max_files=2,download_path=None):
        '''
        Purpose: This method is used to verify whether attachments are downloaded and then delete them.
        :param max_files: Provides count for maximum files to download and verify. Default value is 2.
        :param download_path: Path where files are downloaded. Default value is None.0
        :return: Nothing
        Note: We are creating one download folder within project directory and adding it in webdriver Browser option
        '''

        if download_path is None:
            path = self.attachment_download_folder
        else:
            path = download_path

        if not os.path.isdir(path):
            os.mkdir(path)

        # downloading the attachments
        count = self.download_attachments(max_files)

        if count != 0:
            #fetch count of files form directory
            actual_files_downloaded = len(os.listdir(path))

            assert actual_files_downloaded == count, "Files to be downloaded '%s' and actual downloaded '%s' mismatched." %(count,actual_files_downloaded)
            log.info("%s Attachments are downloaded successfully" % count)
        else:
            assert False, "Problem has occurred in downloading attachments."

        #After verification removing all downloaded files
        filelist = os.listdir(path)
        for f in filelist:
            os.remove(os.path.join(path, f))
        os.rmdir(path)
        log.info("Attachments are removed from downloaded location")


    def delete_attachements(self,attachment_delete_elements,confirmation='No'):
        '''
        Purpose: This method is used to delete the attachments based on provided confirmation
        :param attachmenet_element: Attachment item to be deleted. (It can be single or multiple)
        :param confirmation: Yes/No. Action to be performed on deleting the attachment
        :return:
        '''
        global button
        section_element = find_elements(self.app.driver, self.attachment_body_section)
        if str(confirmation).lower() == "no":
            button = "//div[@class='ant-popover ant-popover-placement-topRight']//div[@class='ant-popover-buttons']/button[span='No']"
        elif str(confirmation).lower() == "yes":
            button = "//div[@class='ant-popover ant-popover-placement-topRight']//div[@class='ant-popover-buttons']/button[span='Yes']"
        else:
            log.error("Invalid value to confirm deletion of attachment. Provide (Yes/No).")

        if len(attachment_delete_elements) > 0 and len(section_element) > 0:
            log.info("Deleting the attachments and selecting '%s' on confirmation" % confirmation)
            JS_tricks.element_to_the_middle(self.app.driver, section_element[0])
            time.sleep(0.5)
            JS_tricks.inner_scroll_to_elementoffset(self.app.driver, section_element[0])
            for element in attachment_delete_elements:
                JS_tricks.element_to_the_middle(self.app.driver, element)
                time.sleep(0.5)
                action_click(self.app.driver, element)
                time.sleep(1)
                button_element = get_element_after_wait(self.app.driver,locator=button,timeout=5)
                if button_element is not None:
                    action_click(self.app.driver, button_element)
                    log.info("Confirmation pop-up to delete attachment is provided")
                    time.sleep(0.5)
                else:
                    assert False, "Confirmation pop-up to delete attachment is not provided"


    def verify_deletion_of_all_attachments(self):
        '''

        :return:
        '''

        attachment_count_before = self.get_attachents_count()
        delete_elements = find_elements(self.app.driver,self.attachment_delete_button)

        # Verify attachments are not deleted from attachment component
        self.delete_attachements(delete_elements,"No")
        attachment_count_after = self.get_attachents_count()

        assert attachment_count_before == attachment_count_after, "Attachments count mismatched before %s and" \
                                                                  "after %s deleting attachments with confirmation 'No'" \
                                                                  % (attachment_count_before, attachment_count_after)
        log.info("Attachments count matched before and after deleting attachments with confirmation 'No'")

        # Verify attachments are deleted from attachment component
        self.delete_attachements(delete_elements, "Yes")
        self.app.driver.implicitly_wait(2)
        attachment_count_after = self.get_attachents_count()
        self.app.driver.implicitly_wait(20)
        assert attachment_count_after == 0, "Attachments count mismatched before %s and" \
                                                                  "after %s deleting attachments with confirmation 'Yes'" \
                                                                  % (attachment_count_before, attachment_count_after)
        log.info("Attachments count matched before and after deleting attachments with confirmation 'Yes'")

    def verify_carousel_is_open(self):
        '''
        Purpose - For certain attachments (such as image,pdf), on clicking them a carousel windows opens up for viewing the doc.
        :return: true or false
        '''

        element = get_element_after_wait(self.app.driver,self.carousel_view_for_attachment, timeout=10)
        if element is not None:
            log.info("Carousel view is opened for the attachment")
            close = find_elements(self.app.driver,self.carousel_close_button)
            if len(close) > 0 :
                ActionChains(self.app.driver).send_keys(Keys.ESCAPE).perform()
                log.info("Closing carousel view")
                time.sleep(0.5)
            return True
        else:
            log.info("Carousel view is not opened for the attachment")
            return False

    def click_on_attachment(self,attachment_element):
        '''
        Purpose - This method is use to click on the attachment
        :param attachment_element: List of attachments which needs to be clicked (It can be single or multiple)
        :return: Nothing
        '''
        section_element = find_elements(self.app.driver, self.attachment_body_section)
        JS_tricks.element_to_the_middle(self.app.driver, section_element[0])
        time.sleep(0.5)
        JS_tricks.inner_scroll_to_elementoffset(self.app.driver, section_element[0])
        if 'list' in type(attachment_element).__name__:
            if len(attachment_element) > 0 :
                for attachment in attachment_element:
                    JS_tricks.element_to_the_middle(self.app.driver, attachment)
                    time.sleep(0.5)
                    action_click(self.app.driver, attachment)
                    time.sleep(0.5)
                    log.info("Attachment is clicked")
        elif attachment_element is not None:
            JS_tricks.element_to_the_middle(self.app.driver, attachment_element)
            time.sleep(1)
            action_click(self.app.driver, attachment_element)
            time.sleep(1)
            log.info("Attachment is clicked")


    def check_whether_carousel_opens_on_clicking_attachment(self):

        locator_check_carousel = "//img[contains(@class,'image')]"
        attachments = find_elements(self.app.driver,self.attachment_items)
        if len(attachments) > 0:
            for num in range(len(attachments)):
                self.click_on_attachment(attachments[num])
                bln_carousel = self.verify_carousel_is_open()
                check_carousel = find_elements(attachments[num],locator_check_carousel)
                if len(check_carousel) > 0:
                    value = check_carousel[num].get_attribute('src')
                    log.info('value %s'%value)
                    if '.svg' in value:
                        if bln_carousel:
                            assert False,"Carousel should not be open for non-embedded doc"
                        elif not bln_carousel:
                            assert True
                    else:
                        if bln_carousel:
                            assert True
                        elif not bln_carousel:
                            assert False, "Carousel vuew is not opened for embedded doc"
                else:
                    log.error("Unable to check if doc is embedded or not")


    def verfify_files_are_not_downlaoded_after_clicking_on_file(self):

        path = self.attachment_download_folder
        attachment_count = self.get_attachents_count()
        log.info("Download path %s" %path)
        if not os.path.isdir(path):
            assert True
        elif os.path.isdir(path) and len(os.listdir(path)) == 0:
            assert True
        elif len(os.listdir(path)) == attachment_count:
            log.info(os.listdir(path))
            log.info(len(os.listdir(path)))
            assert False, "Attachments have got downloaded after clicking on attachment file"

    def check_presence_of_dark_mode_button(self):
        '''
        Purpose: To check the availability of dark mode button
        :return: True/False
        '''
        dark_button = find_elements(self.app.driver,self.dark_mode_button)
        if len(dark_button) > 0:
            return True
        else:
            return False

    def verify_dark_button_is_available(self):
        '''
        Purpose: To verify dark button is present
        :return: Nothing
        '''
        assert self.check_presence_of_dark_mode_button(),"Dark mode Button is not available on the page"
        log.info("Dark button to increase contrast is available")

    def verify_dark_button_is_not_available(self):
        '''
        Purpose: To verify dark button is not present
        :return: Nothing
        '''
        assert not self.check_presence_of_dark_mode_button(),"Dark mode Button is available on the page. But it should not be available."
        log.info("Dark button to increase contrast is not available as expected")

    def activate_dark_mode(self):
        '''
        Purpose: To activate the dark mode by clicking on dark mode button
        :return: Nothing
        '''
        dark_button = find_elements(self.app.driver, self.dark_mode_button)
        if len(dark_button) > 0:
            time.sleep(0.5)
            action_click(self.app.driver,dark_button[0])
            time.sleep(2)
        else:
            assert False, "Dark mode button is not available on page"
        self.verify_dark_mode_style_is_activated()

    def deactivate_dark_mode(self):
        '''
       Purpose: To deactivate the dark mode by clicking on dark mode button
       :return: Nothing
       '''
        # dark_button = find_elements(self.app.driver, self.dark_mode_button)
        dark_button = self.app.driver.find_element_by_id("dark-mode")
        if dark_button:
            self.app.driver.execute_script("arguments[0].click();", dark_button)
        else:
            assert False, "Dark mode button is not available on page"
        self.verify_dark_mode_style_is_deactivated()

    def check_dark_mode_style(self):
        '''
        Purpose: To check the dark mode style is applied
        :return: True/False
        '''
        element = find_elements(self.app.driver,self.style_on_dark_mode)
        if len(element) > 0:
            log.info(len(element))
            log.info(element[0].get_attribute('value'))
            return True

        else:
            return False

    def verify_dark_mode_style_is_activated(self):
        '''
       Purpose: To verify the dark mode style is activated.
       :return: Nothing
       '''
        assert self.check_dark_mode_style(),"Dark mode style is not available on the page"
        log.info("Dark mode style is activated")

    def verify_dark_mode_style_is_deactivated(self):
        '''
       Purpose: To verify the dark mode style is deactivated.
       :return: Nothing
       '''

        assert not self.check_dark_mode_style(),"Dark mode style is available on the page. But it should not be available."
        log.info("Dark mode style is deactivated")