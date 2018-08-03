#!/usr/bin/python
from __future__ import unicode_literals
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import songdetails
import youtube_dl
from os import curdir, sep, system
import cgi

PORT_NUMBER = 8080
class myHandler(BaseHTTPRequestHandler):

	def do_GET(self):
	   try:
                if self.path=="/":
		   	print "No Input"
                        self.path="/index.html"
			self.send_response(200)
                	self.send_header('Content-type','text/html')
                	self.end_headers()
			f = open('index2.html','r')
                	self.wfile.write(f.read())
			return
		else:
			imsi = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('imsi', None)

			link = imsi[0]
			name = imsi[1]
                	print "Your URL is: "+link
               		print "Your Filename: "+name
                	ydl_opts = {'outtmpl': 'songs/'+name+'.mp3','format': 'bestaudio/best','postprocessors':
                           	[{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],}
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                   	   ydl.download([link])
			f = open('songs/'+name+'.mp3','rb')

			self.send_response(200)
			self.send_header('Content-type','audio/mpeg')
			self.send_header('Content-Disposition', 'attachment; filename="%s.mp3"'% name)
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
			return
	   except IOError:
              self.send_error(404,'File Not Found: %s or maybe unvalid URL or not allowd charachters' % self.path)
	
	def do_POST(self):
		return


try:
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()

