#!/usr/bin/python
#encoding:utf-8

import tool_util
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def start(bill_file):
	infos = tool_util.parseHTML(bill_file)        
	sort_infos = tool_util.sortInfos(infos)
	output_infos = tool_util.getTop3Caller(sort_infos)

	print '------------------------------'
	print '电话号码         主叫                 被叫'
	for x in xrange(0,3):
		active_time = tool_util.cmnctTime(output_infos[x][1][0])
		passive_time = tool_util.cmnctTime(output_infos[x][1][1])
		caller = output_infos[x][0]
		print caller+'    '+active_time+'      '+passive_time

if __name__ == '__main__':
	bill_file = '152xxxx3279.html'
	start(bill_file)
