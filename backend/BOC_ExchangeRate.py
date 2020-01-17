import requests
import re


def get_html_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('爬取失败')
        return None


def parse_page(html):
    # print(html)
    # pattern = re.compile('<li.*?p-price">.*?<i>(.*?)</i>.*?p-name.*?<em>(.*?)</em>.*?</li>', re.S)
    pattern = re.compile(
        '<td>加拿大元</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td class="pjrq">(.*?)</td>.*?<td>(.*?)</td>',
        re.S)
    items = re.findall(pattern, html)
    # print(len(items))  # 结果应该是1的，如果不是1就是正则表达式出问题了
    item = items[0]
    # print(item)
    #  现汇买入    现钞买入  现汇卖出   现钞卖出   中行折算   发布日期                发布时间
    # ('525.08', '508.5', '528.95', '530.76', '528.17', '2020.01.14 13:49:34', '13:49:34')
    return {
        'bank_name': '中国银行',
        'price': item[2],
        'update_time': item[5],
    }


def start_spider():
    html_page = get_html_text("https://www.boc.cn/sourcedb/whpj/")
    china_bank_dictionary = parse_page(html_page)
    mail_content = china_bank_dictionary['bank_name'] + ' ' + china_bank_dictionary['price'] + ' ' + \
                   china_bank_dictionary['update_time']
    return mail_content