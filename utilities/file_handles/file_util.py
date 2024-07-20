import os
import csv
import pandas as pd
import utilities.report_utility.loggers as log
from utilities.ui_utility.ui import update_step
from utilities.config._config import WORKING_DIRECTORY

class Files:

    def get_absolute_file_path(self, relative_file_path):
        """
        Description:
            This method is used to get the absolute file path from given relative file path.\n
        :param relative_file_path: Relative File Path\n
            Example: "DemoApplication-QAAutomation-utilities/resources/testData.csv"\n
        :return: Returns absolute file path as string\n
            Example: "C:/MyWork/GitRepository/utilities/resources/testData.csv"
        """
        try:
            dir_path = os.path.abspath('..')
            root_fold = relative_file_path.split("/")
            abs_path = dir_path.split(root_fold[0])
            path = abs_path[0] + "/" + relative_file_path
            #WORKING_DIRECTORY+relative
            # str (#WORKING_DIRECTORY+relative )
            tdpath=os.path.normpath(str (WORKING_DIRECTORY+'/'+relative_file_path))
            log.logger1.info(f"API testdata path {tdpath}")
            if os.path.exists(tdpath) :return tdpath
            else:
                raise(f"Unable to find the API testdata path {tdpath}")
             #path.replace('\\', '/')
        except Exception as EX:
            log.logger1.info("Unable to process")
            update_step("File Path Exists", "File Path is Invalid. " + str(EX), "FAIL", False)
            return False

    def read_csv_data(self, file_path):
        """
        Description:
            This method is used to read data from CSV file.\n
        :param file_path: Relative File Path.It should be started with app_test.\n
            Don't include E: or C:\n
            Example: "app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_1.csv"\n
        :return: Returns CSV data in Pandas DataFrame\n
        Example: How to use this method\n
            fso = Files()\n
            path = "app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_1.csv"\n
            df = fso.read_csv_data(self.path)\n
            for row in df.itertuples(index=True, name='Pandas'):\n
                query = getattr(row, "Query")\n
                expquery = getattr(row, "ExpQuery")\n
                desc = getattr(row, "Desc")
        """
        try:
            path = self.get_absolute_file_path(file_path)
            if not os.path.exists(path):
                log.logger1.info("File does not exist")
                return
            data = pd.read_csv(path)
            return pd.DataFrame(data)
        except Exception as EX:
            log.logger1.info("Unable to read CSV file " + str(EX))
            update_step("Read CSV Data", "Unable to read CSV Data. " + str(EX), "FAIL", False)
            return False

    def read_json_data(self, file_path):
        """
        Description:
            This method is used to read data from JSON file.\n
        :param file_path: Relative File Path.It should be started with app_test.\n
            Don't include E: or C:\n
            Example: "app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_1.json"\n
        :return: Returns CSV data in Pandas DataFrame\n
        Example: How to use this method\n
            fso = Files()\n
            path = "app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_1.json"\n
            df = fso.read_csv_data(self.path)\n
            for row in df.itertuples(index=True, name='Pandas'):\n
                query = getattr(row, "Query")\n
                expquery = getattr(row, "ExpQuery")\n
                desc = getattr(row, "Desc")
        """
        try:
            path = self.get_absolute_file_path(file_path)
            if not os.path.exists(path):
                log.logger1.info("File does not exist")
                return
            data = pd.read_json(path)
            return pd.DataFrame(data)
        except Exception as EX:
            log.logger1.info("Unable to read JSON file " + str(EX))
            update_step("Read JSON Data", "Unable to read JSON Data. " + str(EX), "FAIL", False)
            return False

    def get_file_path(self, test_data_path):
        """
        Description: This method is used to get the absolute file path from given relative file path.\n
        :param test_data_path: Relative File Path. It should start with app_test\n
            Example: "app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_1.csv"\n
        :return: Returns absolute file path as string\n
            Example: "C:/MyWork/GitRepository/DS-CMP-Platform/QAAutomation-utilities/app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_1.csv"
        """
        try:
            dir_name = os.path.dirname(__file__)
            file_name = os.path.join(dir_name, "")
            x = file_name.split("app_test")
            return x[0] + test_data_path
        except Exception as Ex:
            update_step("File Path Exists", "File Path is Invalid. " + str(Ex), "FAIL", False)
            return False
