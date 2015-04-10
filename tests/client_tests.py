__author__ = 'ToothlessRebel'
from nose.tools import *
import client


def setup():
    print("SETUP!")


def teardown():
    print('TEARDOWN!')


def test_basic():
    print("I RAN!")