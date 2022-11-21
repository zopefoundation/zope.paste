Change History
--------------

1.1.0 (2022-11-21)
~~~~~~~~~~~~~~~~~~

- Add support for Python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11.

- Drop support for Python 2.7 and 3.5.


1.0.0 (2017-01-04)
~~~~~~~~~~~~~~~~~~

- Changed support from Python 3.3 to 3.5.

- Dropped Python 2.6 support.


1.0.0a1 (2013-02-27)
~~~~~~~~~~~~~~~~~~~~

- Added support for Python 3.3.

- Dropped support for Python 2.4 and 2.5.

- Removed support for employing WSGI middlewares inside a Zope 3
  application. Only the script-based server startup is now supported.

- Added a new console script to run a paste-configured WSGI server and
  application.

- Conform to standard ZF project layout.

- Added license and copyright file. Also fixed copyright statement in file
  headers.

- Added ``MANIFEST.in`` and ``tox.ini``.


0.4 (2012-08-21)
~~~~~~~~~~~~~~~~

- Add this changelog, reconstructed from svn logs and release dates on
  PyPI.

- Support a 'features' config option in the PasteDeploy INI file, which
  can contain a space-separated list of feature names.  These can be
  tested for in ZCML files with the <*directive*
  zcml:condition="have *featurename*"> syntax.

  Previously the only feature that could be enabled was 'devmode' and
  it had its own option.  For backwards compatibility, ``devmode = on``
  adds a 'devmode' feature to the feature list.


0.3 (2007-06-02)
~~~~~~~~~~~~~~~~

- Release as an egg with explicit dependencies for zope.app packages.

- Buildoutify the source tree.


0.2 (2007-05-29)
~~~~~~~~~~~~~~~~

- Extended documentation.

- Added a real PasteDeploy application factory. This allows you to run
  Zope 3 on any WSGI capable server, without integration code.

- Support for devmode.

- Support multiple databases through a config file (specify db_definition
  instead of file_storage).

- Accept filenames relative to the location of the PasteDeploy INI file.


0.1 (2006-01-25)
~~~~~~~~~~~~~~~~

- Initial release.
