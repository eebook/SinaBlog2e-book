# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    list2Html.py
# Description :    接收article_package，转换成适合的html
# Author      :    Frank
# Date        :    2014.06.04
# ######################################################


import re


class list2Html(object):
    def __init__(self, article_package, blog_title):
        """
        article_package:  [[article_title, article_body, post_time], [...]]
        """
        self.trans = Transfer(article_package, blog_title)
        return

    def get_result(self):
        return self.trans.get_result()

    def get_img_set(self):
        return


class Transfer(object):
    u"""
    转换类，提供将字典转换为Html的方法
    """
    def __init__(self, article_package, blog_title):
        """
        article_package:  [[article_title, article_body, post_time], [...]]
        :param article_package:
        :return:
        """
        self.package = article_package
        self.blog_title = blog_title
        self.img_set = set()
        self.html_list = []
        self.content_list = []      # [{'file_name':'...', 'file_content':'...'}]
        self.info_list = []         # [{'file_name':'...', 'file_content':'...'}]
        return

    def img_fix(self, article_content):
        """
        TODO
        :param article_content:
        :return:
        """
        return

    def get_image_name(self, img_href=''):
        """
        TODO
        :param img_href:
        :return:
        """

    def author_link(self, uid):
        """
        TODO
        :param uid:
        :return:
        """

    def get_image_set(self):
        return self.img_set

    def get_result(self):
        """
        先运行content_trans()和index_trans() TODO 产生content_list
        :return: content_list
        """
        self.content_trans()
        # self.
        return self.content_list

    def content_trans(self):
        """

        :return:
        """
        print "content_trans????"
        for now_article_num in range(len(self.package)):
            # print "what is now_article_num" + str(now_article_num)
            # print "package 中的" + str(self.package[now_article_num])
            article_title = str(self.package[now_article_num][0])
            article_body = self.clean_href(str(self.package[now_article_num][1]))
            article_body = self.clean_target(article_body)
            article_body = self.clean_color(article_body)
            # print "article_body???" + article_body
            post_time = str(self.package[now_article_num][2])

            # TODO 用HTML模板
            file_content = "<html>\n<head>\n<meta http-equiv=""Content-Type"" content=""text/html; charset=utf-8"" />\n<title>" + article_title + \
                "</title>\n<link href=""../article.css"" type=""text/css"" rel=""stylesheet"" />\n</head>\n<body>\n<h2>" + \
                article_title + "</h2>\n<p>By: <em>" + self.blog_title + \
                "</em> 原文发布于：<em>" + post_time + "</em></p>\n" + "<div class=""left-column""> </div>" + "<div class=""middle-column"">" + \
                article_body + "\n<p><a href=""index.html"">返回目录</a></p>\n</div>\n<div class=""right-column""> </div></body>\n</html>"
            buf = {'file_name': article_title, 'file_content': file_content}
            self.content_list.append(buf)

    def index_trans(self):
        """
        TODO  生成目录
        :return:
        """
        return

    def clean_href(self, str_content):
        return re.sub('href=".*?"', '', str_content)

    def clean_target(self, str_content):
        return re.sub('target=_blank', '', str_content)

    def clean_color(self, str_content):
        return re.sub('color=#0000ff', '', str_content)

