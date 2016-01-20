# -*- coding: utf-8 -*-

from debug import Debug


class DB(object):
    u"""
    存放常用的 SQL 代码
    """
    cursor = None
    conn = None

    @staticmethod
    def