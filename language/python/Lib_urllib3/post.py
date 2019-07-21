from urllib3 import *

http= PoolManager()

http.request(url="http://127.0.0.1:5000/register",method="POST",fields={'username':'lqd','password':'123456'})

