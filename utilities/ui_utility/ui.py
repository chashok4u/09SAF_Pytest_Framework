import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from msedge.selenium_tools import Edge
from selenium.webdriver import Chrome
from utilities.ui_utility.TypeDeclaration import *
from utilities.file_handles.fileobjects import *
import utilities.report_utility.loggers as log
import utilities.config._config as config
from utilities.ui_utility.BrowserstackUtility import BrowserStack
import os

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager

listVal = []
status_check = ["TRUE", "PASS", "PASSED", "YES"]

browser_stack = BrowserStack()


class Browser:

    def __init__(self):
        pass

    def initialize_driver(self, browser_type):
        """
        Description: This method will created driver object for given browser type \n
        :param browser_type(string): This Parameter will contains the Browser type \n
                example :CHROME Or IE : BROWSER_TYPE="CHROME" or "IE" \n
        :return:
            this method will return driver
        Example:
            browser.initialize_driver("CHROME")
        """
        if browser_type.upper() == "CHROME" or browser_type.upper() == "HEADLESS":
            log.logger1.info(f"Browser : {browser_type.upper()}")
            _capabilities_chrome = desired_capabilities_chrome(browser_type.upper())

            if config.AutomationRunInfo.REMOTE_EXECUTION:
                log.logger1.info(
                    "Chrome Driver Path: REMOTE_EXECUTION : %s" % str(config.AutomationRunInfo.REMOTE_SERVER_URL))
                self.driver = webdriver.Remote(config.AutomationRunInfo.REMOTE_SERVER_URL,
                                               options=_capabilities_chrome)
            else:
                self.driver = Chrome(
                    executable_path=r"C:\Users\Ashok Kumar\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe",
                    options=_capabilities_chrome)
        elif browser_type.upper() == "IE":
            log.logger1.info("Browser : IE")
            _capabilities_ie = desired_capabilities_ie()
            if config.AutomationRunInfo.REMOTE_EXECUTION:
                log.logger1.info(
                    "IE Driver Path: as REMOTE_EXECUTION %s" % str(config.AutomationRunInfo.REMOTE_SERVER_URL))
                self.driver = webdriver.Remote(config.AutomationRunInfo.REMOTE_SERVER_URL,
                                               desired_capabilities=_capabilities_ie.to_capabilities())
            else:
                self.driver = webdriver.Ie(IEDriverManager().install(), options=_capabilities_ie)

        elif browser_type.upper() == "EDGE":
            _capabilities_edge_chromium_option = desired_capabilities_edge()
            log.logger1.info("Browser : EDGE")
            self.driver = Edge(EdgeChromiumDriverManager().install(),
                               options=_capabilities_edge_chromium_option)
        else:
            raise Exception("Please choose the browser type CHROME or IE or HEADLESS ")

        return self.driver

    def initialization_browser_go_to_app(self, browser_type, app_url):
        """
        Description: This method will navigate to selected browser along with provide URL. \n
        :param browser_type(string): This Parameter will contain the Browser type \n
                example :CHROME Or IE : BROWSER_TYPE="CHROME" or "IE" \n
        :param app_url(string):This Parameter will contain APPLICATION Url \n
                example: app_url\n
        :return:
            this method won't return but it will create driver as (self object)to use across the test script.\n
        Example:
            browser.initialization_browser_go_to_app("CHROME","https://www.google.com/")
        """
        self.initialize_driver(browser_type)
        self.define_size(config.OS_TYPE, browser_type)
        self.driver.delete_all_cookies()
        log.logger1.info(f"Current Window Size:.............")
        log.logger1.info(self.driver.get_window_size())

        self.go_to(app_url)
        self.add_step("Initial Application launch",
                      f"User should able to launch the application  \n {app_url} in {browser_type.upper()}", True)
        self._wait = WebDriverWait(self.driver, config.MAX_WAIT_TIME)
        log.logger1.info("MAX_WAIT_TIME element is %s" % config.MAX_WAIT_TIME)
        return self.driver

    def driver_wait(self, wait_time=config.MAX_WAIT_TIME):
        self._wait = WebDriverWait(self.driver, wait_time)

    def define_size(self, os_type, browser_type):
        """
        Description: This method help to set the windows size \n
        :param os_type: this parameter will contain the os type \n
        :param browser_type(string): This Parameter will contains the Browser type \n
                example :CHROME Or IE : BROWSER_TYPE="CHROME" or "IE" \n
        :return: None.\n
        """
        if os_type != 'Windows' or browser_type.upper() == "HEADLESS":
            log.logger1.info("Adding Browser Window Size to 1920*1080 - In Headless Mode")
            self.driver.set_window_size(1920, 1080)
        elif browser_type.upper() == "BROWSERSTACK":
            log.logger1.info("Maximize not allowed in BrowserStack")
        else:
            self.driver.maximize_window()

    def driver_object(self):
        """
        Description : This method help to getting driver object -to write Project custom methods\n
        :return: driver obj\n

        Example:
                driverObj =browser.driverObject()
        """
        if self.driver is not None:
            return self.driver
        else:
            log.logger1.warning("Make sure, Application browser chooses one of the CHROME/ IE/ HEADLESS")
            return None

    def go_to(self, app_url):
        """
        Description: This method will help to navigate other independent/dependent URL.\n
             can able to store all the urls independent of the platform and\n
            the same method can be used for all different environments and able to navigate based on URL\n
        :param app_url(string):This parameter contain the actual URL or independent/dependent URL.\n
                Based on user validation\n
        :return: None.\n

        Example:
                browser.go_to("https://www.google.com/")
        """

        try:
            self.driver.get(app_url)
            log.logger1.info("Application URL %s" % app_url)
        except Exception as e:
            log.logger1.error(f"Application URL {app_url} and error is {e}")

    def title(self):

        """
        Description: This method help to get title of the current browser\n
        :return: string- (Current page tile)\n

        Example:
                page_title = browser.title()\n
                print(page_title)
        """
        if self.driver is not None:
            return self.driver.title
        else:
            return "Driver Object Is none, Please re-execute script"

    def current_url(self):
        """
        Description : This method help to get the current browser URL
        Returns : current browser URL
        -------
        Examples:
            browser.current_url()
        """

        if self.driver is not None:
            return self.driver.current_url
        else:
            log.logger1.error("Driver Object is none, Please re-execute script")
            return None

    def find_element(self, in_element_property):
        """
        Description : This method used to find the element based given proper\n
        :param in_element_property(string): in_element_property: \n
        it contain the locator identification__(double underscore)propertyValue\n
            example: "xpath__//a[@id='Check_property']\n
        :return: element(obj)
        """
        _ele = None
        element_property_values = check_element_property(in_element_property)
        identifier_type = element_property_values[0]
        element_property = element_property_values[1]
        try:
            if identifier_type == IdentifierType.id:
                _ele = self._wait.until(EC.presence_of_element_located((By.ID, element_property)))
            elif identifier_type == IdentifierType.name:
                _ele = self._wait.until(EC.presence_of_element_located((By.NAME, element_property)))
            elif identifier_type == IdentifierType.link_text:
                _ele = self._wait.until(EC.presence_of_element_located((By.LINK_TEXT, element_property)))
            elif identifier_type == IdentifierType.class_name:
                _ele = self._wait.until(EC.presence_of_element_located((By.CLASS_NAME, element_property)))
            elif identifier_type == IdentifierType.css_selector:
                _ele = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element_property)))
            elif identifier_type == IdentifierType.xpath:
                self.driver.execute(Command.STATUS)
                _ele = self._wait.until(EC.presence_of_element_located((By.XPATH, element_property)))
            elif identifier_type == IdentifierType.spauto:
                # "//*[@sp-auto={element_property}]"
                # // *[ @ sp - auto = "5"]
                self.driver.execute(Command.STATUS)
                _ele = self._wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//*[@sp-auto='{element_property}']")))
            elif identifier_type == IdentifierType.spautomation:
                # "//*[@sp-auto={element_property}]"
                # // *[ @ sp - auto = "5"]
                self.driver.execute(Command.STATUS)
                _ele = self._wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//*[@sp-automation='{element_property}']")))
            else:
                log.logger1.error(
                    f"Please make use of Pre-define Keyword defined by utilities Libraries {in_element_property}")
            return _ele
        except Exception as e:
            log.logger1.error(f"Unable to find element {in_element_property} and exception message {e}")
            return None

    def _find_element(self, in_element_property):
        """
        Description : This method used to find the element based given proper\n
        :param in_element_property(string): in_element_property: \n
        it contain the locator identification__(double underscore)propertyValue\n
            example: "xpath__//a[@id='Check_property']\n
        :return: element(obj)
        """
        self._element = self.find_element(in_element_property)
        if self._element and self._element is not None:
            log.logger1.info(f"successfully verified the element : {in_element_property}")
        else:
            self.add_step("find the object", f"Object:find element {in_element_property} :", "FAIL")

        return self._element

    def find_elements(self, in_element_property):
        """
        Description : This method used to find the element based given proper\n
        :param in_element_property(string): in_element_property: \n
        it contain the locator identification__(double underscore)propertyValue\n
            example: "xpath__//a[@id='Check_property']\n
        :return: list of element
        """
        element_property_values = check_element_property(in_element_property)
        identifier_type = element_property_values[0]
        element_property = element_property_values[1]

        try:
            if identifier_type == IdentifierType.id:
                self._elements = self.driver.find_elements_by_id(element_property)
            elif identifier_type == IdentifierType.name:
                self._elements = self.driver.find_elements_by_name(element_property)
            elif identifier_type == IdentifierType.link_text:
                self._elements = self.driver.find_elements_by_link_text(element_property)
            elif identifier_type == IdentifierType.class_name:
                self._elements = self.driver.find_elements_by_class_name(element_property)
            elif identifier_type == IdentifierType.css_selector:
                self._elements = self.driver.find_elements_by_css_selector(element_property)
            elif identifier_type == IdentifierType.xpath:
                self.driver.execute(Command.STATUS)
                self._elements = self.driver.find_elements_by_xpath(element_property)
            else:
                log.logger1.error(
                    "In IF Case-Please use Pre defined Keyword by utilities Libraries. " + identifier_type)

            return self._elements
        except Exception as e:
            log.logger1.error(f"Please use Pre defined Keyword by utilities Libraries.{identifier_type} : {e}")
            self.add_step("Unable to find element",
                          "Unable to find element {} and exception message {}".format(in_element_property, e), "FAIL")
            return None

    def set_text_by_index(self, in_element_property, index_val, input_text, description, expected_result):
        """
        Description: This method is used to set/enter text list of edit box based on index value.\n
        :param in_element_property: in_element_property:it contain the locator identification__(double underscore)propertyValue\n
            example: "xpath__//a[@id='Check_property']\n
        :param index_val : Nth Element to identify in list of element\n
        :param input_text: inputs text or input value for edit/text box for given index.\n
        :param: description: (string) What is all about this step.\n
        :param: expected_result: (string) what is expected response or result.\n
        :return: None and it will add step to report automatically\n
        Example:
                browser.set_text_by_index(index_val,input_text,description,expected_result)
        """

        try:
            self.find_elements(in_element_property)
            self._element = self._elements[index_val]
            self._element.clear()
            time.sleep(1)
            self._element.send_keys(input_text)
            self.add_step(description, expected_result, "PASS")
            self._element = None
            return True
        except Exception as e:
            log.logger1.error("Unable to click element ", e)
            self.add_step(description, expected_result + str(e), "FAIL")
            return False

    def click_element_by_index(self, in_element_property, index_val, description, expected_result):
        """
        Description: This method is used to clicking element in list of element based on index value. \n
        :param: in_element_property :it contain the locator identification__(double underscore)propertyValue \n
                example: "xpath__//a[@id='Check_property']\n
        :param index_val: index number - example: 0,1,2\n
        :param description: Step description .\n
        :param expected_result: what is expected response or result.\n
        :return: None\n

        example:
            browser.click_element_by_index("xpath__//a[@id='Check_property'],1,"description","expected_result")
        """
        try:
            self.find_elements(in_element_property)
            self._element = self._elements[index_val]
            self._element.click()
            self.add_step(description, expected_result, "PASS")
            self._elements = None
            self._element = None
            return True
        except Exception as e:
            log.logger1.error("Unable to find element%s" % e)
            self.add_step(description, expected_result, "FAIL")
            return False

    def click_element(self, in_element_property, description, expected_result):
        """
        Description :
            This method will click on the element which is provided by user based input property.\n
            It will "find the element" for the element property. and check that element is present or not\n
            by calling internal utilities method "find_element" Once Element is found -It will click on that.\n

        :param:in_element_property(string): in_element_property:it contain the locator identification__(double underscore)propertyValue\n
            example: "xpath__//a[@id='Check_property']\n
        :param: description(string): What is all about this step.\n
        :param: expected_result(string): what is expected response or result.\n
        :return: None\n
        Example: 
            browser.click ("xpath__//*[@id='']","description","expected result")
        """

        try:
            self._find_element(in_element_property)
            if self._element is not None:
                self._element.click()
                self.add_step(description, expected_result, "PASS")
                self._element = None
                return True
            self.add_step(description, expected_result, "FAIL")
            return False
        except Exception as e:
            log.logger1.error("Unable to find element %s " % e)
            self.add_step(description, expected_result + str(e), "FAIL")
            return False

    def set_text(self, in_element_property, input_text, description, expected_result):
        """
        Description :
            This method will set input a element which is provided by user based input property.\n
            It will use "find the element" for the element property. and check that element is present or not\n
            by calling internal utilities method "find_element" Once Element is found -It will set input value to that.\n
        :param:in_element_property(string): in_element_property:it contain the  \n
        locator identification__(double underscore)propertyValue\n
            example: "xpath__//a[@id='Check_property']\n
        :param: description(string): What is all about this step.\n
        :param: expected_result(string): what is expected response or result.\n
        :return: None\n
        Example:
            browser.set_text("xpath__//*[@id='']","step description","expected result")
        """

        try:
            self._find_element(in_element_property)
            self._element.clear()
            self._element.send_keys(input_text)
            self.add_step(description, expected_result, "PASS")
            self._element = None
            return True
        except Exception as e:
            log.logger1.error("Unable to set element", e)
            self.add_step(description, expected_result, "FAIL")
            return False

    def clear_text(self, in_element_property):
        """
        Description: This method used to clear the text field.
        :param:in_element_property(string): in_element_property:it contain the  \n
        locator identification__(double underscore)propertyValue\n
        example: "xpath__//a[@id='Check_property']\n
        :return: True or False
        """
        try:
            self._find_element(in_element_property)
            self._element.clear()
            self._element = None
            return True
        except Exception as e:
            log.logger1.error("Unable to set element", e)
            self.add_step("clear_text", "unable to clear_text" + " : " + str(e), "FAIL")
            return False

    def switch_to_window(self, window_id=None):
        """
        Description: This method use to switch to another window in same browser \n
         (if only if we two browser opened )\n
        :param window_id : parent window id or None (if randomly)\n
        :return: parent window ID\n

        Example:
            browser.switch_to_window(window_id='idValue123455')\n
                or\n
            browser.switch_to_window() - and return parent or previous window id
        """
        if window_id is not None:
            self.driver.switch_to.window(window_id)
            return window_id
        else:
            current_window = self.current_window()
            all_windows = self.all_opened_windows()
            for window in all_windows:
                if window != current_window:
                    self.driver.switch_to.window(window)
                    return window

    def browser_info(self):
        """
        Description: This method help to get browser information like ID,title,URL\n
        :return: dictionary object having keys (url,title,window_id)\n
        Example:
           appInfo= browser.browser_info()\n
           print(appInfo)
        """
        _info = {}
        _info['url'] = self.driver.current_url
        _info['title'] = self.driver.title
        _info['window_id'] = self.driver.current_window_handle
        return _info

    def current_window(self):
        """
        Description : This method help to get current window information\n
        :return: Window ID\n

        Example: window_id = browser.current_window()\n
                 print(window_id)
        """
        return (self.driver.current_window_handle)

    def all_opened_windows(self):
        """
        Description : This help to find all the opened browser windows\n
        :return: list object : which contains all opened browser windows IDs\n
        Example:   all_windows =browser.all_opened_windows()\n
                    print(all_windows)
        """
        return (self.driver.window_handles)

    def close_all_browser_except_parent_browser(self, parent_window):
        """
        Description :this method help user to close all the existing browser except parent browser.\n
        :parameter: parent_window: id need to pass.\n
                    usage: Before running this, by using "current_window" get the parent window id.\n
        :return: None\n

        Example:
            browser.close_all_browser_except_parent_browser(parent_window="IdValue12345")
        """
        try:
            for child_window in self.driver.window_handles:
                if parent_window != child_window:
                    self.driver.switch_to.window(child_window)
                    self.driver.close()

            self.driver.switch_to.window(parent_window)
            log.logger1.info("Closing all browser except parent browser..")
        except Exception as e:
            log.logger1.info(e)
            self.add_step("close_all_browser_except_parent_browser",
                          "unable to close_all_browser_except_parent_browser" + " : " + str(e), "FAIL")
            return False

    def selection(self, in_element_property, select_type, input_parameter, description, expected_result):
        """
        Description: This method is used to clicking element in list of element based on index value.\n
        :parameter:
         in_element_property:it contain the locator identification__(double underscore)propertyValue\n
         example: "xpath__//a[@id='Check_property']\n
        :param select_type: Choosing option: BY_INDEX, BY_VALUE,BY_TEXT\n
        :param input_parameter: select_type input parameter\n
        :param description: step description\n
        :param expected_result: expected result for this particular step\n
        :return: None\n

        Example:
            browser.selection("xpath__//a[@id='']","ByIndex",1,"Step description","expected result")
        """

        try:
            self._find_element(in_element_property)
            if self._element != False:
                select = Select(self._element)
                if str(select_type).upper() in ["BY_VALUE", "BY_INDEX", "BY_TEXT"]:
                    if str(select_type).upper() == "BY_VALUE":
                        select.select_by_value(input_parameter)
                        self.add_step(description, expected_result, "PASS")
                        return True
                    elif str(select_type).upper() == "BY_INDEX":
                        select.select_by_index(input_parameter)
                        self.add_step(description, expected_result, "PASS")
                        return True
                    elif str(select_type).upper() == "BY_TEXT":
                        select.select_by_visible_text(input_parameter)
                        self.add_step(description, expected_result, "PASS")
                        return True
                    else:
                        return False
        except Exception as E:
            self.add_step(description, expected_result, "FAIL")
            log.logger1.error(E)
            return False

    def switch_to_frame(self, in_element_property):
        """
        Description :This method used to help to switch to I FRAME based on provided input"\n
        :param:in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
            example: "xpath__//a[@id='Check_property']\n

        :return: None\n
        Example:
            browser.switch_to_frame("xpath__//*[@title='iFrame'])
        """
        property_list = ((in_element_property).strip()).split('__')
        try:
            self.driver.switch_to.frame(property_list[1])
            return True
        except Exception as e:
            try:
                self.driver.switch_to.frame(int(property_list[1]))
                return True
            except Exception as e:
                log.logger1.error(e)
                self.add_step("switch_to_frame", "unable to switch_to_frame " + str(e), "FAIL")
                return False

    def switch_to_default(self):
        """
        Description: This method help to switch back to default content\n
        :return: None\n

        Example:
            browser.switch_to_default()\n
            usage: Moving back to main content after switch to iFrame
        """
        try:
            self.driver.switch_to.default_content()
            return True
        except Exception as e:
            self.driver.switch_to_default_content()
            print("Switch to default...")
            log.logger1.error(e)
            return False

    def add_step(self, description, expected_result, status):
        """
        Description : This method help to add step information explicit to report.\n
        :param description: Step description\n
        :param expected_result:  expected step out come\n
        :param status:  PASS/FAIL or True/False - True i.e pass  and False i.e Failed\n
        :return: None\n

        Example:
            browser.add_step("step info","expected result",True/False Or "PASS"/"FAIL")
        """
        sublist_addstep = [(description.lower()).capitalize(), (expected_result.lower()).capitalize()]
        actual_result = (expected_result.upper()).replace('SELECT', 'Selected')
        actual_result = (actual_result.upper()).replace('BE', '')

        sub_tst_step_info = {
            "Description": (description.lower()).capitalize(),
            "Expected_Result": (expected_result.lower()).capitalize(),
            "Actual_Result": (actual_result.lower()).capitalize(),
        }

        if str(status).upper() in ["TRUE", "PASS", "PASSED", "YES"]:
            actual_result = ((actual_result).upper()).replace('SHOULD', 'Successfully')
            sublist_addstep.append((actual_result.lower()).capitalize())
            sublist_addstep.append("PASS")
            sub_tst_step_info["Step_Status"] = "PASS"
        else:
            actual_result = ((actual_result).upper()).replace('SHOULD', 'Failed to ')
            sublist_addstep.append((actual_result.lower()).capitalize())
            sublist_addstep.append("FAIL")
            sub_tst_step_info["Step_Status"] = "FAIL"

        path_location = self.screenshot()
        sublist_addstep.append(path_location)
        sub_tst_step_info["Screenshot_Location"] = path_location
        listVal.append(sublist_addstep)

        data = pd.DataFrame(listVal)
        print("DATAFRAME", data)
        data.columns = ['Description', 'Expected Results', 'Actual Results', 'Status', 'Screenshot']
        name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        print("Testcase Name", name)
        log.logger1.info(sublist_addstep)

    def tear_down(self):
        """
        Description : This method help to quite the driver or close the driver instance\n
        :return: True or False
        """
        try:
            log.logger1.info("tear down the all existing browser and quite the driver..")
            self.driver.quit()
            log.logger1.info("Quite...........")
            self.driver = None
            return True
        except:
            return False

    def wait_till_element_appear(self, in_element_property):
        """
        Description: This method help user to wait till object appear\n
        :param:
             in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
        :return: None\n

        Example:
            browser.wait_till_element_appear("xpath__//*[@title="pyraft_button"])
        """
        try:
            ele = self.find_element(in_element_property)
            if ele:
                log.logger1.info(f"Able to find the element with in time period i.e .....{in_element_property}")
                return True
            else:
                log.logger1.error(f"Able to find the element with in time period i.e .....{in_element_property}")
                return False
        except Exception as e:
            log.logger1.error("*" * 80)
            log.logger1.error(e)
            log.logger1.error("In wait_till_element_appear method .....")
            log.logger1.error(f"Unable to find the element with in time period i.e .....{in_element_property}")
            log.logger1.error("*" * 80)
            return False

    def is_enabled(self, in_element_property):
        """
        Description: This method help to find the provided element is enable or disable\n
        :parameter:
             in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
        :return: True or False\n
        Example:
            browser.is_enabled("xpath__//button[@id="PyRAFT_checkbox"])
        """
        try:
            ele = self.find_element(in_element_property)
            if ele:
                if ele.is_enabled():
                    return True
                return False
            return False
        except Exception as e:
            log.logger1.info(e)
            return False

    def is_selected(self, in_element_property):
        """
        Description: This method help to find the provided element is selected or not.\n
        :param:
        in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
        example: "xpath__//a[@id='Check_property']\n
        :return: True or False\n
        Example:
            browser.is_selected("xpath__//*[@id="PyRAFT_checkbox"])
        """
        try:
            self._find_element(in_element_property)
            if self._element.is_selected():
                return True
            else:
                return False
        except Exception as e:
            log.logger1.info(e)
            return False

    def is_displayed(self, in_element_property):
        """
          Description : this method help user to verify particular object based on inputs property.\n
          :param:
            in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
               example: "xpath__//a[@id='Check_property']\n
           description:  step information\n
           expected_result: expected step output\n
          :return: True or False\n

          Example:
            browser.is_displayed("xpath__//*[@title='utilities'])
          """
        try:
            ele = self.find_element(in_element_property)
            if ele:
                if ele.is_displayed():
                    return True
                else:
                    return False
            return False
        except Exception as e:
            log.logger1.error("Error checking object..", e)
            return False

    def location_once_scrolled_into_view(self, in_element_property, description=None, expected_result=None):
        """
        Description: This method help user to scroll till particular object element based on input property only once \n
         and come back to normal.\n
        :param:
             in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
        :return: None\n
        Example:
            browser.location_once_scrolled_into_view("xpath__//button[@title="pyRAFT"],"step info","expected info")
        """
        try:
            self._find_element(in_element_property)
            self._element.location_once_scrolled_into_view()
            try:
                self.driver.execute_script("window.scrollTo(0, Y)")
                if description is not None: self.add_step(description, expected_result, "PASS")
                return True
            except:
                log.logger1.info("Element Scrolled not happen..")
                if description is not None and expected_result is not None:
                    self.add_step(description, expected_result, "FAIL")
                return False
        except Exception as e:
            log.logger1.error(e)
            log.logger1.info("Element Scrolled not happen..")
            return False

    def scroll_to_view(self, in_element_property, description, expected_result):
        """
        Description: This method help user to scroll till particular object element based on input property.\n
        :param:
             in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
        :return: True or False\n
        Example:
            browser.scrollIntoView("xpath__//button[@title="pyRAFT"],"step info","expected info")
        """
        try:
            self._find_element(in_element_property)
            self.driver.execute_script("arguments[0].scrollIntoView();", self._element)
            if description is not None and expected_result is not None:
                self.add_step(description, expected_result, "PASS")
            log.logger1.info("Element Scrolled.....")
            return True
        except Exception as e:
            log.logger1.error("Element Scrolled not happened..", e)
            if description is not None and expected_result is not None:
                self.add_step(description, expected_result, "FAIl")
            return False

    def enter(self, in_element_property):
        """
        Description: This method used to help to Perform ENTER at provided input\n
        :param  in_element_property(string):it contain the locator identification__(double underscore)propertyValue\n
        example: "xpath__//a[@id='Check_property']\n
        :return: True or False\n

        Example:
            browser.enter("xpath__//a[@id='Check_property'])
        """

        try:
            self._find_element(in_element_property)
            self._element.send_keys(Keys.ENTER)
            time.sleep(1)
            return True
        except Exception as e:
            log.logger1.info("Error:", e)
            try:
                self._element.send_keys(Keys.RETURN)
                return True
            except Exception as e:
                log.logger1.error("Send Keys - enter..")
                log.logger1.error(e)
                return False

    def press_enter(self):
        """
        Description : This method used to help on performing key board action "PRESS_ENTER"\n
        :return:  True or False\n
        Example:
            browser.press_enter()
        """
        try:
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)
            return True
        except Exception as e:
            try:
                ActionChains(self.driver).send_keys(Keys.RETURN).perform()
                return True
            except:
                log.logger1.error("Send Keys - Press enter..")
                log.logger1.error(e)
                return False

    def press_tab(self):
        """
        Description : This method used to help on performing key board action "PRESS_TAB"\n
        :return:  True or False \n
        Example:
            browser.press_tab()
        """
        try:
            ActionChains(self.driver).send_keys(Keys.TAB).perform()
            return True
        except Exception as e:
            log.logger1.error("Press tab method")
            log.logger1.error(e)
            return False

    def press_down_arrow(self):
        """
        Description : This method used to help on performing key board action "down_arrow"\n
        :return:  True or False\n
        Example:
            browser.press_down_arrow()
        """
        try:
            ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).perform()
            return True
        except Exception as e:
            log.logger1.error("Unable to perform press_down_arrow method")
            log.logger1.error(e)
            return False

    def press_up_arrow(self):
        """
        Description : This method used to help on performing key board action "up_arrow"\n
        :return:  True or False\n
        Example:
           browser.press_up_arrow()
        """
        try:
            ActionChains(self.driver).send_keys(Keys.ARROW_UP).perform()
        except Exception as e:
            log.logger1.error("Unable to perform up_arrow method")
            log.logger1.error(e)
            return False

    def press_right_arrow(self):
        """
        Description : This method used to help on performing key board action "right_arrow"\n
        :return:  True or False\n
        Example:
           browser.press_right_arrow()
        """
        try:
            ActionChains(self.driver).send_keys(Keys.ARROW_RIGHT).perform()
            return True
        except Exception as e:
            log.logger1.error("Unable to perform press_right_arrow ", e)
            return False

    def press_left_arrow(self):
        """
        Description : This method used to help on performing key board action "left_arrow"\n
        :return:  True or False\n
        Example:
           browser.press_left_arrow()
        """
        try:
            ActionChains(self.driver).send_keys(Keys.ARROW_LEFT).perform()
            return True
        except Exception as e:
            log.logger1.error("Unable to perform press_left_arrow", e)
            return False

    def press_space_bar(self):
        """
        Description : This method used to help on performing key board action "press space bar"\n
        :return:  True or False\n
        Example:
            browser.press_space_bar()
        """
        try:
            ActionChains(self.driver).send_keys(Keys.SPACE).perform()
            return True
        except Exception as e:
            log.logger1.error("Unable to perform, press space bar :", e)
            return False

    def press_escape(self):
        """
        Description : This method used to help on performing key board action "ESCAPE"\n
        :return:  True or False\n
        Example:
           browser.press_escape()
        """
        try:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            return True
        except Exception as e:
            log.logger1.error("Unable to perform, press_escape :", e)
            return False

    def space_bar(self, in_element_property):
        """
        Description: This method used to help to Perform SPACE BAR at provided input\n
        :param  in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
        example: "xpath__//a[@id='Check property']
        :return: True or False\n

        Example:
            browser.space_bar("xpath__//a[@id='Check property'])
        """
        try:
            self._find_element(in_element_property)
            self._element.send_keys(Keys.SPACE)
            return True
        except Exception as e:
            log.logger1.error("Error Send Keys -..", e)
            return False

    def up_arrow(self, in_element_property):
        """
        Description: This method used to help to Perform UP_ARROW at provided input\n
        :param  in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
        example: "xpath__//a[@id='Check_property']\n
        :return: True or False\n

        Example:
            browser.up_arrow("xpath__//a[@id='Check_property'])
        """
        try:
            self._find_element(in_element_property)
            self._element.send_keys(Keys.ARROW_UP)
            return True
        except Exception as e:
            log.logger1.error("Error Send Keys -..", e)
            return False

    def down_arrow(self, in_element_property):
        """
        Description: This method used to help to Perform down_arrow at provided input\n
        :param  in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
        example: "xpath__//a[@id='Check_property']\n
        :return: True or False\n

        Example:
            browser.down_arrow("xpath__//a[@id='Check property'])
        """
        try:
            self._find_element(in_element_property)
            self._element.send_keys(Keys.ARROW_DOWN)
            return True
        except Exception as e:
            log.logger1.error("Error Send Keys -..", e)
            return False

    def left_arrow(self, in_element_property):
        """
        Description: This method used to help to Perform left_arrow at provided input\n
        :param  in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
        example: "xpath__//a[@id='Check_property']\n
        :return: True or False\n

        Example:
                browser.left_arrow("xpath__//a[@id='Check_property'])
        """
        try:
            self._find_element(in_element_property)
            self._element.send_keys(Keys.ARROW_LEFT)
            return True
        except Exception as e:
            log.logger1.error("Error Send Keys -..", e)
            return False

    def right_arrow(self):

        """
        Description: This method used to help to Perform right_arrow at provided input\n
        :param  in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
        example: "xpath__//a[@id='Check_property']\n
        :return: True or False \n

        Example:
            browser.right_arrow("xpath__//a[@id='Check_property'])
        """

        try:
            self._element.send_keys(Keys.ARROW_RIGHT)
            return True
        except Exception as e:
            log.logger1.error("Error Send Keys -..", e)
            return False

    def tab(self, in_element_property):

        """
        Description: This method used to help to Perform Tab at provided input\n
        :param  in_element_property (string) : it contain the locator identification__(double underscore)propertyValue\n
                example: "xpath__//a[@id='Check_property']
        :return: True or False\n

            Example:
                browser.tab("xpath__//a[@id='Check_property'])
        """

        try:
            self._find_element(in_element_property)
            self._element.send_keys(Keys.TAB)
            return True
        except Exception as e:
            log.logger1.error("Error Send Keys -..", e)
            return False

    def double_click_element(self, in_element_property, description, expected_result):
        """
        Description: This method used to help double click on provided element\n

        :param in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
                example:"xpath__//a[@id='Check_property']\n
        :param description: Step description\n
        :param expected_result: expected result\n
        :return: True or False \n

        Example:
             browser.double_click_element("xpath__//*[@title='utilities'], "step info", "Expected outcome")
        """
        try:
            self._find_element(in_element_property)
            action_chains = ActionChains(self.driver)
            action_chains.double_click(self._element).perform()
            action_chains = None
            self.add_step(description, expected_result, "PASS")
            return True
        except:
            self.add_step(description, expected_result, "FAIL")
            log.logger1.error("Failed to Element Scrolled ..")
            return False

    def right_click_element(self, in_element_property):
        """
        Description: This method provides support for a right mouse click  \n
        :param in_element_property (string): contains the locator identification__(double underscore)propertyValue  \n
                example:"xpath__//a[@id='Check_property']   \n
        :return: True or False  \n

        Example:  browser.right_click_element('xpath__//a[text() = "Coronavirus"]')
        """
        try:
            element = self._find_element(in_element_property)
            action_chains = ActionChains(self.driver)
            action_chains.context_click(element).perform()
            return True
        except Exception as Ex:
            log.logger1.error("Failed to perform Right-Click " + str(Ex))
            return False

    def click_and_hold_element(self, in_element_property, description, expected_result):
        """
        Description: This method help user to click element and hold on desired element\n
        info:Holds down the left mouse button on an element.\n
        :parameter:
             in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
             description: what this step all about\n
             expected_result: expected result.\n
        :return: None-  (This method automatically add step to report.)\n

        Example:
             browser.click_nd_hold_element("xpath__//*[@title='utilities'], "step info", "Expected outcome")
        """
        try:
            _element = self._find_element(in_element_property)
            action_chains = ActionChains(self.driver)
            action_chains.click_and_hold(_element).perform()
            action_chains = None
            self.add_step(description, expected_result, "PASS")
        except:
            self.add_step(description, expected_result, "FAIL")
            log.logger1.error("Failed to 'Click and hold on element'")

    def _get_text(self, __element):
        """
        Description: This method used to get the text
        :param __element:
        """
        try:
            return self._element.text
        except Exception as e:
            log.logger1.error("Error while reading text..", e)

    def gettext(self, in_element_property):
        """
        Description: This method used to read the text\n
        :parameter:
          in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
        :return: string -Text value of that element\n

        Example:
            browser.gettext("xpath__//*[@title='utilities'])
        """
        try:
            self._find_element(in_element_property)
            element_text = self._get_text(self._element)
            return element_text
        except Exception as e:
            log.logger1.error(f"error while reading text..{e}")

    def refresh(self):
        """
        Description : This is help user to refer existing driver object\n
        :return: None\n
        Example:
                browser.refresh()
        """
        self.driver.refresh()
        log.logger1.info("browser refresh....")

    def screenshot(self):
        """
        Description : This method help user to take screen shot in runtime\n
        :return:  string -Screen shot path\n

        Example:
            screen_shot_path= browser.screen shot()\n
            print(screen_shot_path)
        """
        screen_shot_path = config.CURRENT_DIR_SNAPSHOTS + os.path.sep + str(
            datetime.now().strftime('%d_%m_%Y_%H_%M_%S')) + '.png'
        if config.OS_TYPE == "Linux":
            self.driver.get_screenshot_as_file(screen_shot_path)
        else:
            try:
                self.driver.save_screenshot(screen_shot_path)
            except:
                self.driver.get_screenshot_as_file(screen_shot_path)

        return screen_shot_path

    def get_table_data(self, in_element_property):
        """
        Description: This method help user to get table data for given element property.\n
        :parameter:
          in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
        :return: list -(Will contain all the table data)\n

        Example:
            browser.get_table_data("xpath_//*[@id="pYARFT_table_01"])
        """
        try:
            self._find_element(in_element_property)
            rows = self._element.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
            th_data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
                td_data = []
                for col in cols:
                    td_data.append(col.text)  # prints text from the element
                th_data.append(td_data)
            return th_data
        except Exception as e:
            log.logger1.error(e)

    def report_update(self, description, expected_result, report_flag, step_status):
        if None not in [description, expected_result] and report_flag:
            self.add_step(description, expected_result, step_status)

    def verifying_element(self, in_element_property):
        """
        Description: This method used to  verify element based given provided input element property\n
        :param:in_element_property(string): in_element_property:it contain the locator identification__(double underscore)propertyValue\n
            example: "xpath__//a[@id='Check_property']\n
        :return: True or False (boolean)\n

        Example:
            browser.verify_element('xpath__//*[@title="Sp global"]')

        """
        return self.verify(in_element_property, report_flag=False)

    def verify(self, in_element_property, description=None, expected_result=None, report_flag=True):
        """
        Description : this method help user to verify particular object based on inputs property.\n
        :parameter:
          in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
         description: about step\n
         expected_result: what is expected output\n
         report_flag : True /False
                if report_flag: True  : step will be updated to report
                   report_flag: False : step will be not updated to report
        :return: True or False\n

        Example:
            browser.verify("xpath__//*[@title="Pyraft"],"Verifying utilities link","PyRaft link should present in ui")
        """
        try:
            ele = self.find_element(in_element_property)
            if ele:
                self.report_update(description, expected_result, report_flag, "PASS")
                return True
            else:
                self.report_update(description, expected_result, report_flag, "FAIL")
                return False
        except Exception as e:
            self.report_update(description, expected_result, report_flag, "FAIL")
            log.logger1.error("element property with error", e)
            log.logger1.info("*" * 80)
            log.logger1.error(f"in_element_property : {in_element_property}")
            log.logger1.info("*" * 80)
            return False

    def _get_clear_browsing_button(self):
        """
        Description :
            Find the "CLEAR BROWSING BUTTON" on the Chrome settings page.
        """
        return self.driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')

    def in_clear_cache(self, timeout=60):
        """
        Description : this method help to clear all the cache files in CHROME Driver\n
         :return: None -This just method.
        """
        """Clear the cookies and cache for the ChromeDriver instance."""
        # navigate to the settings page
        self.driver.get('chrome://settings/clearBrowserData')
        # wait for the button to appear
        wait = WebDriverWait(self.driver, timeout)
        wait.until(self._get_clear_browsing_button())
        # click the button to clear the cache
        self._get_clear_browsing_button().click()
        # wait for the button to be gone before returning
        wait.until_not(self._get_clear_browsing_button())

    def clear_cache(self):
        """
        Description : this method help to clear all the cache files in CHROME Driver\n
         :return: None -This just method.
        """
        self.driver.get('chrome://settings/clearBrowserData')
        time.sleep(10)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3)  # send right combination
        actions.perform()
        time.sleep(2)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB * 4 + Keys.ENTER)  # confirm
        actions.perform()
        time.sleep(5)  # wait some time to finish
        # (self.driver()).close()

    def implicitly_wait(self, wait_time):
        """
        Description :this help user  to wait till certain based on i\n
        :parameter: wait time: (int) -No of second to wait to go next object\n
                    example: 20 (seconds)\n
        :return: None\n

        Example: browser.implicitly_wait(30)
        """
        self.driver.implicitly_wait(wait_time)

    def verify_title(self, input1):
        """
        Description : This method help user to verify tile\n
        :param:
            input1:(string) - input title which user have to verify\n
        :return: None -but it will add to step to reports\n

        Example: browser.verify_title("Title : utilities")
        """
        page_name = self.title()
        log.logger1.info("Page title {}.".format(page_name))

        if input1 == str(page_name):
            update_step("verifying title", "{} is verify with {}".format(input1, page_name),
                        "{} is verified successfully {}".format(input1, page_name), True)
        else:
            update_step("verifying title", "{} is verify with {}".format(input1, page_name),
                        "{} is unable to verified with {}".format(input1, page_name), False)

    def get_attribute_value(self, in_element_property, attribute):
        """
        Description:This method will return the  attribute value for the element by\n
        using the element property passed and then return the attribute value\n

        :param:
            in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
               example: "xpath__//a[@id='Check_property']\n
        :param
                attribute: by tag, td, properties of the particular element\n
        :return: string\n

        Example: browser.get_attribute_value("xpath__*//a[@title="utilities"],"name or title or text")
        """
        try:
            self._find_element(in_element_property)
            return self._element.get_attribute(attribute)
        except Exception as e:
            log.logger1.error("Error while reading attribute..", e)

    def click_table_data(self, in_element_property, value, description, expected_result):
        """
        Description :This method help to click on particular value in TABLE.\n
        :param in_element_property:\n
        :param value: value which need to click\n
        :return: True or False\n
        Example: browser.click_table_data("xpath__//*a[@title="pyraft"],"12345","step info","step expected result")
        """
        try:
            self._find_element(in_element_property)
            rows = self._element.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
            th_data = []
            checkflag = False
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 is col 2
                td_data = []
                for col in cols:
                    td_data.append(col.text)  # prints text from the element
                    tb_value = col.text.strip()
                    if tb_value == value:
                        row.click()
                        checkflag = True
                        break
                th_data.append(td_data)

            if checkflag:
                self.add_step(description, expected_result, "PASS")
            else:
                self.add_step(description, expected_result, "FAIL")
        except Exception as e:
            log.logger1.error("Unable to find table tag and table data..")
            log.logger1.error(e)

    def update_step(self, description, expected, actual, status, attachment=None):
        """
        Description : This method help to add step information explicit to report.\n
        :param description: Step description\n
        :param expected:  expected step out come\n
        :param actual:  actual result\n
        :param status:  True or False - True i.e pass  and False i.e Failed\n
        :param attachment: if any attachment path or None is by default.or use "Screen shot" method\n
        :return: None\n

        Example:
            browser.update_step("step info","expected result","actual result", True or false, "c:\Test\sample.xls")
        """
        sublist_addstep = [description, expected, actual]
        if str(status).upper() in status_check:
            sublist_addstep.append("PASS")
        else:
            sublist_addstep.append("FAIL")
        if attachment is None:
            sublist_addstep.append("")
        else:
            sublist_addstep.append(attachment)
        listVal.append(sublist_addstep)
        log.logger1.info(sublist_addstep)

    def element_is_checked(self, in_element_property):
        """
        Description :This method help to check the element is checked or not ?\n
        :param in_element_property:\n
        :param value: id of the table\n
        :return: True or False\n
        Example:
            browser.element_is_checked("id__check101")
        """
        try:
            self._find_element(in_element_property)
            if self._element.is_selected():
                return True
            return False
        except Exception as e:
            log.logger1.error(e)

    def alert_accept(self):
        """
        Description: This method help to accept alert pop window in browser\n
        :return: None\n
        Example:
            browser.alert_accept
        """
        try:
            Alert(self.driver).accept()
            return True
        except:
            try:
                alert = self._wait.until(EC.alert_is_present)
                alert.accept()
                return True
            except:
                try:
                    obj = self.driver.switch_to.alert
                    obj.accept()
                    return True
                except:
                    return False

    def alert_dismiss(self):
        """
        This method help to dismiss alert pop window in browser.\n
        :return:True or False\n
        Example:
            browser.alert_dismiss()
        """
        try:
            Alert(self.driver).dismiss()
            return True
        except:
            try:
                alert = self._wait.until(EC.alert_is_present)
                alert.dismiss()
                return True
            except:
                try:
                    obj = self.driver.switch_to.alert
                    obj.accept()
                    return True
                except:
                    return False

    def alert_sendtext(self, keys_to_send):
        """
        This method used to help to provide text to alert window in browser\n
        :param keys_to_send: "OK"\n
        :return: None\n
        browser.alert_sendtext()
        """
        Alert(self.driver).send_keys(keys_to_send)

    def alert_gettext(self):
        """
        Description: This method used to help on get text on alert window.\n
        :return: text\n
        browser.alert_gettext()
        """
        try:
            alert = self._wait.until(EC.alert_is_present)
            alert_text = alert.text
            return alert_text
        except:
            try:
                obj = self.driver.switch_to.alert
                return obj.text
            except:
                return False

    def mouse_over_element_and_click_under_over_element(self, in_element_property1, in_element_property2,
                                                        description, expected_result):
        """
        Description: This method used to help to move one property of element location to another element property location\n
        :param in_element_property1: for example like "Menu" -property"<Xpath or id or name or cssselector..>__<Property value>\n
        :param in_element_property2: for example  "Under menu option- file/open/save/".."<Xpath or id or name or cssselector..>__<Property value>\n
        :param description: About step info\n
        :param expected_result: expected results\n
        :return: None\n
            Example:
            browser.mouserOverElement_nd_clickOnUnderOveredElement("xpath__//*[@id=currentElement]","xpath_//*[@id="expectedMoveLocation"],"description","Expected result")
        """
        try:
            from_element = self._find_element(in_element_property1)
            _actions = ActionChains(self.driver)
            _actions.move_to_element(from_element)
            to_element = self._find_element(in_element_property2)
            _actions.click(to_element)
            _actions.perform()
            _actions = None
        except Exception as e:
            self.add_step(description, expected_result, "FAIL")
            log.logger1.error("drag_nd_drop....")
            log.logger1.error(e)

    def drag_and_drop_element_to_another_element(self, element_property_1, element_property_2, description,
                                                 expected_result):
        """
        Description : This method used to help to move one property of element location to another element property location\n
        info:Holds down the left mouse button on the source element,then moves to the target element and releases the mouse button.\n
        :param in_element_property1: for example "<Xpath or id or name or cssselector..>__<Property value>\n
        :param in_element_property2: for example "<Xpath or id or name or cssselector..>__<Property value>\n
        :param description: About step info\n
        :param expected_result: expected results\n
        :return: None\n

        Example:
            browser.drag_nd_drop_elementToAnotherElement("xpath__//*[@id=currentElement]","xpath_//*[@id="expectedMoveLocation"],"description","Expected result")
        """

        try:
            from_element = self._find_element(element_property_1)
            to_element = self._find_element(element_property_2)
            ActionChains(self.driver).drag_and_drop(from_element, to_element).perform()
            self.add_step(description, expected_result, "PASS")
        except Exception as e:
            self.add_step(description, expected_result, "FAIL")
            log.logger1.error("drag_nd_drop....")
            log.logger1.error(e)

    def drag_and_drop_by_xy_offset(self, in_element_property1, x_off_set, y_off_set, description, expected_result):
        """
        Description: This method used to help user to drag and drop element based on provided xy co-ordinates.\n
        info: Holds down the left mouse button on the source element,then moves to the target offset and releases the mouse button.\n
        :param in_element_property1: it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
        :param x_off_set: int for example: 10\n
        :param y_off_set:  int  for example: 89\n
        :param: description : step description\n
        :param : expected_result : expected outcome/result.\n
        :return: None\n

        Example: browser.drag_and_drop_by_XY_offSet("xpath__//a[@id='CheckProperty'],20,30,"step description","expected result")
        """
        try:
            _element = self._find_element(in_element_property1)
            _actions = ActionChains(self.driver)
            _actions.drag_and_drop_by_offset(_element, x_off_set, y_off_set)
            _actions.perform()
            _actions = None
            self.add_step(description, expected_result, "PASS")
        except Exception as e:
            self.add_step(description, expected_result, "FAIL")
            log.logger1.error("drag_and_drop_by_XY_offSet....")
            log.logger1.error(e)

    def mouse_over(self, in_element_property, description, expected_result):
        """
         Description : This method help user to mouse element till particular element.\n
        :param:
          in_element_property(string): it contain the locator identification__(double underscore)propertyValue\n
             example: "xpath__//a[@id='Check_property']\n
        :param: description : step description\n
        :param : expected_result : expected outcome/result.\n
        :return: None\n

        Example: browser.mouse_over("xpath__//a[@id='CheckProperty'],"step description","expected result")
        """
        try:
            _element = self._find_element(in_element_property)
            _actions = ActionChains(self.driver)
            _actions.move_to_element(_element).perform()
            self.add_step(description, expected_result, "PASS")
        except Exception as e:
            self.add_step(description, expected_result, "FAIL")
            log.logger1.error("mouse over method..")
            log.logger1.error(e)

    def page_end(self):
        """
        Description: This method help to go till page end.\n
        :return: None\n
        Example:
            browser.page_end()
        """
        len_of_page = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        return len_of_page

    def get_elements_values(self, in_element_property):
        """
        Description: This method is used to clicking element in list of element based on index value.\n
        :parameter:
         in_element_property:it contain the locator identification__(double underscore)propertyValue\n
         example: "xpath__//a[@id='Check_property']\n
         index: index number - example: 0,1,2\n
         description: What is the step all about.\n
         expected_result: what is expected response or result.\n
        :return: None
        """
        _find_elements = self.find_elements(in_element_property)
        list_in = []
        for element in range(len(_find_elements)):
            _element = _find_elements[element]
            list_in.append(_element.text)

        return list_in

    def click_element_by_javascript(self, in_element_property, description, expected_result):
        """
         Description : This method will click on the element which is provided by user based input property.\n
         :return: - None
        """
        try:
            _element = self._find_element(in_element_property)
            self.driver.execute_script("arguments[0].click();", _element)
            self.add_step(description, expected_result, "PASS")
            self._element = None
        except Exception as e:
            log.logger1.error("Unable to find element %s" % e)
            self.add_step(description, expected_result, "FAIL")

    def internal_file_check(self, file_path, seconds=None):
        """
        Description: This method will help you check file whether it is exist in provided location are not with in 120 seconds
        :param downloaded_path: c:\\downloads\\sample.xls
        :return: True/False
        """
        file_status = False
        n = 60
        if seconds is not None: n = int(seconds)

        if file_path is not None:
            while n > 0:
                if os.path.exists(file_path):
                    log.logger1.info("File exists..")
                    update_step(f"Verifying Downloaded file ",
                                "file should  available  in downloaded location ",
                                f"successfully verified downloaded file at: {file_path}.", True)
                    file_status = True
                    break
                else:
                    n -= 1
                    log.logger1.info("Waiting for Excel to download...")
                    time.sleep(2)

        if file_status is not True:
            log.logger1.info("No file founded...")
            update_step(f"Verifying downloaded file path", "file should  available  in desire location ",
                        f"Failed to verified downloaded file {file_path}.", False)
            return False
        else:
            return True

    def internal_file_delete(self, file_path):
        """
        Description.This method used to delete file
        :param file_path:  c:\\download\\sample.xls
        :return: True/False
        """
        try:
            if delete_file(file_path):
                update_step(f"Delete the file from system",
                            "User should able to file the location ",
                            f"successfully delete from : {file_path}.", True)
                return True
            else:
                update_step(f"Delete existing file from system", "User should able to delete file ",
                            f"Failed to delete {file_path}.", False)
                return False
        except Exception as e:
            log.logger1.error(e)
            return False

    def get_system_user_name(self):
        """
        Description:This method used to get the current system user name
        :return: str: System User name example : Test
        """
        return str(config.SYSTEM_USER_NAME)

    def go_back_to_page(self, description=None, expected_result=None):
        """
        Description: This method used to go back to previous page of browser
        :return: True/False
        """
        try:
            self.driver.back()
            if description is not None and expected_result is not None:
                self.add_step(description, expected_result, "PASS")
            return True
        except Exception as e:
            log.logger1.error("Unable to go back screen %s" % e)
            if description is not None and expected_result is not None:
                self.add_step(description, expected_result, "FAIL")
            return False

    def go_forward_to_page(self, description=None, expected_result=None):
        """
         Description: This method used to go forward to next page of browser
         :return: True/False
         """
        try:
            self.driver.forward()
            if description is not None and expected_result is not None:
                self.add_step(description, expected_result, "PASS")
            return True
        except Exception as e:
            log.logger1.error("Unable to forward page screen %s" % e)
            if description is not None and expected_result is not None:
                self.add_step(description, expected_result, "FAIL")
            return False

    def _process_browser_log_entry(self, entry):
        response = json.loads(entry['message'])['message']
        return response

    def get_network_response(self):
        """
        Description :This Method will help you to get browser network logs current browser window
        :return: events (networks logs in list format)
        """
        try:
            browser_log = self.driver.get_log('performance')
            events = [self._process_browser_log_entry(entry) for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]
            return events
        except Exception as e:
            log.logger1.warning("Unable to get the network logs and check the driver object")
            log.logger1.error("Unable to get_network_logs  %s" % e)

    def close_all_ie_drivers(self):
        """
        Description :This Method will help you to close all IE drivers
        :return: None
        """
        kill_ie_drivers()

    def close_all_chrome_drivers(self):
        """
        Description :This Method will help you to close all chrome drivers
        :return: None
        """
        kills_chrome_driver()

    def open_new_tab(self):
        """
        Description : This method helps to open a new tab in the current browser
        :return: new window object
        """
        return self.driver.execute_script("window.open()")


class Assertion():
    def is_equal(self, input1, input2, description):
        """
        Description : This method help to assert equal condition\n
        :param input1: string1\n
        :param input2:  string 2\n
        :param description: Description/step info\n
        :return: True or False
        """
        if input1 == input2:
            update_step(description, "{} is verify with {}".format(input1, input2),
                        "{} is verified successfully {}".format(input1, input2), True)
            return True
        else:
            update_step(description, "{} is verify with {}".format(input1, input2),
                        "{} is unable to verified with {}".format(input1, input2), False)
            return False


def update_step(description, expected, actual, status, attachment=None):
    """
    Description: This method help to add step to information to report\n
    :param description: What this step all about\n
    :param expected: what expected description of current step\n
    :param actual:  actual description\n
    :param status: True or False\n
    :param attachment: If any path available (to attach any csv or excel or any files)\n
    :return: None\n
    for the attachment, Use browser.screenshot() -if wanted to take browser screen shot!\n
    Example:
    update_step("Step info","Expected step result","Actual step result" ,True/False or PASS/FAIL,"c:\\Test\\check.png")
    """

    sublist_addstep = []
    sublist_addstep.append(description)
    sublist_addstep.append(expected)
    sublist_addstep.append(actual)
    if str(status).upper() in status_check:
        sublist_addstep.append("PASS")
    else:
        sublist_addstep.append("FAIL")
    sublist_addstep.append(attachment)
    listVal.append(sublist_addstep)

    data = pd.DataFrame(listVal)
    print("DATAFRAME", data)
    data.columns = ['Description', 'Expected Results', 'Actual Results', 'Status', 'Screenshot']
    name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    print("Testcase Name", name)

    sublist_addstep = None


def add_step(description, expected, actual, status, attachment=None):
    """
     Description :This is independent method.Used to update report - \n
    :param description: for example, Step info (description) \n
    :param expected: for example, Step expected results or Outcome\n
    :param actual:  for example, Step actual results or Outcome \n
    :param status:  True or False or YES Or NO \n
    :return: None\n
    Example:
            add_step("Step info","Expected step result","Actual step result" ,True/False or PASS/FAIL)
    """
    update_step(description, expected, actual, str(status), attachment)
