import utilities.report_utility.loggers as log

import pandas as pd
import re
import decimal
import random
import string
import json

from typing import List, Dict, Any
from utilities.db_utility.db import Database
from utilities.ui_utility.ui import update_step
from datetime import datetime, timedelta
from utilities.api_utility.file_read import ReadFile


class DynamicParameters:

    def __init__(self, set_env, dynamic_data_path=None):

        read_file = ReadFile()
        if dynamic_data_path is not None:
            self.dynamic_parameter_df: pd.DataFrame = read_file.read_sheet_df(dynamic_data_path)
            self.tc_dynamic_elements_list_dict = list()
            self.database_details_dict = dict()
            self.database_details = None
            self.set_env = set_env
            self.error_details = dict()
        self.tc_dynamic_value_dict = dict()

    def get_dynamic_sheet_details(self, in_tc_id):
        """
        Description: This method read dynamic data from csv file corresponding test case id provided\n
        :param in_tc_id: test case id mentioned in dynamic data csv file\n  
        : return: None
        """
        dp_list_dict = list()
        dp_row_dict = dict()
        dp_row_dict['STATUS'] = False

        try:
            self.dynamic_parameter_df.dropna(subset=["TC_ID"], inplace=True)

            self.dynamic_parameter_df['TC_ID'] = ',' + self.dynamic_parameter_df['TC_ID'].astype(str) + ','
            self.dynamic_parameter_df['TC_ID'] = self.dynamic_parameter_df['TC_ID'].astype(str).replace(' ', '',
                                                                                                        regex=True)

            dynamic_parameter_tc_df = self.dynamic_parameter_df.loc[
                self.dynamic_parameter_df['TC_ID'].str.contains(',' + str(in_tc_id) + ',')]
            dp_row_dict = dict()

            if len(dynamic_parameter_tc_df) > 0:
                for row in dynamic_parameter_tc_df.itertuples(index=True, name='pandas'):
                    dp_row_dict = dict()
                    dp_row_dict['STATUS'] = False

                    dp_row_dict['TC_ID'] = in_tc_id
                    dp_row_dict['TC_Desc'] = getattr(row, "TC_Desc")
                    dp_row_dict['ELEMENT_NAME'] = getattr(row, "ELEMENT_NAME")
                    dp_row_dict['DYNAMIC_IND'] = getattr(row, "DYNAMIC_IND")
                    dp_row_dict['PREDEFINED_VALUES'] = getattr(row, "PREDEFINED_VALUES")
                    dp_row_dict['DYNAMIC_ELEMENT_TYPE'] = getattr(row, "DYNAMIC_ELEMENT_TYPE")
                    dp_row_dict['ELEMENT_LENGTH'] = getattr(row, "ELEMENT_LENGTH")
                    dp_row_dict['DYNAMIC_VALUE_FORMAT'] = str(getattr(row, "DYNAMIC_VALUE_FORMAT"))
                    dp_row_dict['CHECK_IF_EXIST_IN_DB'] = getattr(row, "CHECK_IF_EXIST_IN_DB")
                    dp_row_dict['SQL_QUERY'] = getattr(row, "SQL_QUERY")
                    dp_row_dict['DATABASE_DETAILS'] = getattr(row, "DATABASE_DETAILS")

                    dp_row_dict['STATUS'] = True
                    dp_list_dict.append(dp_row_dict.copy())

            self.tc_dynamic_elements_list_dict = dp_list_dict.copy()
        except Exception as e:
            log.logger1.error(
                "Function get_dynamic_sheet_details :  Dynamic Parameter record Issue{0}\n Exception :{1}".format(
                    json.dumps(dp_row_dict), str(e)))
            raise Exception(
                "Function get_dynamic_sheet_details :  Dynamic Parameter record Issue{0}\n Exception :{1}".format(
                    json.dumps(dp_row_dict), str(e)))

    def set_dynamic_value_dict(self):
        """
        Description: This method helps to set dynamic values as configured in Dynamic data csv file\n
        : return: None
        """
        try:
            dynamic_data_dict = dict()
            dynamic_ele_dict_list = dict()

            for dp_row_dict in self.tc_dynamic_elements_list_dict:

                tc_id = dp_row_dict.get('TC_ID')
                test_case_name = dp_row_dict.get('TC_Desc')
                element_name = dp_row_dict.get('ELEMENT_NAME')
                dynamic_ind = dp_row_dict.get('DYNAMIC_IND')
                predefined_values = dp_row_dict.get('PREDEFINED_VALUES')
                dynamic_element_type = dp_row_dict.get('DYNAMIC_ELEMENT_TYPE')
                element_length = dp_row_dict.get('ELEMENT_LENGTH')
                dynamic_value_format = str(dp_row_dict.get('DYNAMIC_VALUE_FORMAT'))
                check_if_exist_in_db = dp_row_dict.get('CHECK_IF_EXIST_IN_DB')
                sql_query = dp_row_dict.get('SQL_QUERY')
                self.database_details = dp_row_dict.get('DATABASE_DETAILS')

                dynamic_ele_dict_val = None

                if dynamic_ind == 'Y':

                    if dynamic_element_type == 'FROM_SQL':
                        dynamic_ele_dict_val = self.get_val_from_sql(sql_query)
                    elif dynamic_element_type == 'SYSDATE':
                        dynamic_ele_dict_val = self.get_sysdate(element_length, dynamic_value_format)
                    elif str(dynamic_element_type).upper() == 'DATE':
                        dynamic_ele_dict_val = self.get_date(element_length, dynamic_value_format)
                    elif dynamic_element_type == 'Decimal':
                        dynamic_ele_dict_val = self.get_decimal(element_length)
                    elif str(dynamic_element_type).upper() == 'ALPHANUMERIC' \
                            or str(dynamic_element_type).upper() == 'ALPHABETS' \
                            or str(dynamic_element_type).upper() == 'NUMERIC':
                        if dynamic_value_format.strip() == '*':
                            item_type = self.get_item_type(dynamic_element_type)
                            dynamic_ele_dict_val = self.check_and_get_ele_dict_val(element_name, check_if_exist_in_db,
                                                                                   dynamic_element_type, item_type,
                                                                                   element_length,
                                                                                   sql_query)
                        else:
                            dynamic_ele_dict_val = self.check_and_get_ele_dict_val2(dynamic_value_format, element_name,
                                                                                    check_if_exist_in_db,
                                                                                    dynamic_element_type,
                                                                                    sql_query)
                    else:
                        raise Exception(f'Incorrect element_name {element_name} dynamic_element_type '
                                        f'{dynamic_element_type} or element_length {element_length}')

                elif dynamic_ind == 'N':
                    dynamic_pre_defined_list = str(predefined_values).replace(' ', '').split(",")
                    dynamic_ele_dict_list[element_name] = dynamic_pre_defined_list
                    """ To be coded"""

                    dynamic_ele_dict_val = dynamic_pre_defined_list[0]

                dynamic_data_dict[element_name] = dynamic_ele_dict_val
                dynamic_data_dict['TC_ID'] = tc_id
                dynamic_data_dict['TC_Desc'] = test_case_name

            self.tc_dynamic_value_dict = dynamic_data_dict.copy()

        except Exception as EX:
            log.logger1.error("function: set_dynamic_value_dict " + str(EX))
            raise Exception("function: set_dynamic_value_dict Unable to set the dynamic value : " + str(EX))

    def get_db_results(self, sql_query) -> Dict[Any, Any]:
        """
        Description: This method helps to connect to DB and execute Query and return Response in Dict format\n
        :param sql_query: sql query to execute\n
        :return: DB response in Dict format\n
        """
        if str(self.database_details) in self.database_details_dict.keys():
            db_obj = self.database_details_dict.get(str(self.database_details))
        else:
            db_obj = Database()
            self.database_details_dict[str(self.database_details)] = db_obj

            db_dict = self.set_env.get_db_connection(str(self.database_details))

            user_name = db_dict.get('username')
            secret_key = db_dict.get('secret_key')
            host = db_dict.get('hostName')
            port = db_dict.get('port')
            db_name = db_dict.get('dbName')

            db_obj.connect_oracle(user_name, secret_key, host, port, db_name)

        db_res_dict = db_obj.fetch_values(sql_query)
        return db_res_dict

    def get_dynamic_item_val(self, dynamic_item_list, dynamic_value_format):
        """
        Description: This method helps to update dynamic values as per configuration mentioned in Dynamic data file\n
        :param dynamic_item_list: Dynamic value list from dynamic data file\n
        :param dynamic_value_format: Dynamic data format which we required to be converted\n
        :return: updated dynamic values in Dict format\n
        """
        try:
            for dynamic_item in dynamic_item_list:
                dynamic_item = str(dynamic_item.replace("<", "").replace(">", ""))

                if dynamic_item.isnumeric():
                    item_type = string.digits
                elif dynamic_item.isalpha():
                    item_type = string.ascii_lowercase
                elif dynamic_item.isalnum():
                    item_type = string.digits + string.ascii_lowercase
                else:
                    item_type = string.ascii_lowercase

                dynamic_item_len = len(dynamic_item)
                dynamic_item_val: str = self.get_random_alphanumeric_string(item_type, dynamic_item_len)

                item = '{' + dynamic_item + '}'
                dynamic_value_format = dynamic_value_format.replace(item, dynamic_item_val, 1)

            dynamic_value_format_val = dynamic_value_format
            return dynamic_value_format_val

        except Exception as EX:
            raise Exception("Function get_dynamic_item_val : " + str(EX))

    @staticmethod
    def get_random_alphanumeric_string(chars, length) -> str:
        """
        Description: This method helps to generate random string based on input parameters\n
        :param chars: type of characters\n
        :param length: length of characters\n
        :return: return a random string\n
        """
        result_str = ''.join((random.choice(chars) for _ in range(int(length))))

        return str(result_str)

    def set_dynamic_values(self, columns_list, tc_list_dict: list, tc_id=None, dynamic_value_dict=None):
        """
        Description: This method helps to update dynamically generated values in main data file\n
        :param columns_list: Data list to be updated with dynamic values\n
        :param tc_list_dict: Test case steps\n
        :param tc_id: Test case id\n
        :param dynamic_value_dict: Dynamically generated values dict\n
        :return: return updated test case steps\n
        """
        log.logger1.info("Before Dynamic Update \n" + json.dumps(tc_list_dict))
        self.error_details.clear()
        try:
            if tc_id is not None:
                self.get_dynamic_sheet_details(tc_id)
                self.set_dynamic_value_dict()

            elif dynamic_value_dict is not None:
                self.tc_dynamic_value_dict.clear()
                self.tc_dynamic_value_dict = dynamic_value_dict

            tc_all_dynamic_elements = list()

            for tc_dict in tc_list_dict:
                for column in columns_list:
                    self.update_env_dynamic_elements_to_dict(tc_dict[column], tc_all_dynamic_elements)

            no_val_payload_dynamic_elements, status = self.check_dp_elements(tc_all_dynamic_elements.copy())

            if status:
                for tc_dict in tc_list_dict:
                    for column in columns_list:
                        col_text = str(tc_dict.get(column))
                        col_text = col_text.replace("{", '{{').replace("}", '}}')
                        col_text = col_text.replace("<<", '{').replace(">>", '}')

                        tc_dict[column] = col_text.format(**self.tc_dynamic_value_dict)

            else:
                log.logger1.error("Dynamic parameter not defined Either in Environment or Dynamic parameter sheet : "
                                  + ''.join(str(elem) for elem in no_val_payload_dynamic_elements))

                update_step("update all Dynamic parameters", "update all Dynamic parameters"
                            + "Dynamic parameters not defined either in Environment or Dynamic parameter "
                              "sheet : ", "FAIL", False)

            log.logger1.info("After Dynamic Update \n" + json.dumps(tc_list_dict))
            return tc_list_dict

        except Exception as EX:
            log.logger1.error("Dynamic parameter not defined Either in Environment or Dynamic parameter sheet")
            raise Exception("Exception from Dynamic Data Updater :" + str(EX))

    def update_env_dynamic_elements_to_dict(self, column, tc_all_dynamic_elements):
        """
        Description: This method helps to update dynamically generated values\n
        :param column: Dynamic value to be updated\n
        :param tc_all_dynamic_elements: list of all dynamic elements\n
        : return: None
        """
        dynamic_item_list = re.findall(r'<<.*?>>', str(column))
        if len(dynamic_item_list) > 0:
            for item in dynamic_item_list:
                item = str(item).replace('<<', '').replace('>>', '')
                tc_all_dynamic_elements.append(item)
                self.set_dynamic_value_dictionary(item)

    def set_dynamic_value_dictionary(self, item):
        """
        Description: This method helps to update dynamically generated values\n
        :param item: Dynamic value to be updated\n
        : return: None
        """
        if len(self.tc_dynamic_value_dict) > 0:
            if item not in self.tc_dynamic_value_dict.keys():
                item_val = self.set_env.getvalue(item)
                if item_val is not None:
                    self.tc_dynamic_value_dict[item] = item_val
        else:
            item_val = self.set_env.getvalue(item)
            if item_val is not None:
                self.tc_dynamic_value_dict[item] = item_val

    def check_dp_elements(self, tc_all_dynamic_elements):
        """
        Description: This method helps to check dynamic values are available or not\n
        :param tc_all_dynamic_elements: list of test cases\n
        :return: return dynamic value list if any, status\n
        """
        dp_keys = []
        for strings in self.tc_dynamic_value_dict.keys():
            strings = strings.replace(' ', '')
            dp_keys.append(strings)

        diff_set = set(tc_all_dynamic_elements) - set(dp_keys)
        no_val_payload_dynamic_elements = list(diff_set)

        if len(no_val_payload_dynamic_elements) > 0:
            status = False
        else:
            status = True

        return no_val_payload_dynamic_elements, status

    @staticmethod
    def get_item_type(dynamic_element_type):
        """
        Description: This method helps to identify dynamic value format type\n
        :param dynamic_element_type: dynamic element type\n
        :return: return dynamic element item type\n
        """
        try:
            if str(dynamic_element_type).upper() == 'ALPHANUMERIC':
                item_type = string.digits + string.ascii_lowercase
            elif str(dynamic_element_type).upper == 'ALPHABETS':
                item_type = string.ascii_uppercase + string.ascii_lowercase
            elif str(dynamic_element_type).upper() == 'NUMERIC':
                item_type = string.digits
            else:
                item_type = string.ascii_lowercase
            return item_type
        except Exception as EX:
            raise Exception("function get_item_type " + str(EX))

    def get_val_from_sql(self, sql_query):
        """
        Description: This method helps to get data from db\n
        :param sql_query: SQL query\n
        :return: return dynamic element value\n
        """
        try:
            db_res_dict = self.get_db_results(sql_query)
            if db_res_dict['no_of_records'] == 1:
                db_df = db_res_dict['output_data']
                if len(db_df.columns) == 1:
                    dynamic_ele_dict_val = str(db_df.values[0][0])
                    return dynamic_ele_dict_val
                else:
                    raise Exception(
                        "function get_val_from_sql " + "Error Message: " + 'The Query is returning Multiple Columns')
            else:
                raise Exception("function get_val_from_sql " + "Error Message: " + 'The Query is returning Multiple '
                                                                                   'Values')

        except Exception as EX:
            raise Exception("function get_val_from_sql " + str(EX))

    @staticmethod
    def get_sysdate(element_length, dynamic_value_format):
        """
        Description: This method helps to generate dynamic date value\n
        :param element_length: number \n
        :param dynamic_value_format: date format in  which dynamic value to be generated\n
        :return: return dynamic element value\n
        """
        try:
            if element_length == 'NOT' or len(str(element_length).strip()) == 0 or not str(
                    element_length).lstrip("-").isnumeric():
                element_length = 0

            dynamic_ele_dict_val = (
                    datetime.now().today() + timedelta(days=int(element_length))).strftime(dynamic_value_format)

            return dynamic_ele_dict_val
        except Exception as EX:
            raise Exception("function get_sysdate " + str(EX))

    @staticmethod
    def get_date(element_length, dynamic_value_format):
        """
        Description: This method helps to generate dynamic date value\n
        :param element_length: number \n
        :param dynamic_value_format: date format in  which dynamic value to be generated\n
        :return: dynamic_ele_dict_val: dynamic element value\n
        """
        try:
            if element_length == 'NOT' or len(str(element_length).strip()) == 0:
                range1 = 0
                range2 = 0
            else:
                range_values: List[str] = str(element_length).replace(' ', '').split(",")
                if len(range_values) > 2 or not str(range_values[0]).lstrip("-").isnumeric() or not str(
                        range_values[1]).lstrip("-").isnumeric():
                    raise Exception("function get_date " + 'Incorrect range given in the ELEMENT_LENGTH column')
                elif len(range_values) == 1:
                    range1 = 0
                    range2: int = int(range_values[0])
                elif len(range_values) == 2:
                    range1 = int(range_values[0])
                    range2 = int(range_values[1])
                else:
                    raise Exception("function get_date " + 'Incorrect range given in the ELEMENT_LENGTH column')

            if range1 > range2:
                temp = range1
                range1 = range2
                range2 = temp
            dynamic_ele_dict_val = (
                    datetime.now().today() + timedelta(days=random.randint(range1, range2))).strftime(
                dynamic_value_format)
            return dynamic_ele_dict_val

        except Exception as EX:
            return {"Error Message": 'get_date' + str(EX)}

    def get_decimal(self, element_length):
        """
        Description: This method helps to generate dynamic decimal value\n
        :param element_length: number of decimal points required\n
        :return: dynamic_ele_dict_val: dynamic element value\n
        """
        try:
            if len(str(element_length).strip(' ')) == 0:
                digit_len = 0
                decimal_len = 0
            else:
                decimal_lengths: List[str] = str(element_length).replace(' ', '').split(",")
                if len(decimal_lengths) > 2 or not str(decimal_lengths[0]).isnumeric() or not str(
                        decimal_lengths[1]).isnumeric():
                    digit_len = 0
                    decimal_len = 0
                elif len(decimal_lengths) == 1:
                    digit_len = int(decimal_lengths[0])
                    decimal_len = 0
                elif len(decimal_lengths) == 2:
                    digit_len = int(decimal_lengths[0])
                    decimal_len = int(decimal_lengths[1])
                else:
                    raise Exception(f"Error Message :  Invalid element_length {element_length}")

            if digit_len > 0:
                digit_val: int = int(self.get_random_alphanumeric_string(string.digits, digit_len))
            else:
                digit_val = 0

            if decimal_len > 0:
                decimal_val: int = int(self.get_random_alphanumeric_string(string.digits, decimal_len))
            else:
                decimal_val = 0

            dynamic_ele_dict_val = decimal.Decimal('%d.%d' % (digit_val, decimal_val))

            return dynamic_ele_dict_val
        except Exception as EX:
            raise Exception("Function get_decimal" + str(EX))

    def check_and_get_ele_dict_val(self, element_name, check_if_exist_in_db,
                                   dynamic_element_type, item_type, element_length,
                                   sql_query):
        """
        Description: This method helps to verify whether dynamically generated value is already exist in DB\n
        :param element_name: element name \n
        :param check_if_exist_in_db: Y/ N \n
        :param dynamic_element_type: element type like Numeric,Date,Alphanumeric,Alphabets,FROM_SQL,SYSDATE,Decimal \n
        :param item_type: item type\n
        :param element_length: length \n
        :param sql_query: SQL Query\n
        :return: dynamic_ele_dict_val: new dynamic element value if element is already available in DB\n
        """
        try:
            dynamic_ele_dict_val = self.get_random_alphanumeric_string(item_type, element_length)

            if check_if_exist_in_db == 'Y' and dynamic_element_type != 'FROM_SQL':
                while True:
                    sql_query_updated: str = str(sql_query).replace('<<', '{').replace('>>', '}')
                    ele_dict = dict()
                    ele_dict[element_name] = dynamic_ele_dict_val
                    sql_query_updated = sql_query_updated.format(**ele_dict)

                    db_res_dict = self.get_db_results(sql_query_updated)

                    if db_res_dict['no_of_records'] == 0 and db_res_dict['Sql_Execution_Status'] == 0:
                        break
                    else:
                        dynamic_ele_dict_val = self.get_random_alphanumeric_string(item_type, element_length)

            return dynamic_ele_dict_val

        except Exception as EX:
            raise Exception("Function check_and_get_ele_dict_val" + str(EX))

    def check_and_get_ele_dict_val2(self, dynamic_value_format, element_name, check_if_exist_in_db,
                                    dynamic_element_type,
                                    sql_query):
        """
        Description: This method helps to verify whether dynamically generated value is already exist in DB\n
        :param dynamic_value_format: format of dynamic value \n
        :param element_name: element name \n
        :param check_if_exist_in_db: Y/ N \n
        :param dynamic_element_type: element type like Numeric,Date,Alphanumeric,Alphabets,FROM_SQL,SYSDATE,Decimal\n
        :param sql_query: SQL Query\n
        :return: dynamic_ele_dict_val: new dynamic element value if element is already available in DB\n
        """
        try:
            dynamic_item_list = re.findall(r'<.*?>', dynamic_value_format)

            if len(dynamic_item_list) == 0:
                dynamic_ele_dict_val = dynamic_value_format

            else:

                dynamic_value_format = dynamic_value_format.replace('{', '{{').replace('}', '}}')
                dynamic_value_format = dynamic_value_format.replace('<', '{').replace('>', '}')

                dynamic_value_format_value = self.get_dynamic_item_val(dynamic_item_list.copy(),
                                                                       dynamic_value_format)

                if check_if_exist_in_db == 'Y' and dynamic_element_type != 'FROM_SQL':

                    while True:
                        sql_query_updated: str = str(sql_query).replace('<<', '{').replace('>>',
                                                                                           '}')
                        ele_dict = dict()
                        ele_dict[element_name] = dynamic_value_format_value
                        sql_query_updated = sql_query_updated.format(**ele_dict)

                        db_res_dict = self.get_db_results(sql_query_updated)

                        if db_res_dict['no_of_records'] == 0 \
                                and db_res_dict['Sql_Execution_Status'] == 0:
                            break
                        else:
                            dynamic_value_format_value = self.get_dynamic_item_val(
                                dynamic_item_list.copy(),
                                dynamic_value_format)

                dynamic_ele_dict_val = dynamic_value_format_value

            return dynamic_ele_dict_val

        except Exception as EX:
            raise Exception(
                "Function check_and_get_ele_dict_val2 : error in checking the element against database" + str(EX))
