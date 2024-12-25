import json
import time
import requests
import re

from login import login
from elect import ElectClass

if __name__ == "__main__":
    print("程序开始运行，请准备登录")
    cookies = login()
    print(cookies)
    ElectClass(cookies, "2614")
