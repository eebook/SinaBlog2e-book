# -*- coding: utf-8 -*-

from src.tools.type import Type
from src.container.initialbook import InitialBook


class Spider(object):
    def __init__(self):
        self.href = ''
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