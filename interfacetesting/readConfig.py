# -*- coding: utf-8 -*-
import os
import codecs
import configparser

absolute_path = os.path.split(os.path.realpath(__file__))[0]
config_path = os.path.join(absolute_path, "config.ini")


class ReadCaonfig:
    def __init__(self):
        fd = open(config_path)
        dataconf = fd.read()
        print(dataconf[0:3])
        if dataconf[0:3] == codecs.BOM_UTF8:   # 代码运行到这 if内的语句不能执行
            dataconf = dataconf[3:0]
            file = codecs.open(config_path, "w")
            file.write(dataconf)
            file.close()
        fd.close()

        self.cp = configparser.ConfigParser()
        self.cp.read(config_path)

    def Zer(self):
        pass

    def get_email(self, name):
        value = self.cp.get("EMAIL", name)
        print(value)
        return value

    def get_http(self, name):
        value = self.cp.get("HTTP", name)
        print(value)
        return value

    def get_headers(self, name):
        value = self.cp.get("HEADERS", name)
        print(value)
        return value

    def get_db(self, name):
        value = self.cp.get("DATABASE", name)
        print(value)
        return value

    def set_headers(self, name, value):
        self.cp.set("HEADERS", name, value)
        with open(config_path, 'w+') as f:
            self.cp.write(f)

    def get_url(self, name):
        value = self.cp.get("URL", name)
        print(value)
        return value



if __name__ == '__main__':
    ab = ReadCaonfig()
    # ab.get_email("mail_host")
    ab.get_headers("token_v")
    ab.get_http("baseurl")