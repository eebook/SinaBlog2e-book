# -*- coding: utf-8 -*-

class Type(object):
    SinaBlog_article = 'SinaBlog_article'       # 类型是单篇的文章
    SinaBlog = 'SinaBlog'                       # 类型是文章的集锦

    SinaBlog_Info = 'SinaBlog_Info'             # 新浪博客的一些基本信息,如作者id

    SinaBlog_article_type_list = ['SinaBlog']

    info_table = {
        SinaBlog_Info: SinaBlog_Info
    }

    type_list = ['SinaBlog', 'SinaBlogAuthor']
