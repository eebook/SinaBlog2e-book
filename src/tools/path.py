# -*- coding: utf-8 -*-
import os
import shutil

# from src.tools.debug import Debug


class Path(object):
    u"""
    定义资源,生成的文件等的路径,以及关于路径操作的一些函数
    # """
    try:
        base_path = unicode(os.path.abspath('.').decode('gbk'))  # 初始地址,不含分隔符
    except:
        base_path = os.path.abspath('.')  # 对于Mac和Linux用户，使用gbk解码反而会造成崩溃，故添加一个try-except，以防万一

    config_path = base_path + u'/SinaBlog_config.json'
    db_path = base_path + u'/SinaBlog_db_002.sqlite'
    sql_path = base_path + u'/db/SinaBlog.sql'

    www_css = base_path + u'/www/css'
    www_image = base_path + u'/www/image'

    html_pool_path = base_path + u'/电子书临时资源库/网页池'
    image_pool_path = base_path + u'/电子书临时资源库/图片池'
    result_path = base_path + u'/生成的电子书/新浪博客'

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except OSError:
            pass
        return

    @staticmethod
    def chdir(path):
        u"""
        换路径,如果路径不存在就新建一个
        :param path:
        :return:
        """
        try:
            os.chdir(path)
        except OSError:
            Path.mkdir(path)
            os.chdir(path)
        return

    @staticmethod
    def reset_path():
        Path.chdir(Path.base_path)
        return

    @staticmethod
    def pwd():
        u"""
        输出绝对路径
        :return:
        """
        print os.path.realpath('.')

    @staticmethod
    def get_pwd():
        u"""
        :return: 绝对路径
        """
        try:
            path = unicode(os.path.abspath('.').decode('gbk'))  # 初始地址,不含分隔符
        except:
            path = os.path.abspath('.')  # 对于Mac和Linux用户，使用gbk解码反而会造成崩溃，故添加一个try-except，以防万一
        return path

    @staticmethod
    def rmdir(path):
        u"""
        删除整个目录,忽略错误
        :param path:
        :return:
        """
        shutil.rmtree(path, ignore_errors=True)

    @staticmethod
    def copy(src, dst):
        if not os.path.exists(src):
            # Debug.logger.info('{}不存在，自动跳过'.format(src))
            return
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src=src, dst=dst)
        return

    @staticmethod
    def get_filename(src):
        return os.path.basename(src)

    @staticmethod
    def init_base_path():
        u"""
        初始化路径,不需要实例化 Path 就能执行
        :return:
        """
        try:
            base_path = unicode(os.path.abspath('.').decode('gbk'))  # 初始地址,不含分隔符
        except:
            base_path = os.path.abspath('.')  # 对于Mac和Linux用户，使用gbk解码反而会造成崩溃，故添加一个try-except，以防万一

        Path.config_path = base_path + u'/SinaBlog_config.json'
        Path.db_path = base_path + u'/SinaBlog_db_001.db'
        Path.sql_path = base_path + u'/db/SinaBlog.sql'

        Path.www_css = base_path + u'/www/css'
        Path.www_image = base_path + u'/www/image'

        Path.html_pool_path = base_path + u'/电子书临时资源库/网页池'
        Path.image_pool_path = base_path + u'/电子书临时资源库/图片池'
        Path.result_path = base_path + u'/生成的电子书/新浪博客'
        return

    @staticmethod
    def init_work_directory():
        Path.reset_path()
        Path.mkdir(u'./电子书临时资源库')
        Path.mkdir(u'./生成的电子书')
        Path.chdir(u'./生成的电子书')
        Path.mkdir(u'./新浪博客')
        Path.chdir(u'../电子书临时资源库')
        Path.mkdir(u'./网页池')
        Path.mkdir(u'./图片池')
        Path.reset_path()
        return

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)



