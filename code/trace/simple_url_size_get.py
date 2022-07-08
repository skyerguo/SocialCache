import urllib.request

req = urllib.request.Request('http://pbs.twimg.com/media/DxZg4i7WwAAgXRL.jpg', method='HEAD')
f = urllib.request.urlopen(req)
print(f.headers['Content-Length'])
