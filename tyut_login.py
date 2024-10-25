import time

import requests
import socket
import json
import re

url = 'https://drcom.tyut.edu.cn:802/eportal/portal/login'
status_url = 'https://drcom.tyut.edu.cn/drcom/chkstatus?callback=dr1001&jsVersion=4.X&v=8249&lang=zh'
user_id = 'your user_name'
user_password = 'your password'
my_ip = ''


def get_ip():
    resp = requests.get(url=status_url)
    status = json.loads(re.search(r'\((.+)\)', resp.text).group(1))
    return status['v46ip']

def get_key(ip):
    """根据 IP 地址生成加密密钥"""
    ret = 0
    for char in ip:
        ret ^= ord(char)
    return ret

def enc_pwd(password, key):
    """对密码进行异或加密"""
    if not password or len(password) > 512:
        return ""
    
    encrypted = ""
    for char in password:
        ch = ord(char) ^ key  # 对字符进行异或操作
        encrypted += format(ch, '02x')  # 转换为十六进制字符串并拼接
    return encrypted


def encrypt_data(data, encryption_type, secret_key, ip_address):
    """对数据进行加密，包括 IP 地址、用户名和密码"""
    if encryption_type == 1:  # 使用密钥
        key = get_key(secret_key)
    else:  # 使用 IP 地址
        key = get_key(ip_address)

    encrypted_data = {}
    
    # 加密 IP 地址
    encrypted_data['ip_address'] = enc_pwd(ip_address, key)

    for key_name, value in data.items():
        if key_name == "error_code":
            encrypted_data[key_name] = value
        else:
            encrypted_data[key_name] = enc_pwd(value, key)  # 加密其他数据

    return encrypted_data


def internet_login():

    # 示例数据
    data_to_encrypt = {
        "username": user_id,
        "password": user_password,
        "error_code": "0"
    }

    # 配置
    encryption_type = 1  # 0-ip, 1-密钥
    secret_key = "drcom"  # 密钥
    ip_address = my_ip

    # 加密数据
    encrypted_result = encrypt_data(data_to_encrypt, encryption_type, secret_key, ip_address)

    data = {
        'callback': '130546474742',
        'login_method': '46',
        'user_account': encrypted_result['username'],
        'user_password': encrypted_result['password'],
        'wlan_user_ip': encrypted_result['ip_address'],
        'wlan_user_ipv6': '',
        'wlan_user_mac': '474747474747474747474747',
        'wlan_ac_ip': '',
        'wlan_ac_name': '',
        'mac_type': '47',
        'authex_enable': '',
        'jsVersion': '435944',
        'web': '47',
        'terminal_type': '46',
        'lang': '0d1f5a1419',
        'enable_r3': '47',
        'encrypt': '1',
        'v': '10327',
        'lang': 'zh'
    }
    print(data)
    try:
        resp = requests.get(url=url, params=data)
        print(resp.url)
        login_res = re.search('"result":(.+?),', resp.text).group(1)
        if login_res == '1':
            return True
        else:
            print(resp.text)
            return False
    except:
        print('登陆解析失败: ', resp.text)
        return False





while True:
    # try:
    #     host_name, aliaslist, ipaddrlist = socket.gethostbyname_ex(socket.gethostname())
    #     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # except:
    #     print("get host name error")
    #     continue
    try:
        # s.connect(('8.8.8.8', 80))
        # ip = s.getsockname()[0]
        ip = get_ip()
        # if ip.startswith('101.7'):
        if True:
            my_ip = ip
            print('Your IP:', my_ip)
        else:
            print('未连接到校园网')
            time.sleep(5)
            continue
    except:        
        print('未连接到校园网')
        time.sleep(5)
        continue

    try:
        resp = requests.get(url=status_url)
        status = json.loads(re.search(r'\((.+)\)', resp.text).group(1))
        if status['result'] == 1:
            print('已登录')
            time.sleep(3)
        else:
            print('未登录')
            if internet_login():
                print('登陆成功')
            else:
                print('登陆失败')
    except:
        pass

    time.sleep(1)




