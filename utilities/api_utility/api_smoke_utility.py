from utilities.api_utility.api_utility import *
# from utilities.file_handles.file_util import *
from utilities.ui_utility.ui import update_step
import time
import json
# from utilities.crypt_utility.encryption_utility import *

# fso = Files()
api = APIRequest()
# crypt = Cryptography()

class SmokeApi:
    """
    This class is used to verify REST api Smoke Test Scenarios\n
    Which cover the status code and response time.
    """


    def get_milli_seconds(self, seconds, roundoff):
        """
        Description: This method is used to convert milli seconds from seconds \n 
        :param seconds: Seconds\n
        :param roundoff: Roundoff Number(Ex:2 or 3 or 4 etc..)\n
        :return: Milli Seconds \n
        """
        milli = seconds * 1000
        return round(milli, roundoff)

    def get_headers(self, key, value):
        """
        Description: This method is used to get headers format.\n
        :param key: Headers Key\n
        :param value: Headers Value\n
        :return: Headers Format
        """
        global headers
        if key.upper() == "CONTENT-TYPE":
            headers = {"'Content-Type': '" + value + "'"}
        if key.upper() == "AUTHORIZATION-BASIC":
            headers = {'Authorization': 'Basic {}'.format(value)}
        if key.upper() == "AUTHORIZATION-BEARER":
            headers = {'Authorization': 'Bearer {}'.format(value)}
        return headers

    def verify_response_time(self, milli_seconds, description):
        """
        Description: This method is used to verify response time\n
        :param milli_seconds: Milli Seconds\n
        :param description: Test Case Description\n
        :return: Boolean(True/False)
        """
        if milli_seconds <= 30000:
            update_step(description, "Successfully Verified Response Time", "PASS", True)
            return True
        else:
            update_step(description, "Verified Response Time", "FAIL", False)
            return False

    def verify_response_object(self, response1, response2, description):
        """
        Description: This method is used to verify two response object data\n
        :param response1: Response Object 1\n
        :param response2: Response Object 2\n
        :param description: Test Case Description\n
        :return: Boolean(True/False)
        """
        try:
            json_response1 = json.loads(response1.text)
            json_response2 = json.loads(response2.text)
            if sorted(json_response1.items()) == sorted(json_response2.items()):
                update_step(description, "Successfully Verified Response Object", "PASS", True)
                return True
            else:
                update_step(description, "Unsuccessfully Verified Response Object", "FAIL", False)
                return False
        except Exception as Ex:
            update_step(description, "Unsuccessfully Verified Response Object. " + str(Ex), "FAIL", False)
            return False

    def verify_response_body_exists(self, response, desc):
        """
        Description: This method is used to verify whether response JSON body or XML exists or not\n
        :param response: Response Object\n
        :param desc: Test Case Description\n
        :return: Boolean(True/False)
        """
        try:
            if "json" in response.headers.get("Content-Type"):
                update_step(desc, "Successfully Verified REST Response Body Exists", "PASS", True)
                return True
            elif "xml" in response.headers.get("Content-Type"):
                update_step(desc, "Successfully Verified SOAP Response Body Exists", "PASS", True)
                return True
            else:
                update_step(desc, "Unsuccessfully Verified Response Body Exists", "FAIL", False)
                return False
        except Exception as Ex:
            update_step(desc, "Unsuccessfully Verified Response Body Exists. No JSON/XML Returned. " + str(Ex), "FAIL",
                        False)
            return False   

    def get_headers_value(self, headers_list):
        """
        Description: This method is used to get headers value\n
        :param headers_list: Headers list if any or enter "NOT"\n
        :return: Returns headers if any or None
        """
        if headers_list == "NOT":
            headers1 = None
        else:
            headers1 = eval(headers_list)
        return headers1

    def get_request_payload(self, payload):
        """
        Description: This method is used to get request payload\n
        :param payload: Request Payload if any or enter "NOT"\n
        :return: Returns request payload if any or None
        """
        if payload == "NOT":
            request_payload = ""
        else:
            request_payload = json.loads(payload)
        return request_payload

    def get_parameters(self, params):
        """
        Description: this method is used to get parameters\n
        :param params: Parameters if any or enter "NOT"\n
        :return: Returns parameters if any or None
        """
        if params == "NOT":
            parameters = None
        else:
            parameters = params
        return parameters

    def get_endpoint(self, url, data):
        """
        Description: This method is used to get an actual end point\n
        :param url: Endpoint\n
        :param data: Dynamic data in end point if any or enter "NOT"\n
        :return: Returns actual end point
        """
        if data == "NOT":
            act_end_point = url
        else:
            act_end_point = url + data
        return act_end_point

    def get_rest_response(self, request_method, act_end_point, parameters, _headers, request_payload, **kwargs):
        """
        Description: This method is used to get REST api response based on request type\n
        :param request_method: Request type (GET/POST/PUT)\n
        :param act_end_point: End point url\n
        :param parameters: Parameters if any\n
        :param _headers:  Headers if any\n
        :param request_payload: Request Payload if any\n
        :param kwargs: Keyword length arguments for username, password and proxies\n
        :return: Returns response object
        """
        time.sleep(1)
        if request_method.upper() == "GET":
            res = api.get_response(act_end_point, parameters, _headers, request_payload, **kwargs)
        elif request_method.upper() == "POST":
            res = api.post_response(act_end_point, parameters, _headers, request_payload, **kwargs)
        elif request_method.upper() == "PUT":
            res = api.put_response(act_end_point, parameters, _headers, request_payload, **kwargs)
        return res

    def get_soap_response(self, request_method, act_end_point, parameters, _headers, request_payload, **kwargs):
        """
        Description: This method is used to get SOAP api response based on request type\n
        :param request_method: Request type (GET/POST)\n
        :param act_end_point: End point url\n
        :param parameters: Parameters if any\n
        :param _headers:  Headers if any\n
        :param request_payload: Request Payload if any\n
        :param kwargs: Keyword length arguments for username, password and proxies\n
        :return: Returns response object
        """
        time.sleep(1)
        if request_method.upper() == "GET":
            res = api.get_response_xml(act_end_point, parameters, _headers, request_payload, **kwargs)
        elif request_method.upper() == "POST":
            res = api.post_response_xml(act_end_point, parameters, _headers, request_payload, **kwargs)
        return res

    def verify_rest_api_smoke_scenarios(self, test_data_path):
        """
        Description: This method is used to verify REST/SOAP api smoke test scenarios\n
        :param test_data_path: Relative Test Data CSV File Path\n
            Example: "app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_1.csv"\n
        :return: None
        """
        time.sleep(1)
        try:
            df = fso.read_csv_data(test_data_path)
            for row in df.itertuples(index=True, name='Pandas'):
                desc = getattr(row, "TC_Desc")
                act_qa_url = getattr(row, "QA_EndPoint")
                data1 = str(getattr(row, "Data"))
                request_method = getattr(row, "Method")
                post_payload = getattr(row, "POST_Request_Payload")
                _user = getattr(row, "Username")
                _skey = getattr(row, "SecretKey")
                params = getattr(row, "Parameters")
                dict_headers = getattr(row, "Headers")
                response_code = int(getattr(row, "Response_Code"))
                try:
                    _proxies = getattr(row, "Proxies")                    
                except:
                    _proxies = "NOT"                    

                try:                    
                    service_type = getattr(row, "Service_Type")
                except:                    
                    service_type = "REST"

                _headers = self.get_headers_value(dict_headers)
                parameters = self.get_parameters(params)
                act_end_point = self.get_endpoint(act_qa_url, data1)

                if _user == "NOT" and _skey == "NOT":
                    user = None
                    skey = None
                else:
                    user = _user
                    skey = crypt.decryption(_skey)

                start_time = time.time()
                if service_type.upper() == "REST":
                    request_payload = self.get_request_payload(post_payload)
                    res = self.get_rest_response(request_method, act_end_point, parameters, _headers, request_payload, username=user, password=skey,
                                                   proxies=_proxies)
                elif service_type.upper() == "SOAP":
                    res = self.get_soap_response(request_method, act_end_point, parameters, _headers, post_payload, username=user,
                                                 password=skey,
                                                 proxies=_proxies)
                end_time = time.time()
                diff = end_time - start_time
                milli_second = self.get_milli_seconds(diff, 2)

                # Verify Response Code
                if not api.verify_response_code(res, response_code):
                    continue

                # Verify Response Time
                self.verify_response_time(milli_second, desc)

                # Verify Response Body Exists
                self.verify_response_body_exists(res, desc)

        except Exception as Ex:
            log.logger1.info("Error in executing : " + str(Ex))
            update_step("api Execution", "Error in execution " + str(Ex), "FAIL", False)
