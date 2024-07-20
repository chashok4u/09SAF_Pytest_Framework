import requests
import json
import pandas as pd
from utilities.ui_utility.ui import update_step
from utilities.config._config import HTML_REPORTS
import os
from datetime import datetime
import string
import random
import time
import utilities.report_utility.loggers as log

class APIRequest:

    def get_user_credentials(self, **kwargs):
        """
        Description: This method is used to receive username and password\n
        :param kwargs: Username & Password argument should be passed like mentioned below also Password should be encrypted\n
                       (username="******", password="******")\n
        :return: Returns username and password\n

        NOTE: THIS IS AN INTERNAL METHOD
        """
        try:
            _authentication = None
            if ("username" and "password" in kwargs) and (
                    kwargs["username"] is not None and kwargs["password"] is not None):
                _authentication = (kwargs["username"],kwargs["password"])
        except:
            _authentication = None
        return _authentication

    def get_proxies(self, **kwargs):
        """
        Description: This method is used to receive proxies\n
        :param kwargs: Proxies argument should be passed like mentioned below\n
                       (proxies="YES" or proxies="NOT")\n
        :return: Returns proxies\n

        NOTE: THIS IS AN INTERNAL METHOD
        """
        try:
            proxies = None
            if "proxies" in kwargs:
                if "YES" in kwargs["proxies"].upper():
                    proxies = {
                        "http": None,
                        "https": None,
                    }
                elif "NOT" in kwargs["proxies"].upper():
                    proxies = None
                elif kwargs["proxies"].upper() != "YES" or kwargs["proxies"].upper() != "NOT":
                    proxies = json.loads(kwargs["proxies"])
            else:
                proxies = None
        except:
            proxies = None
        return proxies

    def get_response(self, _url, parameters=None, _headers=None, payload=None, **kwargs):
        """
         Description: This method is used to receive the response from REST api Endpoint(GET)\n
        :param _url: api url for GET request\n
        :param parameters: Input parameter or payload or Key value of api (if any)\n
        :param _headers: Headers if any\n
        :param payload: JSON Request Payload\n
        :param _username: User Authentication of api (if any )\n
        :param _password: ****** (if any/use the python password encryption method to get the encrypted password)\n
        :param proxies: proxies if applicable\n
        :return: response object\n

        Note: This Method only validate service not the service DATA **
        """
        async_fn_wait_by_second()
        _authentication = self.get_user_credentials(**kwargs)
        _proxies = self.get_proxies(**kwargs)

        if not isinstance(payload, str): payload = json.dumps(payload)

        try:
            if "https" in _url:
                verify = False
            else:
                verify = None

            response1 = requests.get(url=_url, headers=_headers, params=parameters, data=payload,
                                     auth=_authentication, verify=verify, proxies=_proxies)
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        "user connected service", True)
            update_step("api response time", "NA", str(response1.elapsed.total_seconds()), True)

        except Exception as EX:
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        f"user failed connected service and exception {EX}", False)
            response1 = False

        return response1

    def post_response(self, _url, parameters=None, _headers=None, payload=None, **kwargs):
        """
        Description: This method is used to receive the response from REST api Endpoint(POST)\n
        :param url: api url for POST request\n
        :param parameters: Input parameter or payload or Key value of api (if any)\n
        :param _headers: Headers if any\n
        :param payload: JSON Request Payload\n
        :param _username: User Authentication of api (if any)\n
        :param _password: ****** (if any/use the python password encryption method to get the encrypted password)\n
        :param proxies: proxies if applicable\n
        :return: response object\n

        Note: This Method only validate service not the service DATA **
        """
        async_fn_wait_by_second()
        _authentication = self.get_user_credentials(**kwargs)
        _proxies = self.get_proxies(**kwargs)

        if "files" in kwargs:
            _files = kwargs["files"]
        else:
            _files = None
        log.logger1.info(f"_url :{_url}")
        log.logger1.info(parameters)
        log.logger1.info(_headers)
        log.logger1.info(payload)
        log.logger1.info(_authentication)

        if not isinstance(payload, str):
            payload = json.dumps(payload)
        else:
            log.logger1.info("Payload Default as String..........")

        try:
            if "https" in _url:
                verify = False
            else:
                verify = None

            response1 = requests.post(url=_url, headers=_headers, params=parameters, data=payload,
                                      auth=_authentication, verify=verify, proxies=_proxies, files = _files)
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        "user connected service", True)
            update_step("api response time", "NA", str(response1.elapsed.total_seconds()), True)

        except Exception as EX:
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        f"user failed connect service and exception {EX}", False)
            response1 = False

        return response1

    def get_response_xml(self, _url, parameters=None, _headers=None, payload=None, **kwargs):
        """
        Description: This method is used to receive SOAP XML Response from SOAP XML Request(GET)\n
        :param _url: api url for SOAP request(WSDL)\n
        :param parameters: Input parameter or payload or Key value of api (if any)\n
        :param _headers: Headers if any\n
        :param payload: XML Request Payload\n
        :param _username: User Authentication of api (if any)\n
        :param _password: ****** (if any/use the python password encryption method to get the encrypted password)\n
        :param proxies: proxies if applicable\n
        :return: response object\n

        Note: This Method only validate service not the service DATA **
        """
        async_fn_wait_by_second()
        _authentication = self.get_user_credentials(**kwargs)
        _proxies = self.get_proxies(**kwargs)

        try:
            if "https" in _url:
                verify = False
            else:
                verify = None

            response1 = requests.get(url=_url, headers=_headers, params=parameters, data=(payload),
                                     auth=_authentication, verify=verify, proxies=_proxies)
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        "user successfully connected service", True)
            update_step("api response time", "NA", str(response1.elapsed.total_seconds()), True)
        except Exception as EX:
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        f"user failed connected service and exception {EX}", False)
            response1 = False

        return response1

    def post_response_xml(self, _url, parameters=None, _headers=None, payload=None, **kwargs):
        """
        Description: This method is used to receive SOAP XML Response from SOAP XML Request(POST)\n
        :param url: api url for SOAP request(WSDL)\n
        :param parameters: Input parameter or payload or Key value of api (if any)\n
        :param _headers: Headers if any\n
        :param payload: XML Request Payload\n
        :param _username: User Authentication of api (if any)\n
        :param _password: ****** (if any/use the python password encryption method to get the encrypted password)\n
        :param proxies: proxies if applicable\n
        :return: response object\n

        Note: This Method only validate service not the service DATA **
        """
        async_fn_wait_by_second()
        _authentication = self.get_user_credentials(**kwargs)
        _proxies = self.get_proxies(**kwargs)

        try:
            if "https" in _url:
                verify = False
            else:
                verify = None

            response1 = requests.post(url=_url, headers=_headers, params=parameters, data=(payload),
                                      auth=_authentication, verify=verify, proxies=_proxies)
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        "user successfully connected service", True)
            update_step("api response time", "NA", str(response1.elapsed.total_seconds()), True)

        except Exception as EX:
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        f"user failed connected service and exception {EX}", False)
            response1 = False

        return response1

    def delete_response(self, _url, parameters=None, _headers=None, payload=None, **kwargs):
        """
        Description: This method is used to receive response from DELETE\n
        :param url: api url for DELETE\n
        :param parameters: Input parameter or payload or Key value of api (if any)\n
        :param _headers: Headers if any\n
        :param payload: JSON Request Payload\n
        :param _username: User Authentication of api (if any)\n
        :param _password: ****** (if any/use the python password encryption method to get the encrypted password)\n
        :param proxies: proxies if applicable\n
        :return: response object\n

        Note: This Method only validate service not the service DATA **
        """
        async_fn_wait_by_second()
        _authentication = self.get_user_credentials(**kwargs)
        _proxies = self.get_proxies(**kwargs)


        try:
            if "https" in _url:
                verify = False
            else:
                verify = None
            response1 = requests.delete(url=_url, headers=_headers, params=parameters, data=json.dumps(payload),
                                        auth=_authentication, verify=verify, proxies=_proxies)
            update_step(f"Connect service {_url}", "User should able to connect service without any issues",
                        "user successfully connected service", True)

        except Exception as EX:
            update_step(f"Connect service {_url}", "User should able to connect service without any issues",
                        f"user failed connected service and exception {EX}", False)
            response1 = False

        return response1

    def put_response(self, _url, parameters=None, _headers=None, payload=None, **kwargs):
        """
        Description: This method is used to receive response from PUT\n
        :param url: api url for PUT request\n
        :param parameters: Input parameter or payload or Key value of api (if any)\n
        :param _headers: Headers if any\n
        :param payload: JSON Request Payload\n
        :param _username: User Authentication of api (if any)\n
        :param _password: ****** (if any/use the python password encryption method to get the encrypted password)\n
        :param proxies: proxies if applicable\n
        :return: response object\n

        Note: This Method only validate service not the service DATA **
        """
        async_fn_wait_by_second()
        _authentication = self.get_user_credentials(**kwargs)
        _proxies = self.get_proxies(**kwargs)


        try:
            if "https" in _url:
                verify = False
            else:
                verify = None

            response1 = requests.put(url=_url, headers=_headers, params=parameters, data=json.dumps(payload),
                                     auth=_authentication, verify=verify, proxies=_proxies)

            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        "user successfully connected service", True)
        except Exception as EX:
            update_step(f"Connect service {_url}", "user should able to connect service without any issues",
                        f"user failed connected service and exception {EX}", False)
            response1 = False

        return response1

    def output_response_data(self, response):
        """
        Description: This method is used to get response data\n
        :param response: Response object (GET/POST/PUT/DELETE response object)\n
        :return: Response in string format or None if any error
        """
        try:
            obj = (response.text)
            CURRENT_TIME_STAMP_API = (datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
            api_txt_report_path = os.path.normpath(
                "".join([HTML_REPORTS, os.path.sep, "RUN_", CURRENT_TIME_STAMP_API, '_API.txt']))
            self.file_write_api(api_txt_report_path, obj)
            update_step(f"fetch service response data", "user should able to connect service without any issues",
                        "user successfully connected service", True, api_txt_report_path)
            return obj

        except Exception as E:
            try:
                obj = (response.content)
                update_step(f"fetch service response data", "user should able to connect service without any issues",
                            "user successfully connected service", True)
                return obj
            except Exception as Ex:
                update_step(f"fetch service response data", "user should able to connect service without any issues",
                            "user failed connected service" + str(Ex), False)
                return False

    def verify_response_code(self, response, response_code=200):
        """
        Description: This method is used to verify response status code\n
        :param response: Response Object\n
        :param response_code: Status code\n
        :return: True or False
        """
        if int(response.status_code) == int(response_code):
            update_step(f"Verify service status code : \n {response_code} ",
                        f"User should able to verify service response code with {response_code}",
                        "Successfully verified service code", True)
            return True
        else:
            update_step(f"Verify service status code : \n {response_code} ",
                        f"User should able to verify service response code with {response_code}",
                        f"Failed verified service code: {response.status_code} {response.reason} with expected service code: {response_code} ",
                        False)
            return False

    def convert_data_into_json_format(self, _data):
        """
        Description : This method is used to convert the given data into JSON format\n
        :param _data: Data to be converted\n
        :return: Data in JSON format or False if any error
        """
        try:
            data = json.loads(_data)
            return data
        except Exception as EX:
            print(f" failed to fetch the service Data", "Exception:", str(EX), False)
            return False

    def convert_data_into_table_format(self, _data):
        """
        Description : This method is used to convert the given data into Table format\n
        :param _data: Data to be converted\n
        :return: Data in Table format or False if any error
        """
        try:
            da = pd.DataFrame(_data)
            update_step(f"Convert the data into a table format ",
                        f"user should able convert data into a table",
                        "Successfully converted data", True)

            return da
        except Exception as E:
            update_step(f"Convert the data into a table format ",
                        f"user should able convert data into a table",
                        f"Failed to converted data as format of data is: {type(_data)} but Expected Json format", False)
            return False

    def convert_response_data_to_table_format(self, str_object):
        """
        Description: This method used to convert input data into table format\n
        :param str_object: Data to be converted\n
        :return: json data
        """
        data_obj = self.convert_data_into_json_format(str_object)
        if data_obj is not None:
            data = self.convert_data_into_table_format(data_obj)
            update_step(f"Convert the data into table format ",
                        f"user should able convert data into table",
                        "Successfully converted data", True)
            return data
        else:
            update_step(f"Convert the data into table format ",
                        f"user should able convert data into table",
                        "Failed converted data into table", False)
            return False

    def file_write_api(self, api_txt_report_path, str_object):
        """
        Description: This method used to write the response content into a given file path\n
        :param api_txt_report_path: example: 'c:\\Test\\test.txt'\n
        :param str_object: "any string or string(response.content) object"\n
        :return: True or False
        """
        try:
            file = open(api_txt_report_path, "w+")
            file.write(str_object)
            file.close()
            return True
        except:
            return False

    def extract_data_from_json(self, obj, key):
        """
        Description: This method is used to pull all the values of specified key from nested JSON.\n
        :param obj: Response Object\n
        :param key: JSON Data Key to pull the value\n
        :return: Returns all the values of specified key in a list or False if any error\n
            Example: api.extract_data_from_json(response, "parentOrgId")\n
        """
        try:
            arr = []

            def extract_data(obj, arr, key):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if isinstance(v, (dict, list)):
                            extract_data(v, arr, key)
                        elif k == key:
                            arr.append(v)
                elif isinstance(obj, list):
                    for item in obj:
                        extract_data(item, arr, key)
                return arr

            results = extract_data(obj, arr, key)
            return results
        except Exception as Ex:
            log.logger1.info("Unable to process. " + str(Ex))
            update_step("Extract JSON Data", "Error in execution " + str(Ex), "FAIL", False)
            return False

    def generate_random_alpha_numeric_string(self, count):
        """
        Description: This method is used to generate random alpha numeric string\n
        :param count: Character Count. Ex: 10 or 12 or 15\n
        :return: Returns alpha numeric string or False if any error\n
        """

        try:
            alpha_numeric = ''.join(random.sample((string.ascii_uppercase + string.digits), int(count)))
            return alpha_numeric
        except Exception as Ex:
            log.logger1.info("Unable to process. " + str(Ex))
            update_step("Generate Random Alpha Numeric String", "Error in execution " + str(Ex), "FAIL", False)
            return False

    def api_response_time(self, response_obj):
        """
        Description: This method is used to get api response time (in seconds)
        :param response_obj: Response Object\n
        :return: Response Time in seconds
        """
        try:
            update_step("api response time", "NA", str(response_obj.elapsed.total_seconds()), True)
            return response_obj.elapsed.total_seconds()
        except Exception as Ex:
            log.logger1.info("Unable to get the response time. " + str(Ex))
            update_step("General Response Error, Please check service status code", "Error in execution " + str(Ex),
                        "FAIL", False)
            return False


def async_fn_wait_by_second():
    import time
    time.sleep(1)