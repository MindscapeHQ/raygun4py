

def build_wsgi_compliant_request(request):
    if not request:
        return self

    # start with WSGI environ variables, then overlay the specific, expected
    # httpRequest keys for RG API compat
    # https://www.python.org/dev/peps/pep-3333/#environ-variables

    http_host = request.get('hostName') \
                or request.get('HTTP_HOST') \
                or "{}:{}".format(request.get('SERVER_NAME'), request.get('SERVER_PORT'))

    if http_host is not None:
        http_host = http_host.replace(' ', '')

    # TODO, better understand how to "properly" fallback to wsgi.input stream
    http_form = request.get('form') or request.get('wsgi.input')
    if http_form is not None:
        http_form = dict(http_form)

    try:
        rg_request = {
            'httpMethod': (request.get('httpMethod') or request.get('REQUEST_METHOD')),
            'url': (request.get('url') or request.get('PATH_INFO')),
            'hostName': http_host,
            'iPAddress': (request.get('ipAddress') or request.get('iPAddress') or request.get('REMOTE_ADDR')),
            'queryString': (request.get('queryString') or request.get('QUERY_STRING')),
            'headers': {}, # see below
            'form': http_form,
            'rawData': {}
        }
    except Exception:
        pass

    # Header processing
    _headers = request.get('headers')
    if _headers is None:
        # manually try to build up headers given known WSGI keys
        _headers = {
            'Content-Type': request.get('CONTENT_TYPE'),
            'Content-Length': request.get('CONTENT_LENGTH'),
        }

        for key, value in request.items():
            if key.startswith('HTTP_'):
                _headers[key] = value

    # force the values to be a dictionary as some frameworks don't treat them that way
    rg_request['headers'] = dict(_headers)

    return rg_request
