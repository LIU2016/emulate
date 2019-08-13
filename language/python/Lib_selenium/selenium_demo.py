'''

selenium \ webdriver

控制浏览器
    chromeDriver
    IEdriverServer
    MicrosoftWebDriver

    https://docs.seleniumhq.org/download/

    附chromedriver与chrome的对应关系表：
    注意本机chrome的版本与chromedriver的版本对应关系
    chromedriver版本	支持的Chrome版本
    v2.43	v69-71
    v2.42	v68-70

查找单个节点


'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import  WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

brower = webdriver.Chrome("./webdriver/chromedriver.exe")
try:
   brower.get("https://www.jd.com")
   input = brower.find_element_by_id('key')
   input.send_keys('Python从菜鸟到高手')
   input.send_keys(Keys.ENTER)
   #等待所有的元素渲染完成
   wait = WebDriverWait(brower,4)
   wait.until(ec.presence_of_all_elements_located((By.ID,'J_goodsList')))
   print(brower.current_url)
   print(brower.page_source)
except Exception as e:
    print(e)
    brower.close()
