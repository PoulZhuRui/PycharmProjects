import unittest
import paramunittest
from asyncio.windows_events import NULL

import readConfig as readconfig
from commonfile import Log as Log
from commonfile import common
from commonfile import configHttp as confighttp

search_xls = common.get_xls("usercase.xlsx", "search")
local_readconfig = readconfig.ReadCaonfig()
confighttp = confighttp.ConfigHttp()


@paramunittest.parametrized(*search_xls)
class search(unittest.TestCase):
    def setParameters(self, case_name, case_no, method, token, barcode, result, code, msg):
        self.case_no = str(case_no)
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.barcode = str(barcode)
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

    def testSearch(self):
        self.url = common.get_url_from_xml("search")
        confighttp.set_url(self.url)
        self.logger.info("请求地址" + self.url)
        print("第一步： 设置url" + self.url)
        self.log.build_start_line(self.case_no)
        if self.token == '0':
            token = local_readconfig.get_headers("token_v")
        elif self.token == '1':
            token = "NULL"

        header = {"X-ACCESS-TICKET": str(token)}
        confighttp.set_headers(header)

        data = {"barcode": self.barcode}
        confighttp.set_data(data)

        self.logger.info("请求头X-ACCESS-TICKET：" + token + "，请求的参数barcode：" + self.barcode)

        print("第三部：发送请求参数")

        self.return_json = confighttp.post()

        self.check_result()
        print("检查结果")

    def tearDown(self):
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])
        self.log.build_end_line(self.case_no)

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

