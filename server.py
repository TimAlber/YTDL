#!/usr/bin/python
from __future__ import unicode_literals
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import urllib
import songdetails
import youtube_dl
from os import curdir, sep, system
import cgi
from lxml import etree

PORT_NUMBER = 8080
class myHandler(BaseHTTPRequestHandler):

	def do_GET(self):
	   if self.path=="/":
	  	
                self.path="index.html"
		f = open(curdir + sep + self.path) 
		self.send_response(200)
               	self.send_header('Content-type','text/html')
               	self.end_headers()
		self.wfile.write(f.read())
		
 
	   elif self.path != "/send":
		try:
			imsi = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('imsi', None)
			if imsi[0] != None:
			   link = imsi[0]
			try:
			   name = imsi[1]
               		except IndexError:
			  name = " ".join(etree.HTML(urllib.urlopen(link).read()).xpath("//span[@id='eow-title']/@title"))
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
           	except IOError:
              		self.send_error(404,'File Not Found: %s or maybe unvalid URL or not allowd charachters' % self.path)

	        return

	def do_POST(self):
		  if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			link=form["url"].value
			
			print "Your URL is: "+link
			try:
			  name = form["filename"].value
			except KeyError:
			  name = " ".join(etree.HTML(urllib.urlopen(link).read()).xpath("//span[@id='eow-title']/@title"))
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


try:
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()

