"""
This module fetches available OS Updates for iOS Devices
# -----------------------------------------------------------
# Original Author: Subhashini Tatipamula
# Created Date : 23-Nov-2018
# ------------------------------------------------------------
"""
# import statements for logger
from FetchiOSOSUpdatesInfo import get_iOS_OS_updates
from lib.HTTPMethodsWrapper import HTTPMethodsWrapper

rest_factory_instance = HTTPMethodsWrapper()
print get_iOS_OS_updates(rest_factory_instance)
