import os
PATH_FILE = "../Bible Academy Milano/DATABASE/"
USE_EXCEL = os.getenv("USE_EXCEL", "true").lower() == "true"
IS_LOCAL = os.getenv("IS_LOCAL", "true").lower() == "true"
PATH_CREDENTIAL = "../Bible Academy Milano/python/utility/"
CREDENTIAL_FIREBASE = os.getenv("CREDENTIAL_FIREBASE")
