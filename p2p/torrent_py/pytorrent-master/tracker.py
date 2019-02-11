import peer

__author__ = 'alexisgallepe'

import bencode
import requests
import logging
import struct, random, socket
from urlparse import urlparse
import threading


class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

class Tracker(object):
    def __init__(self, torrent):
        self.torrent = torrent
        self.threads_list = []
        self.list_ip_port = []
        self.banned_ips = []
        self.connected_peers = []

    def get_peers_from_trackers(self):
        for tracker in self.torrent.announce_list:
            if tracker[0][:4] == "http":
                continue
                t1 = FuncThread(self.http_scraper, self.torrent, tracker[0])
                self.threads_list.append(t1)
                t1.start()

            elif tracker[0][:3] == "udp":
                t2 = FuncThread(self.udp_scrapper, self.torrent, tracker[0])
                self.threads_list.append(t2)
                t2.start()

        for t in self.threads_list:
            t.join()

        self.try_peer_connect()
        return self.connected_peers

    def try_peer_connect(self):
        for ip, port in self.list_ip_port:
            print '> len connected_peers : ', len(self.connected_peers)
            if len(self.connected_peers) > 8: break

            if not ip in self.banned_ips:
                new_peer = peer.Peer(self.torrent, ip, port)
                if not new_peer.connect():
                    self.banned_ips.append(ip)
                else:
                    self.connected_peers.append(new_peer)


    def http_scraper(self, torrent, tracker):
        params = {
            'info_hash': torrent.info_hash,
            'peer_id': torrent.peer_id,
            'uploaded': 0,
            'downloaded': 0,
            'left': torrent.total_length,
            'event': 'started'
        }

        try:
            answer_tracker = requests.get(tracker, params=params, timeout=5)
            list_peers = bencode.bdecode(answer_tracker.content)
            self.parse_tracker_response(list_peers['peers'])

        except Exception as e:
            logging.debug("HTTP scraping failed : %s" % e.message)

    def udp_scrapper(self, torrent, announce):
        try:
            parsed = urlparse(announce)
            ip = socket.gethostbyname(parsed.hostname)

            if ip == '127.0.0.1':
                return

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(10)

            conn = (ip, int(parsed.port))
            msg, trans_id, action = self.make_connection_id_request()
            response = self.send_message(conn, sock, msg, trans_id, action, 16)

            if not response:
                return

            conn_id = response[8:]
            msg, trans_id, action = self.make_announce_input(torrent.info_hash, conn_id, torrent.peer_id)
            response = self.send_message(conn, sock, msg, trans_id, action, 20)

            if not response:
                return

            for ip, port in self.parse_tracker_response(response[20:]):
                self.list_ip_port.append((ip, port))

        except Exception as e:
            logging.error("UDP scraping failed : %s" % e.message)

    def parse_tracker_response(self, peers_byte):
        raw_bytes = [ord(c) for c in peers_byte]
        for i in range(len(raw_bytes) / 6):
            start = i * 6
            end = start + 6
            ip = ".".join(str(i) for i in raw_bytes[start:end - 2])
            port = raw_bytes[end - 2:end]
            port = port[1] + port[0] * 256
            yield (ip, port)

    def make_connection_id_request(self):
        conn_id = struct.pack('>Q', 0x41727101980)
        action = struct.pack('>I', 0)
        trans_id = struct.pack('>I', random.randint(0, 100000))

        return conn_id + action + trans_id, trans_id, action

    def make_announce_input(self, info_hash, conn_id, peer_id):
        action = struct.pack('>I', 1)
        trans_id = struct.pack('>I', random.randint(0, 100000))

        downloaded = struct.pack('>Q', 0)
        left = struct.pack('>Q', 0)
        uploaded = struct.pack('>Q', 0)

        event = struct.pack('>I', 0)
        ip = struct.pack('>I', 0)
        key = struct.pack('>I', 0)
        num_want = struct.pack('>i', -1)
        port = struct.pack('>h', 8000)

        msg = (conn_id + action + trans_id + info_hash + peer_id + downloaded +
               left + uploaded + event + ip + key + num_want + port)

        return msg, trans_id, action

    def send_message(self, conn, sock, msg, trans_id, action, size):
        sock.sendto(msg, conn)

        try:
            response = sock.recv(2048)
        except socket.timeout as e:
            logging.debug("Timeout : %s" % e.message)
            return
        except Exception as e:
            logging.error("Unexpected error when sending message : %s" % e.message)
            return

        if len(response) < size:
            logging.debug("Did not get full message. Connecting again...")
            return self.send_message(conn, sock, msg, trans_id, action, size)

        if action != response[0:4] or trans_id != response[4:8]:
            logging.debug("Transaction or Action ID did not match. Trying again...")
            return self.send_message(conn, sock, msg, trans_id, action, size)

        return response
