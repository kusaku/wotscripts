# Embedded file name: scripts/client_common/client_request_lib/data_sources/fetcher.py


class FakeResponse(object):

    def __init__(self, r):
        """
                Create wrapper for response object
        """
        self.responseCode = r.status_code
        self.body = r.content

    def __repr__(self):
        return '[HTTP status: {}] {}'.format(self.responseCode, self.body)


def fetchURL(url, callback, headers = {}, timeout = 30, method = 'GET', postData = ''):
    """
            Simple synchronous implementation via requests library
            see http://docs.python-requests.org/en/latest/
    """
    import requests
    data = postData
    if isinstance(headers, (list, tuple)):
        res = {}
        for header in headers:
            a, b = header.split(':')
            res[a] = b

        headers = res
    if not isinstance(data, str) and data is not None:
        raise Exception('Unsupported parameter {}'.format(data))
    if method == 'GET':
        r = requests.get(url, headers=headers, data=data, verify=False)
    elif method == 'PUT':
        r = requests.put(url, headers=headers, data=data)
    elif method == 'POST':
        r = requests.post(url, headers=headers, data=data)
    elif method == 'PATCH':
        r = requests.patch(url, headers=headers, data=data)
    elif method == 'DELETE':
        r = requests.delete(url, headers=headers, data=data)
    else:
        raise Exception('Unsupported method {}'.format(method))
    callback(FakeResponse(r))
    return