import SimpleHTTPServer
import SocketServer
import urlparse
import json
import queryRedis
from SocketServer import ThreadingMixIn
import queryRedis2

HOST_IP = ''
PORT = 9001

class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        print "GET"
        qs = urlparse.parse_qs(urlparse.urlparse(self.path).query)


        result_list = json.loads(queryRedis.query(qs))
        #result_list = queryRedis.query(qs)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        #print result_list
        print len(result_list)

        self.wfile.write(json.dumps(result_list))
        return


    #def do_GET(self):
    #    try:
    #        print "GET"
    #        qs = urlparse.parse_qs(urlparse.urlparse(self.path).query)
#
#
    #        result_list = json.loads(queryRedis.query(qs))
    #        #result_list = queryRedis.query(qs)
#
    #        self.send_response(200)
    #        self.send_header('Content-type', 'application/json')
    #        self.send_header('Access-Control-Allow-Origin', '*')
    #        self.end_headers()
#
    #        #print result_list
    #        print len(result_list)
#
    #        self.wfile.write(json.dumps(result_list))
    #    except IOError:
    #        self.send_error(404, message=None)

#class ThreadingHttpServer( ThreadingMixIn, SimpleHTTPServer ):
#    pass


httpd = SocketServer.TCPServer((HOST_IP, PORT), myHandler)
#httpd = ThreadingHttpServer((HOST_IP, PORT), myHandler)
print "serving at port", PORT
httpd.serve_forever()