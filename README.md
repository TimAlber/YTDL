# YTDL
Execute server.py on your Server
Vist your server ip with port 8080 to see the index.html

Visit http://MY-SERVER-IP:8080/?imsi=YOUTUBE-URL&imsi=FILENAME <br>
Where YOUTUBE-URL is the entire URL of a Youtube Video and FILENAME is the name you want your .mp3 file to have.

For Example: http://192.168.178.70:8080/?imsi=https://www.youtube.com/watch?v=vVy9Lgpg1m8&imsi=meinehoe

If You leave out the Name (what comes after the &), The Title of the Youtube Video will be the filename.
For Example: http://192.168.178.70:8080/?imsi=https://www.youtube.com/watch?v=vVy9Lgpg1m8
The script will then download the Video from youtube to the server, convert it into .mp3 give it the name of your choice and the send it to your client.

Feel free to Fork me and let me know about any bugs.
