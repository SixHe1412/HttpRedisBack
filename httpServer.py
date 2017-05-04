import SimpleHTTPServer
import SocketServer
import urlparse
import json
import queryRedis

PORT = 9001

class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        print "GET"
        qs = urlparse.parse_qs(urlparse.urlparse(self.path).query)

        result_list = queryRedis.query(qs)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        #print result_list
        print len(result_list)

        self.wfile.write(json.dumps(result_list))
        return


httpd = SocketServer.TCPServer(("", PORT), myHandler)
print "serving at port", PORT
httpd.serve_forever()