from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
from selenium.webdriver import ActionChains


def react_loadmask(driver):
    if driver.find_elements_by_id('__react-redux-loadmask__'):
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.ID, '__react-redux-loadmask__')))


def find_element(driver, value, mode=By.XPATH):
    return driver.find_element(mode, value)


def find_elements(driver, value, mode=By.XPATH):
    return driver.find_elements(mode, value)

def go_to_page(driver, value):
    driver.get(value)

def get_current_url(driver):
    '''
    Purpose: To fetch the url of current web page
    :param driver: Webdriver
    :return: url of current web page
    '''
    return driver.current_url

def get_element_after_wait(driver, locator, mode=By.XPATH,timeout=10, pollFrequency=0.5):
    element = None
    try:
        wait = WebDriverWait(driver, timeout, poll_frequency=pollFrequency,
                             ignored_exceptions=[NoSuchElementException,
                                                 ElementNotVisibleException,
                                                 ElementNotSelectableException])
        element = wait.until(EC.element_to_be_clickable((mode,locator)))
        print("Element appeared on the web page")
    except:
        print("Element not appeared on the web page")
    return element

def get_element_list_after_wait(driver, locator, mode=By.XPATH,timeout=10, pollFrequency=0.5):
    wait_counter = 0
    elements = driver.find_elements(mode,locator)
    while len(elements) <= 0 and wait_counter < timeout:
        time.sleep(pollFrequency)
        elements = driver.find_elements(mode, locator)
    assert len(elements) > 0, "Required element list is not found"
    return elements

def action_click(driver,element):
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(0.5)
