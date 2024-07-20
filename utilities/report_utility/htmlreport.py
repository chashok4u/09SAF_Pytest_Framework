'''

@author:
'''

from utilities.file_handles.fileobjects import *
import utilities.config._config as _config
import utilities.report_utility.loggers as log

modules_summary = []


def testcase_summary(testcases_info,tc_summary):
    main_body='''<!DOCTYPE html><html><head>
    <style>
    table {width:90%;}
    table {font-family: arial, sans-serif; border-collapse: collapse;}
    td, th {border: 2px solid #dddddd;text-align: left;padding: 8px;}
    tr:nth-child(even) {background-color: #dddddd;}
    table#t01 {background-color: #00FF00;}
    table#t02 th,td {color: white;background-color: gray;}
    </style></head><body>
    <table id="t01"><th><h2><Center>Automation Execution Results</center></h2></th></table>'''

    test_body=('''<table id="t02">
    <tr><th>Module Name&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;{}</th></tr>
    <tr><th>Execution TIME:&nbsp;{}</th></tr>
    <tr><th>Date&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp:&nbsp;{}</th></table>
    </br>'''.format(testcases_info[0],testcases_info[1],testcases_info[2]))

    table_headings='''<tr><th>SNo</th><th>TESTCASE NAME</th><th>STATUS</th></tr>'''
    steps =[]
    SNO =1
    for sublist in tc_summary:
        if sublist[1]=="PASS" or sublist[1]=="Pass" :
            step = '<tr><td>'+str(SNO)+'</td><td><a href='+repr(sublist[2])+'>'+sublist[0] +'</td><td><font color="#A0FFA4">'+ sublist[1]+'</font></td></tr>'
        else:
            step = '<tr><td>'+str(SNO)+'</td><td><a href='+repr(sublist[2])+'>'+sublist[0] +'</td><td><font color="#FF716D"> '+ sublist[1]+'</font></td></tr>'

        steps.append(step)
        SNO +=1

    SNO=None

    steps=''.join(steps)
    closing_body='''<table>'''+table_headings+steps+'''</table>'''
    step_status=pass_fail_count(tc_summary)
    steps_status_body='''<table><tr><th>Total No of steps :{}</th><th>Pass : {}</th><th>Fail : {}</th></tr></table>'''.format(step_status[0],step_status[1],step_status[2])
    closing_html='''</body></html>'''
    body=main_body+test_body+closing_body+steps_status_body+closing_html

    sub_summary_report=[]
    sub_summary_report.clear()
    if step_status[2]>0:
        sub_summary_report.append(testcases_info[0])
        sub_summary_report.append("FAIL")

    else:
        sub_summary_report.append(testcases_info[0])
        sub_summary_report.append("PASS")

    path=_config.Curent_Directory+'\\'+str(testcases_info[0])+"_TestCase_Summary"+_config.currentTimeStamp_format+".html"

    htmlfile = open(path,'w')
    htmlfile.write(body)
    htmlfile.close()
    log.logger1.info("closing html report for testcase result..")
    sub_summary_report.append(path)
    #print(sub_summary_report)
    modules_summary.append(sub_summary_report)
    print(body)


def module_summary_report(app_info,tc_summary):
    main_body='''<!DOCTYPE html><html><head>
    <style>
    table {width:90%;}
    table {font-family: arial, sans-serif; border-collapse: collapse;}
    td, th {border: 2px solid #dddddd;text-align: left;padding: 8px;}
    tr:nth-child(even) {background-color: #dddddd;}
    table#t01 {background-color: #f1f1c1;}
    table#t02 th,td {color: white;background-color: gray;}
    </style></head><body>
    <table id="t01"><th><h2><Center>Application Automation Execution Summary</center></h2></th></table>'''

    test_body=('''<table id="t02">
    <tr><th>Application NAME&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp;{}</th></tr>
    <tr><th>Execution TIME:&nbsp;{}</th></tr>
    <tr><th>Date&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp:&nbsp;{}</th></table>
    </br>'''.format(app_info[0],app_info[1],app_info[2]))

    table_headings='''<tr><th>SNo</th><th>MODULE NAME</th><th>STATUS</th></tr>'''
    steps=[]
    SNO=1
    for sublist in tc_summary:
        if sublist[1]=="PASS" or sublist[1]=="Pass" :
            step='<tr><td>'+str(SNO)+'</td><td><a href='+repr(sublist[2])+'>'+(sublist[0].capitalize())+'</a></td><td><font color="#A0FFA4">'+sublist[1]+'</font></td></tr>'
        else:
            step='<tr><td>'+str(SNO)+'</td><td><a href='+repr(sublist[2])+'>'+(sublist[0].capitalize())+'</a></td><td><font color="#FF716D">'+sublist[1]+'</font></td></tr>'

        steps.append(step)
        SNO +=1

    SNO=None

    steps=''.join(steps)
    closing_body='''<table>'''+table_headings+steps+'''</table>'''
    step_status=pass_fail_count(tc_summary)
    steps_status_body='''<table><tr><th>Total No of steps :{}</th><th>Pass : {}</th><th>Fail : {}</th></tr></table>'''.format(step_status[0],step_status[1],step_status[2])
    closing_html='''</body></html>'''
    body=main_body+test_body+closing_body+steps_status_body+closing_html
    path=_config.Curent_Directory+'\\'+"Module_summary"+_config.currentTimeStamp_format+".html"
    htmlfile = open(path,'w')
    htmlfile.write(body)
    htmlfile.close()
    log.logger1.info("closing html report for Testcaseresult..")
    print(body)


