import logging
import logging.config
#import os
# import yaml
# Read logging.yaml format file
# try:
#     with open(os.path.dirname(os.path.abspath(__file__)) + "/logging.yaml", 'r') as f:
#         log_cfg = yaml.safe_load(f.read())
# except Exception as E:
#     raise E

from utilities.format_logging import format_logger as log_cfg

# Logger format configuration
logging.config.dictConfig(log_cfg)


# Creating logger method for global use..
def get_logger():
    complete_log = logging.getLogger(__name__)
    complete_log.setLevel(logging.DEBUG)
    return complete_log


