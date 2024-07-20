from app_test.pageobjects.api.api_env_switch import env_app_url, default_env
from app_test.config._test_config import browser
from app_test.config._app_config import AppConfig
import time


class application_common_methods:

    def navigate_url(self, env, url=None):
        """
        Description: This method is for Navigates to  URL
        param: URL of the Application
        return: None
        """

        if env is None or env == 'default name': env = default_env
        env = env.upper()
        ui_url = env_app_url(env)
        try:
            if url:
                browser.initialization_browser_go_to_app(AppConfig.BROWSER_TYPE, url)
            else:
                browser.initialization_browser_go_to_app(AppConfig.BROWSER_TYPE, ui_url)
        except Exception as Ex:
            browser.update_step("Connect to URL", "User unable to navigate to URL",
                                "URL has not Connected" + str(Ex), False)

    def select_dropdown_list(self, dropdown_locator, dropdown_data_locator, dropdown_data):
        """
        Description: This method helps to Select the Value From Dropdown List
        return: None
        Param: dropdown_locator, dropdown_data_locator, dropdown_data
        """
        time.sleep(5)
        browser.click_element(dropdown_locator, "Clicks on Dropdown Link",
                              "User Should be able to see the Dropdown Values")
        time.sleep(2)
        dropdown_values = browser.find_elements(dropdown_data_locator)
        if len(dropdown_values) > 0:
            for value in dropdown_values:
                if value.text == dropdown_data:
                    time.sleep(4)
                    value.click()
                    browser.add_step("Select Dropdown Value",
                                     "User Should select the dropdown value as :" + str(dropdown_data), True)
                    break
        else:
            browser.add_step("Verify the Dropdown Values",
                             "Dropdown Values didn't Loaded", False)

    def select_multi_value_dropdown(self, dropdown_locator, dropdown_data_locator, dropdown_data):
        """
        Description: This method helps to multi Select the Value From Dropdown List
        return: None
        Param: dropdown_locator, dropdown_data_locator, dropdown_data
        """
        time.sleep(5)
        browser.click_element(dropdown_locator, "Clicks on Dropdown Link",
                              "User Should be able to see the Dropdown Values")
        dropdown_values = browser.find_elements(dropdown_data_locator)
        if len(dropdown_values) > 0:
            count = 0
            for data in dropdown_values:
                if data.text in dropdown_data:
                    time.sleep(3)
                    data.click()
                    count = count + 1
                    if count == 3:
                        break

    def verify_dropdown_list(self, dropdown_locator, dropdown_data_locator, dropdown_data):
        """
        Description: This method helps to Select the Value From Dropdown List
        return: None
        Param: dropdown_locator, dropdown_data_locator, dropdown_data
        """

        browser.click_element(dropdown_locator, "Clicks on Dropdown Link",
                              "User Should be able to see the Dropdown Values")
        time.sleep(5)
        data = []
        dropdown_values = browser.find_elements(dropdown_data_locator)
        if len(dropdown_values) > 0:
            for value in dropdown_values:
                data.append(value.text)
                print("COUNTRY", data)
                if not (value.text in dropdown_data):
                    browser.add_step("Verify Dropdown Data", "The Value Doesn't Exists in Dropdown: " + str(value.text),
                                     False)
                else:
                    browser.add_step("Verify Dropdown Data", "The Value Should be Matched: " + str(value.text), True)

        else:
            browser.add_step("Verify the Dropdown Values",
                             "Dropdown Values didn't Loaded", False)

    def select_dropdown_option(self, dropdown_locator, value):
        """
        Description: This method helps to Select the Value from select Dropdown option
        Param: Dropdown Locator and Dropdown Values
        return: None
        """
        select_values = browser.find_elements(dropdown_locator)
        options = [x for x in select_values.find_elements_by_tag_name("select")]
        for ele in options:
            if ele.text == value:
                ele.click()
                browser.add_step("Select Dropdown Value",
                                 "User Should be able to Select the Dropdown Value as: " + str(value), True)
            else:
                browser.add_step("Select Dropdown Value",
                                 "User Unable to Select the Dropdown Values as : " + str(value), False)

    def verify_dropdown_data(self, dropdown_locator, values):
        """
        Description: This method helps to verify the Dropdown Data
        Param: Dropdown Locator and Dropdown values
        return: None
        """
        select_values = browser.find_element(dropdown_locator)
        options = [x for x in select_values.find_elements_by_tag_name("option")]
        for ele in options:
            if not (ele.text in values):
                browser.add_step("Verify Dropdown Data", "The Value Doesn't Exists in Dropdown" + str(ele.text), False)
            else:
                browser.add_step("Verify Dropdown Data", "The Value Should be Matched" + str(ele.text), True)

    def select_all_checkboxes(self, checkbox_locator):
        """
        Description: This method helps to Select All Checkboxes
        return: None
        Param: checkbox_locator
        """
        checkboxes = browser.find_elements(checkbox_locator)
        if len(checkboxes) > 0:
            for checkbox in checkboxes:
                if not checkbox.is_selected():
                    checkbox.click()
                    browser.add_step("Select All Checkboxes", "User Should select all the Checkboxes", True)
                else:
                    browser.add_step("Select All Checkboxes", "Checkboxes has already selected", True)
        else:
            browser.add_step("Verify the Checkboxes",
                             "Checkboxes didn't Loaded", False)

    def verify_headers(self, in_element_property, data):
        """
        Description: This method helps to verify the Headers
        Param: Locators of the headers and Data
        return: param
        """
        headers = browser.find_elements(in_element_property)
        if len(headers) > 0:
            for ele in headers:
                value = ele.text
                value = value.strip()
                if not (value in data):
                    browser.add_step("Verify Data", "The Value Doesn't Exists" + str(value), False)
                else:
                    browser.add_step("Verify Data", "The Value Should be Match" + str(value), True)

    def verify_data(self, in_element_property, data_list):
        """
        Description: This method helps to verify the Data
        return: None
        Param: in_element_property, data_list
        """

        header = browser.find_elements(in_element_property)
        data_set = []
        if len(header) > 0:
            for data in header:
                value = data.get_attribute('textContent')
                value = value.strip()
                data_set.append(value)
                if value in data_list:
                    browser.add_step("Verify Data", "The Value Should be Match" + str(value), True)
        else:
            browser.add_step("Verify Data", "Values didn't loaded", False)

    def get_table_data(self, in_element_link_property):
        """
            Description: This method is used to get the UI table data
            :param: in_element_property: Object identifier; for the table grid
            :return: df_data; Data Frame
        """
        table_data = []
        table_values = browser.find_elements(in_element_link_property)
        if len(table_values) > 0:
            for value in table_values:
                data = value.get_attribute('textContent')
                table_data.append(data)
                table_data = list(map(str.strip, table_data))
        return table_data

    def select_accordions(self, acordian_locator, acordian_data):
        """
        Description: This method helps to Select All Checkboxes
        return: None
        Param: checkbox_locator
        """
        acordians = browser.find_elements(acordian_locator)
        if len(acordians) > 0:
            for tab in acordians:
                if tab.text == acordian_data:
                    tab.click()
                    browser.add_step("Select The Accordions", "User Should select the Accordions" + str(tab.text), True)
                    break
        else:
            browser.add_step("Verify the Accordions",
                             "Accordions didn't Loaded", False)

    def verify_page_title(self, in_element_property, value):
        """
        Description: This method helps to verify the Page Title
        Param: Page Title
        return: title
        """
        if browser.is_displayed(in_element_property):
            title = browser.gettext(in_element_property)
            if title == value:
                browser.add_step("Verify Page Title", "Page Title Should be Match: " + str(value), True)
            else:
                browser.add_step("Verify Page Title", "Page Title Didn't Matched: " + str(value), False)
            return title

    def get_dropdown_data(self, dropdown_locator, dropdown_data_locator):
        """
        Description: This method helps to Select the Value From Dropdown List
        return: None
        Param: dropdown_locator, dropdown_data_locator, dropdown_data
        """

        browser.click_element(dropdown_locator, "Clicks on Dropdown Link",
                              "User Should be able to see the Dropdown Values")
        time.sleep(5)
        data = []
        dropdown_values = browser.find_elements(dropdown_data_locator)
        if len(dropdown_values) > 0:
            for value in dropdown_values:
                data.append(value.text)
            return data
        else:
            browser.add_step("Verify the Dropdown Values",
                             "Dropdown Values didn't Loaded", False)

    def select_mega_menu(self, tab, subtab=None):
        """
        Description: Select tab from the Mega Menu
        :parameter:
                   tab: (string) - input tab name (i.e. 'Menu')
                   sabtab: (string) - input subtab name (i.e. 'Sub-Menu')
        :return: None
        """
        time.sleep(5)
        selected_tab = "XPATH__//strong[text()='"+tab+"']/../parent::a"
        browser.click_element(selected_tab, "click on menu: " + str(tab), "tab should be selected")
        if subtab:
            selected_subtab = "XPATH__//a[contains(text(), '{0}')]".format(subtab)
            browser.wait_till_element_appear(selected_subtab)
            browser.click_element(selected_subtab, "click on sub-menu: " + str(subtab), "tab should be selected")

    def switching_windows(self):
        """Description: This method is used to switch between multiple windows
        :parameter: mainwindow is parent window
        :return: Child Url"""
        try:
            mainwindow = browser.driver.window_handles[0]
            parent_url = browser.driver.current_url
            windows = browser.driver.window_handles
            for handle in windows:
                browser.driver.switch_to.window(handle)
                child_url = browser.driver.current_url
                if parent_url != child_url:
                    browser.update_step("verify switching of windows", "Switch windows should be displayed",
                                        "Switch windows is displayed", True)
                    browser.driver.close()
            browser.driver.switch_to.window(mainwindow)
            return child_url
        except Exception as Ex:
            browser.update_step("verify switching of windows doesn't displyed", "Switch windows should  be dispalyed",
                                "Switch windows is not dispalyed" + str(Ex), False)
            return False

    def switch_to_child_window(self, handle_id):
        """Description: This method is used to switch to child window
        :parameter: mainwindow is parent window
        :return: Child Url"""
        try:
            childwindow = browser.driver.window_handles[handle_id]
            browser.driver.switch_to.window(childwindow)
            browser.update_step("verify switching of windows displayed", "Switch windows should  be dispalayed",
                                "Switch windows is completed", True)
        except Exception as Ex:
            browser.update_step("verify switching of windows doesn't displyed", "Switch windows should  be dispalyed",
                                "Switch windows is not dispalyed" + str(Ex), False)