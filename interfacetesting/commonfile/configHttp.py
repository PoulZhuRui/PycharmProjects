import requests
import readConfig as readconfig
from commonfile.Log import MyLog as Log
import json
local_readconfig = readconfig.ReadCaonfig()


class ConfigHttp:
    def __init__(self):
        global host, port, timeout
        host = local_readconfig.get_http("baseurl")
        port = local_readconfig.get_http("port")
        timeout = local_readconfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        self.url = host + url

    def set_headers(self, headers):
        self.headers = headers
        print(self.headers)

    def set_params(self, params):
        self.params = params

    def set_data(self, data):
        self.data = data
        print(self.data)

    def set_file(self, file):
        if file != "":
            file_path = "F:\PycharmProjects\interfacetesting\img" + file
            self.files = {"file":open(file_path, "rb")}
        if file == "" or file is None:
            self.state = 1

    """界定get方法"""
    def get(self):
        """defined get method"""
        try:
            response = requests.get(self.url, params=self.params, headers=self.headers, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("time out!!")
            return None

    """界定post方法，包含get参数和post数据，不提供上传文件，"""
    def post(self):
        """"""
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data, timeout=float(timeout))
            print(response.text)
            self.logger.debug(response.text)
            return response

        except requests.exceptions.ConnectTimeout:
            self.logger.error("time out!!")
            return None


    """界定post方法，包含上传文件 """

    def past_with_File(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("time out!!")
            return None
    """界定的post方法， json"""
    def post_with_json(self):
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    """界定的post方法， json"""
    def post_common_json(self, url, header, data):
        try:
            response = requests.post(url, headers=header, data=data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ == '__main__':
    confighttp = ConfigHttp()
    confighttp.post()
    print("ConfigHTTP")