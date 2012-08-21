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
"""zope.paste - wsgi applications in zope 3 using paste.deploy
"""
import os
from setuptools import setup, find_packages

classifiers = """\
Development Status :: 3 - Alpha
Environment :: Web Environment
License :: OSI Approved :: Zope Public License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet :: WWW/HTTP
Topic :: Software Development :: Libraries :: Python Modules
"""

def read_file(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

long_description = read_file('README.txt') + '\n\n' + read_file('CHANGES.txt')

setup(name="zope.paste",
      version='0.5.dev0',
      author="Sidnei da Silva",
      author_email="sidnei@enfoldsystems.com",
      description="Zope 3 and PasteDeploy",
      long_description=long_description,
      keywords="web wsgi application server",
      url="http://cheeseshop.python.org/pypi/zope.paste",
      license="Zope Public License",
      platforms=["any"],
      classifiers=filter(None, classifiers.split("\n")),
      namespace_packages=['zope'],
      packages=find_packages(exclude='tests'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'PasteDeploy',
                        'zope.interface',
                        'zope.app.appsetup',
                        'zope.app.wsgi',
                        'zope.app.twisted',
                        'zope.app.server'],
      entry_points = """
      [paste.app_factory]
      main = zope.paste.factory:zope_app_factory
      """)
