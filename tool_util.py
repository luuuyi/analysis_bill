#!/usr/bin/python
#coding:utf-8

from bs4 import BeautifulSoup
'''import sys
reload(sys)
sys.setdefaultencoding('utf-8')'''

#解析账单html文件，返回信息dict对象，key为电话号码，value为一个list对象，第一位是主叫时间，第二位是被叫时间
def parseHTML(filename):
	soup = BeautifulSoup(open(filename),'lxml')

	soup1 = BeautifulSoup("<td>主叫&nbsp;</td>",'lxml')
	tmp = soup1.find_all('td')
	flag1 = str(unicode(tmp[0].string))
	soup2 = BeautifulSoup('<td>被叫&nbsp;</td>','lxml')
	tmp = soup2.find_all('td')
	flag2 = str(unicode(tmp[0].string))

	tr_tags = soup.find_all('tr',class_='content2')
	infos = dict()
	for tr_tag in tr_tags:
		info_list = list()
		td_tags = tr_tag.find_all('td',class_='talbecontent1')
		if len(td_tags) <= 3:
			continue
		for td_tag in td_tags:
			info_list.append(unicode(td_tag.string))

		tele = str(info_list[5])
		call_type = str(info_list[4])
		call_time = info_list[2]
		times = spliteTime(call_time)

		if tele in infos.keys():
			if call_type == flag1:
				infos[tele][0] += times
			else:
				infos[tele][1] += times
		else:
			time_list = list([0,0])
			infos[tele] = time_list
			if str(call_type) == flag1:
				infos[tele][0] = times
			else:
				infos[tele][1] = times
	return infos

#将字符类型的通话时间转换为秒为单位，返回int对象
def spliteTime(time_str):
	hour_list = time_str.split('小时')
	hour = 0
	minute_string = ''
	if len(hour_list) == 1:
		minute_string = hour_list[0]
	else:
		minute_string = hour_list[1]
		hour = int(hour_list[0])
	#print hour

	minute_list = minute_string.split('分')
	minute = 0
	sec_string = ''
	if len(minute_list) == 1:
		sec_string = minute_list[0]
	else:
		sec_string = minute_list[1]
		minute = int(minute_list[0])
	#print minute

	sec_list = sec_string.split('秒')
	sec = int(sec_list[0])
	#print sec
	return hour*3600+minute*60+sec

#将int对象的数据转换为string对象，返回string对象
def cmnctTime(num_int):
	sec = num_int % 60
	minute_int = num_int / 60
	if minute_int == 0:
		return str(sec)+'秒'
	minute = minute_int % 60
	hour_int = minute_int / 60
	if hour_int == 0:
		return str(minute)+'分'+str(sec)+'秒'
	hour = hour_int % 24
	day_int = hour_int / 24
	if day_int == 0:
		return str(hour)+'小时'+str(minute)+'分'+str(sec)+'秒'
	day = day_int
	return str(day)+'天'+str(hour)+'小时'+str(minute)+'分'+str(sec)+'秒'

#将dict对象排序，排序规则为通话时间的升序
def sortInfos(infos):
	tmp = sorted(infos.iteritems(),key = lambda d:d[1][0]+d[1][1], reverse = True)
	return tmp

#返回通话时间最多的前三个号码
def getTop3Caller(infos):
	tmp = list([x for x in infos[0:3]])
	return tmp

if __name__ == '__main__':
	ret = cmnctTime(01)
	print ret

	infos = dict({'a':[10,10], 'b':[10,0], 'c':[10,20], 'd':[30,5]})
	sort_infos = sortInfos(infos)
	print sort_infos

	output_infos = getTop3Caller(sort_infos)
	print output_infos

	for x in infos.iteritems():
		print x

	infos = parseHTML("152xxxx3279.html")
	print infos
