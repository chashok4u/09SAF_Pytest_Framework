class EnvConfig(object):
    from pathlib import Path
    WORKING_DIRECTORY = Path(__file__).parent.parent.parent
    import os
    import getpass
    USER_NAME = getpass.getuser()
    """ Please Add Application environment details , Translations details , TFS information
        #environment details , #Translations details, #TFS information
        param: EXECUTION_TIME_ZONE , MAX_WAIT_TIME,APP_NAME,APP_URL,BROWSER_TYPE
        example :
            "defining execution time zone defined"
            EXECUTION_TIME_ZONE     ='Asia/Kolkata' (Update only timezone. Don't modify that variable name as variable is pre-defined)
            "defining Maximum wait for the object appear in page"
            MAX_WAIT_TIME = 30 (Update only second time. Don't modify that variable name as variable is pre-defined)
            "Please mention respective application information"
            APP_NAME             ='GOOGLE_TEST'
            APP_GOOGLE_URL       ="https://www.google.com"
            BROWSER_TYPE         ='CHROME'
        #Config Driver,System Configuaration
        """
    """defining execution time zone defined"""
    EXECUTION_TIME_ZONE = 'Asia/Kolkata'  # Time Zone
    """defining Maximum wait for the object appear in page"""
    MAX_WAIT_TIME = 30  # (seconds)

    class ApplicationEnv:
        def __init__(self, env_type):
            self.env_type = env_type.upper()
            envls = self.env_type.split('_')
            print("ENV::::::", envls[0])
            if "PREQA" in env_type.upper():
                print("Execution is in Default Dev Env")
                self.URL = 'https://www.se.com/in/en/'

            elif "SI" in env_type.upper():
                print("Execution is in SI Env")
                self.URL = ''

            elif "PROD" in env_type.upper():
                print("Execution is in PROD Env")
                self.URL = ''

            elif "QA" in env_type.upper():
                print("Execution is in QA Env")
                self.URL = ''

            elif "UAT" in env_type.upper():
                print("Execution is in UAT Env")
                self.URL = ''

            elif "HOTFIX" in env_type.upper():
                print("Execution is in HOTFIX Env")
                self.URL = ''

            elif "DR" in env_type.upper():
                print("Execution is in DR Env")
                self.URL = ''

            else:
                print("Execution is standard")
                self.URL = 'https://www.se.com/in/en/'

    class ApiEnv:
        def __init__(self, env_type):
            self.env_type = env_type.upper()
            envls = self.env_type.split('_')
            print("ENV::::::", envls[0])
            if "PREQA" in env_type.upper():
                print("Execution is in Default Dev Env")
                self.URL = ""

            elif "SI" in env_type.upper():
                print("Execution is in QA Env")
                self.URL = ''

            elif "PROD" in env_type.upper():
                print("Execution is in PROD Env")
                self.URL = ''

            elif "QA" in env_type.upper():
                print("Execution is in QA Env")
                self.URL = ''

            elif "UAT" in env_type.upper():
                print("Execution is in UAT Env")
                self.URL = ''

            elif "HOTFIX" in env_type.upper():
                print("Execution is in HOTFIX Env")
                self.URL = ''

            elif "DR" in env_type.upper():
                print("Execution is in DR Env")
                self.URL = ''

            else:
                print("Execution is standard")
                self.URL = ''
