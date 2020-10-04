#contact@ash-king.co.uk

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("", "utf-8"))

    def do_GET(self):
        if self.path == '/status':
            self.resp_status()
        elif str(self.path).find('message?device=') > -1:
            self.resp_message()
        elif str(self.path).find('Fb4aBundle.bundle') > -1:
            self.resp_fb4a()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def resp_message(self):
        logging.info("resp_message")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("", "utf-8"))
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

    def resp_status(self):
        logging.info("resp_status")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("packager-status:running", "utf-8"))
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        
    def resp_fb4a(self):
        logging.info("resp_bundle")
        self.send_response(200)
        self.send_header('Content-type', 'multipart/mixed')
        self.end_headers()
        with open('FB4abundle.js', 'rb') as file: 
            self.wfile.write(file.read())
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

def run(server_class=HTTPServer, handler_class=S, port=8224):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    run()
