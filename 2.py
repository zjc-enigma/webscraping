#!/usr/bin/python
# coding=gb2312

import mechanize
import re
import cookielib
import sys

from bs4 import BeautifulSoup
from random import randint
from time import sleep

pageNum = str(sys.argv[1])

cj = cookielib.LWPCookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.set_debug_http(True)

br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.11) Gecko/20100701 Firefox/3.5.11')]


#html_files = ["1.html", "2.html", "3.html", "4.html"]
#for hfile in html_files:



hfile = "pages/" + str(pageNum) + ".html"
html = open(hfile).read()

soup = BeautifulSoup(html)
hreflist = soup.find_all('a')

out = open('res' + str(pageNum), 'a')


cachefile = "cache/" + str(pageNum) +".cache"
finishedUrl = []
cacheIn = open(cachefile)
for line in cacheIn:
    line = line.strip('\r\n')
    line = line.strip('\n')
    finishedUrl.append(line)
cacheIn.close()


cacheOut = open(cachefile, 'a')

try:
    for string in hreflist:
        Encoding = True
        detailurl = string[r'href']
        s = re.search(r'CPMX', detailurl)
        if not s:
            continue
        if detailurl in finishedUrl:
            continue

        print "fetching html : " + str(detailurl)

        content = br.open(detailurl, timeout=30.0).read()

        print "url opened"
#        print "html :" + content
        sleep(1)

        try:
            detailsoup = BeautifulSoup(content)

        except socket.timeout:

            print "reload url"
            content = br.reload().read()
            detailsoup = BeautifulSoup(content)

        print "html parsing by soup"
        tablelist = detailsoup.find_all(r'table')
        table = tablelist[0]


        trlist = table.find_all(r'tr')
        print "find tr total number :" + str(len(trlist))
        if(len(trlist) < 3):
#            content = re.sub("</html>","",content,flags=re.S|re.IGNORECASE)+"</html>"
            detailsoup = BeautifulSoup(content, "xml", from_encoding="gb18030")
            encoding  = False
            trlist = detailsoup.find_all(r'tr')
            # for f in trlist:
            #     print f
            #     print "----------------------------------"
            # exit(5)
#            trlist.append(tl[0].find_all('tr'))
#            trlist.append(tl[1].find_all('tr'))
            #            for table in detailsoup.find_all('table'):
#            trlist.append([0].find_all('tr'))
#            trlist.append(detailsoup.find_all('table')[1].find_all('tr'))

            print "refind tr total number :" + str(len(trlist))

        productRow = 0
        companyRow = 1
        percentRow = 2
        dateRow = 3
        corpRow =  4

        # ----------- product ---------------
        print "parsing product info"
        productTd = trlist[productRow].find_all(r'td')
        licenseNum = productTd[1].get_text()
        productName = productTd[3].get_text()

        # ----------- company ---------------
        print "parsing company info"
        companyTd = trlist[companyRow].find_all(r'td')
        companyName = companyTd[1].get_text()
        toxicity = companyTd[3].get_text()

        # ----------- percent ---------------
        print "parsing percent info"
        percentTd = trlist[percentRow].find_all(r'td')
        percent = percentTd[1].get_text()

        # ----------- date ---------------
        print "parsing date info"
        dateTd = trlist[dateRow].find_all(r'td')
        date = dateTd[1].get_text()
        form = dateTd[3].get_text()

        # ----------- corp ---------------
        print "parsing corp info"
        corpTd = trlist[corpRow].find_all(r'td')
        del corpTd[0:5]
        corpNameList = []
        corpDiseaseList = []
        corpQuantityList = []
        corpUsageList = []
        res = r""
        corpName = r"-"
        diseaseName = r"-"
        quantity = r"-"
        usage = r"-"

        while(len(corpTd)):
            corpNameList.append(corpTd.pop(0).get_text())
            corpDiseaseList.append(corpTd.pop(0).get_text())
            corpQuantityList.append(corpTd.pop(0).get_text())
            corpUsageList.append(corpTd.pop(0).get_text())

            corpName = r'/'.join(corpNameList)
            diseaseName = r'/'.join(corpDiseaseList)
            quantity = r'/'.join(corpQuantityList)
            usage = r'/'.join(corpUsageList)

        print "generating result"
        res = licenseNum + '\t' + productName + '\t' + companyName + '\t' + toxicity + '\t' + percent + '\t' + date.replace(r'-', '\t') + '\t' + form + '\t' + corpName + '\t' + diseaseName + '\t' + quantity + '\t' + usage + '\n'

        print "writing into result file"

        out.write(res.encode('gb18030'))
        cacheOut.write(detailurl+'\n')
        print "result writing finished"
except Exception, e:
    print e

finally:
    print "finally"
    cacheOut.close()
    out.close()
    exit(2)

print "finished web scraping"
exit(0)
