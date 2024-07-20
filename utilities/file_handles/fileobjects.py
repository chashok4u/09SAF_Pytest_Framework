import datetime
import pytz
from datetime import datetime
import os
import shutil
import json
import random
import string
import pandas as pd
import utilities.report_utility.loggers as log


def check_file(file_path):
    """
    Description : This method used to check the files\n
    :param file_path: example :'c:\\Test\\sample.xlsx':\n
    :return: True or False
    """
    if os.path.exists(file_path):
        log.logger1.info("File exist. successfully verified  file")
        return True
    else:
        log.logger1.info("Please check in file in download folder")
        return False


def delete_file(file_path):
    """
    Description: This method used to delete the current file\n
    :param file_path: example :'c:\\Test\\sample.xlsx':\n
    :return: True or False
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        log.logger1.info("File exist. and delete local current file")
        return True
    else:
        log.logger1.info("file does not exist..")
        return False


def special_character_replace(input_string):
    """
    Description: This method used to replace the special characters based on input_string\n
    :param input_string: for example="hello world"\n
    :return: input_string
    """
    input_string = input_string.replace('   ', '_')
    input_string = input_string.replace('  ', '_')
    input_string = input_string.replace(' ', '_')
    input_string = input_string.replace(')', '')
    input_string = input_string.replace('(', '')
    input_string = input_string.replace('#', '')

    return input_string


def read_excel(excel_file_path, sheet_name=None):
    """Description:
        This method is used to read specific sheet data in excel file.\n
        If sheet name is None- This method read entire excel file.\n
    :param excel_file_path: absolute file path \n
        Example: r"C:\\Users\\Test\\Downloads\\OTE_Automation.xlsx;" -any file format\n
    :param sheet_name : sheet name
    :return: Returns DataFrame (in table format rows, columns)
    """
    try:
        temp_df = None
        if check_file(excel_file_path):
            temp_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            return temp_df
    except Exception as e:
        log.logger1.info(e)


def get_current_time_zone_timestamp(timezone):
    """
    Description :This method used to current time based on input timezone.\n
    :param timezone: 'Asia/Kolkata'\n
    :return: current time in '%m/%d/%Y-%I:%M:%S' format- as string\n
    """
    tz = pytz.timezone(timezone)
    ENTRY_CURREN_TIME_STAMP = ((datetime.now(tz=tz)).strftime('%m/%d/%Y-%I:%M:%S'))
    return str(ENTRY_CURREN_TIME_STAMP)


def pass_fail_count(test_case_result):
    """
    Description : This method used for internal purpose (utilities)\n
    :param test_case_result: it is list format which contains "PASS/Pass or FAIL/fail"\n
    :return: PASS/Pass or FAIL/Fail Test cases count
    """
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


def current_time_stamp_ddmmyyyhms():
    """
    Description :This method used to get current time stamp in DDMMYYH:M:S format\n
    :return: string: DDMMYYH:M:S\n
    """
    try:
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    except Exception as e:
        log.logger1.info(e)


def get_canonical_path(file_path):
    """
    Description: This method used to get files absolute path\n
    :param file_path: example :'c:\\Test\\sample.xlsx':\n
    :return: file path
    """
    return os.path.abspath(file_path)


def create_file_path(parent_path, child_parts, file_name, extension):
    """
    Description: This method is used to create the files path\n
    :param parent_path: users: 'c:\\'
    :param child_parts: automation folder : example :Test':\n
    :param file_name: example :'c:\\Test\\sample.xlsx':\n
    :param extension: .xlsx\n
    :return: 'c:\\Test\\sample.xlsx'
    """
    dir_path = os.pathsep.join([
        parent_path,
        os.pathsep.join(child_parts)
    ])
    os.makedirs(dir_path)
    return os.pathsep.join(dir_path, file_name + extension)


def is_file(path, d=None):
    """
    Description: IS it a file or not\n
    :param path: example :'c:\\Test\\sample.xlsx':\n
    :param d: None\n
    :return: True or False
    """
    p = path
    if d:
        p = os.path.join(d, p)
    return os.path.exists(p) and os.path.isfile(p)


def is_dir(path):
    """
    Description: This method is used to check path is exist or not\n
    :param path: example: 'c:\\Test\\sample.xlsx'\n
    :return: True or False
    """
    return os.path.exists(path) and os.path.isdir(path)


def is_absolute_path(path):
    """
    Description: This method help to get absolute path of the file\n
    :param path: example: c:\\Test\\sample.xlsx'\n
    :return: path
    """
    return os.path.isabs(path)


def validate_file(path):
    """
    Description: This method used to validate the file path\n
    :param path: example: c:\\Test\\sample.xlsx'\n
    :return: True or False
    """
    if not os.path.exists(path):
        raise Exception("File does not exist.")
    elif os.path.isfile(path):
        raise Exception("Not a file.")


def validate_dir(path):
    """
    Description: This method used to validate the directory path\n
    :param path: example: 'c:\\Test\\sample.xlsx'\n
    :return: True or False
    """
    if not os.path.exists(path):
        raise Exception("Directory does not exist.")
    elif os.path.isfile(path):
        raise Exception("Not a directory.")


def get_file_modified_time_stamp(path):
    """
    Description: This method used to get file modified time\n
    :param path: example: 'c:\\Test\\sample.xlsx'\n
    :return: Modified time
    """
    return os.path.getmtime(path)


def get_latest_file_path_from_dir(path):
    """
    Description: This method used to get the latest directory path\n
    :param path: example: 'c:\\Test\\sample.xlsx'\n
    :return: last(latest directory path)
    """
    check = 0
    last = None
    for f in os.listdir(path):
        m = get_file_modified_time_stamp(os.pathsep.join(path, f))
        if m > check:
            check = m
            last = m
    return last


def delete_dir(dir_path):
    """
    Description: This method used to delete directory path\n
    :param dir_path: example: 'c:\\Test\\sample.xlsx'\n
    :return: True or False
    """
    validate_dir(dir_path)
    shutil.rmtree(dir_path)


def delete_dir_if_exists(path):
    """
    Description: This method used to delete the directory if file exists\n
    :param path: example: 'c:\\Test\\sample.xlsx'\n
    :return: True or False
    """
    if not os.path.exists(path): return
    if not is_dir(path):
        raise Exception("{} is not a directory.".format(path))
    shutil.rmtree(path)


def copy_file(src_file, dest_file):
    """
    Description: This method used to copy the file from src location to destination location\n
    :param src_file: example: 'c:\\Test\\sample.xlsx'\n
    :param dest_file: example: 'c:\\Test\\sample1.xlsx'\n
    :return: True or False
    """
    validate_file(src_file)
    validate_dir(os.path.dirname(dest_file))
    shutil.copy2(src_file, dest_file)


def copy_file_to_dir(src_file, dest_dir):
    """
    Description: This method used to copy the file to directory\n
    :param src_file: example: 'c:\\Test\\sample.xlsx'\n
    :param dest_dir: example: 'c:\\Test\\dir'\n
    :return: True or False
    """
    validate_file(src_file)
    validate_dir(dest_dir)
    shutil.copy2(src_file, dest_dir)


def move_file_to_dir(src_file, dest_dir):
    """
    Description: This method used to move the file from src to destition directory\n
    :param src_file: example: 'c:\\Test\\sample.xlsx'\n
    :param dest_dir: example: 'c:\\Test\\dir'\n
    :return: True or False
    """
    shutil.move(src_file, dest_dir)
    return os.pathsep.join(dest_dir, os.path.basename(src_file))


def create_empty_file(path):
    """
    Description: This method used to create empty file\n
    :param path: example : 'c:\\Test\\sample.txt'\n
    :return: True or False
    """
    os.makedirs(os.path.dirname(path))
    f = open("path", "w")
    f.close()


def __base_name_parts(fpath):
    """
    :param fpath:
    :return:
    """
    name = os.path.basename(fpath)
    main, *ext = name.rsplit(".", 1)
    if ext:
        return main, ext[0]
    else:
        return main, ""


def get_extension(fpath):
    """
    Description: This method used to get the file extension\n
    :param fpath: example: 'c:\\Test\\sample.xlsx'\n
    :return: extension of file
    """
    return __base_name_parts(fpath)[1]


def read_json(filepath):
    """
    Description: This method help to Read Json file in key and value pair based on input file\n
    :param filepath: example: 'c:\\Test\\sample.json'\n
    :return: dictionary object
    """
    file_sys_directory = os.path.normpath(filepath)
    file = open(file_sys_directory, 'r')
    json_inputs = file.read()
    try:
        request_json = json.loads(json_inputs)
        return request_json
    except Exception as e:
        return e


def time_difference(starttime, endtime):
    """
    Description: This method helps to get the time difference of two methods\n
    :param starttime: example: s1 = '10:33:26'\n
    :param endtime: example: s2 = '11:15:49'\n
    :return: hh:mm:ss
    """

    format_time = '%m/%d/%Y-%I:%M:%S'
    tdelta = datetime.strptime(endtime, format_time) - datetime.strptime(starttime, format_time)
    days, seconds = tdelta.days, tdelta.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    tdelta = '{}:{}:{}'.format(hours, minutes, seconds)
    return tdelta


def read_json_data(filename):
    """
    Description: This method help to read json dat\n
    :param filename: examlple: 'sample.json'\n
    :return: dictionary object
    """
    file_sys_directory = os.path.normpath(os.path.join(os.path.dirname(__file__), filename))
    file = open(file_sys_directory, 'r')
    json_inputs = file.read()
    try:
        request_json = json.loads(json_inputs)
        return request_json
    except Exception as e:
        return e


def generate_random_string(count=5):
    """
    Description: this method help to generate random string (5 characters- as by default).\n
     User can specify the number characters
    :param count: int example - 1 or 2 or .....or 9
    :return: random string
    # val = ''.join(random.choice(letters) for i_char in range(string_length))
    # return val
    """
    try:
        alpha_numeric = ''.join(random.sample((string.ascii_uppercase + string.digits), int(count)))
        return alpha_numeric
    except Exception as Ex:
        log.logger1.info("Unable to process. " + str(Ex))
        update_step("Generate Random Alpha Numeric String", "Error in execution " + str(Ex), "FAIL", False)
        return False


def label_status(row):
    """
    description : This is internal method used for get label update
    :return:  Pass/Fail
    """
    if int(row['total_steps']) > 0:
        if int(row['total_steps']) == int(row['pass_steps']) and int(row['total_steps']) != 0:
            return 'PASS'
        else:
            return 'FAIL'
    else:
        return "FAIL"
