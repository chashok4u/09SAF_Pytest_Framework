import json
import os
import re
import traceback
from datetime import datetime

import pandas as pd
import requests
import urllib3
import utilities.report_utility.loggers as log

from utilities.config._config import CURRENT_DIR
from deepdiff import DeepDiff
from flatten_json import flatten_json
from jsontable import jsontable

from utilities.api_utility.dynamic_data_updater import DynamicParameters
from utilities.api_utility.filter_json import Filterjson
from utilities.api_utility.file_read import ReadFile
from utilities.api_utility.api_utility import APIRequest
from utilities.db_utility.db import Database
from utilities.ui_utility.ui import update_step

read_file = ReadFile()
api = APIRequest()


class APIValidations:

    def __init__(self, set_env, test_case_path, dynamic_data_path=None):
        self.test_case_sheet_df: pd.DataFrame = read_file.read_sheet_df(test_case_path)
        self.db_connection_dict = dict()
        self.in_tc_id = 0
        self.set_env = set_env

        if dynamic_data_path is None:
            self.dynamic_tc_flag = 'N'
            self.dy_parm = DynamicParameters(set_env)
        else:
            self.dynamic_tc_flag = 'Y'
            self.dy_parm = DynamicParameters(set_env, dynamic_data_path)

    def get_test_case_details(self, in_tc_id):
        """
        Description: This method is used to get the variables from CSV for a given test case and returns csv dictionary
        :param in_tc_id: relative path of test data sheet
        :return csv_dict: dictionary with necessary key values
        """
        tc_list_dict = list()
        tc_row_dict = dict()
        tc_row_dict['STATUS'] = False

        try:
            test_case_df = self.test_case_sheet_df.loc[self.test_case_sheet_df['TC_ID'] == in_tc_id]
            if len(test_case_df) == 0:
                update_step(in_tc_id, in_tc_id + " should be available in sheet",
                            "Test case not found in the test data Sheet", False)
                return tc_list_dict

            else:
                for row in test_case_df.itertuples(index=True, name='pandas'):
                    tc_row_dict = dict()
                    tc_row_dict['STATUS'] = False
                    tc_row_dict['TC_ID'] = getattr(row, "TC_ID")
                    tc_row_dict['TC_Desc'] = getattr(row, "TC_Desc")
                    tc_row_dict['EndPointURL'] = getattr(row, "EndPointURL")
                    tc_row_dict['Data'] = getattr(row, "Data")
                    tc_row_dict['Method'] = getattr(row, "Method")
                    tc_row_dict['POST_Request_Payload'] = getattr(row, "POST_Request_Payload")
                    tc_row_dict['Username'] = getattr(row, "Username")
                    tc_row_dict['SecretKey'] = getattr(row, "SecretKey")
                    tc_row_dict['Parameters'] = getattr(row, "Parameters")
                    tc_row_dict['Headers_Key'] = getattr(row, "Headers_Key")
                    tc_row_dict['Headers_Value'] = getattr(row, "Headers_Value")
                    tc_row_dict['Headers'] = getattr(row, "Headers")
                    tc_row_dict['Response_Code'] = getattr(row, 'Response_Code')
                    tc_row_dict['DBVerificationFlag'] = getattr(row, 'DBVerificationFlag')
                    tc_row_dict['FilterRecordKey'] = getattr(row, 'FilterRecordKey')
                    tc_row_dict['sqlQuery'] = getattr(row, 'sqlQuery')
                    tc_row_dict['ValidateResponseElements'] = getattr(row, 'ValidateResponseElements')
                    tc_row_dict['ValidateRequestPayLoadJsonElements'] = getattr(row,
                                                                                'ValidateRequestPayLoadJsonElements')
                    tc_row_dict['TargetDBConnectionDetails'] = getattr(row, 'TargetDBConnectionDetails')
                    tc_row_dict['ExpectedResponse'] = getattr(row, 'ExpectedResponse')
                    tc_row_dict['WaitForSync'] = getattr(row, 'WaitForSync')
                    tc_row_dict['Tag'] = getattr(row, 'Tag')

                    tc_row_dict['STATUS'] = True
                    tc_list_dict.append(tc_row_dict.copy())

            return tc_list_dict
        except Exception as e:
            actual_result = "Exception occurred  " + str(e)
            update_step("File Issue", " File Issue", actual_result, False)
            raise Exception("Function get_test_case_details: Error File Issue : " + str(e))

    @staticmethod
    def get_headers(key, value):
        """
        Description: This method is used to get headers format.
        :param key: Headers Key
        :param value: Headers Value
        :return: Headers Format
        """
        if str(key).upper() == "CONTENT-TYPE":
            headers = {"'Content-Type': '" + value + "'"}
        if str(key).upper() == "AUTHORIZATION-BASIC":
            headers = {'Authorization': 'Basic {}'.format(value)}
        if str(key).upper() == "AUTHORIZATION-BEARER":
            headers = {'Authorization': 'Bearer {}'.format(value)}
        return headers

    def get_request_attributes(self, tc_row_dict):
        """
        Description: This method is used to get the variables from CSV for a given test case and returns csv dictionary
        :param tc_row_dict: relative path of test data sheet
        :return csv_dict: dictionary with necessary key values
        """
        api_attribute = dict()

        method = tc_row_dict['Method']
        data = tc_row_dict['Data']
        end_point_url = tc_row_dict['EndPointURL']
        parameters = tc_row_dict['Parameters']
        headers_key = tc_row_dict['Headers_Key']
        headers_value = tc_row_dict['Headers_Value']
        headers = tc_row_dict['Headers']
        post_request_payload = tc_row_dict['POST_Request_Payload']
        username = tc_row_dict['Username']
        secret_key = tc_row_dict['SecretKey']
        response_code = tc_row_dict['Response_Code']

        api_attribute['REQUEST_METHOD'] = method

        self.set_end_point_url(api_attribute, end_point_url, data)
        self.set_parameters(api_attribute, parameters)
        self.set_header(api_attribute, headers_key, headers_value)
        self.set_headers(api_attribute, headers)
        self.set_request_payload(api_attribute, post_request_payload)
        self.set_username(api_attribute, username)
        self.set_secret_key(api_attribute, secret_key)
        self.set_response_code(api_attribute, response_code)

        return api_attribute.copy()

    @staticmethod
    def set_end_point_url(api_attribute, end_point_url, data):
        """
        Description: This method is used to set end point URL
        :param api_attribute: temp dict
        :param end_point_url: end point URL
        :param data: data if any
        : return: None
        """
        if data == "NOT":
            api_attribute['ACT_END_POINT'] = end_point_url
        else:
            api_attribute['ACT_END_POINT'] = end_point_url + data

    @staticmethod
    def set_parameters(api_attribute, parameters):
        """
         Description: This method is used to set parameters
         :param api_attribute: temp dict
         :param parameters: parameters if any
         : return: None
         """
        if parameters == "NOT":
            api_attribute['PARAMETERS'] = None
        else:
            api_attribute['PARAMETERS'] = json.loads(parameters)

    def set_header(self, api_attribute, headers_key, headers_value):
        """
         Description: This method is used to set headers
         :param api_attribute: temp dict
         :param headers_key: Header key
         :param headers_value: Header value
         : return: None
         """
        if headers_key == "NOT" and headers_value == "NOT":
            api_attribute['HEADER'] = None
        else:
            api_attribute['HEADER'] = self.get_headers(headers_key, headers_value)

    @staticmethod
    def set_headers(api_attribute, headers):
        """
        Description: This method is used to set headers
        :param api_attribute: temp dict
        :param headers: headers dictionary
        : return: None
        """
        if headers == "NOT":
            api_attribute['HEADERS'] = None
        else:
            api_attribute['HEADERS'] = eval(headers)

    @staticmethod
    def set_request_payload(api_attribute, post_request_payload):
        """
         Description: This method is used to set request payload
         :param api_attribute: temp dict
         :param post_request_payload: payload
         : return: None
         """
        if post_request_payload == "NOT":
            api_attribute['REQUEST_PAYLOAD'] = ""
        else:
            api_attribute['REQUEST_PAYLOAD'] = json.loads(post_request_payload)

    @staticmethod
    def set_username(api_attribute, username):
        """
         Description: This method is used to set username
         :param api_attribute: temp dict
         :param username: username
         : return: None
         """
        if username == "NOT":
            api_attribute['USERNAME'] = None
        else:
            api_attribute['USERNAME'] = username

    @staticmethod
    def set_secret_key(api_attribute, secret_key):
        """
        Description: This method is used to set secret key
        :param api_attribute: temp dict
        :param secret_key: secret key
        : return: None
        """
        if secret_key == "NOT":
            api_attribute['SECRET_KEY'] = None
        else:
            api_attribute['SECRET_KEY'] = secret_key

    @staticmethod
    def set_response_code(api_attribute, response_code):
        """
         Description: This method is used to set response json
         :param api_attribute: temp dict
         :param response_code: response json
         : return: None
         """
        if response_code == "NOT":
            api_attribute['RESPONSE_CODE'] = None
        else:
            api_attribute['RESPONSE_CODE'] = response_code

    @staticmethod
    def get_proxies(proxies_list):
        """
        Description:
        :param proxies_list:
        :return: proxies
        """
        try:
            if "YES" in proxies_list.upper():
                proxies = {
                    "http": None,
                    "https": None,
                }
            elif "NO" in proxies_list.upper():
                proxies = None
            else:
                proxies = json.loads(proxies_list)
        except Exception as e:
            proxies = None
        return proxies

    @staticmethod
    def json_table_dataframe(json_data):
        """
        Description: This method is used to convert the nested json or flat json to table row column format
        :param json_data: json load object returned from json_loads json.loads(response.content)
        :return json_df: dataframe having all the elements in Json file in table row column format
        """
        try:
            json_tree_list = []
            if not isinstance(json_data, dict):
                da = pd.DataFrame(json_data)
                da.columns = map(str.upper, da.columns)
                return da
            else:
                flat_json_df = flatten_json(json_data)

                for key, val in flat_json_df.items():
                    node = re.sub('_+?[0-9]+_', '.', key)
                    node = str(node).replace("_", ".")
                    node = node.replace("..", ".")
                    if node not in json_tree_list:
                        json_tree_list.append(node)

                act_json_col_list = [x.split(".")[-1] for x in json_tree_list]
                # json_col_list = [x.split(".")[-1].upper() for x in json_tree_list]

                json_tree_list = [{str("$.") + x: x.split(".")[-1].upper()} for x in json_tree_list]

                converter = jsontable.converter()
                converter.set_paths(json_tree_list)
                lst = converter.convert_json(json_data)

                json_df = pd.DataFrame(lst, columns=act_json_col_list)
                json_df = json_df[1:]

                return json_df
        except Exception as e:
            raise Exception("Function json_table_dataframe " + str(e))

    @staticmethod
    def validate_expected_json(tc_id, str_expected_response, response_dict):
        """
         Description: This method is used to validate expected json with actual response json
         :param tc_id: test case id
         :param str_expected_response: expected response
         :param response_dict: response as dictionary format
         : return: None
         """
        try:
            if str_expected_response != 'NOT':

                str_expected_response = str_expected_response.replace("{", '{{').replace("}", '}}')
                str_expected_response = str_expected_response.replace("<<", '{').replace(">>", '}')
                str_expected_response = str_expected_response.format(**response_dict)

                expected_response = json.loads(str_expected_response)

                diff = DeepDiff(expected_response, response_dict)

                if len(diff.to_dict().keys()) == 0:
                    log.logger1.info("Response Json is same as expected")
                    update_step(tc_id, "Verify response Json is same as expected"
                                + "Response Json is same as expected", "Pass", True)
                else:
                    log.logger1.info(f"Response Json is not same as expected "
                                     f"\n Expected: \n{str_expected_response} "
                                     f"\nActual:\n{response_dict}"
                                     f"\n difference:\n {diff}")

                    update_step(tc_id, "Verify response Json is same as expected"
                                + f"Response Json is not same as expected "
                                  f"\n Expected: \n{str_expected_response}"
                                  f"\nActual:\n{response_dict}\n"
                                  f"difference:\n {diff} ", "Fail", False)
        except Exception as e:
            raise Exception("Function validate_expected_json " + str(e))

    def verify_rest_api(self, in_tc_id):
        """
        Description: This method is used verify the value of json element/s with database column/s
        :param in_tc_id: dictionary with db connection details
        :return True/False: return True if the elements match with database else return False
        """
        self.in_tc_id = in_tc_id
        urllib3.disable_warnings()

        tc_list_dict = self.get_test_case_details(in_tc_id)

        try:
            env = str(self.set_env.getenvironment()).lower()
            self.check_post_prod(env, tc_list_dict.copy())

            api_req_dp_columns_list = ['TC_Desc', 'EndPointURL', 'Data', 'POST_Request_Payload', 'Username',
                                       'SecretKey', 'Parameters', 'Headers_Key', 'Headers_Value', 'Headers',
                                       'Response_Code']

            if self.dynamic_tc_flag == 'Y':
                tc_list_dict = self.dy_parm.set_dynamic_values(api_req_dp_columns_list,
                                                               tc_list_dict.copy(), in_tc_id)
            else:
                tc_list_dict = tc_list_dict

            response_payload_dict = dict()
            json_req_res_dict = dict()

            for tc_row_dict in tc_list_dict:

                row_status = tc_row_dict.get('STATUS')

                if row_status:
                    api_attributes_dict = self.get_request_attributes(tc_row_dict)
                    response_code = api_attributes_dict.get('RESPONSE_CODE')

                    res = self.get_res(tc_row_dict, api_attributes_dict, response_payload_dict, json_req_res_dict)

                    if isinstance(res, requests.Response) and api.verify_response_code(res, response_code):
                        response_payload_dict, json_req_res_dict = \
                            self.update_dynamic_val_dict(res,
                                                         api_attributes_dict,
                                                         tc_row_dict,
                                                         response_payload_dict,
                                                         json_req_res_dict)
                    elif res != 'NOT' \
                            and not isinstance(res, requests.Response) \
                            and not api.verify_response_code(res, response_code):
                        break

        except Exception as ex:
            log.logger1.error('Exception Occurred ' + str(ex))
            tb = traceback.format_exc()
            log.logger1.exception("Exception Details: \n" + str(tb))

    def check_post_prod(self, env, tc_list_dict):
        """
         Description: This method is used to check the test case is allowed to execute in prod or not
         :param env: environment name
         :param tc_list_dict: test cases
         : return: None
         """
        post_check_df = pd.DataFrame(tc_list_dict)

        if env == 'prod':
            list_methods: list = post_check_df['Method']
            if any("POST" in s for s in list_methods) or any("PUT" in s for s in list_methods) \
                    or any("PUT" in s for s in list_methods):
                if self.post_method_validation(post_check_df):
                    return True
                else:
                    raise Exception('Cannot Run Post in PROD')

                put_df = self.test_case_sheet_df.loc[self.test_case_sheet_df['Method'] == 'PUT']
                if len(put_df) > 0:
                    update_step("Cannot Run PUT in PROD' ", "Cannot Run Post in PROD' ",
                                "Fail",
                                False)
                    raise Exception('Cannot Run PUT in PROD')

                del_df = self.test_case_sheet_df.loc[self.test_case_sheet_df['Method'] == 'DELETE']
                if len(del_df) > 0:
                    update_step("Cannot Run DELETE in PROD' ", "Cannot Run Post in PROD' ",
                                "Fail",
                                False)

                    raise Exception('Cannot run DELETE in PROD')

    def post_method_validation(self,post_check_df):
        """
        Description: This method is used to connect to DB and execute query
        :param:post_check_df: methods (GET/POST/PUT/DELETE) given in input file in dataframe format
        : return: True/ False
        """
        post_df = post_check_df.loc[post_check_df['Method'] == 'POST']
        if len(post_df) > 0:
            post_list_dict = post_df.to_dict('r')
            for post_dict in post_list_dict:
                if post_dict.get('Tag') != 'Override_prod':
                    update_step("Cannot Run Post in PROD' ", "Cannot Run Post in PROD' ",
                                "Fail",
                                False)
                    return False
                else:
                    return True

    def get_val_from_database(self, tc_row_dict, response_payload_dict, json_req_res_dict):
        """
         Description: This method is used to connect to DB and execute query
         :param tc_row_dict: test cases
         :param response_payload_dict: response payload
         :param json_req_res_dict: request payload
         : return: None
         """
        try:

            if tc_row_dict['DBVerificationFlag'] == 'Y':
                api_response_dp_column_list = ['TC_ID', 'TC_Desc', 'FilterRecordKey', 'sqlQuery',
                                               'ValidateResponseElements',
                                               'ValidateRequestPayLoadJsonElements',
                                               'TargetDBConnectionDetails', 'WaitForSync']

                api_db_val_tc_dict = dict()

                for column in api_response_dp_column_list:
                    api_db_val_tc_dict[column] = tc_row_dict.get(column)

                tc_api_res_list_dict = list()

                tc_api_res_list_dict.append(api_db_val_tc_dict)

                updated_tc_api_res_dict = self.dy_parm.set_dynamic_values(
                    api_response_dp_column_list,
                    tc_api_res_list_dict.copy(), None,
                    response_payload_dict.copy())

                tc_api_res_dict = updated_tc_api_res_dict[0]

                test_col_list_response = tc_row_dict['ValidateResponseElements']

                test_col_list_payload = tc_row_dict['ValidateRequestPayLoadJsonElements']

                if test_col_list_response != 'NOT' and test_col_list_payload == 'NOT':

                    self.validate_json_db(json_req_res_dict.get('RESPONSE'), tc_api_res_dict,
                                          test_col_list_response)

                elif test_col_list_response == 'NOT' and test_col_list_payload != 'NOT':
                    json_payload_data = json_req_res_dict.get('PAYLOAD')
                    print(json_payload_data)
                    self.validate_json_db(json_payload_data, tc_api_res_dict, test_col_list_payload)

                elif test_col_list_response == 'NOT' and test_col_list_payload == 'NOT':
                    try:
                        db_connection_details_dict = self.set_env.get_db_connection(
                            str(tc_row_dict['TargetDBConnectionDetails']))

                        db_connection_details_dict['sqlQuery'] = str(tc_row_dict['sqlQuery'])
                        user_name = db_connection_details_dict.get('username')
                        secret_key = db_connection_details_dict.get('secret_key')
                        host = db_connection_details_dict.get('hostName')
                        port = db_connection_details_dict.get('port')
                        db_name = db_connection_details_dict.get('dbName')
                        sql_query = tc_api_res_dict.get('sqlQuery')

                        connect_str = ','.join(db_connection_details_dict.values())

                        db_obj = self.get_db_obj(connect_str, db_name, host, port, user_name, secret_key)

                        cur = db_obj.cursor
                        cur.execute(sql_query)

                        row_count = cur.rowcount  # Add for rowcount fetching - Gopal
                        cur.execute('commit')  # Add for update/delete query - Gopal

                        update_step(tc_row_dict['TC_Desc'],
                                    f"Executed update/delete query - [{sql_query}] - successfully",
                                    f"Successfully updated / deleted [{row_count}] rows - Pass",
                                    True)
                    except Exception as e:
                        raise Exception("Unable to connect to database" + str(e))
        except Exception as e:
            raise Exception("Function get_val_from_database " + str(e))

    def get_db_obj(self, connect_str, db_name, host, port, user_name,secret_key):
        """
        Description: This method is used to connect to DB and execute query
        :param connect_str: connection string which is combination of host,port,dbname, username & secret key
        :param db_name: db name
        :param host: host name
        :param port: port number
        :param user_name: username
        :param secret_key: secret key
        : return: db_obj
        """
        if connect_str in self.db_connection_dict.keys():
            db_obj = self.db_connection_dict.get(connect_str)

        else:
            db_obj = Database()
            db_obj.connect_oracle(user_name, secret_key, host, port, db_name)
            self.db_connection_dict[connect_str] = db_obj
        return db_obj

    def sql_out_dataframe(self, db_connection_details_dict, test_description="Test"):
        """
        Description: This method is used to connect database, fetch the query result into dataframe and write the query
                     results to a csv file
        :param db_connection_details_dict: as dictionary values
            user_name  =db_connection_details_dict.get('username')
            secret_key   =db_connection_details_dict.get('secret_key')
            host       =db_connection_details_dict.get('hostName')
            port       =db_connection_details_dict.get('port')
            db_name    =db_connection_details_dict.get('dbName')
            sql_query  =db_connection_details_dict.get('query')
        :param test_description: test case description used for file name
        :return sql_out_df: Query result as dataframe
        """
        user_name = db_connection_details_dict.get('username')
        secret_key = db_connection_details_dict.get('secret_key')
        host = db_connection_details_dict.get('hostName')
        port = db_connection_details_dict.get('port')
        db_name = db_connection_details_dict.get('dbName')
        sql_query = db_connection_details_dict.get('sqlQuery')

        try:
            try:
                connect_str = ','.join(db_connection_details_dict.values())
                db_obj = self.get_db_obj(connect_str, db_name, host, port, user_name, secret_key)
            except Exception as e:
                update_step('Unable to connect to Db ', "Unable to connect to Db", 'Fail', False)
                traceback.print_exc()
                raise Exception("Unable to connect to Db " + str(e))

            sql_out_df = db_obj.fetch_values(sql_query)

            if sql_out_df['Sql_Execution_Status'] == 0:
                current_time_stamp = (datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
                query_out_path = os.path.normpath("".join([CURRENT_DIR, os.path.sep, "QueryOut",
                                                           current_time_stamp, str(self.in_tc_id), "-",
                                                           str(test_description)[1:10], ".csv"]))
                sql_out_df['output_data'].to_csv(query_out_path, index=False)

                return sql_out_df

        except Exception as e:
            actual_result = "Exception occurred " + str(e)
            update_step(test_description, "Query output", actual_result, False)
            tb = traceback.format_exc()
            raise Exception("Unable to connect to Db " + str(e) + "\n" + str(tb))

    @staticmethod
    def dataframe_difference(dataframe1, dataframe2):
        """
         Description: This method is used to compare the two dataframes and returns the difference using outer join
        :param dataframe1: Dataframe 1
        :param dataframe2: Dataframe 2
        :return diff_dataframe: dataframe with differences in left and right dataframes
        """
        dataframe2 = dataframe2.astype(str)
        dataframe1 = dataframe1.astype(str)

        dataframe1 = dataframe1.replace('nan', 'None')
        dataframe2 = dataframe2.replace('nan', 'None')

        dataframe1 = dataframe1.replace('None', '')
        dataframe2 = dataframe2.replace('None', '')

        which = None
        comparison_df = dataframe1.merge(dataframe2, indicator=True, how='outer')

        if which is None:
            diff_dataframe = comparison_df[comparison_df['_merge'] != 'both']
        else:
            diff_dataframe = comparison_df[comparison_df['_merge'] == which]

        try:
            if (diff_dataframe.empty):
                update_step("validate dataframe differance", "Database and Denodo view records got matched", "diff_dataframe", True)
            else:
                update_step("validate dataframe differance", "Database and Denodo view records not matched", "diff_dataframe", False)
        except Exception as EX:
            update_step("validate dataframe differance", "Exception occured in data frame differance", str(EX), False)

        return diff_dataframe

    def validate_json_db(self, json_data: str, api_db_val_tc_dict: dict, test_cols):
        """
         Description: This method is used to compare DB query response against json response
         :param json_data: json data
         :param api_db_val_tc_dict: data from input file as dict
         :param test_cols: columns to compare
         :return boolean
         """
        # TC_ID = api_db_val_tc_dict['TC_ID']
        tc_desc = api_db_val_tc_dict['TC_Desc']
        filter_record_key = api_db_val_tc_dict['FilterRecordKey']
        target_db_connection_details = api_db_val_tc_dict['TargetDBConnectionDetails']
        sql_query = api_db_val_tc_dict['sqlQuery']
        WaitForSync = api_db_val_tc_dict['WaitForSync']

        db_connection_details_dict = self.set_env.get_db_connection(str(target_db_connection_details))

        db_connection_details_dict['sqlQuery'] = sql_query

        test_col_list = str(test_cols).replace(' ', '').split(',')

        expected_results = "Data element/elements " + test_cols + " should be same as in Database"

        try:
            if filter_record_key != 'NOT':
                res_obj = Filterjson()
                res_json = res_obj.getvalue(json_data, filter_record_key)
                if isinstance(res_json, list):
                    json_df = self.json_table_dataframe(res_json)
                elif isinstance(res_json, dict):
                    json_df = self.json_table_dataframe(list(res_json))
                elif isinstance(res_json, str):
                    temp_dict = dict()
                    temp_dict[filter_record_key] = res_obj
                    json_df = self.json_table_dataframe(list(res_json))
                else:
                    json_df = pd.DataFrame()
            else:
                json_df = self.json_table_dataframe(json_data)

            json_df = json_df.reset_index()

            test_col_list = [x.upper() for x in test_col_list]
            json_df.columns = map(lambda x: str(x).upper(), json_df.columns)

            diff_columns = list(set(test_col_list) - set(json_df.columns.values))

            for d_col in diff_columns:
                list_temp = []
                for _ in range(0, len(json_df)):
                    list_temp.append(str('None'))
                json_df[d_col] = list_temp

            json_df = json_df[test_col_list]

            sql_out_df_dict = self.sql_out_dataframe(db_connection_details_dict, tc_desc)

            if sql_out_df_dict['Sql_Execution_Status'] == 0:
                sql_out_df = sql_out_df_dict['output_data'].reset_index(drop=True)

                json_df[json_df.columns] = json_df.astype(str)
                json_df[json_df.columns] = json_df.apply(lambda x: x.str.strip())
                sql_out_df[sql_out_df.columns] = sql_out_df.astype(str)
                sql_out_df[sql_out_df.columns] = sql_out_df.apply(lambda x: x.str.strip())

                diff_dataframe = self.dataframe_difference(json_df, sql_out_df)

                if len(diff_dataframe) == 0:
                    actual_result = "Data element/elements " + ','.join(test_col_list) + \
                                    " compared with Database and are same"
                    update_step(tc_desc, expected_results, actual_result, True)
                    return True
                else:
                    actual_result = "Data element/elements " + ','.join(test_col_list) \
                                    + " compared with Database and are not same"
                    current_time_stamp = (datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
                    data_diff_path = os.path.normpath("".join([CURRENT_DIR, os.path.sep, "diffFile",
                                                               current_time_stamp, tc_desc, ".csv"]))
                    diff_dataframe.to_csv(data_diff_path, index=False)
                    update_step(tc_desc, expected_results, actual_result, False)
                    return False
        except Exception as e:
            actual_result = "Exception occurred  " + str(e)
            update_step(tc_desc, expected_results, actual_result, False)
            log.logger1.error('Function validate_json_db ' + str(e))
            raise Exception("Function validate_json_db " + str(e))

    def get_response_payload_dict(self, json_response, parameters, response_payload_dict):
        """
         Description: This method is used to get response payload in dict format
         :param json_response: json response
         :param parameters: parameters to retrieve from json
         :param response_payload_dict: response payload dict
         :return response_payload_dict: response payload in dict format
         """
        try:

            res_df = self.json_table_dataframe(json_response)

            res_df_dict: dict = res_df.to_dict('r')[0]

            if isinstance(res_df_dict, dict):
                for k, v in res_df_dict.items():
                    res_df_dict[k] = str(v).replace(',', '\',\'')
                response_payload_dict = dict(response_payload_dict, **res_df_dict)

            if isinstance(parameters, dict):
                for k, v in parameters.items():
                    parameters[k] = str(v).replace(',', '\',\'')
                response_payload_dict = dict(response_payload_dict, **parameters)

            return response_payload_dict
        except Exception as ex:
            log.logger1.error('get_response_payload_dict due to ' + str(ex))
            tb = traceback.format_exc()
            raise Exception("Function get_response_payload_dict :" + str(ex) + "\n" + str(tb))

    def write_json_to_file(self, res):
        """
         Description: This method is used to write json to a file
         :param res: response
         : return: None
         """
        current_time_stamp = (datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
        query_out_path = os.path.normpath("".join([CURRENT_DIR, os.path.sep, "JSON",
                                                   current_time_stamp, str(self.in_tc_id), ".json"]))
        file1 = open(query_out_path, "w")
        file1.write(res.text)
        file1.close()

    @staticmethod
    def set_dict_items(input_list_or_dict):
        """
         Description: This method is used to set dict items
         :param input_list_or_dict: input list/ dict
         :return out_dict: response_payload_dict: dict as output
         """
        try:
            out_dict = dict()
            if isinstance(input_list_or_dict, dict):
                out_dict = input_list_or_dict.copy()
            elif isinstance(input_list_or_dict, list):
                for dict_temp in input_list_or_dict:
                    if isinstance(dict_temp, dict):
                        out_dict = dict(out_dict, **dict_temp)

            return out_dict

        except Exception as ex:
            log.logger1.error('set_dict_items due to ' + str(ex))
            tb = traceback.format_exc()
            raise Exception("Function set_dict_items :" + str(ex) + "\n" + str(tb))

    def get_res(self, tc_row_dict: dict, api_attributes_dict: dict, response_payload_dict, json_req_res_dict):
        """
         Description: This method is used to connect to get response
         :param tc_row_dict: test cases
         :param api_attributes_dict: input data in csv file in dict format
         :param response_payload_dict: response payload
         :param json_req_res_dict: request & response data in dict format
         :return res: response
         """
        request_method = api_attributes_dict.get('REQUEST_METHOD')
        act_end_point = api_attributes_dict.get('ACT_END_POINT')
        parameters = api_attributes_dict.get('PARAMETERS')
        headers = api_attributes_dict.get('HEADERS')
        request_payload = api_attributes_dict.get('REQUEST_PAYLOAD')
        username = api_attributes_dict.get('USERNAME')
        secret_key = api_attributes_dict.get('SECRET_KEY')

        if request_method.upper() == "GET":
            res = api.get_response(act_end_point, parameters, headers, request_payload,
                                   username=username, password= secret_key)
            self.write_json_to_file(res)
        elif request_method.upper() == "POST":
            res = api.post_response(act_end_point.rstrip(), parameters, headers, request_payload,
                                    username=username, password= secret_key)
            self.write_json_to_file(res)
        elif request_method.upper() == "PUT":
            res = api.put_response(act_end_point, parameters, headers, request_payload,
                                   username=username, password= secret_key)
            self.write_json_to_file(res)
        elif request_method.upper() == "DELETE":
            res = api.delete_response(act_end_point, parameters, headers, request_payload,
                                      username=username, password= secret_key)
            self.write_json_to_file(res)
        elif request_method.upper() == 'NOT':
            res = 'NOT'
            self.get_val_from_database(tc_row_dict, response_payload_dict, json_req_res_dict)
        else:
            raise Exception('Invalid request_method' + str(request_method))

        return res

    def update_dynamic_val_dict(self, res, api_attributes_dict, tc_row_dict, response_payload_dict: dict,
                                json_req_res_dict: dict):
        """
         Description: This method is used to set dictionary to update dynamic values
         :param res: response
         :param api_attributes_dict: input data in csv file in dict format
         :param tc_row_dict: test cases
         :param response_payload_dict: response payload
         :param json_req_res_dict: request & response data in dict format
         :return response_payload_dict, json_req_res_dict: return response payload & json request, response
         """
        request_method = api_attributes_dict.get('REQUEST_METHOD')
        parameters = api_attributes_dict.get('PARAMETERS')
        request_payload = api_attributes_dict.get('REQUEST_PAYLOAD')

        json_response = json.loads(res.text)
        json_req_res_dict['REQUEST_METHOD'] = request_method
        json_req_res_dict['RESPONSE'] = json_response

        if request_method == 'GET':

            response_payload_dict = self.get_response_payload_dict(json_response, parameters, response_payload_dict)

        elif request_method != 'NOT':

            json_payload = self.set_dict_items(request_payload)
            response_dict = self.set_dict_items(json_response)

            if str(tc_row_dict['ExpectedResponse']) != 'NOT':
                self.validate_expected_json(tc_row_dict['TC_Desc'],
                                            str(tc_row_dict['ExpectedResponse']),
                                            response_dict)

            if bool(json_payload):
                json_req_res_dict['PAYLOAD'] = json_payload
                res_pay_df = self.json_table_dataframe(request_payload)

                payload_dict = res_pay_df.to_dict('r')[0]
                response_payload_dict = dict(response_payload_dict, **payload_dict)
                response_payload_dict = dict(response_payload_dict, **response_dict).copy()

            else:
                response_payload_dict = response_dict.copy()

        return response_payload_dict, json_req_res_dict
