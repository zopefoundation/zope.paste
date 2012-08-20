##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
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
import os.path
import ZConfig
import zope.event
import zope.app.appsetup
from zope.app.appsetup.appsetup import multi_database
from zope.app.wsgi import WSGIPublisherApplication

_zope_app = None
def zope_app_factory(global_conf, site_definition, file_storage=None,
                     db_definition=None, devmode='no'):
    global _zope_app
    if _zope_app is not None:
        return _zope_app

    # load ZCML (usually site.zcml)
    features = ()
    if devmode.lower() in ('yes', 'true', 'on'):
        features += ('devmode',)
    filename = os.path.join(global_conf['here'], site_definition)
    zope.app.appsetup.config(filename, features)

    if file_storage is not None and db_definition is not None:
        raise TypeError("You may only provide a 'file_storage' or a "
                        "'db_definition' setting, not both.")

    # open database
    if file_storage is not None:
        filename = os.path.join(global_conf['here'], file_storage)
        db = zope.app.appsetup.database(filename)
    elif db_definition is not None:
        filename = os.path.join(global_conf['here'], db_definition)
        schema_xml = os.path.join(os.path.dirname(__file__), 'schema.xml')
        schema = ZConfig.loadSchema(schema_xml)
        cfgroot, cfghandlers = ZConfig.loadConfig(schema, filename)

        result, databases = multi_database(cfgroot.databases)
        db = result[0]
        zope.event.notify(zope.app.appsetup.DatabaseOpened(db))
    else:
        db = None

    _zope_app = WSGIPublisherApplication(db)
    return _zope_app
