# 爬取百度翻译
import re
import execjs
import requests
import json
import time

# 2021/6/21编写
# 可能后续百度反爬策略更新

print("正在休眠")


# 初始化请求头
def init():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36",
        # cookie可以用自己的，打开百度翻译F12查看
        "Cookie": "BIDUPSID=9FA9F35CF7C248ACEFB06859AF46B393; PSTM=1617936255; BAIDUID=9FA9F35CF7C248AC70347FF51DD64FD6:FG=1; __yjs_duid=1_07f5c95dc173d21ddf1a35c5368173e01617936262582; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; HISTORY_SWITCH=1; SOUND_PREFER_SWITCH=1; BDUSS=JUeEQxQn52NUZ0VlZKRnRDQ0dFZzBRbUt3dERjVy1sUTFMd1RzUkZ3dGdxWmhnSVFBQUFBJCQAAAAAAAAAAAEAAAD2L0g4wO3Wx7XjNTI1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAccWBgHHFgej; BDUSS_BFESS=JUeEQxQn52NUZ0VlZKRnRDQ0dFZzBRbUt3dERjVy1sUTFMd1RzUkZ3dGdxWmhnSVFBQUFBJCQAAAAAAAAAAAEAAAD2L0g4wO3Wx7XjNTI1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAccWBgHHFgej; MCITY=-180%3A; BDSFRCVID=HPKsJeCCxG3tz3veRh_YXtsoVK084lzbh8Ef3J; H_BDCLCKID_SF=tRk8oI0aJDvjDb7GbKTMbtCSbfTJetJyaROhQJ7E-b7hqRONHtJb24tWqGKHJ6DDtJkXoD_htDDKMTu4D6LKDjjWJloJ2lRL5Cn0LRCBK-Jf245mhqnEb5us5p62-KCHtJCHoC_5HD_KhD_lD6t_D6jLDGLHt5n7Lg3eaJ5n0-nnhPbuDnjq04kmWJ7Jb-RpWb4O_nRLKJPWsJLRy66jK4JKja_HJ6QP; BDSFRCVID_BFESS=HPKsJeCCxG3tz3veRh_YXtsoVK084lzbh8Ef3J; H_BDCLCKID_SF_BFESS=tRk8oI0aJDvjDb7GbKTMbtCSbfTJetJyaROhQJ7E-b7hqRONHtJb24tWqGKHJ6DDtJkXoD_htDDKMTu4D6LKDjjWJloJ2lRL5Cn0LRCBK-Jf245mhqnEb5us5p62-KCHtJCHoC_5HD_KhD_lD6t_D6jLDGLHt5n7Lg3eaJ5n0-nnhPbuDnjq04kmWJ7Jb-RpWb4O_nRLKJPWsJLRy66jK4JKja_HJ6QP; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1623470109; H_PS_PSSID=34099_31254_34004_33855_33607_34107_34134_26350; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=9FA9F35CF7C248AC70347FF51DD64FD6:FG=1; delPer=0; PSINO=5; BA_HECTOR=8l8h8k84048585agh81gd03mj0r; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1624248232; __yjs_st=2_YmI0NDEyNmJmOGY0M2EyNmE0ZjcwMjYxNTA3NjEwNzU4ODNjMjYyNTVhMmRhMGYxYzcxMmQ3YjJhNmNkYjljMTI4NWVjMTRmYjEwYWEwNGYzZjA5ZjQyNDIxOGVkYzUwNzMzZWQ1ZTI3NmVhNzMwNGJiOGRmZTdiODg4MTExMzVhMzM1M2M3MzQ3M2I3MzIyN2ZlZDBiOWExODY2MWU5MWE4NzBlNDdiNGE0Y2I0MjMzNDQzYzFkNzdkMTg4NzAxZThlMmM2ZjlkOTQ5NWQwZTRjZWYzZTExMDA2NzQ3ZDQzMDVjNDZlYzQ3NjQxZjJiMTRkNzI5YTczMWM0MGFiYl83XzgwNTJlNTlm; ab_sr=1.0.1_MzlhYTdmYjJjNzAyYzg4NjExMGNmZDE3NzEyZjEwZjAzNDEyMjBmZmExZjIwY2QzMzRjY2NiMzJkMTY4MWE5Mzg0ZDA0MmQ3M2ZiZjRlOGE3NWJjZDc3Zjc0M2UxNTNjNTQ2Y2ViMGM5NDI4ZmM0MjVmY2U5MzJjMGE4ZTU1ZWFjZGY5M2E4YTNjNDMzZDBiNjcxYmJkMTEyMjVmYWU1OGFkODk5MTA0MTgxZDQwMjRiY2NjOWZiMTUzZDY3OThi"
    }
    return headers


def getToken():
    # 获得token
    token_url = 'https://fanyi.baidu.com'
    html = requests.get(token_url, headers=headers).text
    token = re.findall("<script>.*? token:(.*?)systime:.*?", html, re.S)
    token = token[0].strip().strip("'").strip("',") if token else ""
    # print(token)
    return token


def geySign(word):
    #python运行js获取sign
    with open('tmp.js', 'r', encoding='utf-8') as f:
        jstext = f.read()
    ctx = execjs.compile(jstext)
    sign = ctx.call('e', word)
    # print(sign)
    return sign


if __name__ == '__main__':
    # 翻译url
    post_url = 'https://fanyi.baidu.com/v2transapi'
    headers = init()
    # 获得token
    token = getToken()

    with open('word.json') as words:
        word_list = json.load(words)
    count = 0
    all_result = []
    id = 1
    lastword = ""
    try:
        for word in word_list:
            count += 1
            if (count == 50):
                print("正在休眠")
                time.sleep(5)
                count = 0
            print(id)
            print(word)
            # words = input("请输入要翻译的内容")
            # 获得sign
            sign = geySign(word)
            data = {
                "from": "zh",
                "to": "en",
                "query": word,
                "transtype": "enter",
                "simple_means_flag": 3,
                "sign": sign,
                "token": token,
                "domain": "common",
            }
            # 发送请求
            while True:
                try:
                    # 一下except都是用来捕获当requests请求出现异常时，
                    # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
                    response = requests.post(url=post_url, data=data, headers=headers, timeout=20)
                    break
                except requests.exceptions.ConnectionError:
                    print('ConnectionError -- please wait 10 seconds')
                    time.sleep(10)
                except requests.exceptions.ChunkedEncodingError:
                    print('ChunkedEncodingError -- please wait 10 seconds')
                    time.sleep(10)
                except:
                    print('Unfortunitely -- An Unknow Error Happened, Please wait 10 seconds')
                    time.sleep(10)
            # 具体所需的功能可以自己print出来看
            dic_obj = response.json()

            # 将结果写入result
            try:
                # 因个人需求避免数据库存取太多means,只取前三个，如果需要所有单词对应的意思，可以去掉该段代码
                means = dic_obj["dict_result"]["simple_means"]["symbols"][0]['parts'][0]['means']
                if len(means) > 3:
                    means = means[:3]
                # print("means = ")
                # print(means)

                result = {
                    'id': id,
                    'word': word,
                    # 音标
                    'symbols': dic_obj["dict_result"]["simple_means"]["symbols"][0]['ph_en'],
                    # 词性
                    'part':
                        dic_obj["dict_result"]["simple_means"]["symbols"][0]['parts'][0]['part'],
                    # 意思
                    'means': means,
                    # 例句
                    "liji":{
                        "ex":dic_obj["dict_result"]["collins"]["entry"][0]["value"][0]["mean_type"][0]["example"][0]["ex"],
                        "tran":dic_obj["dict_result"]["collins"]["entry"][0]["value"][0]["mean_type"][0]["example"][0]["tran"]
                    }
                }
                id += 1

                # print(result)
                all_result.append(result)
                lastword = word
            except:
                print(word + '出现异常，可能没有例句等等')
                continue
    finally:
        # print(all_result)
        fp = open('./word_translated.json', 'w', encoding='utf-8')
        fp.write(str(all_result))
        print(lastword)
        print('over!!')
