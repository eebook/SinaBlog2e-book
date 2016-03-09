# -*- coding: utf-8 -*-
import sqlite3


from src.tools.path import Path

from src.book import Book
from src.tools.config import Config
from src.tools.debug import Debug
from src.tools.db import DB
from src.read_list_parser import ReadListParser
from src.worker import worker_factory
from src.tools.type import Type


class SinaBlog(object):
    def __init__(self):
        u"""
        配置文件使用$符区隔，同一行内的配置文件归并至一本电子书内
        """
        Path.init_base_path()       # 设置路径
        Path.init_work_directory()  # 创建路径
        self.init_database()        # 初始化数据库
        Config._load()
        return

    @staticmethod
    def init_config():       # TODO 输出提示语之类的
        Config._save()
        return

    def start(self):
        u"""
        程序运行的主函数
        :return:
        """
        Debug.logger.debug(u"#Debug模式#: 不检查更新")
        self.init_config()
        Debug.logger.info(u"开始读取ReadList.txt的内容")
        with open('./ReadList.txt', 'r') as read_list:
            counter = 1
            for line in read_list:
                line = line.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')  # 移除空白字符
                self.create_book(line, counter)
                counter += 1
        return

    @staticmethod
    def create_book(command, counter):
        Path.reset_path()

        Debug.logger.info(u"开始制作第 {} 本电子书".format(counter))
        Debug.logger.info(u"对记录 {} 进行分析".format(command))

        task_package = ReadListParser.get_task(command)     # 分析命令

        if not task_package.is_work_list_empty():
            worker_factory(task_package.work_list)  # 执行抓取程序
            Debug.logger.info(u"网页信息抓取完毕")

        if not task_package.is_book_list_empty():
            Debug.logger.info(u"开始从数据库中生成电子书")
            Debug.logger.debug(u"task_package.book_list.sql.info:" + str((task_package.book_list[Type.SinaBlog][0]).sql.info))  #.sql.info))
            book = Book(task_package.book_list)
            book.create()
        return

    @staticmethod
    def init_database():
        if Path.is_file(Path.db_path):
            DB.set_conn(sqlite3.connect(Path.db_path))
        else:
            DB.set_conn(sqlite3.connect(Path.db_path))
            # 没有数据库, 新建一个出来
            with open(Path.sql_path) as sql_script:
                DB.cursor.executescript(sql_script.read())
            DB.commit()







