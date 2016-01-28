# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup

SinaBlog_author_id = 1287694611
href_article_list = 'http://blog.sina.com.cn/s/articlelist_{}_0_1.html'.format(SinaBlog_author_id)
href_index = 'http://blog.sina.com.cn/u/{}'.format(SinaBlog_author_id)
href_profile = 'http://blog.sina.com.cn/s/profile_{}.html'.format(SinaBlog_author_id)


html = urllib2.urlopen(href_index)
content = html.read()

# print "content内容:" + content

soup = BeautifulSoup(content, "lxml")


# print soup.prettify()
print soup.find_all("div", "info_txt")
# print soup.