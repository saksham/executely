#!/usr/bin/python
from nose.tools import *
from executely import executor
import os

def setup():
    print("SETUP!")

def teardown():
    app_name = get_app_name()
    app_path = get_app_path()
    executor.cleanup(app_name, app_path)

def get_app_name():
    return 'Hello World!'

def get_app_path():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir('hello-world')
    app_path = os.getcwd()
    return app_path


def test_run_app():
    app_name = get_app_name()
    app_path = get_app_path()
    exit_code = executor.start(app_name, app_path)
    eq_(exit_code, 0)

