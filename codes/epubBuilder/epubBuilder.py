# -*- coding: utf-8 -*-

# ######################################################
# File Name   :    epubBuilder
# Description :    接收article_package，输出电子书
# Author      :    Frank
# Date        :    2014.06.04
# ######################################################


class SinaBlog2ebook():
    """
    将article_package的内容转换成电子书
    """
    def __init__(self, article_package):
        self.package = article_package
        self.img_set = set()            # TODO：把文章中的图片下到本地

        self.base_path = './temp_source_repository/'