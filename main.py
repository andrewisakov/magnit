#!/usr/bin/python3
from wsgiref.simple_server import make_server
import settings
import views
import routes


ROUTES = {
    'GET': {
        '/view/': views.view,
        '/comment/': views.comment,
        '/delete_comment/': views.delete_comment,
        '/stat/': views.stat,
        '/stat_region/': views.stat_region,
    },
    'POST': {
        '/comment/': views.post_comment,
        '/villages': views.villages,
    },
}


def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    path = environ['PATH_INFO'].lower()
    method = environ['REQUEST_METHOD'].upper()
    query_string = environ['QUERY_STRING']
    response_body = b''
    # print('\n'.join([f'{e} {environ[e]}' for e in sorted(environ)]))
    try:
        # print('request_body_length=', environ.get('CONTENT_LENGTH', 0))
        # print('wsgi.input', environ['wsgi.input'].readline())
        request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
    except (TypeError, ValueError) as e:
        print(e)
        request_body = '0'
    # print('requst_body=', request_body)

    # print(environ['SERVER_PROTOCOL'].upper())

    if path == '/':
        status = '302 Found'
        response_headers = [('Location', 'http://'+environ['HTTP_HOST']+'/view/')]
    else:
        if method == 'POST':
            response = ROUTES['POST'][path](request_body)
            if response[0]:
                status, target = response
                response_headers = [('Location', 'http://' + environ['HTTP_HOST'] + target)]
                response_body = b''
            else:
                response_body = response[1]

        if method == 'GET':
            # path = '/view/' if path == '/' else path
            html = path.split('/')[0]
            html = (settings.TEMPLATES + html + '.html') if html else ''
            # if html:
            # print(method, path, query_string)
            try:
                status, response_body = ROUTES['GET'][path](query_string) if query_string else ROUTES['GET'][path]()
                if status:
                    response_headers = [('Location', 'http://' + environ['HTTP_HOST'] + response_body)]
                    response_body = b''
                else:
                    status = '200 OK'
                # print(response_body)
            except Exception as e:
                print('application.GET exception:', e)

    # print(status, response_headers)
    start_response(status, response_headers)
    return [response_body]


if __name__ == '__main__':
    # print(settings.BASE_DIR)
    # print(settings.TEMPLATES)
    # print(settings.DB_NAME)
    # print(settings.SQL_PATH)
    with make_server('', 8000, application) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
