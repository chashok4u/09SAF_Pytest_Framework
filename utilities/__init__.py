from utilities.ui_utility.ui import Browser, update_step
from utilities.api_utility.api_utility import APIRequest
from utilities.api_utility.api_smoke_utility import SmokeApi
from utilities.report_utility.TestReports import ReportsFinal
# from utilities.db_utility.db import Database
from utilities.compare_utility.compare import Compare
# from utilities.crypt_utility.encryption_utility import Cryptography
# from utilities.sftp_utility.sftp import Sftp

browser = Browser()
api = APIRequest()
smoke_api = SmokeApi()
report = ReportsFinal()
# db = Database()
compare = Compare()
# cryptography = Cryptography()
# sftp =Sftp ()


__version__ = "3.1.0"
__name__ = "utilities"
