import requests

resp = requests.get("http://www.baidu.com")
print(resp.cookies)
cookiess = resp.cookies
for key, value in cookiess.items():
    print(key, '=', value)

# headers cookie

headers = {

    'Host': 'localhost',
    'User-Agent': 'Mozilika',
    'Cookie': 'username=123456;password=8888888'
}

cookiese = "username=lqd;password=000000"
cookiesjar = requests.cookies.RequestCookieJar()
for cooki in cookiese.split(';'):
    key, value = cooki.split('=')
    cookiesjar.set(key, value)
requests.get("http://127.0.0.1:5000/readCookie", headers=headers, cookies=cookiesjar)

#
