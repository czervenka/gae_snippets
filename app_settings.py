__author__ 'czervenka'
"""
Simple database app settings

BASIC USE
---------
    from app_settings import settings
    print settings['version']  # read settings
    settinges['version'] = '1'  # stores settings

INITIALIZATION
--------------
    from app_settings import settings
    settings['version'] = '1'
    # use Datastore Viewer to change your own settings

DEPENDENCY
----------
none
"""
from google.appengine.ext import ndb


class AppSettings(ndb.Model):

    version = ndb.StringProperty(default='0', indexed=False)
    debug = ndb.BooleanProperty(default=False, indexed=False)


class LazyAppSettings(object):
    """
    Settings row property descriptor used in SettingsDict.
    """

    def __get__(self, instance, owner=None):
        if not hasattr(instance, '_cached_settings'):
            key = ndb.Key(AppSettings, 'app_settings')
            row = key.get()
            if row is None:
                row = AppSettings(key=key)
            instance._cached_settings = row
        return instance._cached_settings


class SettingsDict(object):
    """
    Dictionary which reads settings from database.

    To list all settings simply calll settings.items()
    """

    _row = LazyAppSettings()

    def __getitem__(self, key):
        if hasattr(self._row, key):
            return getattr(self._row, key)
        else:
            raise KeyError('Key %s not found.' % key)

    def __setitem__(self, key, value):
        setattr(self._row, key, value)
        self._row.put()

    def __contains__(self, key):
        return hasattr(self._row, key)

    def keys(self):
        return self._row._properties.keys()

    def items(self):
        return [(key, self[key]) for key in self.keys()]

    def values(self):
        return [self[key] for key in self.keys()]

    def __iter__(self):
        for key in self.keys():
            yield key


settings = SettingsDict()
