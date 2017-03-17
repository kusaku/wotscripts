# Embedded file name: scripts/common/exchangeapi/ErrorCodes.py
SUCCESS = 0
TIME_OUT = 1
IFACE_NOT_FOUND = 2
ADAPTER_NOT_FOUND = 3
WRONG_DATA_FORMAT = 4
VALIDATION_DATA_ERROR = 5
OBJECT_NOT_FOUND = 6
SAVE_TO_RESPOND_LATER = 7
CONCURRENT_REQUEST = 8
OBJECT_BUSY = 9
REQUESTS_LIMIT_OVERHEAD = 10
OUTDATED_DATA = 11
ERROR_DESCRIPTION = {SUCCESS: 'Ok',
 TIME_OUT: 'Time out',
 IFACE_NOT_FOUND: 'Iface not found',
 ADAPTER_NOT_FOUND: 'Adapter not found',
 WRONG_DATA_FORMAT: 'Wrong data format',
 VALIDATION_DATA_ERROR: 'Validation data error',
 OBJECT_NOT_FOUND: 'Object not found',
 CONCURRENT_REQUEST: 'Request till previous not processed',
 REQUESTS_LIMIT_OVERHEAD: 'Too mach requests in given period of time',
 OUTDATED_DATA: 'Data is outdated'}