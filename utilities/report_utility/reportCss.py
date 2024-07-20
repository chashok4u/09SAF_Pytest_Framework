'''
@author: Test
'''

import json
import os
import pandas as pd
from datetime import datetime, timedelta
import time
import stat as stat
import xlsxwriter
from pathlib import Path
global Css_Main, Css_Testresult, Css_Header, Css_Status_True, Css_Status_Fail
global workbook
import datetime
import utilities.report_utility.reportsFormat as css
import utilities.config._config as _config
import utilities.report_utility.loggers as log
from datetime import datetime
import base64
import json
from os import path

global FOR_EACH_TESTCASE_STEPS_INFO

from junit_xml import TestSuite, TestCase

xml_test_cases_info = []

FOR_EACH_TESTCASE_STEPS_INFO = []
jsonFormatTotalTestcasesInfo = []
info_testcase_summary = []
info_modules_Summary = []



class Report:
    def __init__(self):
        pass

    def intiate_result_workbook(self):
        self.workbook = xlsxwriter.Workbook(_config.TC_REPORT_PATH)

    def add_steps_to_excel_report(self, test_case_result, test_case_name, worksheet):
        pass

    def add_testcase_result(self, testcase_name, test_steps):
        worksheet = self.workbook.add_worksheet(testcase_name)
        self.add_steps_to_excel_report(test_steps, testcase_name, worksheet)

    def close_result_excel_book(self):
        log.logger1.info("closing work book .. End of the result")
        self.workbook.close()

    def html_report(self, testcase_info, testcases_result):
        _json_format_report_testcase = {}
        for _item1 in testcase_info: _json_format_report_testcase.update(_item1)
        main_body = style() + '''<body>''' + '<table>' + logoinfo() + tcinfo() + '</table></br>'
        test_body = '<table>' + info_td(testcase_info) + '</table></br>'
        table_headings = '''<tr><th>Step</th><th>Description</th><th>Expected Results</th><th>Actual Results</th></tr>'''

        steps = []
        sno = 1
        for sublist in testcases_result:
            _json_step_formating(sno, sublist[0], sublist[1], sublist[2], sublist[3], repr(sublist[4]))
            # _json_format_report_testcase['steps'].append(_dictionary_step)
            STATUS_CHECK = ["TRUE", "PASS", "PASSED", "YES"]

            if str(sublist[3]).upper() in STATUS_CHECK:
                # step = '<tr><td>' + str(sno) + '</td><td>' + sublist[0] + '</td><td>' + str(sublist[
                #     1]) + '</td><td><font color="#A0FFA4"><a href=' + repr(sublist[4]) + 'style="color:#417505">' + \
                #        sublist[2] + '</font></td></tr>'
                # if os.path.exists(sublist[4]):
                try:
                    # if os.path.exists(sublist[4]):
                    # if sublist[4] is not None and sublist[4] != '.':
                    snapshotpath = os.path.normpath(sublist[4])
                    # log.logger1.info(f"Path of Snapshot:{snapshotpath}")
                    with open(snapshotpath, "rb") as html_file:
                        _encoded_string = (base64.b64encode(html_file.read()).decode('ascii'))
                    step1 = """<tr><td>{}</td><td>{}</td><td>{}</td><td><u><font color="#A0FFA4"><a href= "javascript:" onclick = "changeImg('data:image/png;base64,{}')" style="color:#417505">{}</font></u></td></tr>"""
                    step = step1.format(str(sno), sublist[0], sublist[1], _encoded_string, sublist[2])
                # else:
                #     step1 = """<tr><td>{}</td><td>{}</td><td>{}</td><td><font color="#A0FFA4">{}</font></td></tr>"""
                #     step = step1.format(str(sno), sublist[0], sublist[1], sublist[2])
                except:
                    step1 = """<tr><td>{}</td><td>{}</td><td>{}</td><td><font color="#417505">{}</font></td></tr>"""
                    step = step1.format(str(sno), sublist[0], sublist[1], sublist[2])

            else:
                try:  # if sublist[4] is not None and sublist[4] != '.':
                    snapshotpath = os.path.normpath(sublist[4])
                    log.logger1.info(f"Path of Snapshot:{snapshotpath}")
                    with open(snapshotpath, "rb") as html_file:
                        _encoded_string = (base64.b64encode(html_file.read()).decode('ascii'))
                    step1 = """<tr><td>{}</td><td>{}</td><td>{}</td><td><u><font color="red"><a href= "javascript:" onclick = "changeImg('data:image/png;base64,{}')" style="color:#D0021A">{}</font></u></td></tr>"""
                    step = step1.format(str(sno), sublist[0], sublist[1], _encoded_string, sublist[2])
                except:  # else:
                    step1 = """<tr><td>{}</td><td>{}</td><td>{}</td><td><font color="red">{}</font></td></tr>"""
                    step = step1.format(str(sno), sublist[0], sublist[1], sublist[2])

            steps.append(step)
            sno += 1

        sno = None
        steps = ''.join(steps)
        closing_body = '''<table>''' + table_headings + steps + '''</table>'''
        step_status = pass_fail_count(testcases_result)
        temp_for_each_tc_steps_info(testcase_info, step_status)
        steps_status_body = '''<table><tr><th>Total steps :{}</th><th>Pass : {}</th><th>Fail : {}</th></tr></table>'''.format(
            step_status[0], step_status[1], step_status[2])
        _json_format_report_testcase['total_steps'] = step_status[0]
        _json_format_report_testcase['pass_steps'] = step_status[1]
        _json_format_report_testcase['fail_steps'] = step_status[2]
        in_time_stamp = (datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
        _json_format_report_testcase['TimeStamp'] = str(in_time_stamp)
        closing_html = '''</body></html>'''
        body = main_body + test_body + closing_body + steps_status_body + closing_html
        location_path = _config.HTML_REPORTS + os.path.sep + "TC_" + str(
            list(testcase_info[0].values())[2]) + "_" + in_time_stamp + ".html"

        _json_format_report_testcase['testcase_attachment'] = location_path
        jsonFormatTotalTestcasesInfo.append(json.dumps(_json_format_report_testcase))
        saveas_html(location_path, body)
        update_to_tc_summary(testcase_info, step_status, location_path)

        # XML REPORT
        x = time.strptime(testcase_info[1]['Execution_Time'], '%H:%M:%S')

        in_seconds = timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
        xml_test_cases_info.append(
            TestCase(name=testcase_info[0]['TestCase_Name'] + "__" + str(testcase_info[0]['VSTS_ID']),
                     classname=testcase_info[0]['module_name'],
                     elapsed_sec=in_seconds, log=steps_status_check(step_status),
                     file=location_path,
                     timestamp=in_time_stamp))


    def tccase_summary(self, module_info, tc_summary):
        main_body = style() + '''<body>''' + '<table>' + logoinfo() + moduleinfo() + '</table></br>'
        test_body = '<table >' + info_td(module_info) + '</table>'

        table_headings = '''<tr><th>Sno</th><th>VSTS ID</th><th>Testcase Name</th><th>Status</th></tr>'''
        greentag = '''<font color = "#417505"><svg width="20px" height = "20px" style = "float:left;"><circle cx = "10" cy = "10" r = "4" stroke = "green" stroke-width ="4" fill ="green"/></svg><span style ="display:inline-block;float:left;padding-top:2px;">'''
        redtag = '''<font color = "#D0021A"><svg width = "20px" height = "20px" style = "float:left;"><circle cx = "10" cy = "10" r = "4" stroke = "red" stroke-width ="4" fill ="red"/></svg><span style = "display: inline-block;float: left;padding-top: 2px;" >'''

        steps = []
        sno = 1
        for sublist in tc_summary:
            if sublist[3] == "PASS" or sublist[3] == "Pass":
                step = '<tr><td>' + str(sno) + '</td><td><a href=' + repr(sublist[4]) + '>' + sublist[
                    1].capitalize() + '</td><td>' + \
                       sublist[2].capitalize() + '</td><td>' + greentag + sublist[3] + '</span></td></tr>'
            else:
                step = '<tr><td>' + str(sno) + '</td><td><a href=' + repr(sublist[4]) + '>' + sublist[
                    1].capitalize() + '</td><td>' + \
                       sublist[2].capitalize() + '</td><td>' + redtag + sublist[3] + '</span></td></tr>'
            steps.append(step)
            sno += 1

        sno = None

        steps = ''.join(steps)
        closing_body = '''<table>''' + table_headings + steps + '''</table>'''
        step_status = pass_fail_count(tc_summary)
        steps_status_body = '''<table><tr><td>Total Testcases :{}</td><td>Pass : {}</td><td>Fail : {}</td></tr></table>'''.format(
            step_status[0], step_status[1], step_status[2])
        closing_html = '''</body></html>'''
        body = main_body + test_body + '</br>' + closing_body + '</br>' + steps_status_body + closing_html
        path = _config.HTML_REPORTS + os.path.sep + "ModuleSummary_" + str(
            list(module_info[0].values())[0]) + _config.CURRENT_TIME_STAMP + ".html"
        saveas_html(path, body)
        log.logger1.info("closing html report for Testcaseresult..")
        update_to_module_summary(module_info, step_status, path)
        # generic_update_to_module_summary(module_info, step_status, path)

    def genrate_report(self, testinfo, test_case_result):
        self.html_report(testinfo, test_case_result)

    def module_summary_report(self, app_info, module_summary):
        mainbodystyle = str(module_style())
        main_body = mainbodystyle + '''<body>''' + '<table>' + logoinfo() + pyliteinfo() + '</table></br>'
        test_body = '<table>' + (info_td(app_info)) + '</table>'
        table_headings = '''<tr><th>sno</th><th>Module Name</th><th>Execution Time</th><th>Status</th></tr>'''
        greentag = '''<font color = "#417505"><svg width="20px" height = "20px" style = "float:left;"><circle cx = "10" cy = "10" r = "4" stroke = "green" stroke-width ="4" fill ="green"/></svg><span style ="display:inline-block;float:left;padding-top:2px;">'''
        redtag = '''<font color = "#D0021A"><svg width = "20px" height = "20px" style = "float:left;"><circle cx = "10" cy = "10" r = "4" stroke = "red" stroke-width ="4" fill = "red"/></svg><span style = "display: inline-block;float: left;padding-top: 2px;" >'''
        steps = []
        sno = 1
        for sublist in module_summary:
            execution_time = sublist[1]
            if (sublist[3]).upper() == "PASS":
                step = '<tr><td>' + str(sno) + '</td><td><a href=' + repr(sublist[4]) + '>' + (sublist[
                    0]).capitalize() + '</a></td><td>' + str(execution_time) + '</td><td>' + greentag + sublist[
                           3] + '</span></td></tr>'
            else:
                step = '<tr><td>' + str(sno) + '</td><td><a href=' + repr(sublist[4]) + '>' + (sublist[
                    0]).capitalize() + '</a></td><td>' + str(execution_time) + '</td><td>' + redtag + sublist[
                           3] + '</span></td></tr>'
            steps.append(step)
            sno += 1
        sno = None
        steps = ''.join(steps)
        closing_body = '''<table>''' + table_headings + steps + '''</table>'''
        step_status = pass_fail_count(module_summary)
        steps_status_body = '''<table><tr><td>Total Modules :{}</td><td>Pass : {}</td><td>Fail : {}</td></tr></table>'''.format(
            step_status[0], step_status[1], step_status[2])
        closing_html = '''</body></html>'''
        body = main_body + test_body + '</br>' + closing_body + '</br>' + steps_status_body + closing_html
        path = _config.HTML_REPORTS + os.path.sep + "AutomationSummary" + "_" + _config.CURRENT_TIME_STAMP + ".html"
        generic_path = _config.HTML_REPORTS + os.path.sep + "AutomationSummary.html"
        log.logger1.info("Total_No_Of_modules:{}".format(step_status[0]))
        log.logger1.info("Passed_Modules:{}".format(step_status[1]))
        log.logger1.info("Failed_Modules:{}".format(step_status[2]))
        if step_status[0] != 0:
            log.logger1.info("Pass_Percentage:{} %".format((int(step_status[1]) / int(step_status[0])) * 100))
        else:
            log.logger1.info("Pass_Percentage: 0%")
        saveas_html(path, body)
        saveas_html(generic_path, body)
        log.logger1.info("closing html report for module_summary_report..")
        return path


def pass_fail_count(test_case_result):
    steps_status = []
    steps_status.clear()
    lit = []
    for item1 in test_case_result: lit = item1 + lit
    PASS_COUNT = (lit.count("PASS") + lit.count("Pass") + lit.count("pass"))
    FAIL_COUNT = (lit.count("FAIL") + lit.count("fail") + lit.count("Fail"))
    steps_status.append(PASS_COUNT + FAIL_COUNT)
    steps_status.append(PASS_COUNT)
    steps_status.append(FAIL_COUNT)
    lit.clear()
    return steps_status


def temp_for_each_tc_steps_info(_testcases_info, _step_status):
    temp_tc_steps_info = []
    temp_tc_steps_info.append(_testcases_info)
    temp_tc_steps_info.append(_step_status)
    FOR_EACH_TESTCASE_STEPS_INFO.append([x for xs in temp_tc_steps_info for x in xs])


def info_td(in_main_table_info):
    tr = []
    for item1 in in_main_table_info:
        th = []
        for key, value in item1.items():
            tvlue = ('<td>' + key + ': <B>' + str(value).capitalize() + '</B></td>')
            th.append(tvlue)
        tr.append(''.join(th))
    info = []
    for td in tr: info.append('<tr>' + td + '</tr>')
    i_table = ''.join(info)
    return (i_table)


def steps_status_check(step_status):
    if step_status[0] > 0:
        if step_status[2] > 0 or step_status[0] == 0 or step_status[1] == 0:
            return "- Failed "
        return "+ Passed "
    return "- Failed "


def update_to_tc_summary(testcase_info, step_status, path):
    log.logger1.info(f"update_to_tc_summary: testcase_info {testcase_info}")
    try:
        sub_summary_report = []
        sub_summary_report.clear()
        in_tc_info = list(testcase_info[0].values())
        sub_summary_report.append(str(in_tc_info[0]))
        sub_summary_report.append(str(in_tc_info[1]))
        sub_summary_report.append(str(in_tc_info[2]))
        if step_status[0] > 0:
            if step_status[2] > 0 or step_status[0] == 0 or step_status[1] == 0:
                sub_summary_report.append("FAIL")

            else:
                sub_summary_report.append("PASS")
        else:
            sub_summary_report.append("FAIL")

        sub_summary_report.append(path)
        in_tc_ex = list(testcase_info[1].values())
        sub_summary_report.append(str(in_tc_ex[1]))
        info_testcase_summary.append(sub_summary_report)
        log.logger1.info(f"update_to_tc_summary:info_testcase_summary {info_testcase_summary}")
    except Exception as e:
        log.logger1.info("update_to_tc_summary %s" % e)


def update_to_module_summary(testcase_info, step_status, path):
    try:
        sub_module_summary_report = []
        sub_module_summary_report.append(testcase_info[0])
        if step_status[2] > 0:
            sub_module_summary_report.append("FAIL")
        else:
            sub_module_summary_report.append("PASS")
        sub_module_summary_report.append(path)
        info_modules_Summary.append(sub_module_summary_report)
    except Exception as e:
        log.logger1.info("update_to_module_summary %s" % e)


def saveas_html(path, body):
    try:
        log.logger1.info(f"HTML:{path}")
        html_file = open(path, 'w+', encoding='utf-16')
        html_file.write(body)
        html_file.close()
        log.logger1.info("closing html report for Testcase result..")
    except Exception as E:
        log.logger1.error(
            "Unable to Generate HTML, Due to Html is going to more then 250 Characters, Move this repo to C:\AutomationProject")
        raise Exception(E)


def style():
    html_css_style_format = '''<!DOCTYPE html><html><head>
      <style>
         table {width:1366px;hight:60px; background-color:#FFFFFF; font-family: Akkurat Pro; border-collapse: collapse;margin-left:auto;margin-right:auto;}    
         td{color: black;border: 2px solid #dddddd; text-align: left;padding: 8px 8px 8px 15px; width:20px height:20px}                   
         th{border: 2px solid #dddddd;text-align: left;padding: 8px 8px 8px 15px; color: black; background-color: #C6C6C6}
         h2{font-family: Akkurat Pro;display: inline-block;float: left;margin: 5PX 0PX;}
         table#td01{width:1366px;hight:60px}
         a{text-decoration:none !important;}
         address{align:right;display: inline-block; float: right;margin-top: 5PX;"}
         img{width:144px; height:auto; padding:10px 0px 0px 0px}
      </style>
      <script type="text/javascript">
    function changeImg(imgsrc){ 
    var image = new Image();
    image.src = imgsrc
    var w = window.open("");
    w.document.write(image.outerHTML);
    }
    </script>
   </head>'''

    return (html_css_style_format)


def module_style():
    module_style_format = ('''<!DOCTYPE html><html><head>
      <style>
         table {width:1366px;hight:60px; background-color:#FFFFFF; font-family: Akkurat Pro; border-collapse: collapse;margin-left:auto;margin-right:auto;}    
         td{color: black;border: 2px solid #dddddd; text-align: left;padding: 8px 8px 8px 15px; width:20px height:20px}                   
         th{border: 2px solid #dddddd;text-align: left;padding: 8px 8px 8px 15px; color: black; background-color: #C6C6C6}
         h2{font-family: Akkurat Pro;display: inline-block;float: left;margin: 5PX 0PX;}
         table#td01{width:1366px;hight:60px}
         a{text-decoration:none !important;}
         address{align:right;display: inline-block; float: right;margin-top: 5PX;"}
         img{width:144px; height:auto; padding:10px 0px 0px 0px}
      </style>
   </head>   
    <script type="text/javascript">
    function changeImg(imgsrc,imgname){ 
    var image = new Image();
    image.src = imgsrc
    var w = window.open(imgname);
    w.document.write(image.outerHTML);
    }
    </script>   
   ''')
    return module_style_format


def pyliteinfo():
    return ('''
      <tr><td><h2>Automation Execution Results</h2>
      <address ><a href="mailto:@email.com">Developed and driven by Automation Team</a></address></td></tr>
      ''')


def moduleinfo():
    return ('''<tr><td><h2>Module Execution Results</h2></td></tr>''')


def tcinfo():
    return ('''<tr><td><h2>Testcase Execution Results</h2></td></tr>''')


def logoinfo():
    return ('''<tr><td bgcolor="#00529b"><img src="data:image/png;base64,{}" alt="" ></td></tr>'''.format(css.img_se))


def _json_step_formating(_sno, _description, _expected_result, _actual_result, _status, _attachment_path):
    _step_info = {}
    _step_info['StepNo'] = str(_sno)
    _step_info['Description'] = str(_description)
    _step_info['ExpectedResult'] = str(_expected_result)
    _step_info['ActualResult'] = str(_actual_result)
    _step_info['stepstatus'] = str(_status)
    try:
        if _attachment_path is not None:
            with open(_attachment_path, "r+b") as html_file:
                _attachment_path_string = (base64.b64encode(html_file.read()).decode('ascii'))
            _step_info['Screenshot'] = str(_attachment_path_string)
            html_file = None
            _attachment_path_string = None
    except:
        _step_info['Screenshot'] = "None"

    return _step_info
