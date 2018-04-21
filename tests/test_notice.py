import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from notice import *

import unittest


class TestNotice(unittest.TestCase):
    """docstring for TestNotice"""

    def test_get_endpage_maxnum(self):
        self.assertTrue(isinstance(get_endpage_maxnum(HOMEURL), int))

    # def test_get_user_param(self):
    #     maxnum = get_endpage_maxnum(HOMEURL)
    #     startpage_num, endpage_num = get_user_param(maxnum)
    #     self.assertEqual

    def test_create_pageurl_list(self):
        self.assertTrue(
            'http://www5.ncwu.edu.cn/channels/5_2.html' in create_pageurl_list(1, 10))

    def test_get_data_from_pageurl(self):
        data = get_data_from_pageurl(HOMEURL)
        self.assertTrue(len(data) == 12)
        self.assertTrue(
            data['http://www5.ncwu.edu.cn/contents/11/45585.html']['title'] == '关于组织全校教职工专项体检的通知')

    def test_get_data_from_pageurl_list(self):
        data = get_data_from_pageurl_list(
            ['http://www5.ncwu.edu.cn/channels/5_2.html',
             'http://www5.ncwu.edu.cn/channels/5_3.html'])
        self.assertTrue(len(data) == 24)
        self.assertTrue(data['http://www5.ncwu.edu.cn/contents/13/45927.html']
                        ['title'] == '关于我校2017-2018学年第二学期国家助学金复核结果公示的通知')

    def test_get_text_and_upload_href(self):
        text, upload_href = get_text_and_upload_href(
            'http://www5.ncwu.edu.cn/contents/11/45585.html')
        self.assertTrue(isinstance(text, str))
        self.assertTrue(isinstance(upload_href, dict))

        self.assertTrue('为保障教职工身心健康' in text)
        self.assertTrue(len(upload_href) == 1)
        self.assertTrue(
            upload_href['http://www5.ncwu.edu.cn/upload/files/2018/3/1985521573.docx'] == '男女教职工体检项目.docx')

    def test_add_text_and_upload_href(self):
        data = add_text_and_upload_href(get_data_from_pageurl(
            'http://www5.ncwu.edu.cn/channels/5_2.html'))
        self.assertTrue(
            '校工会决定在全校开展2018年度“文明家庭”评选工' in data['http://www5.ncwu.edu.cn/contents/11/45920.html']['text'])
        self.assertTrue(data['http://www5.ncwu.edu.cn/contents/11/45920.html']['upload_href']
                            ['http://www5.ncwu.edu.cn/upload/files/2018/4/1219324962.docx']
                        == '评选标准.docx')


if __name__ == '__main__':
    unittest.main()
