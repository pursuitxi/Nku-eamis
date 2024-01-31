import bs4
from datetime import datetime
import requests
from cookies import *

def get_exam(cookies):
    timestamp = f'{int(datetime.now().timestamp() * 1000)}'

    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'Connection': 'keep-alive',
        # 'Cookie': 'wengine_vpn_ticketwebvpn_nankai_edu_cn=4ce1af13ee0d66d2; show_vpn=0; show_fast=0; heartbeat=1; show_faq=0; refresh=1',
        'Referer': 'https://webvpn.nankai.edu.cn/https/77726476706e69737468656265737421f5f64c95347e6651700388a5d6502720dc08a5/eams/home.action',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    requests.packages.urllib3.disable_warnings()

    response = requests.get(
        fr'https://webvpn.nankai.edu.cn/https/77726476706e69737468656265737421f5f64c95347e6651700388a5d6502720dc08a5/eams/stdExam!examTable.action?vpn-12-o2-eamis.nankai.edu.cn&examBatch.id=543&_={timestamp}',
        cookies=cookies,
        headers=headers,
        verify=False
    )

    if response.status_code == 200:
        html = response.content
        soup = bs4.BeautifulSoup(html, "html.parser")

        tbody = soup.find("tbody")

        exam_list = []

        # 遍历每一行
        for row in tbody.find_all("tr"):
            # 遍历每一列
            exam = ''
            for col in row.find_all("td"):
                # 在这里处理每个<td>元素的值
                value = col.get_text()
                if value == '\n':
                    continue
                else:
                    exam = exam + ' ' + value

            exam = exam.strip()
            exam_list.append(exam)

        for exam in exam_list:
            print(exam + '\n')
    else:
        print('error'+' '+str(response.status_code))

def main():
    username = input('请输入学号： ')
    password = input('请输入密码： ')
    start_time = time.time()
    try:
        file = open('cookies.txt', 'r')
        js = file.read()
        cookies = json.loads(js)
        get_exam(cookies)
        end_time = time.time()
    except Exception as e:
        print('cookie已过期，更新cookie')
        cookies = get_cookie(username,password)
        get_exam(cookies)
        get_exam(cookies)
        end_time = time.time()
    print('spend_time: ', end_time-start_time)

if __name__ == '__main__':
    main()