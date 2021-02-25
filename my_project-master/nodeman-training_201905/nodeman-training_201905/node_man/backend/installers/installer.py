# -*- coding: utf-8 -*-
import os
import hashlib
import urllib2
from abc import ABCMeta, abstractmethod


class Installer(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def prepare_installer_files(self, file_names):
        md5_mapping = self.get_md5_mapping()
        for file_name in file_names:
            if self.is_small_enough(file_name):
                self.download_file(file_name)
            else:
                if not self.is_latest(file_name, md5_mapping):
                    self.download_file(file_name)

    def is_small_enough(self, file_name):
        return file_name.endswith(".sh") or file_name.endswith(".ksh") or file_name.endswith(".bat") or (file_name in [
            "direct_non_cygwin.tgz"])

    def is_latest(self, file_name, md5_mapping):
        file_path = os.path.join(self.local_tmp_path, file_name)
        if not os.path.exists(file_path):
            return False
        try:
            return self.caculate_md5(file_path) == md5_mapping[file_name]
        except KeyError:
            return False

    def get_md5_mapping(self):
        md5_fname = "MD5"
        self.download_file(md5_fname)
        with open(os.path.join(self.local_tmp_path, md5_fname)) as md5_file:
            return dict([self.get_kv_pair(line) for line in md5_file])

    def get_kv_pair(self, line):
        v, k = line.split()
        return k.strip(), v.strip()

    def download_file(self, file_name):
        self.log("fetch {}".format(file_name))
        r = urllib2.urlopen('{}/{}'.format(self.nginx_cfg, file_name))
        self.log("successfully fetched {}".format(file_name))
        with open(os.path.join(self.local_tmp_path, file_name), 'wb') as f:
            f.write(r.read())
        self.log("successfully downloaded {}".format(file_name))

    def caculate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @abstractmethod
    def execute(self):
        pass
