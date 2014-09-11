#!/usr/bin/python


import urllib2
from bs4 import BeautifulSoup
import re
import sys

import sqlite3
cx = sqlite3.connect("/Users/thunisoft/Desktop/hello.db")
cu = cx.cursor()
cu.execute("drop table cases")
cu.execute("create table cases (id integer primary key AutoIncrement,c_name varchar(100),c_desc varchar(10240),\
				c_href varchar(100) ,c_thumb_url varchar(100) ,c_video_url varchar(200))")

#conn = MySQLdb.connect(host='114.255.140.110', user='root', passwd='resroot', db='db_zgfyw', port=3306, charset='utf8')
#cur = conn.cursor()

reload(sys)
sys.setdefaultencoding( "utf-8" )
baseurl = 'http://ts.chinacourt.org'
url = 'http://ts.chinacourt.org/huigu.html?page=1'

req = urllib2.Request(url)
con = urllib2.urlopen(req)

print url
doc = con.read()
soup = BeautifulSoup(doc)

pages = soup.html.body.findAll('li', {'class': 'page'});


for page in pages:
	pageurl = page.find('a')['href'];
	print pageurl

	req2 = urllib2.Request(baseurl + pageurl)
	con2 = urllib2.urlopen(req2)
	doc2 = con2.read()
	soup2 = BeautifulSoup(doc2)

	names = soup2.html.body.findAll('div', {'class' : 'video_hg_img'})

	for x in names:
		ahref = x.find('a')
		href= ahref['href']
		m3u8url = ""


		url_inner = baseurl + href;
		req_inner = urllib2.Request(url_inner)
		con_inner = urllib2.urlopen(req_inner)
		doc_inner = con_inner.read()
		soup_inner = BeautifulSoup(doc_inner)

		desc = soup_inner.find('div', {'class' : 'video_info'})
		desc = desc.get_text()

		iframe = soup_inner.find('iframe')
		videourl = iframe['src']
		print videourl

		req_video = urllib2.Request(videourl)
		con_video = urllib2.urlopen(req_video)
		doc_video = con_video.read()
		soup_video = BeautifulSoup(doc_video)
		p = re.compile(r'http://\S+.m3u8')
		ary = p.findall(soup_video.get_text())
		for m3u8 in ary:
			if m3u8 != "":
				m3u8url = m3u8
				print m3u8url

		#print desc


		alt = ahref.contents[0]['alt']
		src = ahref.contents[0]['src']
		cu.execute("insert into cases (c_name,c_href,c_thumb_url,c_desc,c_video_url) values ('%s','%s','%s','%s','%s')" % 
			(alt,href,src,desc,m3u8url))
		cx.commit()

	con2.close()

cu.close()
cx.close()
con.close()
