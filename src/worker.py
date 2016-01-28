# -*- coding: utf-8 -*-
import json

from src.tools.controler import Control
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.db import DB

from src.lib.SinaBlog_parser.author import AuthorParser
from src.lib.SinaBlog_parser.SinaBlogparser import SinaBlogParser

# # -*- coding: utf-8 -*-
#
# import threading
# import re
#
# from codes.baseclass import *
#
#
# class PageWoker(BaseClass, HttpBaseClass):
#     def __init__(self, url_info={}):
#         self.url_info = url_info
#         # self.print_dict(url_info)
#         # str_base_url_response = self.getHttpContent(url=url_info['base_url'])
#         # print "返回的目录内容？？：" + str_articlelist_response
#         # self.article_num = self.get_article_num(str_base_url_res=str_base_url_res)
#         # self.get_uid(str_base_url_response=str_base_url_response)
#
#     def get_article_package(self):
#         """
#         article_package:  [[article_title, article_body, post_time], [...]]
#         :return:
#         """
#         list_article_url = []
#         for int_current_page in range(self.url_info['article_pages']):
#             current_blog_page_url = "http://blog.sina.com.cn/s/articlelist_" + str(self.url_info['uid']) + "_0_" + str(int_current_page+1) + ".html"
#             # print current_blog_page_url
#             str_response = self.getHttpContent(url=current_blog_page_url)
#             now_article_url = re.findall(r'blog.sina.com.cn/s/blog_(\w+)\.html', str_response)
#             list_article_url = list_article_url + now_article_url
#
#         list_article_url.remove('4cf7b4ec0100eudp')     # 移除意见反馈留言板的ID（博文的形式）
#         # print "list_article_url" + str(list_article_url)
#         article_package = []       # 用来将所有的文章打包
#         for now_article_id in list_article_url:
#             # print now_article
#             article_url = "http://blog.sina.com.cn/s/blog_" + now_article_id + ".html"
#             article_url_response = self.getHttpContent(url=article_url)
#             now_article_title, now_article_body, now_post_time =\
#                 self.get_article_info(article_url_response=article_url_response, blog_title=self.url_info['blog_title'])
#             # TODO 没用title是因为制作电子书不能有中文
#             article_package.append([now_article_id, now_article_body, now_post_time])
#         # print "article_package！！！！" + str(article_package[0][0])
#         return article_package
#
#     def get_blog_info(self, base_url=''):
#         u"""
#         获得文章的数量，首页就有
#         :param base_url:
#         :return:
#         """
#         # print "article_num"
#         base_url_response = self.getHttpContent(url=base_url)
#         match = re.search(r'(?<=<em class="count SG_txtb">\()(\d{1,})', base_url_response)
#
#         if match:
#             article_num = match.group(0)
#             article_num = int(article_num)
#         else:
#             return 0     # 如果一篇博客都没有？？？TODO
#
#         match = re.search(r'(?<=<title>).*?(?=</title>)', base_url_response)
#         if match:
#             blog_title = match.group(0)
#         else:
#             blog_title = str(self.url_info['uid']) + "的博客"
#         return article_num, blog_title
#
#     def get_article_info(self, article_url_response, blog_title):
#         u"""
#         解析每篇文章，返回文章标题，内容，最后修改时间
#         :param article_url_response:
#         :return: article_title, article_body, post_time
#         """
#         match = re.search(r'(?<=<title>).*?(?=</title>)', article_url_response)
#         if match:
#             article_title = match.group(0).replace("_" + blog_title, "").replace("_新浪博客", "")
#         else:
#             article_title = "未匹配的文章标题"
#         # print "article title??:" + article_title
#         article_body = \
#             article_url_response[article_url_response.find("<!-- 正文开始 -->")+len("<!-- 正文开始 -->"):article_url_response.find("<!-- 正文结束 -->")]
#         # print "article_body:" + article_body
#         match = re.search(r'(?<=<span class="time SG_txtc">\().*?(?=\)</span>)', article_url_response)     # 最后更新时间
#         if match:
#             post_time = match.group(0)
#         else:
#             post_time = "未知时间"
#         # print "post_time:" + post_time
#
#         return article_title, article_body, post_time
#
#     def get_uid(self, base_url):
#         """
#         获得用户的uid
#         :param base_url:
#         :return:
#         """
#         str_base_url_response = self.getHttpContent(url=base_url)
#         match = re.search(r'(?<=articlelist_)\d{1,}', str_base_url_response)
#         if match:
#             article_num = match.group(0)
#             return int(article_num)
#         else:
#             return 0




class PageWorker(object):
    def __init__(self, task_list):
        self.task_set = set(task_list)
        self.task_complete_set = set()
        self.work_set = set()  # 待抓取网址池
        self.work_complete_set = set()  # 已完成网址池
        self.content_list = []  # 用于存放已抓取的内容

        self.info_list = []
        self.extra_index_list = []
        self.info_url_set = self.task_set.copy()
        self.info_url_complete_set = set()

        self.add_property()  # 添加扩展属性
        # Http.set_cookie()

    def add_property(self):

        return

    @staticmethod
    def parse_max_page(content):
        u"""
        :param content: 博客目录的页面内容
        :return:
        """
        max_page = 1
        try:
            floor = content.index('">下一页</a>')
            floor = content.rfind('</a>', 0, floor)
            cell = content.rfind('>', 0, floor)
            max_page = int(content[cell + 1:floor])
            Debug.logger.info(u'答案列表共计{}页'.format(max_page))
        except:
            Debug.logger.info(u'答案列表共计1页')
        finally:
            return max_page

    @staticmethod
    def parse_blog_link_from_article_list(content):
        u"""
        :param content: 某一页博客目录的内容
        :return:
        """

    def create_save_config(self):    # TODO
        # config = {'Answer': self.answer_list, 'Question': self.question_list, }
        # return config
        return

    def clear_index(self):
        u"""
        用于在collection/topic中清除原有缓存
        """
        return

    def save(self):         # TODO
        self.clear_index()
        save_config = self.create_save_config()
        # for key in save_config:
        #     for item in save_config[key]:
        #         if item:
        #             DB.save(item, key)
        # DB.commit()
        return

    def start(self):
        self.start_catch_info()
        self.start_create_work_list()
        self.start_worker()
        # self.save()  TODO
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url + '?nr=1&sort=created')
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}?nr=1&sort=created&page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def clear_work_set(self):
        self.work_set = set()
        return

    def start_create_work_list(self):
        self.clear_work_set()
        argv = {'func': self.create_work_set, 'iterable': self.task_set, }
        Control.control_center(argv, self.task_set)
        return

    def worker(self, target_url):
        if target_url in self.work_complete_set:
            # 自动跳过已抓取成功的网址
            return

        Debug.logger.info(u'开始抓取{}的内容'.format(target_url))
        content = Http.get_content(target_url)
        if not content:
            return
        content = Match.fix_html(content)  # 需要修正其中的<br>标签，避免爆栈
        self.content_list.append(content)
        Debug.logger.debug(u'{}的内容抓取完成'.format(target_url))
        self.work_complete_set.add(target_url)
        return

    def parse_content(self, content):
        # parser = QuestionParser(content)  TODO
        # self.question_list += parser.get_question_info_list()
        # self.answer_list += parser.get_answer_list()
        return

    def start_worker(self):
        u"""
        work_set是所有的需要抓取的页面
        :return:
        """
        a = list(self.work_set)
        a.sort()
        argv = {'func': self.worker,  # 所有待存入数据库中的数据都应当是list
                'iterable': a, }
        Control.control_center(argv, self.work_set)
        Debug.logger.info(u"所有内容抓取完毕，开始对页面进行解析")
        i = 0
        for content in self.content_list:
            i += 1
            Debug.print_in_single_line(u"正在解析第{}/{}张页面".format(i, self.content_list.__len__()))
            self.parse_content(content)
        Debug.logger.info(u"网页内容解析完毕")
        return

    def catch_info(self, target_url):
        return

    def start_catch_info(self):
        argv = {'func': self.catch_info, 'iterable': self.info_url_set, }
        Control.control_center(argv, self.info_url_set)
        return


class SinaBlogAuthorWorker(PageWorker):
    def parse_content(self, content):
        parser = AuthorParser(content)    # TODO TODO

    def catch_info(self, target_url):
        u"""
        将info的信息放入info_list中
        :param target_url: 新浪博客首页地址,
        :return:
        """
        if target_url in self.info_url_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.info_url_complete_set.add(target_url)
        parser = AuthorParser(content)
        self.info_list.append(parser.get_extra_info())
        return

class SinaBlogWorker(PageWorker):
    u"""
    Sina博客的worker
    """
    def parse_article_num_page_num(self, target_url):
        u"""

        :param target_url: 博客首页的url
        :return:
        """
        # result = Match.SinaBlog(target_url)
        # SinaBlog_author_id = result.group('SinaBlog_people_id')
        # articlelist_url = 'http://blog.sina.com.cn/s/articlelist_{}_0_1.html'.format(SinaBlog_author_id)
        content = Http.get_content(target_url)
        Debug.logger.info("target_url是????:" + target_url)
        if not content:
            return
        parser = SinaBlogParser(content)
        print u"parser.get_SinaBlog_info_list:!!!!!!" + str(parser.get_SinaBlog_info_list())

    def create_work_set(self, target_url):
        print u"target_url是:" + str(target_url)
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url)
        if not content:
            return
        self.task_complete_set.add(target_url)
        self.parse_article_num_page_num(target_url)    # TODO
        max_page = 2
        for page in range(max_page):
            url = 'http://blog.sina.com.cn/s/articlelist_{}_0_{}.html'.format(1287694611, page+1)   # TODO
            # self.work_set.add(url)
        return



def worker_factory(task):
    type_list = {'SinaBlog': SinaBlogWorker, 'SinaBlogAuthor': SinaBlogAuthorWorker}
    for key in task:
        Debug.logger.debug(u"key:" + str(key))
        worker = type_list[key](task[key])
        worker.start()
    return
