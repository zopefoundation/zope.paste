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

Configuration is very simple. There are three steps that need to be
performed:

1. Configure a named IServerType utility (by default, we already
   define a utility named `Paste.Main`).

2. Change the <server> directive on <INSTANCE_HOME>/etc/zope.conf to
   use the newly-created 'IServerType' utility (out of the box, you
   can just swap out 'HTTP' or 'WSGI-HTTP' by 'Paste.Main').

3. Configure a WSGI application using `paste.deploy`_ syntax in
   <INSTANCE_HOME>/etc/paste.ini

Here's an example of how to configure the `Paste.Main` application
using paste.deploy to use the Zope 3 publisher as a WSGI app:

[app:Paste.Main]
paste.app_factory = zope.paste.application:zope_publisher_app_factory


.. _paste.deploy: http://pythonpaste.org/deploy/
