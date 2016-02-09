#!/usr/bin/python
import sys, os, platform
import configparser
from executely.constants import Java

class AppConfiguration(object):
    def __init__(self, app_path):
        if (not os.path.exists(app_path)):
            raise Exception('The app folder "%s" does not exist!' % app_path)

        config = configparser.ConfigParser()
        config.read(os.path.join(app_path, 'app.cfg'))
        self.__main_class = AppConfiguration.parse_property(config, 'main_class')
        self.__jvm_args = AppConfiguration.parse_property(config, 'jvm_args')
        self.__command_line_args = AppConfiguration.parse_property(config, 'command_line_args')
        self.__classpath = AppConfiguration.parse_classpath(app_path, AppConfiguration.parse_classpath_from_config(config, 'classpath'))
        self.__app_path = app_path
        self.__stdout_path = os.path.join(app_path, AppConfiguration.parse_property(config, 'stdout_path', 'stdout.log'))
        self.__stderr_path = os.path.join(app_path, AppConfiguration.parse_property(config, 'stderr_path', 'stderr.log'))

    @property
    def main_class(self):
        return self.__main_class

    @property
    def jvm_args(self):
        return self.__jvm_args

    @property
    def command_line_args(self):
        return self.__command_line_args

    @property
    def classpath(self):
        return self.__classpath

    @property
    def app_path(self):
        return self.__app_path

    @property
    def stdout_path(self):
        return self.__stdout_path

    @property
    def stderr_path(self):
        return self.__stderr_path

    def get_command(self, java_command=Java.DEFAULT_COMMAND):
        args = self.command_line_args.split()
        command = [java_command, self.jvm_args, "-classpath", self.classpath, self.main_class] + args
        return [token for token in command if token]

    def is_valid(self):
        mandatory_fields = [self.main_class]
        if not all(mandatory_fields):
            print("Some mandatory fields are missing from configuration file!")
            return False
        return True

    @staticmethod
    def parse_classpath(app_path, app_classpath=''):
        non_posix_os_prefix = ['CYGWIN', 'WINDOWS']
        classpath_separator = ':'
        for os in non_posix_os_prefix:
            if platform.platform().upper().startswith(os):
                classpath_separator = ';'
                break

        default_classpath = ['.', 'dependency/*', 'target/*', 'target/dependency/*', ('%s/*' % app_path), ('%s/dependency/*' % app_path)]
        classpath = classpath_separator.join(app_classpath + default_classpath)
        return classpath

    @staticmethod
    def parse_property(config, key, default=''):
        if config.has_option('defaults', key):
            return config.get('defaults', key)
        else:
            return default

    @staticmethod
    def parse_classpath_from_config(config, key):
        app_config_classpath_separator = ","
        classpath = AppConfiguration.parse_property(config, key, default='')
        if classpath:
            return [cp.strip() for cp in classpath.split(app_config_classpath_separator)]
        return []
