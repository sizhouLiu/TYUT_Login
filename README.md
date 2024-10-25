# TYUT_Loign

----

本项目是TYUT校园网自动登录脚本 可用于服务器以及日常使用

## 依赖

本脚本依赖Requests库

在命令行输入

```shell
pip install requests
```



## 使用

更换代码中的

```python
user_id = 'your user_name'
user_password = 'your password'
```

user_id和user_password为你的校园网账号ID 和密码

运行脚本 即可自动登录 校园网

如果没有自动登录校园网 请关闭诸如VPN 加速器等 网络代理工具 检查网络设置



# 校园网接口解析

### 内网ip获取接口

https://drcom.tyut.edu.cn/drcom/chkstatus?callback=dr1001&jsVersion=4.X&v=8249&lang=zh

### 请求方式：GET 

参数 ：无

返回

```json
{
    "result": 1,
    "time": 1330,
    "flow": 18542900,
    "fsele": 1,
    "fee": 0,
    "m46": 0,
    "v46ip": "101.7.141.200",
    "myv6ip": "",
    "oltime": 4294967295,
    "olflow": 4294967295,
    "lip": "101.7.141.200",
    "stime": "2024-10-25 19:15:51",
    "etime": "2024-10-25 19:17:14",
    "uid": "liusizhou5141",
    "v6af": 0,
    "v6df": 0,
    "v46m": 4,
    "v4ip": "101.7.141.200" 内网IPv4 ip,
    "v6ip": "2001:250:c01:9000::3:2ac1" IPv6 IP,
    "AC": "你的用户名",
    "ss5": "101.7.141.200",
    "ss6": "219.226.127.250",
    "vid": 0,
    "ss1": "0010f387448a",
    "ss4": "000000000000",
    "cvid": 0,
    "pvid": 0,
    "hotel": 0,
    "aolno": 5470,
    "eport": -1,
    "eclass": 1,
    "zxopt": 1,
    "NID": "N/A",
    "olno": 0,
    "udate": "",
    "olmac": "a4a93025b0fe",
    "ollm": 10,
    "olm1": "00000014",
    "olm2": "0000",
    "olm3": 0,
    "olmm": 1,
    "olm5": 0,
    "gid": 1,
    "ispid": 0,
    "opip": "0.0.0.0",
    "actM": 1,
    "actt": 7651,
    "actdf": 586108,
    "actuf": 11561616,
    "act6df": 0,
    "act6uf": 0,
    "allfm": 1,
    "d1": 0,
    "u1": 0,
    "d2": 0,
    "u2": 0,
    "o1": 0,
    "nd1": 2344433,
    "nu1": 46246464,
    "nd2": 0,
    "nu2": 0,
    "no1": 0
}
```

这里我们只要IPv4 ip

### 登录接口

### https://drcom.tyut.edu.cn:802/eportal/portal/login

### 请求方式： GET

### 参数

大部分参数的功能都没有被使用 懒得看他们的烂代码了
这里用固定的 

```python
'callback': '130546474742',
'login_method': '46',
'user_account': 加密过的username,
'user_password': 加密过的userpassword,
'wlan_user_ip': 校园网分配的内网ip 由获取接口获取,
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
```



## 加密函数

## get_key(ip)

**功能**: 根据给定的 IP 地址生成一个加密密钥。

**参数**:

- `ip`: 字符串类型，表示一个 IP 地址。

**实现过程**:

- 初始化一个整数 `ret` 为 0，用于存储结果。
- 遍历 IP 地址中的每个字符，使用 `ord(char)` 获取字符的 ASCII 值。
- 使用异或操作 (`^=`) 将每个字符的 ASCII 值依次与 `ret` 进行异或。这种组合方式使得相同的字符输入会生成相同的密钥，而不同的字符组合会导致不同的密钥。

**返回值**:

- 返回最终的 `ret` 值，作为加密密钥。

## 2. enc_pwd(password, key)

**功能**: 对密码进行异或加密，使用先前生成的密钥。

**参数**:

- `password`: 字符串类型，表示待加密的密码。
- `key`: 整数类型，由 `get_key` 函数生成的加密密钥。

**实现过程**:

- 首先检查密码是否为空或长度是否超过 512 个字符。如果是，则返回一个空字符串。
- 初始化一个字符串 `encrypted` 用于存储加密后的结果。
- 遍历密码中的每个字符，使用 `ord(char)` 获取它的 ASCII 值。
- 将字符的 ASCII 值与 `key` 进行异或，生成加密字符的值。
- 将该值格式化为两个字符的十六进制字符串（使用 `format(ch, '02x')`）并拼接到 `encrypted` 字符串中。

**返回值**:

- 返回加密后的十六进制字符串。

