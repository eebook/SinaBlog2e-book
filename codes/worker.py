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

    def get_article_package(self):
        """
        article_package:  [[article_title, article_body, post_time], [...]]
        :return:
        """
        list_article_url = []
        for int_current_page in range(self.url_info['article_pages']):
            current_blog_page_url = "http://blog.sina.com.cn/s/articlelist_" + str(self.url_info['uid']) + "_0_" + str(int_current_page+1) + ".html"
            # print current_blog_page_url
            str_response = self.getHttpContent(url=current_blog_page_url)
            now_article_url = re.findall(r'blog.sina.com.cn/s/blog_(\w+)\.html', str_response)
            list_article_url = list_article_url + now_article_url

        list_article_url.remove('4cf7b4ec0100eudp')     # 移除意见反馈留言板的ID（博文的形式）
        # print "list_article_url" + str(list_article_url)
        article_package = []       # 用来将所有的文章打包
        for now_article_id in list_article_url:
            # print now_article
            article_url = "http://blog.sina.com.cn/s/blog_" + now_article_id + ".html"
            article_url_response = self.getHttpContent(url=article_url)
            now_article_title, now_article_body, now_post_time =\
                self.get_article_info(article_url_response=article_url_response, blog_title=self.url_info['blog_title'])
            # TODO 没用title是因为制作电子书不能有中文
            article_package.append([now_article_id, now_article_body, now_post_time])
        # print "article_package！！！！" + str(article_package[0][0])
        return article_package

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

    def get_article_info(self, article_url_response, blog_title):
        u"""
        解析每篇文章，返回文章标题，内容，最后修改时间
        :param article_url_response:
        :return: article_title, article_body, post_time
        """
        match = re.search(r'(?<=<title>).*?(?=</title>)', article_url_response)
        if match:
            article_title = match.group(0).replace("_" + blog_title, "").replace("_新浪博客", "")
        else:
            article_title = "未匹配的文章标题"
        # print "article title??:" + article_title
        article_body = \
            article_url_response[article_url_response.find("<!-- 正文开始 -->")+len("<!-- 正文开始 -->"):article_url_response.find("<!-- 正文结束 -->")]
        # print "article_body:" + article_body
        match = re.search(r'(?<=<span class="time SG_txtc">\().*?(?=\)</span>)', article_url_response)     # 最后更新时间
        if match:
            post_time = match.group(0)
        else:
            post_time = "未知时间"
        # print "post_time:" + post_time

        return article_title, article_body, post_time

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