# -*- coding: utf-8 -*-
from typing import List

import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import pandas as pd
from time import sleep


# 数据结构定义
# 使用 @dataclass 和 @dataclass_json 装饰器，
# 使得该类可以方便地从 JSON 数据中解析，并支持 JSON 序列化。
@dataclass_json
@dataclass
class Comment: # 评论结构
    accountId: str
    accountName: str
    approveCounts: str
    cipherVersion: str
    commentAppId: str
    commentId: str
    commentInfo: str
    commentType: str
    id: str
    isAmazing: int
    isModified: int
    levelUrl: str
    logonId: str
    nickName: str
    phone: str
    operTime: str
    photoUrl: str
    rating: str
    replyComment: str
    replyCounts: int
    serviceType: str
    stars: str
    title: str
    versionName: str


@dataclass_json
@dataclass
class CommentPage: # 一页评论数据
    totalPages: int
    count: int
    devWords: List[str]
    list: List[Comment]
    encoding: str = 'utf-8'


# 爬虫逻辑
class HuaweiSpider:

    @staticmethod
    def commentPage(page) -> CommentPage:
        """
        评论分页
        :param page: 页码，从1开始
        :return:
        """
        url = "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.user.commenList3&serviceType=20&reqPageNum=%s&maxResults=25&appid=C110782717&version=10.0.0&zone=&locale=zh" % page
        # url = "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.user.commenList3&serviceType=20&reqPageNum=%s&maxResults=25&appid=C109089785&version=10.0.0&zone=&locale=zh" % page
        # url = "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.user.commenList3&serviceType=20&reqPageNum=%s&maxResults=25&appid=C111568535&version=10.0.0&zone=&locale=zh" % page
        print(url)
        # 发送请求，设置请求头模拟浏览器行为，避免被服务器拒绝
        r = requests.get(url, headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,ko;q=0.8,und;q=0.7,en;q=0.6,zh-TW;q=0.5,ja;q=0.4',
            'Connection': 'keep-alive',
            'Host': 'web-drcn.hispace.dbankcloud.cn',
            'Referer': 'https://appgallery.huawei.com/',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        }, verify=False)
        r.encoding = r.apparent_encoding
        if r and r.status_code == 200:
            print(r.content)
            # 解析json数据
            content = CommentPage.from_json(r.content)
            content.encoding = r.encoding
            return content


# 数据抓取与存储
if __name__ == '__main__':

    page = 1

    columns = ['用户名', '评论', '评分', '评论时间', '版本号', '设备']
    data = []

    # while True:
    #     commentPage = HuaweiSpider().commentPage(page)

    #     if len(commentPage.list) > 0:
    #         print(commentPage)
    #         for row in commentPage.list:
    #             data.append([row.nickName, row.commentInfo, row.stars, row.operTime, row.versionName, row.phone])
    #         page += 1

    #         sleep(2)
    #     else:
    #         break
    total_pages = 1  # 初始化为 1，确保至少执行一次循环

    while page <= total_pages:
        comment_page = HuaweiSpider().commentPage(page)
        if comment_page is not None:
            total_pages = comment_page.totalPages  # 更新总页数   // 总共是有40页，每页是25条数据   但是每次爬到第5页就变0了
            print(f"当前页码: {page}, 总页数: {total_pages}, 本页数据量: {len(comment_page.list)}")  # 调试信息
            for row in comment_page.list:
                data.append([row.nickName, row.commentInfo, row.stars, row.operTime, row.versionName, row.phone])
            page += 1
            sleep(2)  # 增加请求间隔，避免被限制
        else:
            break

    df = pd.DataFrame(data, columns=columns)
    df.to_excel('D:\Code\python-workspace\TestDemo\yuanbao.xlsx', index=False)
    """
    yuanbao----sleep(2)
    yuanbao1----sleep(20)
    yuanbao2----sleep(100)
    """
    # df.to_excel('D:\\Code\\python-workspace\\doubao.xlsx', index=False)
    # df.to_excel('D:\\Code\\python-workspace\\jimengAI.xlsx', index=False)


    
