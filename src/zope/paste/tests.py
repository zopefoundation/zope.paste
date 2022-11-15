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
import asyncore
import doctest
import gc
import os
import shutil
import sys
import tempfile
import unittest
from urllib.request import urlopen

import paste.deploy
from waitress.server import WSGIServer


# let every Python version run on its own port to allow parallel runs:
PORT = 8765 + 10 * sys.version_info.major + sys.version_info.minor


def setUp(test):
    test.tmpdir = tempfile.mkdtemp(prefix='zope.paste-', suffix='-test')
    test.orig_cwd = os.getcwd()
    test.orig_loadapp = paste.deploy.loadapp
    test.orig_loadserver = paste.deploy.loadserver
    zcml = os.path.join(os.path.dirname(__file__), 'test_app', 'app.zcml')
    shutil.copy(zcml, os.path.join(test.tmpdir, 'app.zcml'))
    ini = os.path.join(os.path.dirname(__file__), 'test_app', 'app.ini.in')
    with open(ini) as app_ini_in:
        app_ini_contents = app_ini_in.read()
        with open(os.path.join(test.tmpdir, 'app.ini'), 'w') as app_ini:
            app_ini.write(app_ini_contents.format(PORT))
    os.chdir(test.tmpdir)


def tearDown(test):
    os.chdir(test.orig_cwd)
    paste.deploy.loadapp = test.orig_loadapp
    paste.deploy.loadserver = test.orig_loadserver
    shutil.rmtree(test.tmpdir)


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


def test_serving_test_app():
    """Test serving a real app.

    Setup logging, so we get the message ``Serving on ...`` into our doctest
    output:

    >>> import logging
    >>> logger = logging.getLogger('waitress')
    >>> handler = logging.StreamHandler(sys.stdout)
    >>> logger.addHandler(handler)
    >>> logger.setLevel(logging.INFO)

    Start the app:

    >>> import os.path
    >>> import threading
    >>> from zope.paste import serve
    >>> app_ini = os.path.abspath('app.ini')
    >>> server = threading.Thread(target=serve.serve, args=([app_ini],))
    >>> server.start()
    >>> import time; time.sleep(5)  # doctest: +ELLIPSIS
    Serving on http://...

    >>> print(urlopen('http://127.0.0.1:{}/'.format(PORT)).read().decode())
    <html>
      <body>
        <h1>Hello World, Zope App!</h1>
      </body>
    </html>

    >>> _ = [asyncore.close_all(obj._map)
    ...      for obj in gc.get_objects() if isinstance(obj, WSGIServer)]
    >>> logger.removeHandler(handler)
    """


def test_suite():
    return unittest.TestSuite((
        doctest.DocTestSuite(
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE),
    ))
