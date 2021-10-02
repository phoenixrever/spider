# coding: utf-8

from lxml import etree
import requests

if __name__ == '__main__':
    url = 'https://javdb30.com/tags?c10=1&c5=123&page=1'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }
    params = {
        'c10': 1,
        'c5': 123,
        'page': 1
    }
    text = requests.get(url, params=params, headers=headers).text
    # print(text)

    # Returns the root node (html)
    tree = etree.HTML(text)
    print(tree)

    # / 从根节点表示一个层级
    # // 表示多个层级  //img  获取下面的子元素的所有img 元素
    # []表示多个 索引从 1开始
    # /@src 获取属性
    img = tree.xpath('/html/body/section/div/div[7]/div/div[2]/a/div[1]/img/@src')[0]
    # /text() 获取直系文本内容(不能获取子标签)  //text()获取所有下面的子标签文本
    tag = tree.xpath('//*[@id="videos"]/div/div[21]//text()')
    # //* == //div 直接到后面的元素层级
    divTags = tree.xpath('//*[@id="videos"]//img/@src')

    # for 循环中 可以继续使用下xpath  ./表示当前div
    divs = tree.xpath('//*[@id="videos"]/div/div')
    for div in divs:
        subtrees= div.xpath('./a/div[5]/span/text()')
        print(subtrees)

    print(img)
    print(tag)
    print(divTags)
