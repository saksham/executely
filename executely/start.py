#!/bin/python
import os, datetime
from executely import executor
import argparse

class CommandLineArgs(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("app_name",    help="Name of the App")
        parser.add_argument("main_class",  help="Main class")
        parser.add_argument("--app-args", help="Argument to pass to the App")
        parser.add_argument("--classpath", help="Classpath as python list")
        parser.add_argument("--jvm-args",  help="Additional JVM arguments")
        parser.add_argument("--java-cmd",  help="Path to java executable. Set this option if java is not in your path")
        parser.add_argument("--disable-locking", action='store_true', help="")
        args = parser.parse_args()
        self.__app_name = args.app_name
        self.__main_class = args.main_class
        self.__app_args = args.app_args
        self.__classpath = args.classpath
        self.__jvm_args = args.jvm_args
        self.__java_cmd = args.java_cmd
        self.__locking_disabled = args.disable_locking

    @property
    def app_name(self):
        return self.__app_name

    @property
    def app_args(self):
        return self.__app_args

    @property
    def jvm_args(self):
        return self.__jvm_args

    @property
    def java_cmd(self):
        return self.__java_cmd

    @property
    def main_class(self):
        return self.__main_class

    @property
    def locking_disabled(self):
        return self.__locking_disabled

    @property
    def classpath(self):
        return self.__classpath

args = CommandLineArgs()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    executor.start(args.app_name, args.main_class, java_cmd=args.java_cmd, app_args=args.app_args, classpath=args.classpath, jvm_args=args.jvm_args, locking_disabled=args.locking_disabled)

if __name__ == '__main__':
    main()
 
