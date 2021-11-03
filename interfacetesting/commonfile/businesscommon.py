from commonfile import common
from commonfile import configHttp
import readConfig as readconfig

local_readconfig = readconfig.ReadCaonfig()
loacl_confighttp = configHttp.ConfigHttp()
local_login_xls = common.get_xls("userCase.xlsx", "login")
loacl_addaddress_xls = common.get_xls("userCase.xlsx", "addAddress")


def login():
    # get url
    url = common.get_url_from_xml("login")
    loacl_confighttp.get(url)

    # set header
    token = local_readconfig.get_headers("token_v")
    header = {"token": token}
    loacl_confighttp.set_headers(header)

    # set param
    data = {"email": local_login_xls[0][3],
            "password": local_login_xls[0][4]}
    loacl_confighttp.set_data(data)

    # login
    response = loacl_confighttp.post().json()
    token = common.get_value_from_return_json(response, "member", "token")
    return token


# login
def logout(token):
    # set url
    url = common.get_url_from_xml("login")
    loacl_confighttp.set_url(url)

    # set header
    header = {'token': token}
    local_readconfig.set_headers(header)

    # logout
    loacl_confighttp.get()