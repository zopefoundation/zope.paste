zope.paste - wsgi applications in zope 3 using paste.deploy
===========================================================

What is it?
-----------

A simple package that enables one to configure WSGI applications to
run inside Zope 3 using `paste.deploy`_.

Why?
----

Because Zope 3 already supported WSGI applications, but didn't provide
a simple way to create and configure them.

How to use it?
--------------

Short version
+++++++++++++

Configuration is very simple. There are three steps that need to be
performed:

1. Configure a named IServerType utility (by default, we already
   define a utility named `Paste.Main`).

2. Change the <server> directive on <INSTANCE_HOME>/etc/zope.conf to
   use the newly-created `IServerType` utility (out of the box, you
   can just swap out `HTTP` or `WSGI-HTTP` by `Paste.Main`).

3. Configure a WSGI application using `paste.deploy`_ syntax in
   <INSTANCE_HOME>/etc/paste.ini

Here's an example of how to configure the `Paste.Main` application
using paste.deploy to use the Zope 3 publisher as a WSGI app:

[app:Paste.Main]
paste.app_factory = zope.paste.application:zope_publisher_app_factory

.. _paste.deploy: http://pythonpaste.org/deploy/

Long version
++++++++++++

The narrative below applies to Zope 3.2.

When you create a Zope 3 instance, you have a choice of creating a
`zope.app.server` (a.k.a. zserver) instance or a `zope.app.twisted`
instance.

This package works with both, but applications that you develop using
WSGI might choose to use only one of them.

After creating an instance, you should have a directory with some
subdirectories like `etc`, `lib`, `var`, `log`, etc. Inside the `etc`
directory you can find a file named `zope.conf` inside it.

This is the file that contains the bootstrap configuration for
starting up a Zope 3 server.

Regardless of the flavor you choose (zserver or twisted) you will end
up with a file that contains something just like this::

  <server>
    type HTTP
    address 8080
  </server>

The part that's most interesting to us here is the `type HTTP`
line. This is what controls what kind of server will be
created.

When starting up, upon finding this directive, Zope 3 will lookup a
`named utility` providing `IServerType`. If you don't know what a
named utility is, you should go read some documentation before
proceeding.

Zope 3.2 has some support to WSGI applications. In fact, it does
define a `IServerType` utility named `WSGI-HTTP`, which is also
aliased to `HTTP`. So when you start up Zope 3 for the first time,
you're actually using WSGI already!

This package, `zope.paste` does define a new `IServerType` utility
named `Paste.Main`. So, effectively, once you have this package
installed you can change your `zope.conf` file to read::

  <server>
    type Paste.Main
    address 8080
  </server>

The `Paste.Main` utility defined in this package though doesn't know
how to create a WSGI application by itself. Instead, it relies on
`paste.deploy` to create a WSGI application. By default, it will load
a file named `paste.ini` in the `etc` directory of your Zope 3
instance.

When loading this file it will look for an application with the *same
name* as the utility defined. So the simplest thing you can do is to
create the `paste.ini` file with some content as follows::

  [app:Paste.Main]
  paste.app_factory = zope.paste.application:zope_publisher_app_factory

What this does is to create a WSGIPublisherApplication, which happens
to be the same WSGI application that is created when you use the
`HTTP` or `WSGI-HTTP` server type utilities.

Now, this is a lot of contortion just to do something that Zope 3 does
out of the box no? Yes, I agree. But this is where stuff starts
getting fun.

`paste.deploy` allows you to chain various WSGI entities
together. There seems to be a distinction between 'apps' and 'filters'
(also referred to as 'middleware'). An example that might interest is
applying a `XSLT` transformation to the output of the Zope 3 WSGI
application.

Happily enough, someone seems to have already created a WSGI filter
for applying a `XSLT` stylesheet. You can find it at::

 http://www.decafbad.com/2005/07/xmlwiki/lib/xmlwiki/xslfilter.py

If you wanted to apply this WSGI filter to Zope 3, you would need three
things:

1. Put the `xslfilter.py` file somewhere in
   PYTHONPATH. <INSTANCE>/lib/python is a good place.

2. Add this snippet to the bottom of `xslfilter.py`

::

   def filter_factory(global_conf, **local_conf):
       def filter(app):
           return XSLFilter(app)
       return filter

3. Change the `paste.ini` file as follows

::

   [pipeline:Paste.Main]
   pipeline = xslt main

   [app:main]
   paste.app_factory = zope.paste.application:zope_publisher_app_factory

   [filter:xslt]
   paste.filter_factory = xslfilter:filter_factory

What this does is to define a `pipeline`. Learn more about this on the
`paste.deploy`_ website. Refer to the source of `xslfilter.py` for
information about how to pass a stylesheet to the filter.

Now, this far we only worked with a single WSGI application. If you
wanted to host *more* than one WSGI application there are a couple
ways of doing it:

1. Using a `composite application` as described in `paste.deploy`_.

2. Setting up extra `IServerType` utilities.

I'm going to show you how to do the latter now.

The trick here is that as mentioned earlier here, you have the option
to use both the `zserver` and the `twisted` WSGI servers. `zope.paste`
is just glue code, so we defined a `IServerType` utility for each, and
the only thing special is that the utility name is passed on to the
WSGI application factory.

Here's an excerpt from the `configure.zcml` as found on this package::

  <configure zcml:condition="have zserver">
    <utility
        name="Paste.Main"
        component="._server.http"
        provides="zope.app.server.servertype.IServerType"
        />
  </configure>

  <configure zcml:condition="have twisted">
    <utility
        name="Paste.Main"
        component="._twisted.http"
        provides="zope.app.twisted.interfaces.IServerType"
        />
  </configure>

Depending on which server is available, the right `IServerType`
utility is registered. You are encouraged to use the same pattern when
defining yours.

So suppose you want to have a second WSGI application. Here's how you
could do it.

1. Create a new `IServerType` utility. This excerpt could be added to
   a `configure.zcml` in your own package, or to a standalone file in
   `etc/package_includes`

::

  <configure zcml:condition="have zserver">
    <utility
        name="Paste.Another"
        component="zope.paste._server.http"
        provides="zope.app.server.servertype.IServerType"
        />
  </configure>

  <configure zcml:condition="have twisted">
    <utility
        name="Paste.Another"
        component="zope.paste._twisted.http"
        provides="zope.app.twisted.interfaces.IServerType"
        />
  </configure>

2. Change your `zope.conf` file to define a new server, using the
   newly-created `Paste.Another` utility

::

  <server>
    type Paste.Main
    address 8080
  </server>

  <server>
    type Paste.Another
    address 8180
  </server>

3. Define a WSGI application `Paste.Another` in `paste.ini`

::

  [pipeline:Paste.Main]
  pipeline = xslt main

  [app:main]
  paste.app_factory = zope.paste.application:zope_publisher_app_factory

  [filter:xslt]
  paste.filter_factory = xslfilter:filter_factory

  [app:Paste.Another]
  paste.app_factory = zope.paste.application:zope_publisher_app_factory

That's it! For more information, learn about the different ways of
configuring applications with `paste.deploy`_.
