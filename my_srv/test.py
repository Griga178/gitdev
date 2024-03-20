'''
cd desktop/myfiles/dev/gitdev/my_srv
'''
from http.server import HTTPServer, BaseHTTPRequestHandler

class My_server(BaseHTTPRequestHandler):
    requests_2 = 0

    def do_GET(self):
        My_server.requests_2 += 1
        print(My_server.requests_2)

        self.send_response(200)
        self.end_headers()

        self.wfile.write(b'Hello, world!')

httpd = HTTPServer(('127.0.0.1', 7777), My_server)


if __name__ == '__main__':
    httpd.serve_forever()
