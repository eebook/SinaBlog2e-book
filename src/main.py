# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    main.py
# Description :    程序的主要内容就在该类中的main方法
# Author      :    Frank
# Date        :    2014.06.03
# ######################################################

import urllib
import time
import re

from codes.worker import *
from codes.epubBuilder.epubBuilder import *
from codes.baseclass import *

from src.tools.path import Path
from src.tools.config import Config
from src.tools.debug import Debug
from src.read_list_parser import ReadListParser


class SinaBlog(object):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        Path.init_base_path()       # 设置路径
        Path.init_work_directory()  # 创建路径
        # self.init_database()      # TODO init_database()
        Config._load()
        return

    @staticmethod
    def init_config():       # TODO
        Config._save()
        return

    def start(self):
        u"""
        程序运行的主函数
        :return:
        """
        if Config.debug is True:
            Debug.logger.info(u"#Debug:# 现在是 Debug 模式")
        self.init_config()


        with open('./ReadList.txt', 'r') as read_list:
            counter = 1
            for line in read_list:
                line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')  # 移除空白字符
                self.create_book(line, counter)
                counter += 1
        return

    @staticmethod
    def create_book(command, counter):
        Path.reset_path()

        Debug.logger.info(u"开始制作第 {} 本电子书".format(counter))
        Debug.logger.info(u"对记录 {} 进行分析".format(command))

        task_package = ReadListParser.get_task(command)     # 分析命令
        worker_factory(task_package)
        Debug.logger.info(u"网页信息抓取完毕")

        # read_list = open('./ReadList.txt', 'r')   # 该文件中存放要爬取的博客首页
        # book_count = 1               # 生成的书的数量
        # for line in read_list:       # 一行表示一本电子书
        #     chapter = 1              # 可以把多个博客放在一本书中，用$符号分隔链接即可 TODO
        #     article_package = []
        #     raw_url = line
        #     # for raw_url in line.split('$'):
        #     # print "debug:rawUrl" + raw_url
        #     print u'正在制作第{}本电子书的第{}节'.format(book_count, chapter)
        #     self.url_info = self.get_url_info(raw_url)
        #     # self.url_info['worker'].start()
        #     chapter += 1
        #     # print "now_article_package" + str(self.url_info['worker'].get_article_package)
        #     article_package = self.url_info['worker'].get_article_package()
        #     self.url_info['worker'].print_url_info()        # 输出url_info的内容
        #     # print "article_package是什么" + str(article_package)
        #     SinaBlog2Epub(article_package=article_package, blog_title=self.url_info['blog_title'], uid=self.url_info['uid'])
        #     self.url_info.clear()    # 这行不需要吧？
        #     del article_package
        #     book_count += 1
        #
        # print "main_start done!"

        return

    def get_url_info(self, raw_url):
        u"""
        返回标准格式的网址查询所需要的内容
        urlInfo 结构
        *   kind
        *   guide
            *   用于输出引导语，告知用户当前工作的状态
        *   worker
            *   用于生成抓取对象，负责抓取网页内容
        *   filter
            *   用于生成过滤器，提取答案，并将答案组织成便于生成电子书的结构
        *   urlInfo
            *   用于为Author获取信息
        *   baseSetting       TODO
            *   基础的设置信息，比如图片质量，过滤标准
            *   picQuality
                *   图片质量
            *   maxThread
                *   最大线程数
        """

        def detect_url(url):
            url_kind = 'homepage'
            self.url_info['base_url'] = url
            return url_kind

        kind = detect_url(raw_url)
        # print "kind??" + kind
        if kind == 'homepage':

            # 一般来说UID有两种方式
            matchs1 = re.search(r'(?<=blog\.sina\.com\.cn/u/)(\d+)', self.url_info['base_url'])
            matchs2 = re.search(r'(?<=blog\.sina\.com\.cn/)(\w+)', self.url_info['base_url'])
            if matchs1 or matchs2:
                self.url_info['worker'] = PageWoker(url_info=self.url_info)
                self.url_info['uid'] = self.url_info['worker'].get_uid(base_url=self.url_info['base_url'])
            else:
                print "ReadList.txt中给出的链接错误，程序终止"
                exit(0)
            self.url_info['guide'] = u'成功匹配到博客地址{}，开始执行抓取任务'.format(self.url_info['base_url'])
            self.url_info['article_list_url'] = \
                "http://blog.sina.com.cn/s/articlelist_" + str(self.url_info['uid']) + "_0_1.html"

        else:
            print "【debug】get_url_info, kind, Wrong!!!"
            print "ReadList.txt中给出的链接错误，程序终止"

        self.url_info['article_num'], self.url_info['blog_title'] = \
            self.url_info['worker'].get_blog_info(self.url_info['base_url'])

        self.url_info['article_pages'] = int(self.url_info['article_num']/50) + 1
        return self.url_info





