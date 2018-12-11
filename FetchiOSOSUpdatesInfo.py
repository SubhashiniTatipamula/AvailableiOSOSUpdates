"""
This module fetches available OS Updates for iOS Devices
# -----------------------------------------------------------
# Original Author: Subhashini Tatipamula
# Created Date : 23-Nov-2018
# ------------------------------------------------------------
"""
# import statements for logger
from lib.LoggerWrapper import LoggerWrapper

import traceback
import re


def get_iOS_OS_updates(rest_factory_instance):
    """
    This method fetches current and Beta OS updates for iOS device
    :arg rest_factory_instance: urllib3 object
    :returns empty or OS update info dictionary
    """
    logger_obj = LoggerWrapper().get_logger()
    logger_obj.debug('iOSOSUpdatesInfo:get_iOS_OS_updates++')
    os_updates = list()
    try:
        url_resource = "https://en.wikipedia.org/wiki/IOS_version_history"
        response, status = rest_factory_instance.make_get_request(url_resource)
        if 200 == status:
            logger_obj.info("successfully got OS updates data")

            # collecting current OS version
            scraped_data = response.split('<td style="background:#d4f4b4;">')[1].split("<th>Legend:")[0]
            scraped_data = scraped_data.strip().splitlines()
            target_expression = re.compile(r'<[^>]+>')

            # Removing HTML Tags
            for index, line in enumerate(scraped_data):
                os_update = dict()
                found = line.find('">')
                while -1 != found:
                    space = line.find(' ')
                    line = line[:space] + ">" + line[found + 2:]
                    if "<sup" in line:
                        line = line[:line.find("<sup")]
                    found = line.find('">')
                line = target_expression.sub('', line)
                scraped_data[index] = line
                if "." in line:
                    os_update["Version"] = line
                    os_update["Build"] = scraped_data[index + 2].split('<td>')[1]
                    os_updates.append(os_update)

            logger_obj.debug(scraped_data)
            logger_obj.info("iOS OS Updates info: " + str(os_updates))
        else:
            logger_obj.error("Failed to fetch iOS OS updates")
    except:
        logger_obj.error("Failed to fetch iOS OS updates")
        logger_obj.exception(traceback.format_exc())
        os_updates = {}
    logger_obj.debug('iOSOSUpdatesInfo:get_iOS_OS_updates--')
    return os_updates
