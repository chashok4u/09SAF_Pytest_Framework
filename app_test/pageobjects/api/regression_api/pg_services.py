from selenium.webdriver import ActionChains

from app_test.pageobjects.api.api_env_switch import env_api_url, default_env
from app_test.config._app_config import AppConfig
from app_test.config._test_config import browser
from app_test.config._test_config import api
# from utilities.crypt_utility.encryption_utility import Cryptography
# from utilities.db_utility.db import Database
import cx_Oracle
import pandas as pd
import json
import csv


# db = Database()
# encrypt = Cryptography()


class rest_services:

    def get_csv_path(self, sheet_name):
        """
        Description: This method helps to read the csv file
        return: Path of the csv
        param: Sheet Name of the CSV
        """
        sheet = "/app_test/testdata/td_api/" + sheet_name + ".csv"
        path = str(AppConfig.WORKING_DIRECTORY) + sheet
        return path

    def get_eps_service_response(self, env, sheet_name, field):
        """
        Description: This method helps to read the Test Data from CSV
        """
        path = self.get_csv_path(sheet_name)
        with open(path, newline='') as csv_file:
            data = csv.DictReader(csv_file, delimiter='|')
            for ele in data:
                api_data = self.get_service_response(ele['Endpoint_URL'], ele['Method_Type'], ele['Payload'],
                                                     ele['Parameters'], env, sheet_name, field)
        return api_data

    def send_api_request(self, url, method_type, headers, data_get, parameters=None):
        """ Description:This method returns response text and response status of a service.
            :param headers: gets the headers value from api_request_services_call method
            :param base_url: gets the URL from endpoints url and testdata
            :param access_token: gets the value from r360_api_login method
            :param method_type: gets the value from test data('POST','GET', etc)
            :param data_get: gets the value from test data
            :param parameters: gets the value from test data
            :return: response.status_code, response.text
        """
        if method_type == "POST":
            response = api.post_response(url, parameters, headers, data_get)
        elif method_type == "GET":
            response = api.get_response(url, parameters, headers, data_get)
        else:
            response = api.put_response(url, parameters, headers, data_get)
        return response

    def service_end_point(self, End_point_url, env):
        """ Description:This method returns the endpoint_url from testdata and App url from select url method.
                :param End_point_url: endpoint_url from testdata and App url
                :param env: Default value is Staging
                :return : endpoint_url (Concat of Application url and Endpoint url)
        """
        if env is None or env == 'default name': env = default_env
        headers = {'Content-Type': 'application/json'}
        service_dns = env_api_url(env)
        service_url = service_dns + End_point_url
        print("headers", headers)
        print("service_url", service_url)
        return service_url

    def get_service_response(self, url, method_type, payload, parameters, env, sheet_name, field):
        """
        Description: This method helps to Get the Response from API Services
        return: None
        Param: url, payload
        """
        base_url = self.service_end_point(url, env)
        if parameters == '':
            service_url = base_url
        else:
            parameter = json.dumps(parameters)
            param = json.loads(parameter)
            # querystring = urlencode(param)
            service_url = base_url + param
        headers = {
            'store': 'mexico_store_view',
            'Content-Type': 'application/json',
            'Cookie': 'PHPSESSID=2c49767614478fa756ed8eb8be3c05bb; private_content_version=213439dfc80cab877fdb3ee91d8e79fa'
        }

        # headers = {
        #     'store': 'za',
        #     'Content-Type': 'application/json',
        #     'Cookie': 'PHPSESSID=511d8bf68480f2598e19943e9013c292; private_content_version=60ac1af5901b37c147a9be948ab08f79'
        # }

        if payload == '':
            req_payload = {}
        else:
            pass
            req_payload = payload

        response = self.send_api_request(service_url, method_type, headers, req_payload)
        api.verify_response_code(response, 200)
        data = api.output_response_data(response)
        count = self.get_total_count(data)
        products_data = self.fetch_products(service_url, method_type, headers, req_payload, count, field)
        return products_data

    def get_total_count(self, api_data):
        parsed_data = json.loads(api_data)
        count = parsed_data['data']['products']['total_count']
        return count

    def fetch_products(self, service_url, method_type, headers, req_payload, total_count, field):
        products_data = []
        query_json = json.loads(req_payload)
        num_pages = total_count // 200
        if total_count % 200 != 0:
            num_pages += 1
        for page in range(1, num_pages + 1):
            query_json['query'] = query_json['query'].replace(f'currentPage:1\n', f'currentPage:{page}\n')
            updated_payload = json.dumps(query_json, indent=2)
            response = self.send_api_request(service_url, method_type, headers, updated_payload)
            api.verify_response_code(response, 200)
            json_data = api.output_response_data(response)
            parsed_data = json.loads(json_data)
            if field == 'name':
                for aggregation in parsed_data['data']['products']['items']:
                    products_data.append(aggregation['name'])
        return products_data

    def get_api_response_data(self, api_data):
        # json_values = json_data[value]
        parsed_data = json.loads(api_data)
        count = parsed_data['data']['products']['total_count']
        print(count)
        all_names = []
        test = []
        for aggregation in parsed_data['data']['products']['items']:
            all_names.append(aggregation['name'])
        for data in parsed_data['data']['products']['aggregations']:
            for option in data['options']:
                # Append the label to the list of all labels
                test.append(option['label'])
        print("TEST", all_names)
        print("TEST", len(test))
        return all_names

    def get_product_url(self, api_data):
        parsed_data = json.loads(api_data)
        product_url = []
        for aggregation in parsed_data['data']['products']['items']:
            data = aggregation['image']['url']
            url = data.split('?optimize=')[0]
            product_url.append(url)
        print(product_url)

    def get_product_price(self, api_data):
        parsed_data = json.loads(api_data)
        product_price = []
        for item in parsed_data['data']['products']['items']:
            for assigned_item in item['assigned_item']:
                price = assigned_item['display_final_price']['value']
                currency = assigned_item['display_final_price']['currency']
                print(f"Value: {price}, Currency: {currency}")
                value = currency + "$" + price
                product_price.append(value)
        return product_price

    # def perform_hover_actions(self, parent_menu, sub_menu=None, child_menu=None, child_sub_menu=None):

    # # Hover over the parent menu
    # browser.mouse_over("xpath__//a[text()='" + parent_menu + "']/parent::li", '', '')
    #
    # # If sub-menu is present, hover over it
    # if sub_menu:
    #     browser.mouse_over("xpath__//a[text()='" + sub_menu + "']/parent::li", '', '')
    #
    #     # If child menu is present, hover over it
    #     if child_menu:
    #         browser.mouse_over("xpath__//a[text()='" + child_menu + "']/parent::li", '', '')
    #
    #         # If child sub-menu is present, hover over it
    #         if child_sub_menu:
    #             browser.mouse_over("xpath__//a[text()='" + child_menu + "']/parent::li", '', '')
    #
    # # Perform the click action
    # actions.click().perform()
