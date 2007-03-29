import zope.app.appsetup
from zope.app.wsgi import WSGIPublisherApplication

def zope_app_factory(global_conf, site_definition, file_storage,
                     devmode='no'):
    features = ()
    if devmode.lower() in ('yes', 'true', 'on'):
        features += ('devmode',)
    zope.app.appsetup.config(site_definition, features)

    db = zope.app.appsetup.database(file_storage)
    return WSGIPublisherApplication(db)
