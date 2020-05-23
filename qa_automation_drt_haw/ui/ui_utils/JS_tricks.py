

def element_to_the_middle(driver,element):
    """
    adjust screen position to show the element in the middle
    """
    current_screen_height = driver.get_window_size()['height']
    element_y_axis_position = element.location['y']
    pxs = int(element_y_axis_position - current_screen_height / 2)

    driver.execute_script('document.body.scrollTop = document.documentElement.scrollTop = 0;')
    driver.execute_script("scroll(0, %s)" % pxs)


def mouse_click_element(driver,element):
    """
    JS implementation of mouse click event
    """
    java_script = "var evObj = document.createEvent('MouseEvents');\n" \
                  "evObj.initMouseEvent(\"click\",true, true, window," \
                  " 0, 0, 0, 80, 20, false, false, false, false, 0, null);\n" \
                  "arguments[0].dispatchEvent(evObj);"
    driver.execute_script(java_script, element)


def inner_scroll_to_element(driver, element, inside_element=None):
    """
    scroll within container
    """
    driver.execute_script("arguments[0].scrollTop = arguments[1];", element, inside_element)

def inner_scroll_to_elementoffset(driver, element, offset=150):
    driver.execute_script("arguments[0].scrollTop = arguments[1]+150;", element, offset)

def mouse_over_element(driver,element):
    """
    JS implementation of mouse over element event
    """
    java_script = "var evObj = document.createEvent('MouseEvents');\n" \
                  "evObj.initMouseEvent(\"mouseover\",true, false, window," \
                  " 0, 0, 0, 0, 0, false, false, false, false, 0, null);\n" \
                  "arguments[0].dispatchEvent(evObj);"
    driver.execute_script(java_script, element)



