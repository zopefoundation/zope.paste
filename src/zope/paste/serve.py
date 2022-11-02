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
"""Serve a Paste Application.
"""
import optparse
import os.path
import sys

import paste.deploy


parser = optparse.OptionParser("%prog [options] <paste-ini>")

config = optparse.OptionGroup(
    parser, "Configuration", "Options that deal with service startup.")

config.add_option(
    '--app-name', '-n', action="store", dest='app_name', default=None,
    help="Load the named application (default: main)")

config.add_option(
    '--server-name', action="store", dest='server_name', default=None,
    help="Use the named server (default: main)")

parser.add_option_group(config)


def serve(args=None):
    if args is None:
        args = sys.argv[1:]
    options, pos = parser.parse_args(args)
    if not len(pos):
        sys.exit('No paster ini file specified.')
    ini_uri = 'config://' + os.path.abspath(pos[0])
    # Load components.
    server = paste.deploy.loadserver(ini_uri, options.server_name)
    app = paste.deploy.loadapp(ini_uri, options.app_name)
    # Run the server.
    server(app)
