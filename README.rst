zope.paste - Zope 3 and PasteDeploy
===================================

zope.paste allows you to deploy the Zope 3 application server on any
WSGI-capable webserver using PasteDeploy_.

.. _PasteDeploy: http://pythonpaste.org/deploy/

zope.paste allows you to run Zope 3 on any WSGI-capable webserver
software using PasteDeploy_.  For this you will no longer need a Zope
3 instance (though you can still have one), you won't configure Zope 3
through ``zope.conf`` and won't start it using ``runzope`` or
``zopectl``.

Configuring the application
---------------------------

zope.paste provides a PasteDeploy_-compatible factory for Zope 3's
WSGI publisher application and registers it in an entry point.  We can
therefore create a very simple Zope 3 application in a PasteDeploy_
configuration file (e.g. ``paste.ini``)::

  [app:main]
  use = egg:zope.paste
  site_definition = /path/to/site.zcml
  file_storage = /path/to/Data.fs
  devmode = on

In this case, ``/path/to/site.zcml`` refers to a ``site.zcml`` as
known from a Zope 3 instance.  You can, for example, put ``paste.ini``
into an existing Zope 3 instance, next to ``site.zcml``.

Configuring the ZODB database
-----------------------------

Instead of referring to a ZODB FileStorage using the ``file_storage``
setting, you can also configure multiple or other ZODB database
backends in a ZConfig-style configuration file (much like
``zope.conf``), e.g. the following configures a ZEO client::

  <zodb>
    <zeoclient>
      server localhost:8100
      storage 1
      cache-size 20MB
    </zeoclient>
  </zodb>

Refer to this file from ``paste.ini`` this way (and delete the
``file_storage`` setting)::

  db_definition = db.conf

Configuring the server
----------------------

In order to be able to use our Zope application, we only need to add a
server definition.  We can use the one that comes with Paste or
PasteScript_, rather::

  [server:main]
  use = egg:PasteScript#wsgiutils
  host = 127.0.0.1
  port = 8080

.. _PasteScript: http://pythonpaste.org/script/

Now we can start the application using the ``paster`` command that
comes with PasteScript_::

  $ paster serve paste.ini

WSGI middlewares can be configured like described above or on the
PasteDeploy_ website.
