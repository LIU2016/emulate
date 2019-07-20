import http.cookiejar, urllib.request

filename = "cookieL.txt"

cookie = http.cookiejar.LWPCookieJar()

cookie.load(filename=filename, ignore_expires=True, ignore_discard=True)

handler = urllib.request.HTTPCookieProcessor(cookie)

opener = urllib.request.build_opener(handler)

resp = opener.open("http://127.0.0.1:5000/readCookie")

print(resp.read().decode())
