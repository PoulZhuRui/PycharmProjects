import os
from xlrd import open_workbook
from xml.etree import ElementTree as elementtree
from commonfile.Log import MyLog as Log
from commonfile import configHttp as confighttp
import requests
import readConfig as readconfig
import json
from datetime import datetime
from xlrd import xldate_as_tuple

local_readconfig = readconfig.ReadCaonfig()
absolute_path = readconfig.absolute_path
local_confighttp = confighttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

caseNo = 0


def get_visitor_token():
    """create a token for visitor
        :return: """
    host = local_readconfig.get_http("baseurl")
    response = requests.get(host + "/v2/User/Token/generate")
    info = response.json()
    token = info.get("info")  # 不能直接获取get
    logger.debug("Create token:%s" % (token))
    return token


def set_visitor_token_to_config():
    """set token that created for visitor to config
        :return: """
    token_v = get_visitor_token()
    local_readconfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\n请求地址:" + url)
    # 可以显示中文
    print("\n请求返回值：" + "\n" + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


# ****************************** read testCase excel ********************************


def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xls_path = os.path.join(absolute_path, "testFile", "case", xls_name)
    # open xls file
    file = open_workbook(xls_path)
    # get sheet by name 通过名称获取一个工作表
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows 获取行数
    nrows = sheet.nrows
    num = 1
    for i in range(nrows):
        if sheet.row_values(i)[0] != u"case_name":
            row_values = sheet.row_values(i)
            if row_values:
                str_obg = []
            for e in range(len(row_values)):
                cell = sheet.cell_value(num, e)
                ctype = sheet.cell(num, e).ctype
                # 0：empty 1: str 2: num 3:date 4:布尔 5:error
                if ctype == 2 and cell % 1 == 0.0:  # 是否是数字类型
                    cell = int(cell)
                    cell = str(cell)
                elif ctype == 3:  # 是否是日期
                    date = datetime(*xldate_as_tuple(cell, 0))
                    cell = date.strftime('%Y-%m-%d %H:%M:%S')
                elif ctype == 4:   # 是否是布尔值
                    cell = True if cell == 1 else False
                str_obg.append(cell)
            cls.append(str_obg)
            num = num + 1
    return cls


def get_common_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xls_path = os.path.join(absolute_path, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xls_path)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    num1 = 1
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_common':
            row_values1 = sheet.row_values(i)
            if row_values1:
                stgos = []
            for e in range(len(row_values1)):
                cell = sheet.cell_value(num1, e)
                ctype = sheet.cell(num1, e).ctype
                if ctype == 2 and cell % 1 == 0.0:
                    cell = int(cell)
                stgos.append(cell)
            cls.append(stgos)
            num1 += 1
    return cls


"""
def get_common_xls(xls_name, sheet_name):
    list = []
    # get xls file's path
    xls_path = os.path.join(absolute_path, "testFile", "case", xls_name)
    # open xls file
    file = open_workbook(xls_path)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u"case_name":
            list.append(sheet.row_values(i))
    return list
"""

# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(absolute_path, "testFile", "SQL.xml")
        tree = elementtree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql

# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(absolute_path, 'testFile', 'interfaceURL.xml')
    tree = elementtree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/'.join(url_list)
    return url



if __name__ == '__main__':
    # print(get_xls("login"))
    set_visitor_token_to_config()