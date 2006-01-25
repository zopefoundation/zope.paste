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

import os
from paste.deploy import loadapp
from zope.interface import implements

from zope.app.wsgi import interfaces
from zope.app.wsgi import WSGIPublisherApplication
from zope.app.publication.httpfactory import HTTPPublicationRequestFactory

class PasteApplication(object):
    """A WSGI application implementation hooking a paste app to the
    zope publisher.

    Instances of this class can be used as a WSGI application object.

    The class relies on a properly initialized request factory.
    """
    implements(interfaces.IWSGIApplication)

    def __init__(self, name):
        # `name` that gets passed here is something like:
        # <utility_name>:<host>:<port> for zope.app.twisted, and just
        # <utility_name> for zope.app.server. Extract just the utility
        # name.
        name = name.rsplit(':', 2)[0]
        # XXX There's no way currently to find out where our
        # INSTANCE_HOME is, so assume the cwd is the INSTANCE_HOME.
        path = os.getcwd()
        self.wsgi_app = loadapp('config:etc/paste.ini',
                                name, relative_to=path)

    def __call__(self, environ, start_response):
        """See zope.app.wsgi.interfaces.IWSGIApplication"""
        return self.wsgi_app(environ, start_response)

# XXX Dirty hack. Since we don't have access to the configured
# database or anything as the ZConfig options object is thrown away,
# we create the application and then stash the request factory into it
# when the database opened event gets fired.
publisher_app = WSGIPublisherApplication(None)

def zope_publisher_app_factory(global_config, **local_config):
    return publisher_app

def databaseOpened(event):
    global publisher_app
    factory = HTTPPublicationRequestFactory(event.database)
    publisher_app.requestFactory = factory
