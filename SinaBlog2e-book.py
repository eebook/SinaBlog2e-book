# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    SinaBlog2e-book.py
# Description :    程序的主入口。
# Author      :    Frank
# Date        :    2014.06.03
# ######################################################

import sys
reload(sys)
# 修改系统（终端输出）默认的编码，文件格式、处理格式
sys.setdefaultencoding('utf-8')

from codes.main import *

gameBegin = SinaBlog2ebook()
gameBegin.main_start()