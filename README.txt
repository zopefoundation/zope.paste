zope.paste - Zope 3 and PasteDeploy
===================================

zope.paste allows you to

* employ WSGI middlewares inside a Zope 3 application

* deploy the Zope 3 application server on any WSGI-capable webserver

using PasteDeploy_.  These are two completely different modi operandi
which only have in common that they are facilitate PasteDeploy_.  Each
is explained in detail below.

.. _PasteDeploy: http://pythonpaste.org/deploy/


WSGI middlewares inside Zope 3
------------------------------

zope.paste allows you to stack WSGI middlewares on top of Zope 3's
publisher application without changing the way you configure Zope
(``zope.conf``) or run it (``runzope``, ``zopectl``).

Configuration is very simple.  Assuming that you've already created a
Zope 3 instance using the ``mkzopeinstance`` script, there are three
steps that need to be performed:

Installing and configuring zope.paste
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

zope.paste can be installed as an egg anywhere onto your
``PYTHONPATH`` or simply dropped into your
``<INSTANCE_HOME>/lib/python`` directory.  Then you need to enable
zope.paste's ZCML configuration by creating the file
``<INSTANCE_HOME>/etc/package-includes/zope.paste-configure.zcml``
with the following contents::

  <include package="zope.paste" />

Configuring the server
~~~~~~~~~~~~~~~~~~~~~~

We create a ``<server>`` directive in
``<INSTANCE_HOME>/etc/zope.conf`` to use zope.paste's server
definition, ``Paste.Main``.  That way the WSGI middlewares will be
invoked when responses are served through this server::

  <server>
    type Paste.Main
    address 8081
  </server>

Configuring the WSGI stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we configure a WSGI application using PasteDeploy_ syntax in
``<INSTANCE_HOME>/etc/paste.ini``.  Here's an example of how to
configure the `Paste.Main` application to use the Zope 3 publisher as
a WSGI application, therefore doing the exact same thing that the
regular ``HTTP`` server definition would do::

  [app:Paste.Main]
  paste.app_factory = zope.paste.application:zope_publisher_app_factory

That's not really interesting, though.  PasteDeploy_ allows you to
chain various WSGI entities together, which is where it gets
interesting.  There seems to be a distinction between 'apps' and
'filters' (also referred to as 'middleware').  An example that might
be of interest is applying a `XSLT` transformation to the output of
the Zope 3 WSGI application.

Happily enough, someone seems to have already created a WSGI filter
for applying a `XSLT` stylesheet.  You can find it at
http://www.decafbad.com/2005/07/xmlwiki/lib/xmlwiki/xslfilter.py

If you wanted to apply this WSGI filter to Zope 3, you would need
three things:

1. Put the ``xslfilter.py`` file somewhere in ``PYTHONPATH``.
   ``<INSTANCE>/lib/python`` is a good place.

2. Add this snippet to the bottom of ``xslfilter.py``::

     def filter_factory(global_conf, **local_conf):
         def filter(app):
             return XSLFilter(app)
         return filter

3. Change ``paste.ini`` file as follows::

     [pipeline:Paste.Main]
     pipeline = xslt main

     [app:main]
     paste.app_factory = zope.paste.application:zope_publisher_app_factory

     [filter:xslt]
     paste.filter_factory = xslfilter:filter_factory

   What this does is to define a *pipeline*.  Learn more about this on
   the PasteDeploy_ website.  Refer to the source of ``xslfilter.py``
   for information about how to pass a stylesheet to the filter.


Deploying Zope 3 on an WSGI-capable webserver
---------------------------------------------

zope.paste allows you to run Zope 3 on any WSGI-capable webserver
software using PasteDeploy_.  For this you will no longer need a Zope
3 instance (though you can still have one), you won't configure Zope 3
through ``zope.conf`` and won't start it using ``runzope`` or
``zopectl``.

Configuring the application
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~

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
