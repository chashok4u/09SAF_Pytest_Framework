import utilities.report_utility.loggers as log


generic_info_testcase_summary =[]
generic_info_modules_Summary = []



def generic_update_to_tc_summary(testcase_info,step_status, path):
    try:
        log.logger1.info(f"update_to_tc_summary: testcase_info {testcase_info}")
        in_tc_info = list(testcase_info[0].values())
        in_tc_ex = list(testcase_info[1].values())
        if step_status[0] > 0 :
            if step_status[2] > 0 or step_status[0] == 0 or step_status[1] == 0 :
                generic_info_testcase_summary.append([str(in_tc_info[0]),str(in_tc_info[1]),str(in_tc_info[2]),"FAILED",path,str(in_tc_ex[1])])
            else:
                generic_info_testcase_summary.append([str(in_tc_info[0]),str(in_tc_info[1]),str(in_tc_info[2]),"PASSED",path,str(in_tc_ex[1])])
        else:
            generic_info_testcase_summary.append([str(in_tc_info[0]),str(in_tc_info[1]), str(in_tc_info[2]), "FAILED", path, str(in_tc_ex[1])])

        log.logger1.info(f"generic_info_testcase_summary: info_testcase_summary {generic_info_testcase_summary}")
    except Exception as e:
        log.logger1.info("generic_info_testcase_summary:update_to_tc_summary %s" % e)


def generic_update_to_module_summary(testcase_info, step_status, path):
    try:
        if step_status[2] > 0:
            generic_info_modules_Summary.append([testcase_info[0],"FAIL",path])
        else:
            generic_info_modules_Summary.append([testcase_info[0], "PASS", path])
    except Exception as e:
        log.logger1.info("generic_update_to_module_summary %s" % e)
