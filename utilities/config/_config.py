"""
    This CONFIGURATION SETUP for the entire solution.

     Logger i having creating directory for as per user info in run time
     will create folder at user system with tool name.
     and also it's has couple of other folder like(log_files,results_file,input_files,report_files)

     *LOGS- will store logger file for each execution with current timestamp
     *INPUTS- Will store execution summary/report_utility.
     *REPORT -will store run time inputs for any comparision by tool.Add test
"""

import os
import getpass
import socket
from datetime import datetime
import json
import platform
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.info("utilities: Automation Engine....")
import pyfiglet
pyfiglet.print_figlet(text="    P Y R A F T   ")

from app_test.config._app_config import AppConfig as AppConfig
from utilities.config._config_setup_utilities import *

SYSTEM_USER_NAME = getpass.getuser()
SYSTEM_NAME = socket.gethostname()
try: 
    IPAddr = socket.gethostbyname(SYSTEM_NAME)
except :
    IPAddr = socket.getfqdn(SYSTEM_NAME)
OS_TYPE = platform.system()


CURRENT_TIME_STAMP = (datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
logger.info(f"CURRENT_TIME_STAMP:{CURRENT_TIME_STAMP}")
APPNAME = AppConfig.APP_NAME
MAX_WAIT_TIME = AppConfig.MAX_WAIT_TIME
EXECUTIONTIMEZONE = AppConfig.EXECUTION_TIME_ZONE
BROWSER_TYPE = AppConfig.BROWSER_TYPE
WORKING_DIRECTORY  = str(AppConfig.WORKING_DIRECTORY)
logger.info(f"WORKING_DIRECTORY : {WORKING_DIRECTORY}")
__properties_file_path = os.path.normpath("".join([WORKING_DIRECTORY, os.path.sep, 'ConfigFile.properties']))
logger.info(f"ConfigFile.properties : {__properties_file_path}")
pyraft_property = PyRAFTConfig(__properties_file_path)

if BROWSER_TYPE == "BROWSERSTACK":
    BROWSERSTACK_USERNAME = AppConfig.BROWSER_STACK_USERNAME
    BROWSERSTACK_KEY = AppConfig.BROWSER_STACK_KEY
    DEVICE_NAME = AppConfig.DEVICE_NAME
    LANDSCAPE_ORIENTATION = AppConfig.LANDSCAPE_ORIENTATION
    
SYS_DIR_PATH = os.path.normpath("".join([WORKING_DIRECTORY,os.path.sep,'results']))
APP_DIR = os.path.normpath("".join([SYS_DIR_PATH,os.path.sep,APPNAME]))
LOGER_DIR = os.path.normpath("".join([APP_DIR,os.path.sep,'logs']))
INPUTSFILES_DIR = os.path.normpath("".join([APP_DIR,os.path.sep,'inputs']))
REPORT_DIR = os.path.normpath("".join([APP_DIR,os.path.sep,'reports']))


LOGGER_PATH = os.path.normpath("".join([LOGER_DIR,os.path.sep,'log_',CURRENT_TIME_STAMP,'.log']))
DB_REPORT_SUMMARY_PATH = os.path.normpath("".join([REPORT_DIR,os.path.sep,"Run_",CURRENT_TIME_STAMP,"_validationSummary",'.xlsx']))
CURRENT_DIR = os.path.normpath("".join([REPORT_DIR,os.path.sep,"RUN_",CURRENT_TIME_STAMP]))
HTML_REPORTS = os.path.normpath("".join([REPORT_DIR,os.path.sep,"RUN_",CURRENT_TIME_STAMP,os.path.sep,'Html_Reports']))
CURRENT_DIR_SNAPSHOTS = os.path.normpath("".join([CURRENT_DIR,os.path.sep,"Snapshot"]))
TEST_DATA_PATH = os.path.normpath("".join([WORKING_DIRECTORY,os.path.sep,"app_test",os.path.sep,"testdata"]))

#PyAzure reporting location :
JSON_TXT_PATH=os.path.normpath("".join([CURRENT_DIR,os.path.sep,'JsonReport','.json']))
ADO_JSON_PATH=os.path.normpath("".join([CURRENT_DIR,os.path.sep,'ADO_CONFIG_DEFAULT','.json']))
XML_REPORT_PATH = os.path.normpath("".join([SYS_DIR_PATH,os.path.sep,'results','.xml']))


_pyraft_dirs  =[SYS_DIR_PATH,APP_DIR,LOGER_DIR,INPUTSFILES_DIR,REPORT_DIR,CURRENT_DIR,HTML_REPORTS,CURRENT_DIR_SNAPSHOTS] #,#EXCEL_REPORTS]
for _custom_dir in _pyraft_dirs:
    if not os.path.exists(_custom_dir):
        os.makedirs(_custom_dir)
        if os.path.exists(_custom_dir) : print("Successfully utilities reporting folder is created %s" %_custom_dir)
    else:
        print("Path is already Exist %s" %_custom_dir)
     

class Azureinfo(object):
    tfs_url = pyraft_property.get_property('AzureConfiguration', 'azure_url')
    username = pyraft_property.get_property('AzureConfiguration','azure_username')
    password = pyraft_property.get_property('AzureConfiguration','azure_password')
    azure_plan_id = pyraft_property.get_property('AzureConfiguration','azure_plan_id')
    azure_test_suite_id = pyraft_property.get_property('AzureConfiguration','azure_test_suite_id')
    run_name = pyraft_property.get_property('AzureConfiguration','azure_run_name')
    azure_project_name = pyraft_property.get_property('AzureConfiguration','azure_project_name')
    azure_area_path = pyraft_property.get_property('AzureConfiguration','azure_area_path')

    if None not in [username,password,azure_plan_id,azure_test_suite_id,run_name,azure_project_name]:
        azure_execution_status = pyraft_property.get_property('AzureConfiguration', 'azure_execution_status')
    else:azure_execution_status = "NO"

    try:
        if "useapp" in str(SYSTEM_NAME): local_execution_status = "NO"
        else: local_execution_status = "YES"
        azure_defect_status = pyraft_property.get_property('AzureConfiguration', 'azure_defect_status')
        print(f"azure_defect_status = pyraft_property.get_property('AzureConfiguration', 'azure_defect_status'): {azure_defect_status}")
    except Exception as ex:
        local_execution_status = "NO"
        azure_defect_status = "NO"
        print(f"Unable to get the : azure_defect_status Hence utilities by default set to 'NO' and error :{ex}")

    ado_config_json = {}
    ado_config_json['azure_username'] = username
    ado_config_json['azure_passcode'] = password
    ado_config_json['azure_testplan_id'] = azure_plan_id
    ado_config_json['azure_testsuite_id'] = azure_test_suite_id
    ado_config_json['azure_project_name'] = azure_project_name
    ado_config_json['azure_product_name'] = run_name
    ado_config_json['azure_area_path'] = azure_area_path
    ado_config_json['azure_execution_status'] = azure_execution_status
    ado_config_json['azure_defect_status'] = azure_defect_status
    ado_config_json['local_execution_status'] = local_execution_status

    try :
        ado_config_json['email_status'] = pyraft_property.get_property('EmailConfiguration', 'Email_status')
        ado_config_json['email_list'] = pyraft_property.get_property('EmailConfiguration', 'Email')
    except Exception as E:
        ado_config_json['email_status'] = "YES"
        ado_config_json['email_list'] = "@email.com"
        print("email_list/email status key error")

    with open(ADO_JSON_PATH, 'w+') as outfile: json.dump(ado_config_json, outfile)
    #with open(GENERIC_ADO_JSON_PATH, 'w+') as outfile: json.dump(ado_config_json, outfile)
    print("Updating ADO Config json...")
    
class Email (object):
        try:
            email_list = pyraft_property.get_property('EmailConfiguration','Email')
            try:
                email_status =pyraft_property.get_property('EmailConfiguration','Email_status')
                print(f"email_status:{email_status}")
            except:
                print ("Observed email status parameter is missing in configfile.property.Please add 'Email_Status';' ")
                email_status = "NO"
        except:
            print ("Observed email address having issues. Please send email address with separated ';' ")
            email_list ="@email.com"

class  AutomationRunInfo(object):
        try:
            _remote_execution=pyraft_property.get_property('RunConfiguration','remote_execution')
            _condition_check=["YES","TRUE"]
            _remote_server_url = pyraft_property.get_property('RunConfiguration','remote_server_url')
            if (str(_remote_execution)).upper() in _condition_check:
                REMOTE_EXECUTION = True
                print("AutomationRunInfo Obj _remote_server_url:",_remote_server_url)
                if "http" in str(_remote_server_url) :
                    REMOTE_SERVER_URL= _remote_server_url
                    print("REMOTE SERVER URL: As per the CONFIG FILE",REMOTE_SERVER_URL)
                else:
                    REMOTE_SERVER_URL = "http://localhost:4444/wd/hub"
            else:
                REMOTE_EXECUTION =False
        except:
            print ("Observed remote_execution parameter is missing in configfile.properties.Please add 'remote_execution';' ")
            REMOTE_EXECUTION = False

        print(f"REMOTE_EXECUTION :{REMOTE_EXECUTION}")


def automatic_mapper(user_name, password, project, product, email_list, test_plan_id, test_suite_id):
    data = {}
    data["azure_info"] = {
        "url": "",
        "username": user_name,
        "password": password,
        "project": project,
        "product": product,
        "result_execution": "YES",
        "defect_creation": "YES",
        "email_execution": "YES",
        "tool": "utilities",
        "email_list": email_list
    }

    data["tests_map"] = [
        {
            "test_plan_id": test_plan_id,
            "testcase_result_map":
                [
                    {
                        "test_suite_id": test_suite_id,
                        "testcase_id": ["ALL"]
                    }
                ]
        }
    ]

    return data

# import json
# import os
# __ado_mapper_json = os.path.normpath("".join([WORKING_DIRECTORY, os.path.sep, 'ado_mapper.json']))
# if not os.path.exists(__ado_mapper_json):
#     __data = automatic_mapper(Azureinfo.username, Azureinfo.password,Azureinfo.azure_project_name,Azureinfo.run_name,
#                      Email.email_list.split(";"), Azureinfo.azure_plan_id, Azureinfo.azure_test_suite_id)
#     with open(__ado_mapper_json, 'w') as outfile:
#         json.dump(__data, outfile)
# else:
#     print("ADO MAPPER Already exist ..")


