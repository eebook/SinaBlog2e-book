# -*- coding:utf-8 -*-
# ######################################################
# File Name   :    parser.py
# Description :    解析HTML格式的字符串
# Author      :    Frank
# Date        :    2014.06.03
# ######################################################

class Parse(object):
    u"""
    基类，解析HTML字符串
    """
    def __init__(self, content):
        self.content = content
        # self.content = con    tent.replace('\r', '').replace('\n', '')
        self.reg_dict = {}   # 这两行不应该放在init_regex函数中
        self.reg_tip_dict = {}
        self.init_regex()

    def init_regex(self):
        self.reg_dict['']