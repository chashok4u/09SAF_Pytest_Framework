# Version = 3.1.0b1

import os , json, pytest
from app_test.config._app_config import AppConfig
from app_test.config import _app_config
from app_test.config._test_config import log

ado_mapper_path = ""
# ado_mapper_path = os.path.normpath("".join([str(AppConfig.WORKING_DIRECTORY), os.path.sep, 'ado_mapper.json']))
# if not os.path.exists(ado_mapper_path): raise RuntimeError (f"ADO_MAPPER is not avaliable.ado_mapper_path")
# application_info = json.load(open(ado_mapper_path))
junit_path = os.path.normpath("".join([str(AppConfig.WORKING_DIRECTORY), os.path.sep,"results",os.path.sep, 'results.xml']))

from utilities import report
# from utilities import pynotify
# import azure_testresults_updater as az  # new Branding

@pytest.fixture(scope="function", autouse=True)
def divider_function(request):
    print('\n        --- function %s() start ---' % request.function.__name__)
    report.start()

    def fin():
        print('        --- function %s() done ---' % request.function.__name__)
        testcase_name = (request.function.__name__).split('__')[0]
        tfs_id = (request.function.__name__).split('__')[-1]
        module_name = (request.module.__name__).split('.')[-1]
        print([testcase_name, tfs_id, module_name])
        print('        --- Module %s() done ---' % request.module.__name__)
        APPLICATION_AUTOMATION_EXECUTION_TIME = "_"
        report.close(module_name, [tfs_id, testcase_name])

    request.addfinalizer(fin)


@pytest.fixture(scope="module", autouse=True)
def divider_module(request):
    print('\n    ------- module %s start ---------' % request.module.__name__)
    report.module_start()

    def fin():
        print('    ------- module %s done ---------' % request.module.__name__)
        module_name = (request.module.__name__).split('.')[-1]
        report.module_close(module_name)

    request.addfinalizer(fin)


@pytest.fixture(scope="session", autouse=True,)
def divider_session(request,envType, input_build_id, input_build_url, input_pipeline_name, input_app_id, marker_info):
    print('\n----------- session start ---------------')
    print("*"*45)
    cmd_session_inputs = {
        "environment": str(envType),
        "build_id": input_build_id,
        "build_url": input_build_url,
        "pipeline_name": input_pipeline_name,
        "app_id": input_app_id,
        # "tags": marker_info
    }
    # --> If Tag validation is failed -->
    # pynotify.send_alert_notification(application_info['azure_info']['email_list'], application_info['azure_info']['product'], "TEST", input_val=cmd_session_inputs)

    report.automation_start()

    def fin():
        print('----------- session done ---------------')
        automation_status = report.automation_close()


        for key, value in cmd_session_inputs.items():
            print(key, ":----->", value)

        # result = az.execute(ado_mapper_path, junit_path,
        #                     build_id=input_build_id,
        #                     build_url=input_build_url,
        #                     pipeline_name=input_pipeline_name,
        #                     environment=envType,
        #                     tags=marker_info)
        # result2 = json.loads(result)
        # if result2[-1]['test_status']['TEST_STATUS'] == "PASS":
        #     print("Automation Execution is Successfully..")

        if not automation_status:
            print("Due to one or more testcases Failed Hence Overall Automation Execution status is marked as Failed")
            raise Exception("Due to one or more testcases Failed Hence Overall Automation Execution status is marked as Failed")

    request.addfinalizer(fin)


def pytest_addoption(parser):
    parser.addoption("--TESTENV", action="store", default=str("default_env"))
    parser.addoption("--build_id", action="store", default="NA/LocalExecution")
    parser.addoption("--build_url", action="store", default="NA/LocalExecution")
    parser.addoption("--pipeline_name", action="store", default="NA/LocalExecution")
    parser.addoption("--APPID", action="store", default="default")


@pytest.fixture(scope="session")
def envType(pytestconfig):
    TESTENV = pytestconfig.getoption("TESTENV")
    TESTENV = TESTENV.upper()
    print("TESTENV", TESTENV)
    return TESTENV


@pytest.fixture(scope="session")
def input_build_id(pytestconfig):
    build_id = pytestconfig.getoption("build_id")
    print("build_id", build_id)
    return build_id


@pytest.fixture(scope="session")
def input_build_url(pytestconfig):
    build_url = pytestconfig.getoption("build_url")
    print("build_url", build_url)
    return build_url


@pytest.fixture(scope="session")
def input_pipeline_name(pytestconfig):
    pipeline_name = pytestconfig.getoption("pipeline_name")
    print("pipeline_name", pipeline_name)
    return pipeline_name


@pytest.fixture(scope="session")
def input_app_id(pytestconfig):
    APPID = pytestconfig.getoption("APPID")
    return APPID


@pytest.fixture(scope="session", autouse=True)
def marker_info(pytestconfig):
    marker_info_ts=(pytestconfig.getoption("-m"))
    return marker_info_ts

##----->This is to validate Marker(s)
def pytest_collection_modifyitems(config,items):
    global lst_usermarkers
    repo_markers = []
    lst_invalidmarkers = []
    flg_marker = False

    user_markers = config.getoption("markexpr", 'False')
    lst_usermarkers = user_markers.split(" or ")
    log.logger1.info("markers passed through terminal: " + str(lst_usermarkers))

    environment = config.getoption("TESTENV")
    # pipeline_name = config.getoption("pipeline_name")
    # build_id = config.getoption("build_id")
    # build_url = config.getoption("build_url")

    dict_invalidmarkers = {
        "environment": environment,
        # "build_id": build_id,
        # "build_url": build_url,
        # "pipeline_name": pipeline_name,
        "tool": "PYRAFT",
        "tags": ""
    }
    if user_markers == "":
        log.logger1.info("Selected testcase(s) will be executed")
    else:
        for item in items:
            lst_repomarkers = list(item.iter_markers())
            for repomkr in lst_repomarkers:
                if repomkr.name in repo_markers:
                    pass
                else:
                    repo_markers.append(repomkr.name)

        log.logger1.info("All markers present in the repo: " + str(repo_markers))

        for usermkr in lst_usermarkers:
            if usermkr in repo_markers:
                pass
            else:
                flg_marker = True
                lst_invalidmarkers.append(usermkr)

        dict_invalidmarkers["tags"] = lst_invalidmarkers

    ## 'when invalid tags/markers are found'##
    if flg_marker:
        log.logger1.error("Invalid marker(s)/tag(s) are used, hence aborting execution....")
        log.logger1.error("List of Invalid marker(s)/tag(s) are: " + str(dict_invalidmarkers["tags"]))
        # pynotify.send_alert_notification(application_info['azure_info']['email_list'],
        #                                  application_info['azure_info']['product'], "TEST",dict_invalidmarkers)
        raise RuntimeError("Invalid marker(s)/tag(s) are used", dict_invalidmarkers["tags"],"Hence aborting execution....")
