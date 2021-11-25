from application import app
from common.lib.DataHelper import getCurrentTime
import os


class UrlManager(object):
    @staticmethod
    def build_Url(path):
        config_domain = app.config["DOMAIN"]
        return config_domain["www"]+path

    @staticmethod
    def build_static_Url(path):
        # return UrlManager.build_Url("/static" + path+"?ver="+UrlManager.getReleaseVersion())
        return UrlManager.build_Url("/static" + path)

    @staticmethod
    def getReleaseVersion():
        '''
        use time to control the version
        '''
        ver = "%s" % (getCurrentTime("%Y%m%d%H%M%S%f"))
        release_path = app.config.get('RELEASE_PATH')
        if release_path and os.path.exists(release_path):
            with open(release_path, 'r') as f:
                ver = f.readline()
        return ver
