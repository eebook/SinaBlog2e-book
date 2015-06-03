# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    worker.py
# Description :    爬取网页的内容
# Author      :    Frank
# Date        :    2014.06.03
# ######################################################

import threading
import re

from codes.baseclass import *


class PageWoker(BaseClass, HttpBaseClass):
    def __init__(self, url_info={}):
        self.url_info = url_info
        # self.print_dict(url_info)
        # str_base_url_response = self.getHttpContent(url=url_info['base_url'])
        # print "返回的目录内容？？：" + str_articlelist_response
        # self.article_num = self.get_article_num(str_base_url_res=str_base_url_res)
        # self.get_uid(str_base_url_response=str_base_url_response)



    def start(self):
        list_article_url = []
        for int_current_page in range(self.url_info['article_pages']):
            current_blog_page_url = "http://blog.sina.com.cn/s/articlelist_" + str(self.url_info['uid']) + "_0_" + str(int_current_page+1) + ".html"
            # print current_blog_page_url
            str_response = self.getHttpContent(url=current_blog_page_url)
            now_article_url = re.findall(r'blog.sina.com.cn/s/blog_(\w+)\.html', str_response)
            list_article_url = list_article_url + now_article_url
        for now_article_id in list_article_url:
            # print now_article
            article_url = "http://blog.sina.com.cn/s/blog_" + now_article_id + ".html"
            article_url_response = self.getHttpContent(url=article_url)


        return


    def get_blog_info(self, base_url=''):
        u"""
        获得文章的数量，首页就有
        :param base_url:
        :return:
        """
        # print "article_num"
        base_url_response = self.getHttpContent(url=base_url)
        match = re.search(r'(?<=<em class="count SG_txtb">\()(\d{1,})', base_url_response)

        if match:
            article_num = match.group(0)
            article_num = int(article_num)
        else:
            return 0     # 如果一篇博客都没有？？？TODO

        match = re.search(r'(?<=<title>).*?(?=</title>)', base_url_response)
        if match:
            blog_title = match.group(0)
        else:
            blog_title = str(self.url_info['uid']) + "的博客"
        return article_num, blog_title

    def get_article_info(self, article_url_response):
        u"""
        解析每篇文章，返回文章标题，内容，最后修改时间
        :param article_url_response:
        :return:
        """
        article_title = re.search(r'(?<=<title>).*?(?=</title>)', article_url_response).group(0)
        article_body = \
            article_url_response[article_url_response.find("<!-- 正文开始 -->")+len("<!-- 正文开始 -->"):article_url_response.find("<!-- 正文结束 -->")]
        post_time =

    def get_uid(self, base_url):
        """
        获得用户的uid
        :param base_url:
        :return:
        """
        str_base_url_response = self.getHttpContent(url=base_url)
        match = re.search(r'(?<=articlelist_)\d{1,}', str_base_url_response)
        if match:
            article_num = match.group(0)
            return int(article_num)
        else:
            return 0


    def print_url_info(self):
        """
        打印dict，工具函数
        :return:
        """
        self.print_dict(self.url_info)