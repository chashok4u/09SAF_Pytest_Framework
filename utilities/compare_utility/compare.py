import datacompy
from utilities.config._config import *
from utilities.ui_utility.ui import update_step
from datetime import datetime
import numpy as np
import pandas as pd
# from utilities.file_handles.file_util import *
import utilities.report_utility.loggers as log

# fso = Files()


class Compare():

    def compare_two_data_frames(self, _df1, _df2):
        """
        Description :This method help to compare two data frame if column are in respective order\n
        :param _df1: data frame 1 (rows and columns)\n
        :param _df2: data frame 2 (rows and columns)\n
        :return: None
        """
        current_time_stamp_format = (datetime.now().strftime('%d_%m_%Y_%H_%M_%S'))
        in_excel_file = "".join(
            [INPUTSFILES_DIR, '\\', CURRENT_TIME_STAMP, "_", current_time_stamp_format, "", '_', 'FINAL_RESULTS.xlsx'])
        in_writer = pd.ExcelWriter(in_excel_file)

        src_records_column_count = len(list(_df1.columns.values))
        trg_records_column_count = len(list(_df2.columns.values))
        if (src_records_column_count == trg_records_column_count) and (len(_df1) != 0 and len(_df2) != 0):
            # if len(_df1) != 0 and len(_df2) != 0:
            join_column_list = []
            for i in range(0, src_records_column_count): join_column_list.append("Column" + str(i))
            _df1.columns = join_column_list
            _df2.columns = join_column_list
            compare = datacompy.Compare(_df1, _df2, join_columns=join_column_list,
                                        # You can also specify a list of columns
                                        abs_tol=0,  # Optional, defaults to 0
                                        rel_tol=0,  # Optional, defaults to 0
                                        df1_name='Original',  # Optional, defaults to 'df1'
                                        df2_name='New'  # Optional, defaults to 'df2'
                                        )
            final_summary_report_ = {
                "DataFrame_name": [compare.df1_name, compare.df2_name],
                "Columns": [compare.df1.shape[1], compare.df2.shape[1]],
                "Rows": [compare.df1.shape[0], compare.df2.shape[0]],
                "df1_unq_rows": compare.df1_unq_rows,
                # self.df1_unq_rows.columns[:10]
                "df2_unq_rows": compare.df2_unq_rows,
                # self.df2_unq_rows.columns[:10]
                "df1_matched": pd.concat([compare.df1, compare.df1_unq_rows]).drop_duplicates(keep=False),
                "df2_matched": pd.concat([compare.df2, compare.df2_unq_rows]).drop_duplicates(keep=False)}

            df1vsdf2_matchedrecords = final_summary_report_.get("df1_matched")
            df1vsdf2_mismatchedrecords = final_summary_report_.get("df1_unq_rows")
            df2vsdf1_matchedrecords = final_summary_report_.get("df2_matched")
            df2vsdf1_mismatchedrecords = final_summary_report_.get("df2_unq_rows")

            pd.DataFrame(df1vsdf2_matchedrecords).to_excel(in_writer, "df1vsdf2_matchedrecords")
            pd.DataFrame(df1vsdf2_mismatchedrecords).to_excel(in_writer, "df1vsdf2_mismatchedrecords")
            pd.DataFrame(df2vsdf1_matchedrecords).to_excel(in_writer, "df2vsdf1_matchedrecords")
            pd.DataFrame(df2vsdf1_mismatchedrecords).to_excel(in_writer, "df2vsdf1_mismatchedrecords")
            in_writer.save()
            in_writer.close()

            src_count = len(df1vsdf2_matchedrecords) + len(df1vsdf2_mismatchedrecords)
            trg_count = len(df2vsdf1_matchedrecords) + len(df2vsdf1_mismatchedrecords)

            update_step("source data info", "No of record present in source data", src_count, True)
            update_step("target data info", "No of record present in target data", trg_count, True)

            if len(df1vsdf2_mismatchedrecords) == 0:
                update_step("Data validation", "source data (input data-1) should match to target data(input-2)",
                            "Successfully verified source data(input-1) with target data(input-2)", True,
                            in_excel_file)
            else:
                update_step("Data validation", "source data (input data-1) should match to target data(input-2)",
                            "failed to  verified source data(input-1) with target data(input-2)", False,
                            in_excel_file)

            if len(df2vsdf1_mismatchedrecords) == 0:
                update_step("Data validation", "target data (input data-1) should match to source data(input-2)",
                            "Successfully verified target data(input-1) with source data(input-2)", True,
                            in_excel_file)
            else:
                update_step("Data validation", "target data (input data-1) should match to source data(input-2)",
                            "failed to  verified target data(input-1) with source data(input-2)", False,
                            in_excel_file)
    

    def compare_two_lists(self, list1, list2):
        """
        Description: This method used to compare two list\n
        :param list1: for example: List1 =[1,2]\n
        :param list2: for example : List2 =[1,2,3]\n
        :return: List of lists [[list1 In list2],[List2 in list1]] similar to (array)\n
                 [[list1-differences],[list2-differences]]
        """
        return_values = [[x for x in list1 if x not in list2], [x for x in list2 if x not in list1]]
        log.logger1.info(return_values)
        if len(return_values[0]) == 0:
            update_step("Data validation", "source data should match to target data",
                        "successfully verified source data with target data " + str(return_values[0]), True)
        else:
            update_step("Data validation", "source data should match to target data",
                        "failed to verified source data with target data" + str(return_values[0]), False)

        if len(return_values[1]) == 0:
            update_step("Data validation", "target data should match to source data",
                        "successfully verified Target data with Source" + str(return_values[1]), True)
        else:
            update_step("Data validation", "target data should match to source data",
                        "failed to verified target data with source" + str(return_values[1]), False)

        return return_values

    # def compare_two_excel_files(self, file_path1, file_path2, diff_dir_path, ignore_columns_file1=None,
    #                             ignore_columns_file2=None):
    #     """
    #     Description: This method is used to compare two excel files in efficient approach.\n
    #     :param file_path1: First File Relative Path Location. It should be started with Project Root Directory.\n
    #         Don't include E: or C:\n
    #         Example: "app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_1.xls"\n
    #     :param file_path2: Second File Relative Path Location. It should be started with Project Root Directory.\n
    #         Don't include E: or C:\n
    #         Example: "app_test/testdata/td_api/smoke/CMP_Smoke_referencedata-domaindata_2.xlsx"\n
    #     :param diff_dir_path: Difference Directory Relative Path Location to store differences in new excel file.\n
    #         It should be started with Project Root Directory.\n
    #         Don't include E: or C:\n
    #         Don't include excel file name as it creates automatically excel file to store mismatch records if there are any.\n
    #         Example: "result_output (Don't include "/" after result_output)\n
    #     :param ignore_columns_file1: Optional Parameter. This parameter is used to skip specific columns\n
    #             which are not to be compared from file2.\n
    #             Pass "None" or column names to be skipped. Example: "Country,City"\n
    #     :param ignore_columns_file2: Optional Parameter. This parameter is used to skip specific\n
    #             columns which are not to be compared from file2.\n
    #             Pass "None" or column names to be skipped. Example: "Country,City"\n
    #     :return: Boolean(True/False) and Mismatch Records if any.
    #     """
    #     try:
    #         file1 = fso.get_absolute_file_path(file_path1)
    #         file2 = fso.get_absolute_file_path(file_path2)
    #         if ignore_columns_file1 is not None:
    #             skip_cols1 = list(ignore_columns_file1.split(","))
    #             data_frame1 = pd.read_excel(file1, usecols=lambda x: x not in skip_cols1)
    #         else:
    #             data_frame1 = pd.read_excel(file1)
    #
    #         if ignore_columns_file2 is not None:
    #             skip_cols2 = list(ignore_columns_file2.split(","))
    #             data_frame2 = pd.read_excel(file2, usecols=lambda x: x not in skip_cols2)
    #         else:
    #             data_frame2 = pd.read_excel(file2)
    #
    #         df1 = data_frame1.fillna(0)
    #         df2 = data_frame2.fillna(0)
    #
    #         if df1.shape != df2.shape:
    #             log.logger1.info(
    #                 "Excel File comparisons are failed. Data frames are not same - DF1" + str(df1.shape) + "/DF2" + str(
    #                     df2.shape))
    #             update_step("Compare two excel files", "Source and Target data should be matched",
    #                         "Failed to compare two excel files. DataFrames are not same - DF1" + str(
    #                             df1.shape) + "/DF2" + str(df2.shape), False)
    #             return False
    #
    #         comparison_value = df1.values == df2.values
    #         result = any(False in sublist for sublist in comparison_value)
    #         if not result:
    #             log.logger1.info("Excel File comparisons are successful. There are no difference")
    #             update_step("Compare two excel files", "Source and Target data should be matched",
    #                         "verified source and target data and its matched as expected", True)
    #             return True
    #
    #         rows, cols = np.where(comparison_value == False)
    #         for item in zip(rows, cols):
    #             df1.iloc[item[0], item[1]] = "{} --> {}".format(df1.iloc[item[0], item[1]], df2.iloc[item[0], item[1]])
    #         dir_name = fso.get_absolute_file_path(diff_dir_path)
    #         if not os.path.exists(dir_name):
    #             os.mkdir(dir_name)
    #         current_time_stamp = (datetime.now().strftime("%m%d%Y_%H%M%S"))
    #         file_path = dir_name + "/Comparison_Reports_" + current_time_stamp + ".xlsx"
    #         df1.to_excel(file_path, index=False, header=True)
    #         log.logger1.info("Excel File comparisons are failed. There are mismatch records available")
    #         update_step("Compare two excel files", "Source and Target data should be matched",
    #                     "Failed to verify source and target data", False, file_path)
    #         return False
    #     except Exception as Ex:
    #         log.logger1.info("Unable to process. " + str(Ex))
    #         update_step("Compare two excel files", "Source and Target data should be matched",
    #                     "Failed to verify source and target data " + str(Ex), False)
    #         return False

    def get_frame_differences(self, df1, df2):
        """
        Description: This method will help us identify and print difference between two data frames
        Note: which is applicable to only command data table i.e. columns names should match.
        :param df1:  data frame 1
        :param df2:  data frame 2
        :output returns data frame with all the records with mismatch
        """
        try:
            assert (df1.columns == df2.columns).all(), "DataFrame column names are different"
            if any(df1.dtypes != df2.dtypes):
                log.logger1.info("Data Types are different, trying to convert")
                df2 = df2.astype(df1.dtypes)

            if df1.equals(df2):
                return None
            else:
                log.logger1.info("handle null values with in the DataFrame")
            diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
            ne_stacked = diff_mask.stack()
            changed = ne_stacked[ne_stacked]
            changed.index.names = ['id', 'col']
            difference_locations = np.where(diff_mask)
            changed_from = df1.values[difference_locations]
            changed_to = df2.values[difference_locations]
            return pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)
        except Exception as Ex:
            log.logger1.info("Unable to process. " + str(Ex))
            return
