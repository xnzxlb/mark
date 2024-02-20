import os
import sys
import time
import requests
import schedule
import datetime


# 短息服务
def Message(txt):
    messurl = 'https://api.smsbao.com/'.format(
        txt)
    msg = requests.get(messurl)
    print(msg)


def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 主方法
def Request():
    # 请求路径
    url = "https://yz.chsi.com.cn/apply/cjcx/cjcx.do"

    # 请求数据
    payload = {
        "xm": "张三",
        "zjhm": "889281999938192918",
        "ksbh": "8888888888",
        "bkdwdm": "18888",
        "checkcode": ""  # 验证码处理方式需要另外考虑
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://yz.chsi.com.cn/apply/cjcx/t/10479.dhtml'
    }

    data_directory = 'Data'

    try:
        # 检查data目录是否存在，如果不存在则创建
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

        res = requests.post(url=url, headers=headers, data=payload)
        res.encoding = 'utf-8'
        if "无查询结果" in res.text:
            print(f"{current_timestamp()}-无查询结果")
        else:
            print(f"{current_timestamp()}-页面发生变动可能出成绩了")
            # 发送短信提醒
            Message("页面发生变动可能出成绩了")
            # 获取当前时间戳
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'result_page_{timestamp}.html'

            # 在data目录下保存页面内容到文件
            full_path = os.path.join(data_directory, file_name)

            # 可以在这里保存页面内容到文件
            with open(full_path, 'w', encoding='utf-8') as fileData:
                fileData.write(res.text)
    except Exception as e:
        print(f"{current_timestamp()}-请求失败:", e)


# 从配置文件读取时间间隔
with open('config.txt', 'r') as file:
    interval = int(file.read().strip())
# 定时任务
schedule.every(interval).seconds.do(Request)

# 循环执行
try:
    while True:
        schedule.run_pending()
        time.sleep(1)  # 减少CPU占用
except KeyboardInterrupt:
    sys.exit(0)
