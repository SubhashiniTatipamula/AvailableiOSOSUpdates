#!c:\python27\bin
# -----------------------------------------------------------
# Original Author: Subhashini Tatipamula
# Created Date : 03-Nov-2014
# Created Date: 11-Nov-2017
# ------------------------------------------------------------
"""
Wrapper APIs written for urllib3 for HTTP Calls
"""

# import statements for logger
from lib.LoggerWrapper import LoggerWrapper
import traceback

# Imports from Python
from datetime import datetime
import time

try:
    import urllib3
    from urllib3.exceptions import ReadTimeoutError
    from urllib3.exceptions import NewConnectionError
    from urllib3.exceptions import ConnectTimeoutError

    urllib3.disable_warnings()

except ImportError, e:
    print "Install urllib3 package"


# Constants / Global variables


class HTTPMethodsWrapper:
    """
    This class has methods of REST calls implementation
    """

    # Making as static variable
    manager = logger = None
    pool_time_out = None

    def __init__(self, pool_time_out=60.0, no_of_retries=0, pool_count=50):
        """
        This constructor initializes class variables
        :arg: pool_time_out connection pool timeout
        :arg: no_of_retries retries count
        :arg: pool_count pool count
        """

        HTTPMethodsWrapper.pool_time_out = pool_time_out

        try:

            if no_of_retries:
                HTTPMethodsWrapper.manager = urllib3.PoolManager(int(pool_count), retries=int(no_of_retries),
                                                                 maxsize=int(pool_count), timeout=pool_time_out)
            else:
                HTTPMethodsWrapper.manager = urllib3.PoolManager(int(pool_count), retries=False,
                                                                 maxsize=int(pool_count), timeout=pool_time_out)
            # Log file handler
            HTTPMethodsWrapper.logger = LoggerWrapper().get_logger()
        except Exception:
            print traceback.format_exc()
            print 'Failed in initializing default values..'

    def make_get_request(self, url_resource, headers_dict=None, request_time_out=None, response_headers=False):
        """
        This function simulates the GET call and extracts the data
        required for the end user based on the URL passed.
            :arg: endpoint url resource string.
            :arg: headers in the form of dictionary.
            :arg: timeout option
            :arg: response headers required or not?
            :returns: Request data/status/headers or 0.
        """
        try:
            self.logger.debug('HTTPMethodsWrapper:make_GET_request++')
            resource = url_resource
            self.logger.debug("GET Request URL: " + resource)
            if headers_dict is None:
                headers_dict = {}
            elif not isinstance(headers_dict, dict):
                self.logger.error(" headers should be of type dictionary .., ")
                return 1
            self.logger.debug("GET Request Headers: " + str(headers_dict))
            if request_time_out is None:
                time_out = HTTPMethodsWrapper.pool_time_out
            else:
                time_out = request_time_out

            self.logger.debug("Invoking Endpoint: " + url_resource)
            start_time = datetime.now()
            request = HTTPMethodsWrapper.manager.request('GET', resource, headers=headers_dict, timeout=time_out)
            end_time = datetime.now()
            self.logger.debug(url_resource + " took: " + str(end_time - start_time))
            self.logger.debug("GET Request: Data: %s" % request.data)
            self.logger.debug("GET Request Status: %s" % request.status)
            if 200 == request.status or 204 == request.status:
                pass
            else:
                self.logger.debug("GET Response Data: %s" % request.data)
                self.logger.debug("GET Response Headers: %s" % request.headers)
            self.logger.debug('HTTPMethodsWrapper:make_GET_request--')
            if response_headers:
                return request.data, request.status, request.headers
            else:
                return request.data, request.status
        except NewConnectionError:
            time.sleep(0.5)
            self.logger.debug("NewConnectionError, retrying after 0.5 sec")
            return self.make_get_request(url_resource, headers_dict, request_time_out, response_headers)
        except ReadTimeoutError:
            self.logger.error("Failed to make GET request, ReadTimeoutError.")
        except ConnectTimeoutError:
            self.logger.error("Failed to make GET request, ConnectTimeoutError.")
        except Exception:
            self.logger.error("Failed to make GET request")
            self.logger.exception(traceback.format_exc())
        self.logger.debug('HTTPMethodsWrapper:make_GET_request--')
        return 0

    def make_post_request(self, url_resource, post_body_data, headers_dict=None, request_time_out=None,
                          response_headers=False):
        """
            This makes a POST request with the given arguments
            :arg: endpoint url resource string
            :arg: post_body_data - Data for POST request body
            :arg: headers in the form of dictionary.
            :arg: timeout option
            :arg: response headers required or not?
            :returns: Request data/status/headers or 0
        """
        try:
            self.logger.debug('HTTPMethodsWrapper:make_POST_request++')
            resource = url_resource
            self.logger.debug("POST Request URL: " + resource)
            self.logger.debug("POST Request Body: " + str(post_body_data))
            if headers_dict is None:
                headers_dict = {}
            elif not isinstance(headers_dict, dict):
                self.logger.error("Header should be of type dictionary ..,")
                return 1
            self.logger.debug("POST Request Header: " + str(headers_dict))
            if request_time_out is None:
                time_out = HTTPMethodsWrapper.pool_time_out
            else:
                time_out = request_time_out
            self.logger.debug("Invoking Endpoint: " + url_resource)
            start_time = datetime.now()
            request = HTTPMethodsWrapper.manager.urlopen('POST', resource, headers=headers_dict, body=post_body_data,
                                                         timeout=time_out)
            end_time = datetime.now()
            self.logger.debug(url_resource + " took: " + str(end_time - start_time))
            self.logger.debug("POST Response Data: %s" % (request.data))
            self.logger.debug("POST Response Status: %s " % request.status)
            if 200 == request.status or 204 == request.status:
                pass
            else:
                self.logger.debug("POST Response Data: %s" % request.data)
                self.logger.debug("POST Response Headers: %s" % request.headers)
            self.logger.debug('HTTPMethodsWrapper:make_POST_request--')
            if response_headers:
                return request.data, request.status, request.headers
            else:
                return request.data, request.status
        except NewConnectionError:
            time.sleep(0.5)
            self.logger.debug("NewConnectionError, retrying after 0.5 sec")
            return self.make_post_request(url_resource, post_body_data, headers_dict, request_time_out,
                                          response_headers)
        except ReadTimeoutError:
            self.logger.error("Failed to make POST request, ReadTimeoutError.")
        except ConnectTimeoutError:
            self.logger.error("Failed to make POST request, ConnectTimeoutError.")
        except Exception:
            self.logger.error("Failed to make POST request")
            self.logger.exception(traceback.format_exc())
        self.logger.debug('HTTPMethodsWrapper:make_POST_request--')
        return 1, 1

    def make_put_request(self, url_resource, put_body_data, headers_dict=None, request_time_out=None,
                         response_headers=False):
        """
            This makes a PUT request with the given arguments
            :arg: endpoint url resource string
            :arg: put_body_data - Data for PUT request body
            :arg: headers in the form of dictionary.
            :arg: timeout option
            :arg: response headers required or not?
            :returns: Request data/status/headers or 0
        """
        try:
            self.logger.debug('HTTPMethodsWrapper:make_PUT_request++')
            resource = url_resource
            self.logger.debug("PUT Request URL: " + resource)
            self.logger.debug("PUT Request Body: " + put_body_data)
            if headers_dict is None:
                headers_dict = {}
            elif not isinstance(headers_dict, dict):
                self.logger.error("Header should be of type dictionary ..,")
                return 1
            self.logger.debug("PUT Request Header: " + str(headers_dict))
            if request_time_out is None:
                time_out = HTTPMethodsWrapper.pool_time_out
            else:
                time_out = request_time_out
            self.logger.debug("Invoking Endpoint: " + url_resource)
            start_time = datetime.now()
            request = HTTPMethodsWrapper.manager.urlopen('PUT', resource, headers=headers_dict, body=put_body_data,
                                                         timeout=time_out)
            end_time = datetime.now()
            self.logger.debug(url_resource + " took: " + str(end_time - start_time))
            self.logger.debug("POST Response Data: %s" % request.data)
            self.logger.debug("POST Response Status: %s " % request.status)
            if 200 == request.status or 204 == request.status:
                pass
            else:
                self.logger.debug("POST Response Data: %s" % request.data)
                self.logger.debug("POST Response Headers: %s" % request.headers)
            self.logger.debug('HTTPMethodsWrapper:make_PUT_request--')
            if response_headers:
                return request.data, request.status, request.headers
            else:
                return request.data, request.status
        except NewConnectionError:
            time.sleep(0.5)
            self.logger.debug("NewConnectionError, retrying after 0.5 sec")
            return self.make_put_request(url_resource, put_body_data, headers_dict, request_time_out, response_headers)
        except ReadTimeoutError:
            self.logger.error("Failed to make PUT request, ReadTimeoutError.")
        except ConnectTimeoutError:
            self.logger.error("Failed to make PUT request, ConnectTimeoutError.")
        except Exception:
            self.logger.error("Failed to make PUT request")
            self.logger.exception(traceback.format_exc())
        self.logger.debug('HTTPMethodsWrapper:make_PUT_request--')
        return 1, 1

    def make_options_request(self, url_resource, headers_dict=None, request_time_out=None):
        """
            This makes a OPTIONS request with the given arguments
            :arg: endpoint url resource string
            :arg: headers in the form of dictionary.
            :arg: timeout option
            :arg: response headers required or not?
            :returns: Request data/status/headers or 0
        """
        try:
            self.logger.debug('HTTPMethodsWrapper:make_OPTIONS_request++')
            resource = url_resource
            self.logger.debug("OPTIONS Request URL: " + resource)
            if headers_dict is None:
                headers_dict = {}
            elif not isinstance(headers_dict, dict):
                self.logger.error("Header should be of type dictionary ..,")
                return 1
            self.logger.debug("OPTIONS Request Header: " + str(headers_dict))
            if request_time_out is None:
                time_out = HTTPMethodsWrapper.pool_time_out
            else:
                time_out = request_time_out
            self.logger.debug("Invoking Endpoint: " + url_resource)
            start_time = datetime.now()
            request = HTTPMethodsWrapper.manager.urlopen('OPTIONS', resource, headers=headers_dict, timeout=time_out)
            end_time = datetime.now()
            self.logger.debug(url_resource + " took: " + str(end_time - start_time))
            self.logger.debug("OPTIONS Response: Data: %s, Status: %s " % (request.data, request.status))
            self.logger.debug('HTTPMethodsWrapper:make_OPTIONS_request--')
            return request.headers, request.status
        except NewConnectionError:
            time.sleep(0.5)
            self.logger.debug("NewConnectionError, retrying after 0.5 sec")
            return self.make_options_request(url_resource, headers_dict, request_time_out)
        except ReadTimeoutError:
            self.logger.error("Failed to make OPTIONS request, ReadTimeoutError.")
        except ConnectTimeoutError:
            self.logger.error("Failed to make OPTIONS request, ConnectTimeoutError.")
        except Exception:
            self.logger.error("Failed to make OPTIONS request")
            self.logger.exception(traceback.format_exc())
        self.logger.debug('HTTPMethodsWrapper:make_OPTIONS_request--')
        return 1, 1

    def make_delete_request(self, url_resource, delete_body_data, headers_dict=None, request_time_out=None,
                            response_headers=False):
        """
            This makes a DELETE request with the given arguments
            :arg: endpoint url resource string
            :arg: delete_body_data - Data for DELETE request body
            :arg: headers in the form of dictionary.
            :arg: timeout option
            :arg: response headers required or not?
            :returns: Request data/status/headers or 0
        """
        try:
            self.logger.debug('HTTPMethodsWrapper:make_DELETE_request++')
            resource = url_resource
            self.logger.debug("DELETE Request URL: " + resource)
            self.logger.debug("DELETE Request Body: " + str(delete_body_data))
            if headers_dict is None:
                headers_dict = {}
            elif not isinstance(headers_dict, dict):
                self.logger.error("Header should be of type dictionary ..,")
                return 1
            self.logger.debug("POST Request Header: " + str(headers_dict))
            if request_time_out is None:
                time_out = HTTPMethodsWrapper.pool_time_out
            else:
                time_out = request_time_out
            self.logger.debug("Invoking Endpoint: " + url_resource)
            start_time = datetime.now()
            request = HTTPMethodsWrapper.manager.urlopen('DELETE', resource, headers=headers_dict,
                                                         body=delete_body_data, timeout=time_out)
            end_time = datetime.now()
            self.logger.debug(url_resource + " took: " + str(end_time - start_time))

            self.logger.debug("DELETE Response Status: %s " % request.status)
            if 200 == request.status or 204 == request.status:
                pass
            else:
                self.logger.debug("DELETE Response Data: %s" % request.data)
                self.logger.debug("DELETE Response Headers: %s" % request.headers)
            self.logger.debug('HTTPMethodsWrapper:make_DELETE_request--')
            if response_headers:
                return request.data, request.status, request.headers
            else:
                return request.data, request.status
        except ReadTimeoutError:
            self.logger.error("Failed to make DELETE request, ReadTimeoutError.")
        except Exception:
            self.logger.error("Failed to make DELETE request")
            self.logger.exception(traceback.format_exc())
        self.logger.debug('HTTPMethodsWrapper:make_DELETE_request--')
        return 1
