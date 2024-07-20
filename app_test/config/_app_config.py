class AppConfig(object):
    from pathlib import Path
    WORKING_DIRECTORY = Path(__file__).parent.parent.parent

    """ Please Add Application environment details , Test details , TFS information
        #environment details , #Test details, #TFS information
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
        """

    """defining execution time zone defined"""
    EXECUTION_TIME_ZONE = 'Asia/Kolkata'
    # Example for different time zone..
    """defining Maximum wait for the object appear in page"""
    MAX_WAIT_TIME = 30  # (seconds)

    """Please mention respective application information"""
    APP_NAME = 'Pepsico'  #
    BROWSER_TYPE = 'CHROME'  # 'BROWSERSTACK' 'REMOTE' #'CHROME' #IE #EDGE
