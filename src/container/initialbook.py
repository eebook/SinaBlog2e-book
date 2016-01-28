# -*- coding: utf-8 -*-

from src.container.image import ImageContainer
from src.tools.config import Config
from src.tools.db import DB
from src.tools.match import Match
from src.tools.type import Type
from src.tools.debug import Debug


class InitialBook(object):
    class Sql(object):
        def __init__(self):
            self.info = ''
            self.article = ''
            self.info_extra = ''
            self.article_extra = ''      # 用来扩展的????
            return

        def get_article_sql(self):
            return self.article_extra + Config.sql_extend_answer_filter

    class Epub(object):
        def __init__(self):
            Debug.logger.debug(u"这里是Epub(object)中的__init__")
            self.article_count = 0
            self.char_count = 0

            self.title = ''
            self.id = ''
            self.split_index = 0
            self.prefix = ''
            return

    def __init__(self):
        self.kind = 'lalalal'
        self.sql = InitialBook.Sql()
        self.epub = InitialBook.Epub()
        self.info = {}
        self.article_list = []
        self.page_list = []
        self.prefix = ''
        self.author_id = 0
        return

    def catch_data(self):
        u"""
        从数据库中获取数据
        :return:
        """
        self.catch_SinaBlog_info()      # 获取博客信息
        self.get_article_list()         # 获取文章所有信息
        # self.__sort()       TODO
        return self

    def catch_SinaBlog_info(self):
        info = {}
        if self.sql.info:
            if self.kind == Type.SinaBlog_Info:
                info = self.catch_article_book_info(self.sql.info)
            else:
                info = DB.cursor.execute(self.sql.info).fetchone()
                Debug.logger.debug(u"catch_info没有成功, info:" + str(info))
                info = DB.wrap(Type.info_table[self.kind], info)
                Debug.logger.debug(u"catch_info没有成功, info:" + str(info))
        self.set_info(info)

    def catch_article_book_info(self, sql):
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.SinaBlog_article, item) for item in info_list]
        info = {}
        print "info!!!!!:" + str(info)
        info['title'] = '_'.join([str(item['title']) for item in info_list])
        info['id'] = '_'.join([str(item['article_id']) for item in info_list])
        return info

    def set_info(self, info):
        self.info.update(info)
        if self.kind == Type.SinaBlog:              # 该博客所有的博文
            self.epub.title = u'新浪博客_{}({})'.format(info['name'], info['creator_id'])
            self.epub.id = info['creator_id']
            self.author_id = info['creator_id']     # TODO
        elif self.kind == Type.SinaBlog_article:    # 单篇博文 TODO
            self.epub.title = u'新浪博客博文集锦({})'.format(info['title'])
            self.epub.id = info['id']       # TODO

    def get_article_list(self):
        # if self.kind in Type.SinaBlog_article_type_list:
        article_list = self.__get_article_list()
        self.set_article_list(article_list)
        return

    def __get_article_list(self):
        def add_property(article):
            article['char_count'] = len(article['content'])
            article['update_date'] = article['publish_date']
            return article
        article_list = [DB.wrap(Type.SinaBlog_article, x) for x in DB.get_result_list(self.sql.get_article_sql())]
        article_list = [add_property(x) for x in article_list]
        return article_list

    def set_article_list(self, article_list):
        self.clear_property()
        for article in article_list:
            self.epub.char_count += article['char_count']
        self.epub.article_count = len(article_list)
        self.article_list = article_list
        return

    def clear_property(self):
        self.epub.article_count = 0
        self.epub.char_count = 0
        return


# class HtmlBookPackage(object):
#     def __init__(self):
#         self.book_list = []
#         self.image_list = []
#         self.image_container = ImageContainer()
#         return
#
#     def get_title(self):
#         title = ''.join([book.epub.title for book in self.book_list])
#         title = Match.fix_filename(title)    # 移除特殊字符
#         return title

