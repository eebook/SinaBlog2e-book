# -*- coding: utf-8 -*-

import json  # 用于JsonWorker

from src.tools.controler import Control
from src.tools.db import DB
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match

from src.lib.SinaBlog_parser.SinaBlogparser import SinaBlogParser
from src.lib.SinaBlog_parser.tools.parser_tools import ParserTools
from bs4 import BeautifulSoup


class PageWorker(object):
    def __init__(self, task_list):
        self.task_set = set(task_list)
        self.task_complete_set = set()
        self.work_set = set()            # 待抓取网址池
        self.work_complete_set = set()   # 已完成网址池
        self.content_list = []           # 用于存放已抓取的内容

        self.answer_list = []
        self.question_list = []

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
        max_page = 1
        try:
            floor = content.index('">下一页</a></span>')
            floor = content.rfind('</a>', 0, floor)
            cell = content.rfind('>', 0, floor)
            max_page = int(content[cell + 1:floor])
            Debug.logger.info(u'答案列表共计{}页'.format(max_page))
        except:
            Debug.logger.info(u'答案列表共计1页')
        finally:
            return max_page

    def create_save_config(self):
        u"""
        key 即为表名
        :return:
        """
        config = {'Answer': self.answer_list, 'Question': self.question_list, }
        return config

    def clear_index(self):
        u"""
        用于在collection/topic中清除原有缓存
        """
        return

    def save(self):
        self.clear_index()
        save_config = self.create_save_config()
        for key in save_config:
            for item in save_config[key]:
                if item:
                    DB.save(item, key)
        DB.commit()
        return

    def start(self):
        self.start_catch_info()
        self.start_create_work_list()
        self.start_worker()
        # print "answer_list!!!!!!!:" + str(self.answer_list)
        self.save()
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
        # parser = QuestionParser(content)
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
    pass


class SinaBlogWorker(PageWorker):
    u"""
    Sina博客的worker
    """
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
        finally:
            return max_page

    def create_save_config(self):    # TODO
        config = {'SinaBlog_Article': self.answer_list, 'SinaBlog_Info': self.question_list, }
        return config

    def parse_content(self, content):
        parser = SinaBlogParser(content)
        self.answer_list += parser.get_answer_list()

    @staticmethod
    def parse_article_num(content):
        u"""

        :param target_url: 博客目录的content
        :return: 博文总数量
        """
        soup = BeautifulSoup(content, "lxml")
        article_num = soup.select('div.SG_connHead span em')
        article_num = article_num[0].get_text()
        article_num = article_num[1:-1]    # 去掉前后两个括号
        return article_num

    @staticmethod
    def parse_get_article_list(article_list_content):
        u"""
        获得每一篇博客的链接组成的列表
        :param article_list_content: 博文目录页面的内容
        :return:
        """
        soup = BeautifulSoup(article_list_content, "lxml")
        article_href_list = []

        article_list = soup.select('span.atc_title a')
        for item in range(len(article_list)):
            article_title = ParserTools.get_attr(article_list[item], 'href')
            article_href_list.append(article_title)

        return article_href_list

    def create_work_set(self, target_url):
        u"""
        根据博客首页的url, 首先通过re获得博客id, 然后根据博客"关于我"的页面的内容获得写入SinaBlog_Info
        的数据(这部分理应不在这个函数中, 可以改进), 最后通过博客目录页面的内容, 获得每篇博文的地址,
        放入work_set中

        :param target_url: 博客首页的url
        :return:
        """
        Debug.logger.debug(u"target_url是:" + str(target_url))
        if target_url in self.task_complete_set:
            return
        result = Match.SinaBlog(target_url)
        SinaBlog_author_id = int(result.group('SinaBlog_people_id'))

        href_article_list = 'http://blog.sina.com.cn/s/articlelist_{}_0_1.html'.format(SinaBlog_author_id)
        href_profile = 'http://blog.sina.com.cn/s/profile_{}.html'.format(SinaBlog_author_id)

        # ############下面这部分应该是SinaBlogAuthorWorker的内容, 写到SinaBlog_Info, 暂时写在这, 以后再优化
        content_profile = Http.get_content(href_profile)

        parser = SinaBlogParser(content_profile)
        self.question_list += parser.get_SinaBlog_info_list()
        # Debug.logger.debug(u"create_work_set中的question_list是什么??" + str(self.question_list))
        # #############上面这部分应该是SinaBlogAuthorWorker的内容, 写到SinaBlog_Info, 暂时写在这, 以后再优化

        # content_index = Http.get_content(href_index)
        content_article_list = Http.get_content(href_article_list)

        article_num = int(self.parse_article_num(content_article_list))
        Debug.logger.debug(u"article_num:" + str(article_num))
        if article_num % 50 != 0:
            page_num = article_num/50 + 1      # 博客目录页面, 1页放50个博客链接
        else:
            page_num = article_num / 50

        self.question_list[0]['article_num'] = article_num  # 这样的话, 每行只能放一个新浪博客地址!!!
        # 上面这行, 暂时只能这样写, 因为"关于我"的页面, 没有文章的数量

        self.task_complete_set.add(target_url)

        for page in range(page_num):
            url = 'http://blog.sina.com.cn/s/articlelist_{}_0_{}.html'.format(SinaBlog_author_id, page+1)
            content_article_list = Http.get_content(url)
            article_list = self.parse_get_article_list(content_article_list)
            for item in article_list:
                self.work_set.add(item)
            # self.work_set.add(article_list[0])
        return


def worker_factory(task):
    type_list = {'SinaBlog': SinaBlogWorker, 'SinaBlogAuthor': SinaBlogAuthorWorker}
    for key in task:
        Debug.logger.debug(u"在worker_factory中, key:" + str(key))
        Debug.logger.debug(u"在worker_factory中, task[key]:" + str(task[key]))
        worker = type_list[key](task[key])
        worker.start()
    return
