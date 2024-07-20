import os
import platform
from enum import Enum, auto
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.ie.options import Options as IeOptions
from msedge.selenium_tools import EdgeOptions as EdgeOptions
from utilities.config._config import TEST_DATA_PATH

# enum Create for Driver
class BrowserType(Enum):
        CHROME  = auto()
        FIREFOX = auto()
        IE      = auto()
        
class ResultType(Enum):
        PASS = auto()
        FAIL = auto()
        
class IdentifierType(Enum):
        id = auto()
        name = auto()
        class_name = auto()
        css_selector = auto()
        xpath = auto()
        link_text = auto()
        spauto = auto()
        spautomation =auto()

class SelectType(Enum):
        _index =auto()
        _by_visible_text = auto()
        _by_value = auto()



def desired_capabilities_ie():
    """
    Description: This method this help user to add desired capabilities\n
    :return: _capabilities
    """

    ie_options = IeOptions()
    ie_options.ignore_protected_mode_settings = True
    ie_options.native_events = False
    ie_options.ensure_clean_session = True
    ie_options.requireWindowFocus = True
    ie_options.ignoreZoomSetting = True
    ie_options.introduceFlakinessByIgnoringProtectedModeSettings = True
    ie_options.set_capability('INTRODUCE_FLAKINESS_BY_IGNORING_SECURITY_DOMAINS',True)

    return ie_options

def desired_capabilities_chrome (input_options = None):
    """
    Description : This method help user to set Desired capabilities for CHROME,\n
    :return: Chrome_Options
    """
    # _chrome_options.add_argument("window-size=1920*1080")

    _chrome_options =ChromeOptions()
    if input_options.upper() == "HEADLESS" or platform.system() == "Linux" or platform.system() =="Darwin":
        if input_options.upper() == "HEADLESS":_chrome_options.add_argument('--headless')
        _chrome_options.add_argument('--no-sandbox')
        _chrome_options.add_argument('--disable-dev-shm-usage')
    elif platform.system() == "Windows" and input_options.upper() == "CHROME" :
        _chrome_options.add_argument("--start-maximized")
        _chrome_options.add_argument("--disable-extensions")
    else:
        raise Exception("Unable to added chrome option")

    _chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    _chrome_options.add_experimental_option("prefs", {'profile.default_content_setting_values.automatic_downloads': 1,
                                                      "download.default_directory": TEST_DATA_PATH,
                                                      "download.prompt_for_download": False,
                                                      "download.directory_upgrade": True,
                                                      "safebrowsing.enabled": True
                                                      })


    return _chrome_options

def desired_capabilities_edge (input_options=None):
    """
    Description : This method help user to set Desired capabilities for EDGE ,\n
    :return: edge_option
    """

    options = EdgeOptions()
    options.use_chromium = True
    return options


def check_element_property(element_property):
    """
    Description : This is internal method which help differentiates locator and key\n
    :param element_property: "locator identification__<property value>\n
    :return: list [locator, property value]
    """

    property_list = ((element_property).strip()).split('__')
    print(property_list)

    e_identification = property_list[0]
    e_property = '__'.join(property_list[1:]) #propertylist[1]
    element_property_list = {
        "ID": IdentifierType.id,
        "NAME": IdentifierType.name,
        "CSSSELECTOR": IdentifierType.css_selector,
        "XPATH": IdentifierType.xpath,
        "LINKTEXT": IdentifierType.link_text,
        "CLASSNAME": IdentifierType.class_name,
        "SP-AUTO" :IdentifierType.spauto,
        "SP-AUTOMATION":IdentifierType.spautomation
    }

    if e_identification.upper() in element_property_list.keys():
        identifier_type = element_property_list[e_identification.upper()]
        return  [identifier_type,e_property]
    else:
        print("Not present")
        raise Exception("Check element property")


def kill_ie_drivers():
    try:
        os.system("taskkill /F /IM iexplore.exe")
        os.system("taskkill /F /IM iexplore.exe*32")
        os.system("taskkill /F /IM IEDriverServer.exe")
        os.system("taskkill /F /IM IEDriverServer.exe*32")
    except:
        print("IE driver are not available in current session")

def kills_chrome_driver():
    try:
        os.system("taskkill /F /IM chromedriver.exe")
        os.system("taskkill /F /IM chromedriver.exe*")
    except:
        print("Chrome driver are not available in current session")



