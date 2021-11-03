import unittest
import paramunittest
import readConfig as readconfig
from commonfile import Log as Log
from commonfile import common
from commonfile import configHttp as confighttp

QueryBarcode_xls = common.get_xls("usercase.xlsx", "QueryBarcode")
local_readconfig = readconfig.ReadCaonfig()
confighttp = confighttp.ConfigHttp()


@paramunittest.parametrized(*QueryBarcode_xls)
class QueryBarcode(unittest.TestCase):
    def setParameters(self, case_name, method, token, barcode, nickname, headimgurl, unionid, province, city, lng, lat, result, code, msg):
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.barcode = str(barcode)
        self.nickname = str(nickname)
        self.headimgurl = str(headimgurl)
        self.unionid = str(unionid)
        self.province = str(province)
        self.city = str(city)
        self.lng = str(lng)
        self.lat = str(lat)
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

    def testQueryBarcode_xls(self):
        self.url = common.get_url_from_xml("QueryBarcode")
        confighttp.set_url(self.url)
        print("第一步： 设置url" + self.url)

        if self.token == '0':
            token = local_readconfig.get_headers("token_v")
        elif self.token == '1':
            token = None

        header = {"X-ACCESS-TICKET": str(token)}
        confighttp.set_headers(header)

        data = {"barcode": self.barcode,
                "nickname": self.nickname,
                "headimgurl": self.headimgurl,
                "unionid": self.unionid,
                "province": self.province,
                "city": self.city,
                "lng": self.lng,
                "lat": self.lat}
        confighttp.set_data(data)
        print("第三部：发送请求参数")

        self.return_json = confighttp.post()

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

