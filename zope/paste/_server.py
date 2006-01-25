##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""
$Id$
"""

from zope.interface import implements
from zope.paste.application import PasteApplication

from zope.server.http.wsgihttpserver import WSGIHTTPServer
from zope.server.http.commonaccesslogger import CommonAccessLogger

from zope.app.server.servertype import IServerType

class ServerType(object):

    implements(IServerType)

    def __init__(self, factory, applicationFactory, logFactory,
                 defaultPort, defaultVerbose, defaultIP=''):
        self._factory = factory
        self._applicationFactory = applicationFactory
        self._logFactory = logFactory
        self._defaultPort = defaultPort
        self._defaultVerbose = defaultVerbose
        self._defaultIP = defaultIP

    # XXX Zope calls ServerType.create() with a db argument, which is
    # the root ZODB database. We must get rid of this for ZODB-less
    # applications.
    def create(self, name, task_dispatcher, db, port=None,
               verbose=None, ip=None):
        'See IServerType'

        application = self._applicationFactory(name)

        if port is None:
            port = self._defaultPort

        if ip is None:
            ip = self._defaultIP

        if verbose is None:
            verbose = self._defaultVerbose

        return self._factory(application, name, ip, port,
                             task_dispatcher=task_dispatcher,
                             verbose=verbose,
                             hit_log=self._logFactory(),
                             )

http = ServerType(WSGIHTTPServer,
                  PasteApplication,
                  CommonAccessLogger,
                  8380, True)
