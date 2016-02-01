# -*- coding: utf-8 -*-
import re

from src.container.page import Page
from src.tools.config import Config
from src.tools.match import Match
from src.tools.template_config import TemplateConfig
from src.tools.type import Type


class HtmlCreator(object):
    u"""
    工具类，用于生成html页面
    """

    def __init__(self, image_container):
        self.image_container = image_container
        return

    def fix_image(self, content):
        content = Match.fix_html(content)
        for img in re.findall(r'<img[^>]*', content):
            # fix img
            if img[-1] == '/':
                img = img[:-1]
            img += '>'

            src = re.search(r'(?<=src=").*?(?=")', img)
            if not src:
                new_image = img + '</img>'
                content = content.replace(img, new_image)
                continue
            else:
                src = src.group(0)
                if src.replace(' ', '') == '':
                    new_image = img + '</img>'
                    content = content.replace(img, new_image)
                    continue
            src_download = HtmlCreator.fix_image_src(src)
            if src_download:
                filename = self.image_container.add(src_download)
            else:
                filename = ''
            new_image = img.replace('"{}"'.format(src), '"../images/{}"'.format(filename))
            new_image += '</img>'
            content = content.replace(img, '<div class="duokan-image-single">{}</div>'.format(new_image))

        return content

    @staticmethod
    def fix_image_src(href):          # TODO 这部分是针对知乎的
        if Config.picture_quality == 0:
            return ''
        if 'equation?tex=' in href:  # tex图片需要额外加上http协议头
            if not 'http:' in href:
                href = 'http:' + href
            return href
        if Config.picture_quality == 1:
            return href
        if Config.picture_quality == 2:
            if not ('_' in href):
                return href
            pos = href.rfind('_')
            return href[:pos] + href[pos + 2:]  # 删除'_m'等图片质量控制符，获取原图
        return href

    def create_comment_info(self, comment_info):
        template = self.get_template('info', 'comment')
        return template.format(**comment_info)

    def create_author_info(self, author_info):
        template = self.get_template('info', 'author')
        # print u"author_info是" + str(author_info)       # TODO 这里不应该是info????
        return template.format(**author_info)

    def wrap_title_info(self, title_image='', title='', description='', **kwargs):
        title_info = {
            'title_image': title_image,
            'title': title,
            'description': description,
        }
        return title_info

    def create_title_info(self, title_info):
        template = self.get_template('info', 'title')
        return template.format(**title_info)

    def create_article(self, article):
        result = {
            'article_info': self.create_author_info(article),
            'comment': self.create_comment_info(article),      # TODO 这里指的是数量????
            'content': article['content']
        }
        template = self.get_template('question', 'answer')      # 暂时先用这个名字
        return template.format(**result)

    def create_SinaBlog(self, package, prefix=''):
        SinaBlog = package['SinaBlog']        # TODO SinaBlog_Info表中的article_num需要写入的
        # Debug:
        article_list = package['SinaBlog_article_list']
        # print u"在create_question中, article是什么???" + str(article_list)
        print (u"在create_question中, question是什么???" + str(SinaBlog))
        article_content = ''.join([self.create_article(article) for article in package['SinaBlog_article_list']])
        title_info = self.wrap_title_info(**SinaBlog)
        SinaBlog['SinaBlog_article_list'] = article_content
        SinaBlog['SinaBlog'] = self.get_template('info', 'title').format(**title_info)
        result = {
            'body': self.get_template('question', 'question').format(**SinaBlog),
            'title': SinaBlog['creator_name']
        }

        content = self.get_template('content', 'base').format(**result)
        page = Page()
        page.content = self.fix_image(content)
        page.filename = str(prefix) + '_' + str(SinaBlog['creator_id']) + '.xhtml'
        page.title = SinaBlog['creator_name']
        return page


    def wrap_front_page_info(self, kind, info):
        result = {}
        if kind == Type.SinaBlog:
            result['title'] = u'新浪博客集锦'
            result['description'] = u'TODO'
        return result

    def create_info_page(self, book):
        kind = book.kind
        info = book.info
        extend = self.wrap_front_page_info(kind, info)
        info.update(extend)
        result = {
            'detail_info': self.get_template('front_page', kind).format(**info),
            'title': info['title'],
            'description': info['description'],
        }
        result = {
            'title': info['title'],
            'body': self.get_template('front_page', 'base').format(**result),
        }
        content = self.get_template('content', 'base').format(**result)
        page = Page()
        page.content = self.fix_image(content)
        page.filename = str(book.epub.prefix) + '_' + 'info.xhtml'
        page.title = book.epub.title
        if book.epub.split_index:
            page.title += "_({})".format(book.epub.split_index)
        return page

    def get_template(self, kind, name):
        file_path = getattr(TemplateConfig, "{}_{}_uri".format(kind, name))
        with open(file_path) as template:
            content = template.read()
        # print u"content的内容是??" + str(content)
        return content
