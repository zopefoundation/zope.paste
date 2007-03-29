import os.path
import ZConfig
import zope.event
import zope.app.appsetup
from zope.app.appsetup.appsetup import multi_database
from zope.app.wsgi import WSGIPublisherApplication

def zope_app_factory(global_conf, site_definition, file_storage=None,
                     db_definition=None, devmode='no'):
    # relative filenames are understood to be relative to the
    # PasteDeploy configuration file
    def abspath(path):
        if os.path.isabs(path):
            return path
        return os.path.join(global_conf['here'], path)

    # load ZCML (usually site.zcml)
    features = ()
    if devmode.lower() in ('yes', 'true', 'on'):
        features += ('devmode',)
    zope.app.appsetup.config(abspath(site_definition), features)

    if file_storage is None and db_definition is None:
        raise TypeError("You must either provide a 'file_storage' or a "
                        "'db_definition' setting.")

    if file_storage is not None and db_definition is not None:
        raise TypeError("You may only provide a 'file_storage' or a "
                        "'db_definition' setting, not both.")

    # open database
    if file_storage is not None:
        db = zope.app.appsetup.database(abspath(file_storage))
    else:
        schema_xml = os.path.join(os.path.dirname(__file__), 'schema.xml')
        schema = ZConfig.loadSchema(schema_xml)
        cfgroot, cfghandlers = ZConfig.loadConfig(
            schema, abspath(db_definition))

        result, databases = multi_database(cfgroot.databases)
        db = result[0]
        zope.event.notify(zope.app.appsetup.DatabaseOpened(db))

    return WSGIPublisherApplication(db)
