# coding=utf8
import os


class Config(object):

    def __init__(self, from_dir):
        self.from_dir = from_dir
        self.zone = os.environ['RKZONE']
        self.bucket_postfix = self.zone
        self._load_config_to()

    def _load_config_to(self):
        module = __import__(self.from_dir, fromlist=[self.zone])
        for k, v in getattr(module, self.zone).Config.__dict__.iteritems():
            if not k.startswith('_'):
                setattr(self, k, v)

    def reload_config(self):
        self._load_config_to()

    # modify by Yoray, JoyGames, ALPHA GROUP CO.,LTD, at 2017-03-07
    # detail: 增加db bucket名称后缀，方便创建不同服db
    def get_bucket_name(self, name):
        if self.bucket_postfix == '' or self.bucket_postfix is None:
            return name
        return name + '_' + self.bucket_postfix


conf = Config('script.common.config')
