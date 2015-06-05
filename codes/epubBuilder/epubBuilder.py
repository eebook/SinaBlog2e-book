# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    epubBuilder
# Description :    接收article_package，输出电子书
# Author      :    Frank
# Date        :    2014.06.04
# ######################################################

from codes.basic_tools import *
from codes.epubBuilder.list2Html import *
from codes.epubBuilder.epub import *


class SinaBlog2Epub(object):
    u"""
    将article_package的内容转换成电子书
    article_package:  [[article_title, article_body, post_time], [...]]
    """
    def __init__(self, article_package, blog_title, uid):
        self.package = article_package  # article_package:  [[article_title, article_body, post_time], [...]]
        self.blog_title = blog_title    # 博客名
        self.uid = uid                  # uid
        self.img_set = set()            # TODO：把文章中的图片下到本地
        self.content_list = []
        self.trans = list2Html(article_package, blog_title)  # list2Html用来转换html的内容

        # 下面定义一些路径
        self.base_path = './temp_source_repository/'        # 存放制作epub文件的所有内容
        self.target_path = './BOOKS/'                       # 存放输出的电子书
        self.base_img_path = './img_pool/'                  # 存放下载的图片 TODO
        self.base_content_path = './cache_repository/'      # 缓存html的内容

        self.file_title = ""        # 文件夹名称，一本书一个文件夹
        # print self.package
        print "blog_title" + blog_title
        self.init_base_path()       # 建立若干文件夹
        self.info2title()           # 确定书对应的文件夹名，即self.file_title
        self.trans2tree()           # 将电子书内容转换为一系列文件夹+html网页，放在base_content_path中
        self.epub_creator()
        return

    def init_base_path(self):
        mkdir(self.base_path)
        mkdir(self.target_path)
        chdir(self.base_path)
        mkdir(self.base_img_path)
        rmdir(self.base_content_path)
        mkdir(self.base_content_path)
        return

    def info2title(self):
        """
        一本书一个文件夹，该函数确定文件夹的名称
        :return:
        """
        self.file_title = u'{title}_博文集锦({uid})'.format(title=self.blog_title, uid=self.uid)
        illegal_char_list = ['\\', '/', ':', '*', '?', '<', '>', '|', '"']
        for illegal_char in illegal_char_list:
            self.file_title = self.file_title.replace(illegal_char, '')
        return

    def trans2tree(self):
        u"""
        将电子书内容转换为一系列文件夹+html网页
        :return:
        """
        self.content_list = self.trans.get_result()
        # self.img_set = self.trans.get_img_set()    # TODO
        i = 1
        for content in self.content_list:
            file_index = str(self.base_content_path + content['file_name'] + '.html').decode('utf-8')
            html_file = open(file_index, 'wb')
            html_file.write(content['file_content'])
            html_file.close()
        return

    def epub_creator(self):
        book = Book(self.blog_title, '12345678')
        for content in self.content_list:
            htmlSrc = '../../' + str(self.base_content_path + content['file_name'] + '.html').decode('utf-8')
            title = content['file_name']
            book.addHtml(src=htmlSrc, title=title)
            # 增加一些属性
        book.addLanguage('zh-cn')
        book.addCreator('Sina2ebook')
        book.addDesc(u'该电子书由Sina2ebook生成，只是为了学习和练习XD')
        book.addRight('CC')
        book.addPublisher('Sina2ebook')
        book.addCss(u'../../../epubResource/article.css')

        print u"开始制作电子书"
        book.buildingEpub()
        return