import requests
import json
from lxml import etree
from models import UserInfo
from multiprocessing import Queue
# 线程池
from concurrent.futures import ThreadPoolExecutor

URL = "https://www.douguo.com"
start_url = "https://www.douguo.com/fenlei"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36"
}

queue = Queue()


def handle_index():
    # 请求首页数据, 获取热门食材 URL
    text = requests.get(start_url, headers=headers).text
    html = etree.HTML(text)
    remeng = html.xpath('//div[@id="content"]/div[2]/div[1]')[0]
    title = remeng.xpath('./h2/text()')[0] if remeng.xpath('./h2/text()') else ""
    li_list = remeng.xpath('./ul[@class="sortlist clearfix"]/li')
    for li in li_list:
        name = li.xpath('./a/text()')[0]
        sub_url = li.xpath('./a/@href')[0]
        url = URL + sub_url
        parse_list(url)


def parse_list(url):
    # 解析单个分类的所有数据
    text = requests.get(url, headers=headers).text
    html = etree.HTML(text)
    li_list = html.xpath('//div[@class="mt25"]/ul/li')
    for li in li_list:
        url = li.xpath('./div[@class="cook-info"]/a/@href')[0]
        print("<<< ", url)
        queue.put(URL + url)

    # 下一页
    # next_lst = html.xpath('//a[@class="anext"]/@href')
    # if next_lst:
    #     next_url = next_lst[0]
    #     print(next_url, " >>>")
    #     parse_list(next_url)


def parse_detail(url):
    # 解析详细数据入库
    details = {}
    text = requests.get(url, headers=headers).text
    html = etree.HTML(text)
    img_url = html.xpath('//div[@id="banner"]/a/img/@src')[0]
    title = html.xpath('//div[@class="rinfo relative"]/h1/text()')[0]
    read_num = html.xpath('//div[@class="vcnum relative"]/span[1]/text()')[0]
    col = html.xpath('//div[@class="vcnum relative"]/span[@class="collectnum"]/text()')[0]
    aut_img = html.xpath('//a[@class="author-img left"]/img/@src')[0]
    aut_name = URL + html.xpath('//div[@class="author-info left"]/a/@href')[0]
    aut_desc = html.xpath('//div[@class="rinfo relative"]/p[@class="intro"]/text()')[0].strip()

    # 用料
    materials = {}
    tr_list = html.xpath('//div[@class="metarial"]/table/tbody/tr/td')
    for td in td_list:
        name = td.xpath('./span[1]/a/text()')[0]
        value = td.xpath('./span[2]/text()')[0]
        materials[name] = value
    details["materials"] = materials

    # 做法
    step = []
    div_list = html.xpath('//div[@class="step"]/div')
    for div in div_list:
        img_url = div.xpath('./a/img/@src')[0]
        info = div.xpath('./div[@class="stepinfo"]/text()')[0]
        step.append([img_url, info])
    details['step'] = step
    details['title'] = title
    details['read_num'] = read_num
    details['col'] = col
    details['aut_img'] = aut_img
    details['aut_name'] = aut_name
    details['aut_desc'] = aut_desc
    try:
        print(details)
        uid = UserInfo().save(**details)
    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    handle_index()
    pool = ThreadPoolExecutor(max_workers=20)
    print(queue.qsize())
    while queue.qsize() > 0:
        pool.submit(parse_detail, queue.get())

