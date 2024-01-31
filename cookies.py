from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import json

def get_cookie(username, password):

    options = webdriver.EdgeOptions() # 创建一个配置对象
    options.add_argument("--headless") # 开启无界面模式

    browser = webdriver.Edge(options=options)

    url = 'https://webvpn.nankai.edu.cn/'

    browser.get(url=url)

    # 填写表单
    input = browser.find_elements(By.TAG_NAME,'input')
    input[0].send_keys(username)
    input[1].send_keys(password)

    # 通过验证码
    btn = browser.find_element(By.ID,'btn')
    action = ActionChains(browser)

    action.click_and_hold(btn).perform()
    action.move_by_offset(xoffset=260, yoffset=0).perform()
    action.release().perform()

    browser.find_element(By.ID,'submitRole').click()

    time.sleep(1)

    cookies = browser.get_cookies()
    cookie = {}

    for item in cookies:
        # print(item['name']+' '+item['value'])
        cookie[item['name']] = item['value']
    # 关闭浏览器
    browser.close()

    with open('cookies.txt', 'w', encoding='utf-8') as f:
        # 将dic dumps json 格式进行写入
        f.write(json.dumps(cookie))

    return cookie
