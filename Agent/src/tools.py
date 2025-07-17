from datetime import datetime
import requests
import hashlib
import random
import time


def get_current_datetime() -> str:
    """
    获取当前日期和时间。
    :return: 当前日期和时间的字符串表示。
    """
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime

def add(a: float, b: float):
    """
    计算两个浮点数的和。
    :param a: 第一个浮点数。
    :param b: 第二个浮点数。
    :return: 两个浮点数的和。
    """
    return str(a + b)

def mul(a: float, b: float):
    """
    计算两个浮点数的积。
    :param a: 第一个浮点数。
    :param b: 第二个浮点数。
    :return: 两个浮点数的积。
    """
    return str(a * b)

def compare(a: float, b: float):
    """
    比较两个浮点数的大小。
    :param a: 第一个浮点数。
    :param b: 第二个浮点数。
    :return: 比较结果的字符串表示。
    """
    if a > b:
        return f'{a} is greater than {b}'
    elif a < b:
        return f'{b} is greater than {a}'
    else:
        return f'{a} is equal to {b}'

def count_letter_in_string(a: str, b: str):
    """
    统计字符串中某个字母的出现次数。
    :param a: 要搜索的字符串。
    :param b: 要统计的字母。
    :return: 字母在字符串中出现的次数。
    """
    string = a.lower()
    letter = b.lower()
    
    count = string.count(letter)
    return(f"The letter '{letter}' appears {count} times in the string.")

def translate(text: str) -> str:
    """
    自动判断输入文本是中文还是英文，并调用百度翻译API实现中英互译。
    你需要去百度翻译开放平台注册账号，获取 appid 和密钥（API key），并填写到下方变量中。
    """
    # 1. 你的百度翻译API信息
    appid = "20250717002408443"  # TODO: 填写你的appid
    secretKey = "mtOUVbligDBfVUehlOQx"  # TODO: 填写你的密钥

    # 2. 判断语言
    def is_chinese(s):
        for ch in s:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
    from_lang = 'zh' if is_chinese(text) else 'en'
    to_lang = 'en' if from_lang == 'zh' else 'zh'

    # 3. 构造请求参数
    salt = str(random.randint(32768, 65536))
    sign = appid + text + salt + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    params = {
        'q': text,
        'from': from_lang,
        'to': to_lang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }
    # 4. 发送请求
    try:
        response = requests.get(url, params=params, timeout=5)
        result = response.json()
        if 'trans_result' in result:
            return result['trans_result'][0]['dst']
        else:
            return f"翻译失败: {result.get('error_msg', '未知错误')}"
    except Exception as e:
        return f"翻译接口调用异常: {e}"
