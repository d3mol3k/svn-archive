# -*- coding: utf-8 -*-

import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import osray

options = {'height': 100, 'dsn': 'dbname=gis', 'width': 100, 'prefix': 'planet_osm', 'quick': False, 'hq': False}
options['bbox']='9.94861 49.79293,9.96912 49.80629' # Europastern
#options['bbox']='9.92498 49.78816,9.93955 49.8002' # Innenstadt


# for tile names and coordinates:
# http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames

class osrayHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            theurl = self.path
            if theurl == "/favicon.ico":
                self.send_response(200)
                self.end_headers()
                self.wfile.write("")
                return
            urlcomponents = urlparse.urlparse(theurl)
            print urlcomponents
            baseurl = urlcomponents[2]
            print "parse=",urlparse.urlparse(theurl)
            print "base=",baseurl
            urlqs = urlparse.urlparse(theurl)[4]
            print "URL qs:", urlqs
            queryparams = urlparse.parse_qs(urlqs)
            print queryparams
            if baseurl.endswith(".png"):
                if queryparams.has_key('width'):
                    options['width']=queryparams['width'][0]
                if queryparams.has_key('height'):
                    options['height']=queryparams['height'][0]
                if queryparams.has_key('hq'):
                    options['hq']=(str(queryparams['hq'][0])=='1')
                print "--- calling osray"
                osray.main(options)
                print "--- calling osray ends"
                f = open(curdir + sep + 'scene-osray.png')
                self.send_response(200)
                self.send_header('Content-type','image/png')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return
            print "URL was ", theurl
            urlqs = urlparse.urlparse(theurl)[4]
            print "URL qs:", urlqs
            queryparams = urlparse.parse_qs(urlqs)
            print queryparams
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("hey, today is the" + str(time.localtime()[7]))
            self.wfile.write(" day in the year " + str(time.localtime()[0]))
            return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


"""
    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query = cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            
            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);
            
        except :
            pass
"""

def main():
    try:
        server = HTTPServer(('', 8087), osrayHandler)
        print 'started osray server...'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
