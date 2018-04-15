'''
功能:
爬取华北水利水电大学的学校通知页面(http://www5.ncwu.edu.cn/channels/5.html)，可指定开始页面和结束页面.

测试平台： ubuntu 16.04

依赖:
requests
bs4

2018/4/15
'''

import requests
import re
import json
import sys
import os
import time
import logging
from datetime import datetime
from bs4 import BeautifulSoup

headers = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate",
    # "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,ja;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    # "Cookie": "pgv_pvi=8494895104",
    "Cookie": "",
    "Host": "www5.ncwu.edu.cn",
    "Pragma": "no-cache",
    # "Referer": "http://www5.ncwu.edu.cn/channels/4.html",
    "Referer": "www5.ncwu.edu.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}





def get_endpage_maxnum():
    home_url = "http://www5.ncwu.edu.cn/channels/5.html"
    res = requests.get(home_url, headers=headers)
    res.encoding = 'utf-8'
    endpage_maxnum = int(re.findall(r'<a href="http://www5.ncwu.edu.cn/channels/\d_(\d+).html">末页</a>', res.text)[0])
    return endpage_maxnum

def get_user_param(ENDPAGE_MAXNUM):
    while True:
        try:
            user_input_raw = input("请输入起始页面和结束页面，以逗号‘，’隔开(如：1，10)。直接按回车以下载所有 {} 个页面。：\n".format(ENDPAGE_MAXNUM))
            if user_input_raw == "":
                startpage_num = 1
                endpage_num = ENDPAGE_MAXNUM                
            else:
                user_input = re.findall(r'\d+', user_input_raw)
                startpage_num, endpage_num = int(user_input[0]), int(user_input[1])
                
        except:
            print("{}\n 请输入整数，而不是字符串 \n".format(e))
            continue

        if not (startpage_num >= 1 and startpage_num <= endpage_num and endpage_num <= ENDPAGE_MAXNUM):
            print("范围出错\n")
            continue
        
        else:
            break

    return startpage_num, endpage_num

        

def main():
    INTERVAL = 10 

    print("程序开始...\n")
    print("正在获取 ncwu 的学校通知栏的页面范围...\n")

    ENDPAGE_MAXNUM = get_endpage_maxnum()
    print("获取到的页面范围为 (1 - {}) ，在输入范围时请不要超过。\n".format(ENDPAGE_MAXNUM))
    
    
    startpage_num,endpage_num = get_user_param(ENDPAGE_MAXNUM)
    
    pageurl_list = create_pageurl_list(startpage_num, endpage_num)

    root_dir = datetime.now().strftime('%Y%m%d_%H_%M_%S_ncwu_notice_')
    os.mkdir(root_dir)
    log_path = os.path.join(root_dir, datetime.now().strftime('%Y%m%d_%H_%M_%S') + '.log')
    logging.basicConfig(filename=log_path, level=logging.WARNING, format='%(asctime)s %(message)s')

    print("-------------------\n")
    print("初始化完成,设置为：\n")
    print("页面总范围：1 - {} \n".format(ENDPAGE_MAXNUM))
    print("下载范围：{} - {} \n".format(startpage_num, endpage_num))
    print("睡眠间隔：{}s \n".format(INTERVAL))
    print("下载文件夹路径 : {}\n".format(os.path.join(os.getcwd(), root_dir)))
    print("log file 路径 :{} \n".format(os.path.join(os.getcwd(), log_path)))
    print("程序将在 5 s 后开始下载...\n")
    print("按 Ctrl + C 取消下载.\n`")
    
    # print("Page url list Created:{}\n".format(pageurl_list))

    time.sleep(5)


    i = 1
    for page_url in pageurl_list:

        page_dir_path = os.path.join(root_dir, 'notice_5_' + str(i))
        os.mkdir(page_dir_path)
        
        data = get_data_from_page_url(page_url)
        # print(data)
        save_data(data, page_dir_path)
        
        i += 1
        time.sleep(INTERVAL)

    print('----------------------------------\n')
    print("下载完成，下载文件夹路径为: {}\n".format(os.path.join(os.getcwd(), root_dir)))
    print("下载失败信息存储在 log file ， 路径为: \n".format(os.path.join(os.getcwd(), log_path)))







def create_pageurl_list(startpage_num,endpage_num):
    pageurl_list = []
    for i in range(startpage_num,endpage_num+1):
        if i == 1:
            pageurl_list.append('http://www5.ncwu.edu.cn/channels/5.html')

        else:
            pageurl_list.append('http://www5.ncwu.edu.cn/channels/5_{}.html'.format(i)) 

    return pageurl_list







def get_data_from_page_url(page_url):
    print("resolve {}...\n".format(page_url))
    res = requests.get(page_url, headers=headers)
    res.encoding = 'utf-8'
    pattern = re.compile(r'<li>\s+【<a href="http://www5.ncwu.edu.cn/channels/\d*.html" class="dw">(.+)</a>】\s+<a href="http://www5.ncwu.edu.cn/contents/(.+)\.html" target="_blank"><span> (.+) </span> </a><i>(\d{4}-\d{2}-\d{2})</i></li>')
    result = re.findall(pattern, res.text)  # get list of tupbles like (department, href, title, create_time)

    data = {n[1]:{'department': n[0],'title': n[2], 'href': n[1], 'create_time':n[3]} for n in result}
    
    for href in data.keys():

        session = requests.Session()
        
        
        url = 'http://www5.ncwu.edu.cn/contents/{}.html'.format(href)
        print("get  {}...\n".format(url))
        res = session.get(url, headers=headers)
        
        soup = BeautifulSoup(res.content, 'lxml')

        try:
            text = get_text(soup)
            data[href]['text'] = text
        except:
            logging.critical('下载 {} 正文失败 \n'.format(url))
            data[href]['text'] = ''
        try:
            upload = get_upload(soup)
            data[href]['upload'] = upload
        except:
            logging.critical('下载 {} 附件失败\n'.format(url))
            data['href']['upload'] = {}

    return data




def get_text(soup):
    text_result = soup.find('div', class_='xinxi_con')
    text = ''
    for n in text_result.children:
        # print(n, n.name, type(n))
        # children includes tag and navigablestring
        if n.name == 'p':
            # print(n.text)
            text += (n.text + '\n')

    return text


def get_upload(soup):
    # upload_pattern = re.compile(r'http://www5.ncwu.edu.cn/upload/files/.+\..+')
    upload_pattern = re.compile(r'http://www5.ncwu.edu.cn/upload/.+')

    # string_pattern = re.compile(r'^(?!附件\d+).*$')
    # upload_result = soup.find_all('a', href=upload_pattern, string=string_pattern)  

    upload_result = soup.find_all('a', href=upload_pattern)  

    if upload_result:   
        upload = {n['href']:n.text for n in upload_result}

    else:
        upload = {}

    return upload





def save_upload(base, upload):
    for url,name in upload.items():
        # suffix = os.path.splitext(url)[-1]
        # save_path = os.path.join(base, name + suffix)
        save_path = os.path.join(base, name)
        print("save {}... \n".format(save_path))
        with open(save_path, 'wb') as f:
            f.write(requests.get(url).content)

def save_data(data, page_dir_path):



    
    for key,value in data.items():

        file_name = '[{}][{}][{}]'.format(value['department'], value['title'], value['create_time'])
        file_name = file_name.replace('/', '')
        file_name = file_name.replace('\\', '')

        # upload file existed, create a dir to save text and upload file
        if value['upload']:
            save_dir_path = os.path.join(page_dir_path, file_name)
            os.mkdir(save_dir_path)
            text_save_path = os.path.join(page_dir_path ,file_name, file_name)
            
            
            save_upload(save_dir_path, value['upload'])

            print("save {}...\n".format(text_save_path))
            with open(text_save_path, 'w') as f:
                f.write(value['text'])

        # no upload file , directly save text
        else:
            text_save_path = os.path.join(page_dir_path, file_name)
            print("save {}...\n".format(text_save_path))
            with open(text_save_path, 'w') as f:
                f.write(value['text'])           
            

if __name__ == '__main__':
    main()
    
