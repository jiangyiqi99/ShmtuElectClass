import requests
import re
import time

# 用于储存用户上一次输入的课程号
lastCourseID = None

def get_course_id():
    """
    用于获取用户输入的课程号，并保存上一次的输入。
    """
    global lastCourseID
    while True:
        courseID = input("请输入课程号（按 Enter 重复上次课程号）：")
        if courseID.strip():
            lastCourseID = courseID.strip()
            return lastCourseID
        elif lastCourseID is not None:
            print(f"重复使用上次的课程号：{lastCourseID}")
            return lastCourseID
        else:
            print("请先输入课程号！")

def fetch_ticket(ticket_url, headers, pattern, max_retries, delay):
    """
    尝试从指定 ticket_url 获取选课所需的 ticket（elecSessionTime）。
    如果在 max_retries 次尝试后依旧失败，则返回 None。
    """
    retries = 0
    ticket = None

    while retries < max_retries:
        try:
            response = requests.get(ticket_url, headers=headers, timeout=(3, 3))
            matches = re.findall(pattern, response.text, re.DOTALL)
            if matches:
                for match in matches:
                    print(f"登录成功代码: {match}")
                    ticket = match
            else:
                print("登录失败，重试中...")
                retries += 1
                time.sleep(delay)
            if ticket is not None:
                break
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            retries += 1
            time.sleep(delay)

    return ticket

def do_elect(elect_url, headers, data):
    """
    发送选课请求，并解析返回结果。
    如果匹配到结果则打印，否则报错。
    """
    try:
        elect_response = requests.post(elect_url, headers=headers, data=data, timeout=(3, 3))
        pattern = r'text-align:left;margin:auto;">\s*(.*?)</div>'
        matches = re.findall(pattern, elect_response.text, re.DOTALL)
        if matches:
            print(matches[0].strip())
        else:
            print("选课错误")
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.RequestException as e:
        print(f"其他请求错误：{e}")

def ElectClass(cookieData, electionProfile: str):
    """
    选课主逻辑：
    1. 先尝试获取 ticket
    2. 循环获取用户输入课程号并发送选课请求
    """
    # 获取 Ticket 的网址
    Ticketurl = f"https://jwxt.shmtu.edu.cn/shmtu/stdElectCourse!defaultPage.action?electionProfile.id={electionProfile}##"

    # 选课的网址
    Electurl = "https://jwxt.shmtu.edu.cn/shmtu/stdElectCourse!batchOperator.action"

    # HTTP 请求头部
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookieData,
        "Host": "jwxt.shmtu.edu.cn",
        "Origin": "https://jwxt.shmtu.edu.cn",
        "Referer": "https://jwxt.shmtu.edu.cn/shmtu/stdElectCourse!defaultPage.action?electionProfile.id=2614",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
        "X-Requested-With": "XMLHttpRequest"
    }

    delay = 1       # 设置重试延时
    max_retries = 10  # 设置最大重试次数
    pattern = r'<input[^>]*id="elecSessionTime"[^>]*value="(\d{14})"'

    # 尝试获取 ticket
    ticket = fetch_ticket(Ticketurl, headers, pattern, max_retries, delay)

    # 如果成功获取到 ticket，则进行选课
    while ticket is not None:
        courseID = get_course_id()

        Electdata = {
            "profileId": electionProfile,
            "elecSessionTime": ticket,
            "operator0": courseID + ":true:0"
        }

        # 发送选课请求
        do_elect(Electurl, headers, Electdata)
