#!/bin/python

class Java(object):
    DEFAULT_COMMAND = 'java'

class ExitCodes(object):
    SUCCESS = 0
    INVALID_PARAMETERS = 2
    INVALID_CONFIGURATION = 5
    FAILED_TO_START = 20
    ALREADY_RUNNING = 21
