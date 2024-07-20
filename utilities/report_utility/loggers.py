'''

@author:
'''

import logging
import os

import utilities.config._config as config


# logger_path=TestConfig.loger_directory+'//'+currentTimeStamp_format+'.log'
# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=config.LOGGER_PATH,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Execution Logger file..')
# Now, define a couple of other loggers which might represent areas in your
# application:
logger1 = logging.getLogger('')


logger1.info("**********************************************************************")   
logger1.info("Automation Execution          :%s"%str(config.CURRENT_TIME_STAMP))
logger1.info("Created APPLICATION Directory :%s"%config.APP_DIR)
logger1.info("Logger Directory              :%s"%config.LOGER_DIR)
logger1.info("Test result directory         :%s"%config.REPORT_DIR)
logger1.info("Test logger directory         :%s"%config.LOGGER_PATH)
# logger1.info("Test case summary file        :%s"%config.TC_REPORT_PATH)
logger1.info("Data Base validation summary  :%s"%config.DB_REPORT_SUMMARY_PATH)
logger1.info("**********************************************************************")


