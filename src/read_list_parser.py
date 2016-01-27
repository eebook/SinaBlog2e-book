# -*- coding: utf-8 -*-

from src.tools.debug import Debug
from src.tools.type import Type
from src.tools.match import Match
from src.container.task import SingleTask, TaskPackage

class ReadListParser():
    u"""
    TODO
    """

    @staticmethod
    def get_task(command):
        u"""
        对外的接口, 用来分析指令,
        :param command:
        :return:
        """
        def remove_comment(command):
            u"""
            去掉#后面的注释
            :param command:
            :return:
            """
            return command.split('#')[0]

        def split_command(command):
            u"""
            # 一行是一本书, 每一行用$符号来区分章节
            :param command: 一行命令
            :return:
            """
            return command.split('$')

        command = remove_comment(command)
        command_list = split_command(command)
        Debug.logger.debug("command_list:" + str(command_list))

        return command_list

    @staticmethod
    def parse_command(raw_command=''):
        u"""

        :param raw_command:   网址原始链接, 如:http://blog.sina.com.cn/u/1287694611
        :return: task
        task格式
        *   kind
            *   字符串，见TypeClass.type_list
        *   spider
            *   href
                *   网址原始链接，例http://www.zhihu.com/question/33578941
                *   末尾没有『/』
        *   book
            *   kind
            *   info
            *   question
            *   answer
        """
        def detect(command):
            for command_type in Type.type_list:
                result = getattr(Match, command_type)(command)
                if result:
                    return command_type
            return 'unknown'

        def parse_SinaBlog(command):
            result = Match.SinaBlog(command)
            SinaBlog_people_id = result.group('SinaBlog_people_id')
            Debug.logger.debug(u"SinaBlog_people_id:" + str(SinaBlog_people_id))
            task = SingleTask()



