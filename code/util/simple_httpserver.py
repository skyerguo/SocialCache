#!/usr/bin/env python3
 
"""Python Web Server with upload functionality and SSL.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

For initial version, see: https://gist.github.com/UniIsland/3346170

Updated by midnightseer to include the ssl wrapper and command line options

"""
 
 
__version__ = "1.0"
__all__ = ["PythonWebServer"]
__author__ = "bones7456,midnightseer"
 
import os,sys
import posixpath
import http.server
import urllib.request, urllib.parse, urllib.error
import html
import shutil
import ssl
import mimetypes
import re
import argparse
from io import BytesIO
 


#######key.pem goes here########
key_pem = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDYe/JzvNhx/O4X
f2RHsSrUsJyTo83in7V9Vk8jhYccCPUeHQPr8n2aqtwkxA/tdTTqf61ynBAx7Ti2
OdN5eTyzocM3Dh0zck2SwWXRTzn6x/Ui+6+utbCWA4c3ueiSS7U+GXYL4hFNWUn1
wjeFCqH6i4WhfEn3tGvBrLextFhOc7N7SGC62WlXLXUD4Afv7LOsJ7lK9fmBv60a
d40Th5rsMDWGU+5QAlWhdcxNQ1fl6wYZ/McdoldLCYKZF0yqLfo2JPpBjgkqVhCt
lMSy67IB+pKiCi9v2syei5GKziZvvrMw/kJOSnL0dfzzVLenqOWZslXjO9JDWBZd
6ZG9iTxxAgMBAAECggEAEpZZ09wkDW11F+llN86badWcLAUFeW7TC2bstpURa7PN
L/+3xXt1k2EWM8XtxCqrF3NM9ik2LsM6elLuuGBTeOzrsP9yPGeVB4O5dUZDKSgg
ARfxFqQc/FRjOMKqmF0Nu74953lKmQSQmBxL3g1yqOtv1tSwGSeRlPh6cTSV3G5k
LRg/IhadwPsA2HwGiR6QU5TSCf9Gndw1GiAkjIzighR9DhTXgscP3grB08ex7K6e
KCebe9yJezBax8ibrrvIHACjcQ43dPGI92g/5oRRdWkOiHqcAtSPwv3TwKheG8pE
BrV+D2BGSUPntQS5t4b0EhNTlOOwLjGoDASIJjstjQKBgQD/J0DmiDjEUFMMxHuh
TVB3CUQ+P0IjCg+83uG6VexTHy4Ti7hzG7co8Do6JIj288qyfCFt16YhTf2o3vFZ
SHSS84KEJQNtIf0I2WUamHxZU48HIGhHg9kT4uDyAy/PTpS3+HFInfaTNp09pNTI
lmKkQpHytxEZoZ83GoNfpHy1rwKBgQDZM9hVjyFPvfs3i70R03ejfmUc7MwPAvSL
5rneuEOQRp3PbNmODnYXqz6UXSjx4CGP9Ajzetlv6n3oXsbYV5ptr1VfbGaN4Fus
Yvwmc5hWpXrJz2B2QWuPt4uPz9vn132cAEucEPGTJihpAZf3m+mZsLAfGi8hjGR3
0pdG8f/X3wKBgQD7zxuH6AxOAg/UW9y/FfRBZg3JeNimh/l8JmKTaNTwO6dXdt60
Czg52Ms+MmxRe8whVcwQAXFdEQEztcJuoMkbdeLq0zSMcaytHQ9grfial5JiMCN5
4K9NpuzlKyv15dFztmbmia6dHpsUCSZOR8xV27T52p2vtAfTdAEPVOAW1QKBgQCD
wludq3H9ubXHgFF1mt6co3QbE9rF0Hkg1Roz7Xuu7eeViOaAsm0Y9pzDy6+m6tvx
Q4yahw+YQJuYdsYRPzNDDnWvqUadElkKPhHQEZd8GG5gNhjCI/Vn/WQAHYu9HI/q
LpOvXOfu59rjuD/DySTwQqrUc0HcDBp2RZ3XP75/6QKBgDY+G8Kg+hcpKScf2SKE
DwChKqTDBIUU6hKMbIomIHBI4tXZGuYWESe7MgypYvftOZJxlAnUzNV1Wd1baX6D
oj4850PjKhaO0TfoIVda0oLOtKQdIQX+pkFmVeJxmwTdcIqA6MvYk+WSOTbaERET
FuHTvZElIItUHjMP9TI6rC44
-----END PRIVATE KEY-----"""

#######crt.pem goes here########
crt_pem = """-----BEGIN CERTIFICATE-----
MIIDazCCAlOgAwIBAgIUUoyr/cijbfsMFutoIiaBs5xS0T8wDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yMDA3MTExNTExMTZaFw0zMDA3
MDkxNTExMTZaMEUxCzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEw
HwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQDYe/JzvNhx/O4Xf2RHsSrUsJyTo83in7V9Vk8jhYcc
CPUeHQPr8n2aqtwkxA/tdTTqf61ynBAx7Ti2OdN5eTyzocM3Dh0zck2SwWXRTzn6
x/Ui+6+utbCWA4c3ueiSS7U+GXYL4hFNWUn1wjeFCqH6i4WhfEn3tGvBrLextFhO
c7N7SGC62WlXLXUD4Afv7LOsJ7lK9fmBv60ad40Th5rsMDWGU+5QAlWhdcxNQ1fl
6wYZ/McdoldLCYKZF0yqLfo2JPpBjgkqVhCtlMSy67IB+pKiCi9v2syei5GKziZv
vrMw/kJOSnL0dfzzVLenqOWZslXjO9JDWBZd6ZG9iTxxAgMBAAGjUzBRMB0GA1Ud
DgQWBBQefIi+94KRWSiWDFnCUB3EAB3tiDAfBgNVHSMEGDAWgBQefIi+94KRWSiW
DFnCUB3EAB3tiDAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQCb
Hn0yRnveHwzFxxRm8Qgra0uAYxs3z6UsK7EXcrnf6pf26eKPM7KV/iI8siEaXFW4
U1ulZ+pxKj6n6g0wFVZOamw5G5EPLkXXibixAdXCTWKOqBK5eNBPIZcsQe1ozDPk
KA1aoIOOFaec6BBaARiNxNEPebtPlFwIxAO4J3rAOYiE7hN3pBfjXlshxsTTYAnx
noTEKQfzLTGWZvRteIzuZGxfwjQvZOmRcTGwosXNzqRs4FWHKrOYhVAkZ9ijjtLR
hqETLhg4SEs82bXzqiSOTAd0R3zLZA54gPb9X0vwZQxnqR1XyQoHuzj8KsQnPeVK
fEOq7niByo0GsG8cvhHz
-----END CERTIFICATE-----"""


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
 
    """Simple HTTP request handler with GET/HEAD/POST commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.

    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.

    """
 
    server_version = "SimpleHTTPWithUpload/" + __version__
 
    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
 
    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()
 
    def do_POST(self):
        """Serve a POST request."""
        self.request.settimeout(10000)
        r, info = self.deal_post_data()
        print("[+] File Uploaded! {} --> {}".format(info, self.client_address))
        f = BytesIO()
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(b"<html>\n<title>Upload Result Page</title>\n")
        f.write(b"<body>\n<h2>Upload Result Page</h2>\n")
        f.write(b"<hr>\n")
        if r:
            f.write(b"<strong>Success:</strong>")
        else:
            f.write(b"<strong>Failed:</strong>")
        f.write(info.encode())
        f.write(("<br><a href=\"%s\">back</a>" % self.headers['referer']).encode())
        f.write(b"</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        
    def deal_post_data(self):
        content_type = self.headers['content-type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="fil.*"; filename="(.*)"', line.decode())
        if not fn:
            return (False, "Unable to locate file for upload...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect end of data.")
 
    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f
 
    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = BytesIO()
        displaypath = html.escape(urllib.parse.unquote(self.path))
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(("<html>\n<title>Directory listing for %s</title>\n" % displaypath).encode())
        f.write(("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath).encode())
        f.write(b"<hr>\n")
        f.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write(b"<input name=\"file\" type=\"file\"/>")
        f.write(b"<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write(b"<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write(('<li><a href="%s">%s</a>\n'
                    % (urllib.parse.quote(linkname), html.escape(displayname))).encode())
        f.write(b"</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f
 
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = [_f for _f in words if _f]
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path
 
    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)
 
    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
 
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']
 
    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })

def ssl_prep():

    try:
        with open("key.pem",'w') as file:
            file.write(key_pem)
    except:
        print("Unable to create key.pem")
        print(sys.exc_info())

    try:
        with open("crt.pem",'w') as file:
            file.write(crt_pem)
    except:
        print("Unable to create crt.pem")
        print(sys.exc_info())

def ssl_cleanup():
    try:
        os.remove("key.pem")
    except FileNotFoundError:
        print("Unable to Delete key.pem")
    try:
        os.remove("crt.pem")
    except FileNotFoundError:
        print("Unable to Delete crt.pem")

def test(PORT, HandlerClass = SimpleHTTPRequestHandler, ServerClass = http.server.HTTPServer):

    http.server.test(HandlerClass, ServerClass,port=PORT)
 
if __name__ == '__main__':
    p = argparse.ArgumentParser(description='A Better Python3 HTTP Server')
    p.add_argument('-p', '--port', type=int, default=8000, dest="port", action="store", help="the port for the http service to listen on")
    p.add_argument('-l', '--listen', type=str, default="0.0.0.0", dest="listen", action="store", help="the interface to bind to")
    p.add_argument('-n', '--no-ssl', action="store_true", default=False, dest="nossl", help="do not serve https / ssl")
    p.add_argument('-d', '--debug', action="store_true", default=False, help="use debug model to print some more logs")
    args = p.parse_args()

    try:
        if args.nossl:
            test(args.port, SimpleHTTPRequestHandler, http.server.HTTPServer)
        else:
            ssl_prep()
            httpd = http.server.HTTPServer((args.listen, args.port), SimpleHTTPRequestHandler)
            httpd.socket = ssl.wrap_socket (httpd.socket, keyfile='key.pem', certfile='crt.pem', server_side=True)
            print("Serving HTTPS on {l} port {p} (https://{l}:{p}/) ...".format(l=args.listen, p=args.port))
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("^punch!")
    finally:
        try:
            if args.nossl:
                pass
            else:
                ssl_cleanup()
        except:
            pass
 
# ####TO UPLOAD####
# get(){
# file=$1
# ip="10.10.14.8"
# port="8080"
# #echo $file $ip $port
# output=$(curl -k -i -X POST -F filename=@"$file" -F name=file "http://$ip:$port")
# if [[ "$output" == *"success"* ]]; then
#   echo "[+] Uploaded! --> $file"
# else
#   echo "[-] Upload Failed! --> $file $ip:$port"
# fi
# }

# get <file>
 
 