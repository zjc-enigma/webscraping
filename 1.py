#!/usr/bin/python
# coding=utf-8

import mechanize
from bs4 import BeautifulSoup

company = '江苏龙灯化学有限公司'
company = company.decode('utf8')
company = company.encode('gb2312')

url = 'http://www.chinapesticide.gov.cn/service/aspx/B2.aspx'
ref = 'http://www.chinapesticide.gov.cn/service/aspx/'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11')]##模拟浏览器头



response = br.open(url)

#for f in br.forms():
#    print f

br.select_form(nr=0)

br.form['Text1'] = company
# br.form['btnQuery'] = action  //readonly
br.submit()
# print br.response().read()

html1 = br.response().read()
soup = BeautifulSoup(html1)
hreflist = soup.find_all('a')

for href in hreflist:
    detailurl = ref + href
    detailhtml = br.open(detailurl)
    detailsoup = BeautifulSoup(detailhtml)
    detailres = detailsoup.get_text()
