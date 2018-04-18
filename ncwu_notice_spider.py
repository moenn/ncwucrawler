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

HEADERS = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate",
    # "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,ja;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    # "Cookie": "pgv_pvi=8494895104",
    # "Cookie": "",
    "Host": "www5.ncwu.edu.cn",
    # "Pragma": "no-cache",
    # "Referer": "http://www5.ncwu.edu.cn/channels/4.html",
    "Referer": "www5.ncwu.edu.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}

HOMEURL = "http://www5.ncwu.edu.cn/channels/5.html"


def get_endpage_maxnum(homeurl):
    resp = requests.get(homeurl, headers=HEADERS)
    resp.encoding = 'utf-8'
    endpage_maxnum = int(re.search(r'<a href="http://www5.ncwu.edu.cn/channels/\d_(\d+).html">末页</a>', resp.text).group(1))

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

def create_pageurl_list(startpage_num,endpage_num):
    pageurl_list = []
    for i in range(startpage_num,endpage_num+1):
        if i == 1:
            pageurl_list.append('http://www5.ncwu.edu.cn/channels/5.html')

        else:
            pageurl_list.append('http://www5.ncwu.edu.cn/channels/5_{}.html'.format(i)) 

    return pageurl_list


def get_data_from_pageurl(pageurl):
    '''
    visit a page url, and return a dict which includes 12 notices's data.  
    '''
    print("resolve {}...\n".format(pageurl))
    resp = requests.get(pageurl, headers=HEADERS)
    resp.encoding = 'utf-8'
    pattern = re.compile(r'<li>\s+【<a href="http://www5.ncwu.edu.cn/channels/\d*.html" class="dw">(.+)</a>】\s+<a href="http://www5.ncwu.edu.cn/contents/(.+)\.html" target="_blank"><span> (.+) </span> </a><i>(\d{4}-\d{2}-\d{2})</i></li>')
    result = re.finditer(pattern, resp.text)  # get list of tupbles like (department, href, title, create_time)

    data = {'http://www5.ncwu.edu.cn/contents/{}.html'.format(n.group(2)):{'department': n.group(1),'title': n.group(3), 'href': 'http://www5.ncwu.edu.cn/contents/{}.html'.format(n.group(2)), 'create_time':n.group(4)} for n in result}

    return data


def get_text_and_upload_href(noticeurl):
    resp = requests.get(noticeurl, headers=HEADERS)
    soup = BeautifulSoup(resp.content, 'lxml')
    # get text
    xinxi_con_children = soup.find('div', class_='xinxi_con').children      # children includes tag and navigablestring

    paragraphs = [n.text for n in xinxi_con_children if n.name == 'p']
    text = '\n'.join(paragraphs)

    # get upload href
    
    # upload_pattern = re.compile(r'http://www5.ncwu.edu.cn/upload/files/.+\..+')
    upload_pattern = re.compile(r'http://www5.ncwu.edu.cn/upload/.+')
    # string_pattern = re.compile(r'^(?!附件\d+).*$')
    # upload_result = soup.find_all('a', href=upload_pattern, string=string_pattern)  

    upload_result = soup.find_all('a', href=upload_pattern)  

    if upload_result:   
        upload_href = {n['href']:n.text for n in upload_result}

    else:
        upload_href = {}

    return text, upload_href

def add_text_and_upload_href(data):
    for key in data.keys():
        text, upload_href = get_text_and_upload_href(key)
        data[key]['text'] = text
        data[key]['upload_href'] = upload_href

    return data

def get_data_from_pageurl_list(pageurl_list):
    result = {}

    for n in map(get_data_from_pageurl, pageurl_list):
        result.update(n)

    return result

def download(data, root_dir):
    count = 0
    page = 1
    for key,value in data.items():

        if count%12 == 0:
            page_dir_path = os.path.join(root_dir, 'notice_5_' + str(page))
            os.mkdir(page_dir_path)
            page += 1
        count += 1

        file_name = '[{}][{}][{}]'.format(value['department'], value['title'], value['create_time'])
        file_name = file_name.replace('/', '')
        file_name = file_name.replace('\\', '')


        # upload file existed, create a dir to save text and upload file
        if value['upload_href']:
            save_dir_path = os.path.join(page_dir_path, file_name)
            os.mkdir(save_dir_path)
            text_save_path = os.path.join(page_dir_path ,file_name, file_name)
            
            # print("save {}...\n".format(text_save_path))
            with open(text_save_path + '.txt', 'w', encoding='utf-8') as f:
                f.write(value['text'])
            
            # save upload file
            for url,name in value['upload_href'].items():
                try:
                    save_path = os.path.join(save_dir_path, name)
                    # print("save {}... \n".format(save_path))
                    with open(save_path, 'wb') as f:
                        f.write(requests.get(url).content)
                except:
                    logging.critical('下载 {}[{}] 附件失败\n'.format(name, url))
                
        # no upload file , only save text
        else:
            text_save_path = os.path.join(page_dir_path, file_name)
            # print("save {}...\n".format(text_save_path))
            with open(text_save_path + '.txt', 'w', encoding='utf-8') as f:
                f.write(value['text'])       

        time.sleep(5)

def main():

    root_dir = datetime.now().strftime('%Y%m%d_%H_%M_%S_ncwu_notice')
    os.mkdir(root_dir)
    log_path = os.path.join(root_dir, datetime.now().strftime('%Y%m%d_%H_%M_%S') + '.log')
    logging.basicConfig(filename=log_path, level=logging.WARNING, format='%(asctime)s %(message)s')

    
    INTERVAL = 5

    print("正在获取 ncwu 的学校通知栏的页面范围...\n")

    ENDPAGE_MAXNUM = get_endpage_maxnum(HOMEURL)
    
    print("获取到的页面范围为 (1 - {}) ，在输入范围时请不要超过。\n".format(ENDPAGE_MAXNUM))
    
    startpage_num,endpage_num = get_user_param(ENDPAGE_MAXNUM)
    
    pageurl_list = create_pageurl_list(startpage_num, endpage_num)

    print("-------------------\n")
    print("初始化完成,设置为：\n")
    print("页面总范围：1 - {} \n".format(ENDPAGE_MAXNUM))
    print("下载范围：{} - {} \n".format(startpage_num, endpage_num))
    print("睡眠间隔：{}s \n".format(INTERVAL))
    print("下载文件夹路径 : {}\n".format(os.path.join(os.getcwd(), root_dir)))
    print("log file 路径 :{} \n".format(os.path.join(os.getcwd(), log_path)))
    print("程序将在 5 s 后开始下载...\n")
    print("按 Ctrl + C 取消下载.\n`")

    time.sleep(5)


    data = get_data_from_pageurl_list(pageurl_list)
    data = add_text_and_upload_href(data)
    download(data, root_dir)


    print('----------------------------------\n')
    print("下载完成，下载文件夹路径为: {}\n".format(os.path.join(os.getcwd(), root_dir)))
    print("下载失败信息存储在 log file ， 路径为: {} \n".format(os.path.join(os.getcwd(), log_path)))


if __name__ == '__main__':
    main()




