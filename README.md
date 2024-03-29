# Automation
A collection of projects for automating repetitive tasks using Python.

___________________________________________________________________________________________________________________________________________________________________________________
___________________________________________________________________________________________________________________________________________________________________________________

# Downloader

Description:

The program is a command line script that downloads audio, a single video or an entire playlist from YouTube, torrents (single or bulk), animated shows (single or bulk) and comic books (single or bulk) in PDF format based on the input search request, it also creates a directory under the user's "Documents" folder (Windows 10) in which to store the saved files - the name of the folder is specified by the user under the content category prompt.


Requirements:

The script uses ffmpeg to process the audio/video(s) and so this software package must be installed on the system. A good ffmpeg installation guide for Windows 10 is provided by the following link (YouTube video tutorial); https://www.youtube.com/watch?v=r1AtmY-RMyQ

For the comic book download capabilities, a version of chrome webdriver matching your chrome web-browser is required to be installed on your machine, and the path to the executable must also be specified to the program by replacing the "path" variable in the main() loop with the appropriate folder location to the webdriver software.

The torrent download feature makes use of the magnet-scraping api from this github project; https://github.com/SameerBidi/Torrent-Scraping in combination with the qbit-torrent server which can be setup (username and password for the UI manager) by following this tutorial; https://www.thepythoncode.com/article/download-torrent-files-in-python

The animated series are downloaded using the application developed in this github project; https://github.com/EpicUnknown/wco-dl
