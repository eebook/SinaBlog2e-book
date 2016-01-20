# -*- coding: utf-8 -*-

from src.tools.debug import Debug

class ReadListParser():
    u"""
    TODO
    """

    @staticmethod
    def get_task(command):
        u"""
        对外的接口, 用来分析指令
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




