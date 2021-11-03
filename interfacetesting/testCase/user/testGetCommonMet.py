import unittest
import paramunittest
import readConfig as readconfig
from commonfile import Log as Log
from commonfile import common
from commonfile import configHttp as confighttp

Result_xls = common.get_common_xls("userCommonCase.xlsx", "Result")
local_readconfig = readconfig.ReadCaonfig()
confighttp = confighttp.ConfigHttp()


@paramunittest.parametrized(*Result_xls)
class QueryBarcode(unittest.TestCase):
    def setParameters(self, case_name, method, type, token, host, data, result, code, msg):
        self.case_name = str(case_name)
        self.method = str(method)
        self.type = str(type)
        self.token = str(token)
        self.host = str(host)
        self.data = data
        self.code = int(code)
        self.msg = str(msg)
        self.result = str(result)
        self.return_json = None
        self.info = None

    def description(self):
        return self.case_name

    def setUp(self):
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()

        print(self.case_name + "测试前的准备")

    def testResult_xls(self):
        url = self.host
        print("第一步： 设置url:" + url)

        header = {self.type: str(self.token)}
        data = (self.data)
        print("第三部：发送请求参数 " + data)

        self.return_json = confighttp.post_common_json(url, header, data)

        self.check_result()
        print("检查结果")

    def tearDown(self):
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def check_result(self):
        self.info = self.return_json.json()
        common.show_return_msg(self.return_json)

        if self.result == '0':
            # email = common.get_value_from_return_json(self.info, 'member', 'barcode')
            self.assertEqual(self.info['code'], int(self.code))
            self.assertEqual(self.info['msg'], self.msg)

        if self.result == '1':
            self.assertEqual(self.info['code'], int(self.code))
            self.assertEqual(self.info['msg'], self.msg)

