'''
@author: Test
'''

import sys
import numpy as vn
from tabulate import tabulate
import utilities.report_utility.reportCss as summary
from utilities.report_utility.reportCss import *
import utilities.ui_utility.ui as Ui
import utilities.config._config as config
from utilities.file_handles.fileobjects import *
import utilities.report_utility.loggers as log
# from utilities.db_utility.db import summary_report
from junit_xml import TestSuite, TestCase
import time

sys.tracebacklimit = 0
_report = Report()
summary_report = [['src_username', 'src_db', 'src_query', 'trg_username', 'trg_db', 'trg_query', 'info', 'Status']]


class StructureReports:
    def initialize_reports(self):
        pass
        # _report.intiate_result_workbook()

    def close_reports(self):
        pass
        # _report.close_result_excel_book()

    def final_db_summary_report(self):
        log.logger1.info(summary_report)
        log.logger1.info("Execution is completed....")

    def add_testcase_result(self, tc_info):
        tc_time_info = {'Date': get_current_time_zone_timestamp('Asia/Kolkata'),
                        'Execution_Time': str(tc_info[2]),
                        'Executed_On': config.BROWSER_TYPE}

        current_tc_info = {'module_name': tc_info[0],
                           'VSTS_ID': tc_info[1][0],
                           'TestCase_Name': tc_info[1][1]}
        print("tc_time_info" + "*" * 50)
        print(tc_time_info)
        testcase_info = [current_tc_info, tc_time_info]
        _report.genrate_report(testcase_info, Ui.listVal)
        tc_info.clear()
        Ui.listVal.clear()

    def add_testcase_summary(self, in_tc_module_info):
        tc_module_info = {'module_name': in_tc_module_info[0], 'Execution_Time': in_tc_module_info[1],
                          'Date': in_tc_module_info[2]}
        in_tc_module_info = [tc_module_info]
        _report.tccase_summary(in_tc_module_info, summary.info_testcase_summary)
        log.logger1.info(f"Summary.info_testcase_summary {summary.info_testcase_summary}")
        summary.info_testcase_summary.clear()

    def module_summary_report(self, app_info):
        application_info = {'Application_Name': app_info[0], 'Execution_Time': app_info[1], 'Date': app_info[2]}

        person_info = {'Executed_On': config.BROWSER_TYPE, 'Executed_By': config.SYSTEM_USER_NAME,
                       'Machine_Name/IPAddress': str(config.SYSTEM_NAME)}

        in_automation_summary = [application_info, person_info]
        self.au_sys_app_info = in_automation_summary
        entire_module_summary = []
        for in_module in summary.info_modules_Summary: entire_module_summary.append(
            list(in_module[0].values()) + in_module[1:])
        self.automation_summary_path = _report.module_summary_report(in_automation_summary, entire_module_summary)
        log.logger1.info(f"Entire_module_summary {entire_module_summary}")
        summary.info_modules_Summary.clear()

    def final_analysis_summary(self):
        log.logger1.info("************************FOR_EACH_TESTCASE_STEPS_INFO*************************************")
        log.logger1.info(f"summary.FOR_EACH_TESTCASE_STEPS_INFO {summary.FOR_EACH_TESTCASE_STEPS_INFO}")
        log.logger1.info("********************************************************************************************")
        log.logger1.info("Total Report In Json Format")
        ado_summary_json = {'testcase_result': summary.jsonFormatTotalTestcasesInfo}
        log.logger1.info(config.JSON_TXT_PATH)
        with open(config.JSON_TXT_PATH, 'w+') as outfile:
            json.dump(ado_summary_json, outfile)
            # for item in alltestcasesFinal:
            #     #pprint.pprint(json.dumps(item, indent=4))
            #     f.write("%s\n" % json.loads(item))
        log.logger1.info("Updating final results...")
        data = [json.loads(tc_result) for tc_result in ado_summary_json['testcase_result']]
        data_frame = (pd.DataFrame(data))

        global result_frame
        result_frame = data_frame[
            ['VSTS_ID', 'TestCase_Name', 'Date', 'Execution_Time', 'total_steps', 'pass_steps', 'fail_steps']]
        result_frame = result_frame.rename(columns={"VSTS_ID": "testcase_id",
                                                    "Execution_Time": "time",
                                                    "total_steps": "total_steps",
                                                    "module_name": "module_name",
                                                    "TestCase_Name": "testcase_name",
                                                    "testcase_attachment": "testcase_attachment"})

        result_frame['testcase_status'] = data_frame.apply(lambda row: label_status(row), axis=1)
        result_frame.columns = [x.upper() for x in result_frame.columns]
        result_frame.index = vn.arange(1, len(result_frame) + 1)
        log.logger1.info(tabulate(result_frame, headers='keys', tablefmt='psql'))

        # pretty printing is on by default but can be disabled using prettyprint=False

        if os.path.exists(config.XML_REPORT_PATH): os.remove(config.XML_REPORT_PATH)
        xml_module_tests_total_info = TestSuite("automation_execution", xml_test_cases_info)
        # print(TestSuite.to_xml_string([xml_module_tests_total_info]))

        with open(config.XML_REPORT_PATH, 'w') as f:
            TestSuite.to_file(f, [xml_module_tests_total_info])  # , prettyprint=False) """


test_reports = StructureReports()


class ReportsFinal:

    def __init__(self):
        self.TC_EXECUTION_START_TIME = None
        self.TC_EXECUTION_END_TIME = None
        self.MODULE_EXECUTION_START_TIME = None
        self.MODULE_EXECUTION_END_TIME = None

    def automation_start(self):
        self.AUTOMATION_EXECUTION_START_TIME = get_current_time_zone_timestamp(config.EXECUTIONTIMEZONE)

    def start(self):
        self.TC_EXECUTION_START_TIME = get_current_time_zone_timestamp(config.EXECUTIONTIMEZONE)
        time.sleep(1)
        return self.TC_EXECUTION_START_TIME


    def close(self, modulename, test_info):
        self.TC_EXECUTION_END_TIME = get_current_time_zone_timestamp(config.EXECUTIONTIMEZONE)
        TC_EXECUTION_TIME = self.execution_interval(self.TC_EXECUTION_START_TIME, self.TC_EXECUTION_END_TIME)
        TC_INFO = [modulename, test_info, TC_EXECUTION_TIME]
        log.logger1.info("**********************************************************************************")
        log.logger1.info(TC_INFO)
        log.logger1.info("**********************************************************************************")
        test_reports.add_testcase_result(TC_INFO)

    def execution_interval(self, starttime, endtime):
        executiontime = time_difference(starttime, endtime)
        return executiontime

    def module_start(self):
        self.MODULE_EXECUTION_START_TIME = get_current_time_zone_timestamp(config.EXECUTIONTIMEZONE)

    def module_close(self, module_name):
        self.MODULE_EXECUTION_END_TIME = get_current_time_zone_timestamp(config.EXECUTIONTIMEZONE)
        MODULE_EXECUTION_TIME = self.execution_interval(self.MODULE_EXECUTION_START_TIME, self.TC_EXECUTION_END_TIME)
        TC_MODULE_INFO = [module_name, MODULE_EXECUTION_TIME, self.MODULE_EXECUTION_END_TIME]
        test_reports.add_testcase_summary(TC_MODULE_INFO)

    def automation_close(self):
        AUTOMATION_EXECUTION_END_TIME = get_current_time_zone_timestamp(config.EXECUTIONTIMEZONE)
        AUTOMATION_EXECUTION_TIME = self.execution_interval(self.AUTOMATION_EXECUTION_START_TIME,
                                                            AUTOMATION_EXECUTION_END_TIME)
        app_info = [config.APPNAME, AUTOMATION_EXECUTION_TIME, self.AUTOMATION_EXECUTION_START_TIME]
        test_reports.module_summary_report(app_info)
        test_reports.close_reports()
        log.logger1.info("Execution is completed")
        test_reports.final_analysis_summary()

        return self.pyraft_close()  # Return the True/False

    def pyraft_close(self):
        fail_count = int(len(result_frame)) - int((result_frame.TESTCASE_STATUS == 'PASS').sum())
        if fail_count > 0:
            log.logger1.error("Due to one or more testcases Failed Hence Overall Automation \
             Execution status is marked as Failed")
            return False
        else:
            log.logger1.info(f"Automation_Execution: PASS")
            return True


