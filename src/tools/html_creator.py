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
            # if img[-1] == '/':
            #     print u"修改前,img为:" + str(img)
            #     img = img[:-1]
            #     print u"修改后,img为:" + str(img[:-1])
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
            new_image = new_image.replace('http://simg.sinajs.cn/blog7style/images/common/sg_trans.gif',\
                                          '../images/{}'.format(filename)) # 硬编码, 可以优化?写到fix_html函数中
            # new_image += '</img>'
            content = content.replace(img, '<div class="duokan-image-single">{}</div>'.format(new_image))

        return content

    @staticmethod
    def fix_image_src(href):
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
        return template.format(**author_info)

    def wrap_title_info(self, title_image='', title='', description='', **kwargs):
        title_info = {
            'title_image': title_image,    # TODO
            'title': title,
            'description': description,
        }
        return title_info

    def create_title_info(self, title_info):
        template = self.get_template('info', 'title')
        return template.format(**title_info)

    def create_answer(self, answer):
        result = {
            'author_info': self.create_author_info(answer),
            'comment': self.create_comment_info(answer),
            'content': answer['content']
        }
        template = self.get_template('question', 'answer')
        return template.format(**result)

    def create_article(self, article, prefix=''):
        article['edit_date'] = article['publish_date']
        article['description'] = ''
        article['agree'] = 'wu'
        # article['title_image'] = 'wu'
        result = {
            'answer': self.create_answer(article),
            'question': self.get_template('info', 'title').format(**article)
        }
        question = self.get_template('question', 'question').format(**result)
        result = {
            'body': question,
            'title': article['title'],
        }
        content = self.get_template('content', 'base').format(**result)
        page = Page()
        page.content = self.fix_image(content)
        page.filename = str(prefix) + '_' + str(article['article_id']) + '.xhtml'
        page.title = article['title']
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
        return content
