import zope.app.appsetup
from zope.app.wsgi import WSGIPublisherApplication

def zope_app_factory(global_conf, site_definition, file_storage):
    zope.app.appsetup.config(site_definition)
    db = zope.app.appsetup.database(file_storage)
    return WSGIPublisherApplication(db)
