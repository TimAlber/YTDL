#!/usr/bin/python
from __future__ import unicode_literals
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import youtube_dl
from os import curdir, sep, system
import cgi

PORT_NUMBER = 8080
class myHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"
		try:
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".mp3"):
				mimetype='audio/mp3' 
				sendReply = True

			if sendReply == True:
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		  if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			link=form["url"].value
			name=form["filename"].value
			print "Your URL is: "+link
			print "Your Filename: "+name
			self.send_response(200)
			self.end_headers()

                        ydl_opts = {'outtmpl': name+'.mp3','format': 'bestaudio/best','postprocessors': 
				[{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],}


                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([link])
			self.wfile.write('<a href="%s.mp3" download>Download<a>' % name)
    			#self.wfile.write('<center><a href="%s.mp3" download >Download<a><br><a href="index.html">Back<a></center>' % name)
			return


try:
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()

