import utilities.config._config as config

class BrowserStack():

    def config_browserstack(self, device=None, landscape_orientation=None):
        """
            Description: This method sets up the mobile device with required capabilities
            :param device: This parameter contains the device name on which we want to test browserstcak.\
            :param landscape_orientation: Landscape Orientation(YES/NO) value.\n
            :return:   This method retunr the brwoserstack configuration.
            """
        config_bs = {"real_mobile": "true", "build": "R360-browserstack", "browserName": "iPhone",
                      "browserstack.local": "true", "name": "BrowserStack-[Python] Demo", "nativeWebTap": "true",
                      "os_version": "13",
                      "device": device}

        if landscape_orientation.upper() == "YES":
            config_bs["deviceOrientation"] = "landscape"
        if device == "iPhone 6":
            config_bs["os_version"] = "11"
            config_bs["browserstack.appium_version"] = "1.16.0"
        if device == "iPhone 7":
            config_bs["os_version"] = "12"
            config_bs["browserstack.appium_version"] = "1.16.0"
        if device == "iPad Pro 11 2020":
            config_bs["os_version"] = "13"
            config_bs["browserstack.appium_version"] = "1.17.0"
        if device == "iPad Pro 12.9 2020":
            config_bs["os_version"] = "13"
            config_bs["browserstack.appium_version"] = "1.17.0"
        if device == "Google Nexus 6":
            config_bs["os_version"] = "6.0"
            config_bs["browserstack.appium_version"] = "1.6.5"
        if device == "iPhone 8":
            config_bs["os_version"] = "13"
            config_bs["browserstack.appium_version"] = "1.17.0"
        if device == "iPhone XS":
            config_bs["os_version"] = "13"
            config_bs["browserstack.appium_version"] = "1.17.0"
        if device == "Samsung Galaxy Note 10":
            config_bs["os_version"] = "9.0"
            config_bs["browserstack.appium_version"] = "1.17.0"
        return config_bs

    def browser_stack_url(self):
        """
        Description: This method use to create browser stack url.\n
        :return: browser stack url
        """
        browser_stack_url = 'https://'+config.BROWSERSTACK_USERNAME+':'+config.BROWSERSTACK_KEY+'@hub-cloud.browserstack.com/wd/hub'
        return browser_stack_url 
    