from pyhocon import ConfigFactory
from utilities.file_handles.file_util import Files
import utilities.report_utility.loggers as log
from utilities.ui_utility.ui import update_step

import os
import traceback

fso = Files()

class Setenv:

    def __init__(self, env_file):
        self.input_json = None
        self.set_input_json(env_file)
        self.env =None

    def setenvironment(self,env):
        """
        Description: This method helps to set environment as global variable\n
        :param env: environment name \n
        : return: None
        """
        self.env =str(env).lower()

    def getenvironment(self):
        """
        Description: This method helps to get environment name\n
        :return: return environment name\n
        : return: None
        """
        return self.env

    def set_input_json(self, env_file_path):
        """
        Description: This method helps to set input json file\n
        :param env_file_path: environment file path name \n
        : return: None
        """
        try:
            path = fso.get_absolute_file_path(env_file_path)
            if not os.path.exists(path):
                log.logger1.info("File does not exist")
                raise Exception('File does not exist')
            else:
                self.input_json = ConfigFactory.parse_file(path)

        except Exception as EX:
            log.logger1.info("Unable to read environment config file " + str(EX))
            update_step("Set Environment", "Unable to read environment config file " + str(EX), "FAIL", False)

            return False

    def get_db_connection(self, db_name):
        """
        Description: This method helps to get DB details\n
        :param db_name: DB name to be connected \n
        :return: return DB details which requires to establish connection\n
        """
        try:
            db_connection_dict = dict()

            db_connection_dict['username'] = next(self.getpath(self.input_json, 'username'))
            db_connection_dict['secret_key'] = next(self.getpath(self.input_json, 'secret_key'))

            dbinfo = next(self.getpath(self.input_json, self.getenvironment()))


            try:
                db_connection_dict['username'] = dbinfo[db_name.lower()]['username']
                db_connection_dict['secret_key'] = dbinfo[db_name.lower()]['secret_key']
            except Exception as e:
                pass

            db_connection_dict['hostName'] = str(dbinfo[db_name.lower()]['hostName'])
            db_connection_dict['port'] = str(dbinfo[db_name.lower()]['port'])
            db_connection_dict['dbName'] = dbinfo[db_name.lower()]['dbName']

            return db_connection_dict.copy()
        except Exception as ex:
            log.logger1.error("Exception is " + str(ex))
            log.logger1.info(traceback.print_exc())

    def getvalue(self, input_key):
        """
        Description: This method helps to get value from json file (environment details file)\n
        :param input_key: value which needs to be retrieve \n
        :return: return retrieved value from json\n
        """
        val = None
        try:
            jsoninfo = next(self.getpath(self.input_json, self.getenvironment()))
            val = jsoninfo[input_key]
        except Exception as e:
            print(e)
        finally:
            return val

    def getpath(self, json_input, lookup_key):
        """
        Description: This method helps to get value from json file (environment details file)\n
        :param json_input: json file \n
        :param lookup_key: value which needs to be retrieve \n
        :return: return retrieved value from json\n
        """
        if isinstance(json_input, dict):
            for k, v in json_input.items():
                if k == lookup_key:
                    yield v
                else:
                    yield from self.getpath(v, lookup_key)
        elif isinstance(json_input, list):
            for item in json_input:
                yield from self.getpath(item, lookup_key)
