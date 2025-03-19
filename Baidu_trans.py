# -*- coding: utf-8 -*-
"""
@Time ： 2023/5/6 20:00
@Auth ： NIDO
@File ：Baidu_trans.py
@IDE ：PyCharm
"""

# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5


class Translator:
    # Set your own appid/appkey.
    __APPID = '20230506001668497'
    __APPKEY = '4pWYQw1OKRaZKRfR64XA'

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    __FROM_LANG = 'auto'
    __TO_LANG = 'zh'

    __URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"

    # Generate salt and sign
    @classmethod
    def __make_md5(cls, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    @classmethod
    def translate(cls, query):
        salt = random.randint(32768, 65536)
        sign = cls.__make_md5(cls.__APPID + query + str(salt) + cls.__APPKEY)

        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': cls.__APPID, 'q': query, 'from': cls.__FROM_LANG, 'to': cls.__TO_LANG, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(cls.__URL, params=payload, headers=headers)
        result = r.json()

        resp = json.dumps(result, indent=4, ensure_ascii=False)
        print(resp)
        return json.loads(resp)["trans_result"]


if __name__ == "__main__":
    print(Translator.translate("The architecture of the TPH-YOLOv5. a) CSPDarknet53 backbone with three transformer "
                               "encoder blocks at the end. b) The Neck use the structure like PANet. c) Four TPHs ("
                               "transformer prediction heads) use the feature maps from transformer encoder blocks in "
                               "Neck. In addition, the number of each block is marked with orange numbers on the left "
                               "side of the block."))
