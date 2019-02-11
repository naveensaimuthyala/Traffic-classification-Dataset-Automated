try:
    import libtorrent as lt
except Exception as e:
    raise e
import time, sys, getpass, os

class Downloader:
    def downloadByName(self, name):
        ses = lt.session()
        info = lt.torrent_info(name)
        directory = '/home/{0}/torrents'.format(getpass.getuser())
        if not os.path.exists(directory):
            os.makedirs(directory)
        h = ses.add_torrent({'ti': info, 'save_path': directory})
        print ('starting', h.name())
        while (not h.is_seed()):
            s = h.status()
            print("Downloading = {0}%".format((s.progress*100)))
            time.sleep(1)
            sys.stdout.flush()
        print (h.name(), 'complete')
