'''

读取Cookie
保存成文件（MozillaCookieJar）
LWPCookieJar
libwww-perl


'''
import http.cookiejar, urllib.request

filenameM = 'cookieM.txt'
filenameL = 'cookieL.txt'

cookieM = http.cookiejar.MozillaCookieJar(filenameM)
cookieL = http.cookiejar.LWPCookieJar(filenameL)

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookieM)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
for item in cookie:
    print(item.name + '=' + item.value)

print('----------------------------------')

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookieL)
opener = urllib.request.build_opener(handler)
response = opener.open("http://127.0.0.1:5000/setCookie")
for item in cookie:
    print(item.name + "=" + item.value)

cookieM.save(ignore_discard=True,ignore_expires=True)
cookieL.save(ignore_discard=True,ignore_expires=True)

