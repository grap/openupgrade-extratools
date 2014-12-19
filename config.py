#! /usr/bin/env python
# -*- encoding: utf-8 -*-

from ConfigParser import ConfigParser
from os.path import isfile


def read_config():
    config_file = './config.ini'
    assert isfile(config_file), (
        'Could not find config file (looking at %s)' % (config_file)
    )
    conf = ConfigParser()
    conf.read(config_file)
    return conf


conf = read_config()
