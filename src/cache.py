import os
import sys
import subprocess
import threading
import urllib2
import time
import json
import logger
import parlrc

log = logger.getLogger(__name__)

class Lrc:
	def __init__(self, notify):
		self.notify = notify
		self.lst_lrc_idx = -1
		self.no_lrc = True

	def load(self, id):
		log.debug("load......")

		self.no_lrc = True
		self.lst_lrc_idx = -1

		try:
			log.debug("http://music.163.com/api/song/media?id=" + str(id));
			data = urllib2.urlopen("http://music.163.com/api/song/media?id=" + str(id)).read()
			lrc_json = json.loads(data)
			if (lrc_json["code"] != 200 or not lrc_json.has_key("lyric")) :
				self.no_lrc = True
			else:
				log.debug("have lyric")
				self.no_lrc = False
				self.lrc = parlrc.par_lrcs(lrc_json["lyric"])
				log.debug(self.lrc)

		except:
			self.no_lrc = True

		log.debug(self.no_lrc)
		if (not self.no_lrc) :
			log.debug(self.lrc)

	def get_idx(self, time):
		lti = self.lrc[self.lst_lrc_idx][0]
		idx = self.lst_lrc_idx
		time = time * 1000
		if lti > time :
			idx = 0
		while idx < len(self.lrc) and self.lrc[idx][0] < time :
			idx = idx + 1
		idx = idx - 1
		return idx

	def played_time(self, nowtime):
		if self.no_lrc:
			return ""
		idx = self.get_idx(nowtime)
		if (idx != self.lst_lrc_idx):
			self.lst_lrc_idx = idx
			log.debug(self.lrc[idx])
			return self.lrc[idx][1]
		return ""

class Notify:
	def __init__(self):
		self.cache = CacheController()
		self.now_play = 0
		self.lrc = Lrc(self)
		self.now_info = ""

		p = subprocess.Popen(["which", "notify-send"], 
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
		time.sleep(0.01)
		o = p.stdout.read()
		e = p.stdout.read()
		self.hava_notify_send = False
		if o != "" and e == "":
			self.hava_notify_send = True

	def send(self, song_name, artist, picUrl, lrc = "  "):
		if not self.hava_notify_send:
			return
		fn = self.cache.cachePicture(picUrl)
		if fn != "" and os.path.exists(fn) :
			subprocess.Popen(["notify-send", "%s - %s"%(song_name, artist), lrc, "-t", "10000", "-i", fn],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)
		else:
			subprocess.Popen(["notify-send", "%s - %s"%(song_name, artist), lrc, "-t", "10000"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE)

	def updateInfo(self, song_info, nowtime):
		if not self.hava_notify_send:
			return
		if song_info["song_id"] != self.now_play:
			self.send(song_info["song_name"], song_info["artist"], song_info["picUrl"])
			self.now_play = song_info["song_id"]
			self.lrc.load(self.now_play)
			self.now_info = song_info
		else :
			lrc = self.lrc.played_time(nowtime)
			if (lrc != "") :
				self.send(song_info["song_name"], song_info["artist"], song_info["picUrl"], lrc)


class CacheController:
	def __init__(self):
		self.current_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
		home_dir = os.getenv('HOME')
		self.cache_path = "%s/.cache/musicbox/"%(home_dir)
		os.system('mkdir -p "%s"'%(self.cache_path))
		

	def startDownload(self, url, fn):
		def download(url, fn):
			data = urllib2.urlopen(url).read()
			f = open(fn, "wb")
			f.write(data)

		thread = threading.Thread(target=download, args=(url, fn))
		thread.start()
		return

	def cachePicture(self, picUrl):
		if picUrl == "":
			return ""
		fn = self.cache_path + os.path.split(picUrl)[-1]
		if not os.path.exists(fn):
			self.startDownload(picUrl + "?param=50x50", fn)
		return fn

	def cacheLrc(self, lrcUrl, id):
		if lrcUrl == "":
			return ""

		fn = self.cache_path + id + ".lrc"
		if not os.path.exists(fn):
			self.startDownload(lrcUrl, fn)
		return fn