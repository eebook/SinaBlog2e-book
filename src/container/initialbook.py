# -*- coding: utf-8 -*-

from src.container.image import ImageContainer
from src.tools.config import Config
from src.tools.db import DB
from src.tools.match import Match
from src.tools.type import Type
from src.tools.debug import Debug


class InitialBook(object):
    u"""
        ->kind
        ->author_id
        ->sql ->class sql
                ->info
                ->article
                ->info_extra
                ->article_extra             
        ->epub ->class Epub
                    ->article_count
                    ->char_count
                    ->title
                    ->id
                    ->split_index
                    ->prefix
        ->info
        ->article_list
        ->page_list
        ->prefix
    """
    class Sql(object):
        def __init__(self):

            self.answer = ''
            self.info = ''
            self.article = ''
            self.info_extra = ''
            self.article_extra = ''      # 用来扩展的????
            return

        def get_answer_sql(self):
            return self.answer + Config.sql_extend_answer_filter

    class Epub(object):
        def __init__(self):
            self.article_count = 0
            self.answer_count = 0
            self.char_count = 0

            self.title = ''
            self.id = ''
            self.split_index = 0
            self.prefix = ''
            return

    def __init__(self):
        self.kind = ''
        self.author_id = 0                 
        self.sql = InitialBook.Sql()
        self.epub = InitialBook.Epub()
        self.info = {}
        self.article_list = []
        self.page_list = []
        self.prefix = ''
        return

    def catch_data(self):
        u"""
        从数据库中获取数据
        :return:
        """
        self.catch_info()
        self.get_article_list()         # 获取文章所有信息
        # self.__sort()       TODO
        return self

    def catch_info(self):
        u"""
        获得博客的信息, 将info作为参数传给set_info
        :return:
        """
        info = {}
        if self.sql.info:
            if self.kind == Type.SinaBlog:
                info = self.catch_SinaBlog_book_info()
        self.set_info(info)
        return

    def catch_SinaBlog_book_info(self):
        u"""

        :param
        :return: info
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.SinaBlog_Info, item) for item in info_list]
        info = {}
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])  # 可以是多个博客组合在一起
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        return info

    def set_info(self, info):
        self.info.update(info)
        if self.kind == Type.SinaBlog:              # 该博客所有的博文
            self.epub.title = u'新浪博客_{}({})'.format(info['creator_name'], info['creator_id'])
            self.epub.id = info['creator_id']
        elif self.kind == Type.SinaBlog_Article:    # 单篇博文 TODO
            self.epub.title = u'新浪博客博文集锦({})'.format(info['title'])
            self.epub.id = info['id']       # TODO

    def get_article_list(self):
        if self.kind in Type.SinaBlog:
            article_list = self.__get_article_list()
        self.set_article_list(article_list)
        return

    def __get_article_list(self):
        def add_property(article):
            article['char_count'] = len(article['content'])
            article['answer_count'] = 1
            if self.kind == Type.SinaBlog:
                article['agree_count'] = "没有赞同数" #article['agree']
                article['update_date'] = article['publish_date']
            return article
        if self.kind == Type.SinaBlog:
            article_list = [DB.wrap(Type.SinaBlog_Article, x) for x in DB.get_result_list(self.sql.get_answer_sql())]

        article_list = [add_property(x) for x in article_list]
        return article_list

    def set_article_list(self, article_list):
        self.clear_property()
        if self.kind == Type.SinaBlog:      # SinaBlog类型
            for article in article_list:
                self.epub.answer_count += article['answer_count']
                self.epub.char_count += article['char_count']
        self.article_list = article_list
        return

    def clear_property(self):
        self.epub.answer_count = 0
        # self.epub.title = ''
        # self.epub.prefix = ''
        self.epub.char_count = 0
        self.epub.article_count = 0
        return


class HtmlBookPackage(object):
    def __init__(self):
        self.book_list = []
        self.image_list = []
        self.image_container = ImageContainer()
        return

    def get_title(self):
        title = '_'.join([book.epub.title for book in self.book_list])
        title = Match.fix_filename(title)  # 移除特殊字符
        return title
