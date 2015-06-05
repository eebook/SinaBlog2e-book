# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    basic_tools.py   Done for now
# Description :    一些常用的工具函数
# Author      :    Frank
# Date        :    2014.06.05
# ######################################################

# 工具函数
import os
import shutil

def mkdir(path):
    try:
        os.mkdir(path)
    except OSError:
        print u'指定目录已存在'
    return

def chdir(path):
    try:
        os.chdir(path)
    except OSError:
        print u'指定目录不存在，自动创建之'
        mkdir(path)
        os.chdir(path)
    return

def rmdir(path):
    shutil.rmtree(path=path, ignore_errors=True)
    return