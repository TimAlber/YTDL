from __future__ import unicode_literals
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse
import urllib
import youtube_dl
from os import curdir, sep, system
import cgi
from lxml import etree

PORT_NUMBER = 8080
class myHandler(BaseHTTPRequestHandler):

	def do_GET(self):
	   try:
              if self.path=="/":
                 self.path="/index.html"
              if self.path.endswith(".html"):
                 mimetype = 'text/html'
              if self.path.endswith(".js"):
                 mimetype = 'application/javascript'
              f = open(curdir + sep + self.path)
              self.send_response(200)
              self.send_header('Content-type',mimetype)
              self.end_headers()
              self.wfile.write(f.read())
	      f.close()
	      return

	   except:
		imsi = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('imsi', None)
                try:
                   link = imsi[0]
		   print "Your URL is: "+link
                   try:
                      name = imsi[1]
                   except IndexError:
                      name = " ".join(etree.HTML(urllib.urlopen(link).read()).xpath("//span[@id='eow-title']/@title"))
                   print "Your Filename: "+name
		except TypeError:
                   print "No URL given"
                   return
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
           	#self.send_error(404,'File Not Found: %s' % self.path)

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

