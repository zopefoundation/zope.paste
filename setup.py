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

zope.paste provides the necessary glue to enable you to use
paste.deploy to configure wsgi apps in zope 3. includes a app_factory
for the zope 3 wsgi zope.app.publisher application.
"""

classifiers = """\
Development Status :: 3 - Alpha
Environment :: Web Environment
License :: OSI Approved :: Zope Public License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet :: WWW/HTTP
Topic :: Software Development :: Libraries :: Python Modules
"""

import os
import sys
from setuptools import setup, find_packages

# We're using the module docstring as the distutils descriptions.
doclines = __doc__.split("\n")

setup(name="zope.paste",
      version="0.1",
      author="Sidnei da Silva",
      author_email="sidnei@enfoldsystems.com",
      keywords="web wsgi application server",
      url="http://cheeseshop.python.org/pypi/zope.paste",
      download_url="http://cheeseshop.python.org/packages/source/z/zope.paste/zope.paste-%s.tar.gz" % VERSION,
      license="Zope Public License",
      platforms=["any"],
      description=doclines[0],
      classifiers=filter(None, classifiers.split("\n")),
      long_description="\n".join(doclines[2:]),
      namespace_packages=['zope'],
      packages=find_packages(exclude='tests'),
      package_data={'zope.paste': ['*.zcml']},
      zip_safe=False,
      )
