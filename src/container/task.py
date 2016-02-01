# -*- coding: utf-8 -*-

from src.tools.type import Type
from src.container.initialbook import InitialBook


class Spider(object):
    def __init__(self):
        self.href_article_list = ''
        self.href_profile = ''
        self.href_index = ''
        return


class SingleTask(object):
    u"""
    任务信息以对象属性方式进行存储
    """
    def __init__(self):
        self.kind = ''
        self.spider = Spider()
        self.book = InitialBook()
        return


class TaskPackage(object):
    def __init__(self):
        self.work_list = {}
        self.book_list = {}
        return

    def add_task(self, single_task=SingleTask()):
        if single_task.kind not in self.work_list:
            self.work_list[single_task.kind] = []
        self.work_list[single_task.kind].append(single_task.spider.href_index)

        if single_task.kind not in self.book_list:
            print u"在add_task, single_task.kind是" + str(single_task.kind)
            self.book_list[single_task.kind] = []
        self.book_list[single_task.kind].append(single_task.book)
        return

    def get_task(self):
        if Type.SinaBlog in self.book_list:
            self.merge_article_book_list(Type.SinaBlog)
        return self

    def merge_article_book_list(self, book_type):
        book_list = self.book_list[Type.SinaBlog]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        book.author_id = book_list[0].author_id       # 这里的len(book_list)比1大怎么办?
        book.sql.info = 'select * from SinaBlog_Info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from SinaBlog_Article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def is_work_list_empty(self):
        for kind in Type.type_list:            # type_list现在只有一种, SinaBlog
            if self.work_list.get(kind):
                return False
        return True

    def is_book_list_empty(self):
        for kind in Type.type_list:
            if self.book_list.get(kind):
                return False
        return True

