# -*- coding: utf-8 -*-

import os
import json

def par_lrc(filename, head = True):
	"""
		从文件解析得到歌词列表:
		[[int timestamp, string lrc], [...], [...], ...]
	"""
	#转换为UTF-8编码
	os.system("enca -L zh_CN -x UTF-8 "+filename)
	f = open(filename, "r")
	data = f.read()
	j = json.loads(data)
	if j.has_key("lyric") :
		return par_lrcs(j["lyric"], head)
	return [[1000000000, ""], [1000000000, ""]]

def par_lrcs(stri, head = True):
	"""
		解析得到歌词列表:
		
		[[int timestamp, string lrc], [...], [...], ...]
		
	"""
	def getti(st):
		"""
			转换诸如 00:01.98 为时间戳
			返回列表(bool succ, int answer)
		"""
		try:
			s1 = set(st)
			if (s1 <= set("0123456789.:")) and (s1 >= set(".:")):
				s = st.split(":")
				s[1] = s[1].split(".")
				s[0] = int(s[0])
				s[1][0] = int(s[1][0])
				s[1][1] = int(s[1][1])
				return True, s[0] * 60000 + s[1][0] * 1000 + s[1][1]
			else:
				return False, 0
		except:
			return False, 0
	stri = stri.replace("\r", "")
	stlist = stri.split("\n")
	
	lrclist = []
	
	#对标签行分割 非标签行舍去
	for i in range(0, len(stlist), 1):
		if (len(stlist[i]) > 0) and (stlist[i][0] == "["):
			lrclist.append(stlist[i].replace("[","").split("]"))
	
	
	#解析时间戳
	for i in lrclist:
		for j in range(0, len(i) - 1, 1):
			ls = getti(i[j])
			if ls[0]:
				i[j] = ls[1]
	
	'''
		[al:这首歌所在的唱片集]
		[ar:歌词作者]
		[by:本LRC文件的创建者]
		[offset:+/- 以毫秒为单位整体时间戳调整，+增加，-减小]
		[re:创建此LRC文件的播放器或编辑器]
		[ti:歌词(歌曲)的标题]
		[ve:程序的版本]
	'''
	#用于保存头
	info = {}

	#将头拎出保存于info中
	_ll = []
	for i in lrclist:
		if (not type(i[0]) == int):
			ls = i[0].split(":")
			info[ls[0]] = ls[1]
		else:
			_ll.append(i)
	lrclist = _ll
	_ll = []

	'''
		将诸如
			[timestamp1][timestamp2]lrc
		解析成
			[timestamp1]lrc
			[timestamp2]lrc
	'''
	for i in lrclist:
		for j in range(0, len(i) - 1, 1):
			_ll.append([i[j], i[-1]])

	lrclist = _ll
	
	#调整offset
	if info.has_key("offset"):
		offset = int(info["offset"])
		for i in lrclist:
			i[0] = i[0] + offset
	
	#如果需要解析头
	if head:
		if info.has_key("ar"):
			lrclist.append([-5, info["ar"]])
		if info.has_key("al"):
			lrclist.append([-4, info["al"]])
		if info.has_key("ti"):
			lrclist.append([-3, info["ti"]])
		lrclist.append([-2, ""])

	lrclist.sort()
	return lrclist	
