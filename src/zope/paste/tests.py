##############################################################################
#
# Copyright (c) 2013 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests.
"""
import doctest
import unittest
import paste.deploy

def setUp(test):
    test.orig_loadapp = paste.deploy.loadapp
    test.orig_loadserver = paste.deploy.loadserver

def tearDown(test):
    paste.deploy.loadapp = test.orig_loadapp
    paste.deploy.loadserver = test.orig_loadserver

def test_basic_serve():
    """Starting a paster server

    Let's stub the loader functions:

    >>> def loadapp(uri, name=None, **kw):
    ...     print('Application: ' + (name or 'main'))
    ...     print(uri)
    ...     return object()
    >>> paste.deploy.loadapp = loadapp

    >>> def server(app):
    ...     print('Start serving app')

    >>> def loadserver(uri, name=None, **kw):
    ...     print('Server: ' + (name or 'main'))
    ...     print(uri)
    ...     return server
    >>> paste.deploy.loadserver = loadserver

    We can now serve the app:

    >>> from zope.paste import serve
    >>> serve.serve(['/test/app.ini'])
    Server: main
    config:///test/app.ini
    Application: main
    config:///test/app.ini
    Start serving app

    We can also specify the names of the app and server:

    >>> serve.serve(
    ...     ['--app-name', 'app', '--server-name', 'server', '/test/app.ini'])
    Server: server
    config:///test/app.ini
    Application: app
    config:///test/app.ini
    Start serving app

    The startup fails, if the ini file is not specified:

    >>> serve.serve([])
    Traceback (most recent call last):
    ...
    SystemExit: No paster ini file specified.

    Now we get the args from ``sys``:

    >>> import sys
    >>> orig_args = sys.argv
    >>> sys.argv = ['serve', '/test/app.ini']

    >>> serve.serve()
    Server: main
    config:///test/app.ini
    Application: main
    config:///test/app.ini
    Start serving app

    >>> sys.argv = orig_args

    """

def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(
                setUp=setUp, tearDown=tearDown),
    ))
