from bot import TorrBot
from coverter import Converter
from downloader import Downloader
import sys, os

magnetLink = raw_input('enter magnet link: ')
converter = Converter()
filename = converter.convertManget(magnetLink)
print("\n{0} has been downloaded in your current directory".format(filename))
willDownloadFile = int(input("\n1. Download the file. \n2. Keep the .torrent file and exit \n3. Delete .torrent and exit\n\n"))

if willDownloadFile == 1:
    download_movie = Downloader()
    download_movie.downloadByName(filename)
    os.unlink(filename)
elif willDownloadFile == 2:
    sys.exit(0)
else:
    print("Deleted {0}".format(filename))
    os.unlink(filename)
    sys.exit(0)
