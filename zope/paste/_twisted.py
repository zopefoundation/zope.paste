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

from twisted.web2 import iweb, log, resource, server, stream, wsgi
from twisted.web2.channel.http import HTTPFactory

from zope.interface import implements
from zope.paste.application import PasteApplication

from zope.app.twisted.http import Prebuffer
from zope.app.twisted.interfaces import IServerType
from zope.app.twisted.server import ZopeTCPServer

class ServerType(object):

    implements(IServerType)

    def __init__(self, factory, defaultPort, defaultIP=''):
        self._factory = factory
        self._defaultPort = defaultPort
        self._defaultIP = defaultIP

    # XXX Zope calls ServerType.create() with a db argument, which is
    # the root ZODB database. We must get rid of this for ZODB-less
    # applications.
    def create(self, name, db, ip=None, port=None, backlog=50):
        'See IServerType'
        if port is None:
            port = self._defaultPort

        if ip is None:
            ip = self._defaultIP

        # Create a twisted.internet.interfaces.IServerFactory
        factory = self._factory(name)
        return ZopeTCPServer(name, port, factory,
                             interface=ip, backlog=backlog)

def createHTTPFactory(name):
    resource = wsgi.WSGIResource(PasteApplication(name))
    resource = log.LogWrapperResource(resource)
    resource = Prebuffer(resource)
    return HTTPFactory(server.Site(resource))

http = ServerType(createHTTPFactory, 8380)
