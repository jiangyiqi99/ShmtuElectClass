import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def login():
    # 配置 Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # 替换为你的 ChromeDriver 路径
    service = Service('./chromedriver')
    browser = webdriver.Chrome(service=service, options=chrome_options)

    # 打开指定网址
    url = "https://jwxt.shmtu.edu.cn/shmtu/stdElectCourse.action"
    browser.get(url)

    # 等待用户登录并检测 cookie 是否写入
    def wait_for_cookie():
        while True:
            cookies = browser.get_cookies()
            cookie_str = format_cookies(cookies)
            if "srv_id" in cookie_str:
                return cookie_str
            time.sleep(1)

    def format_cookies(cookies):
        cookie_list = [f"{cookie['name']}={cookie['value']}" for cookie in cookies]
        return "; ".join(cookie_list)

    try:
        print("请在打开的窗口中完成登录...")
        cookies_str = wait_for_cookie()

        # 检测到包含 "device_id" 的 Cookie 长字符串后保存
        print("Cookies 已保存:", cookies_str)
        return cookies_str

    finally:
        # 关闭浏览器窗口
        browser.quit()
