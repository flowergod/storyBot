import requests
from bs4 import BeautifulSoup
import time
import datetime as dt
import csv
import os
from openai import OpenAI


def cls_news(start_time,source, title_list, url_list, time_list):
    web_name = '财联社'
    web_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=utf-8"
    }
    urls = {
#        "热门文章排行榜": "https://www.cls.cn/v2/article/hot/list?app=CailianpressWeb&os=web&sv=7.7.5&sign=bf0f367462d8cd70917ba5eab3853bce", 
        "头条": "https://www.cls.cn/v3/depth/home/assembled/1000?app=CailianpressWeb&os=web&sv=7.7.5&sign=bf0f367462d8cd70917ba5eab3853bce"
    }
    cookies = {
        "HWWAFSESID": "30285a05653ec0b42f",
        "HWWAFSESTIME": "1712558765671",
        "Hm_lvt_fa5455bb5e9f0f260c32a1d45603ba3e": "712558767", 
        "hasTelegraphRemind": "on",
        "hasTelegraphSound": "on",
        "vipNotificationState": "on",
        "hasTelegraphNotification": "off",
        "wafatcltime" : "2854268",
        "wafatcltoken": "ae315cee111b0428a685f9674e507653",
        "Hm_lpvt_fa5455bb5e9f0f260c32a1d45603ba3e": "1712564832", 
        "tfstk": "f8FWPefse3x70XzjxYQ45hhw-QlQOu1wOegLSydyJbhJvHUt07lE4ynQdmETUDoUTU20bPdzaTceObcn9GSN_1zzrXcKBDbHI04Yo2QmIoJ3rzcHoyYV0-zkdvIP4aGLvjhx5VhKJQ3Rls3ZDQ3pw2KAl2mxvX3-JsLx82xpy0hVSFgCF045xrIX1eBvpziX9CTiPYnRsmOpMSg7lcUR-BdLG4M7Tub0mukzpPDgay1Bibz_Hj3QtNpIAAwLajFRD1HmpSExku7eKqwQJ5coEeA3fbZIB7HXJQG0zmhjk5QeImPj4kFSHNRsLjFZBbeVngkENVZLZuTB9lU477D0OGtxx8uiM2NhWpiIpglv_ct1tpTjIBgjbZ_XKp8tpIrpwp69KY3mPx7fl3eneq0jbZ_XKpD-o4gNlZt8K"
    }
    for key, url in urls.items():
        try:
            # 获取页面内容
            res = requests.get(url, headers=web_headers, cookies=cookies)
            res.encoding = res.apparent_encoding
            # 2.用BeautifulSoup提取标题、时间、作者、来源、正文、图片
            soup = BeautifulSoup(res.text, 'html.parser')

            data = res.json()

            # 头条
            if key == '头条':
                # 头条置顶
                for j in data['data']['top_article']:
                    news_time = j['ctime']
                    if news_time >= start_time:
                        source.append('头条置顶')
                        title_list.append(j['title'])
                        url_list.append('https://www.cls.cn/detail/' + str(j['id']))
                        time_list.append(dt.datetime.fromtimestamp(news_time))
                    else:
                        continue            
                # 头条列表
                for j in data['data']['depth_list']:
                    news_time = j['ctime']
                    if news_time >= start_time:
                        source.append('头条列表')
                        title_list.append(j['title'])
                        url_list.append('https://www.cls.cn/detail/' + str(j['id']))
                        time_list.append(dt.datetime.fromtimestamp(news_time))
                    else:
                        continue

        except Exception as e:
            print(e)

def summarize(url):
    client = OpenAI(
        api_key="sk-G1XW4KDMwFgvwZKRSUrvonSyiitbBMOihnv1mEjGNl6dQxvC",
        base_url="https://api.moonshot.cn/v1",
    )
    messageContent = "打开并访问页面：" + url +" ，请为我总结文章的观点和结论，并进行以下分析：1. 文章对哪个行业有影响，2. 影响是正面的还是负面的3. 按1~10评分，影响程度有多大。请以表格的形式输出，包含字段：文章观点，结论，影响行业，影响方向和程度"
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
            {"role": "user", "content": messageContent}
        ],
        temperature=0.3,
        )
    print(messageContent)
    print('\n')
    print(completion.choices[0].message)

if __name__=='__main__':
#    summarize("https://www.cls.cn/detail/1640995")
    current_time = time.time()
    start_time = current_time - 24*60*60
    title_list = []
    url_list = []
    time_list = []
    source = []
    cls_news(start_time,source, title_list, url_list, time_list)

    # 写入csv
    filename = 'cls_news.csv'
    if os.path.exists(filename):
        os.remove(filename)
    cntNews = len(title_list)
    lNews = [["分类, 标题, 地址, 时间"]]
    strNewsUrls = ''

    for i in range(0, 10):
        strNewsUrls = strNewsUrls + url_list[i] + " , "
        row = ', '.join([source[i], title_list[i], url_list[i], time_list[i].strftime("%c")])
        lNews.append([row])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar=' ')
        writer.writerows(lNews)
    
    promptMsg = "打开并访问页面：" + strNewsUrls +" ，请为我总结文章的观点和结论，并进行以下分析：1. 文章对哪个行业有影响，2. 影响是正面的还是负面的3. 按1~10评分，影响程度有多大。请以表格的形式输出，包含字段：文章观点，结论，影响行业，影响方向和程度"

    print(promptMsg + '\n')

    print(dt.datetime.now().strftime("%c") + " Done!")


