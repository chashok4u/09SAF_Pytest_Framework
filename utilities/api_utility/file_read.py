from utilities.file_handles.file_util import Files
import utilities.report_utility.loggers as log
from utilities.ui_utility.ui import update_step

import os
import pandas as pd
import traceback

fso = Files()

class ReadFile:

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
            path = fso.get_absolute_file_path(file_path)
            if not os.path.exists(path):
                log.logger1.info("File does not exist")
                return
            data = pd.read_csv(path, quotechar='"',sep='|')
            return data
        except Exception as EX:
            log.logger1.info("Unable to read CSV file " + str(EX))
            update_step("Read CSV Data", "Unable to read CSV Data. " + str(EX), "FAIL", False)
            return False

    def read_excel_data(self, file_path):
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
            path = fso.get_absolute_file_path(file_path)
            if not os.path.exists(path):
                log.logger1.info("File does not exist")
                return
            data = pd.read_excel(path)
            df = pd.DataFrame(data)
            return df
        except Exception as EX:
            log.logger1.info("Unable to read excel file " + str(EX))
            update_step("Read excel Data", "Unable to read excel Data. " + str(EX), "FAIL", False)
            return False

    def read_sheet_df(self, sheet):
        """
        Description: This method helps to read excel/ csv file\n
        :param sheet: value which needs to be retrieve \n
        :return: return data as dataframe\n
        """
        try:
            if str(sheet).endswith('.csv'):
                sheet_df = self.read_csv_data(sheet)
            elif str(sheet).endswith('.xlsx') or str(sheet).endswith('.xls'):

                sheet_df = self.read_excel_data(sheet)


            else:
                update_step("File is not in proper format", "File is not in proper format",
                            "File is not in proper format", False)

        except Exception as e:
            actual_result = "Exception occured  " + str(e)
            update_step("File Issue", "CSV File Issue", actual_result, False)
            traceback.print_exc()
        finally:
            return sheet_df

    def read_excel_to_csv_pipe(self, file_path):
        """
        Description:
            This method is used to read data from Excel file and convert to csv pipe delimited.\n
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
            excel_df = self.read_excel_data(file_path)
            path = fso.get_absolute_file_path(file_path)
            if str(path).endswith('xls') :
                path = str(path).replace('.xls', '.csv')
            elif str(path).endswith('xlsx'):
                path = str(path).replace('.xlsx', '.csv')
            excel_df.to_csv(path,  sep = '|', index=False )

        except Exception as EX:
            log.logger1.info("Unable to convert Excel to Csv " + str(EX))
            update_step("Excel to CSV ", "Unable to convert Excel to Csv " + str(EX), "FAIL", False)
            return False

