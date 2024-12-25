import json
import time
import requests
import re

from login import login
from elect import ElectClass

if __name__ == "__main__":
    cookies = login()
    print(cookies)
    ElectClass(cookies, "2614")
