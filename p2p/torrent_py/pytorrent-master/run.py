__author__ = 'alexisgallepe'

import time
import peers_manager
import pieces_manager
import torrent
import tracker
import logging
import os
import message

class Run(object):
    percentage_completed = -1

    def __init__(self):
        self.torrent =torrent.Torrent("https://thepiratebay.org/torrent/29225643/Ashampoo_Music_Studio_7.0.2.4_Final___Crack")
        self.pieces_manager = pieces_manager.PiecesManager(self.torrent)
        self.peers_manager = peers_manager.PeersManager(self.torrent, self.pieces_manager)

        self.peers_manager.start()
        logging.info("PeersManager Started")
        logging.info("PiecesManager Started")

    def start(self):
        peers = self.tracker.get_peers_from_trackers()
        self.peers_manager.add_peers(peers)

        while not self.pieces_manager.all_pieces_completed():
            if not self.peers_manager.has_unchoked_peers():
                time.sleep(0.1)
                continue

            self.display_progression()

            for piece in self.pieces_manager.pieces:
                if piece.is_full: continue

                peer = self.peers_manager.get_random_peer_having_piece(piece.piece_index)
                if not peer: continue

                data = self.pieces_manager.pieces[piece.piece_index].get_empty_block()
                if data:
                    piece_index, block_offset, block_length = data
                    piece_data = message.Request(piece_index, block_offset, block_length).to_bytes()
                    peer.send_to_peer(piece_data)

                if piece.all_blocks_full():
                    piece.set_to_full()

                piece.update_block_status()

            time.sleep(0.1)

        self._exit_threads()

    def display_progression(self):
        new_progression = 0

        for i in range(self.pieces_manager.number_of_pieces):
            for j in range(self.pieces_manager.pieces[i].number_of_blocks):
                if self.pieces_manager.pieces[i].blocks[j][0] == "Full":
                    new_progression += len(self.pieces_manager.pieces[i].blocks[j][2])

        if new_progression == self.percentage_completed:
            return

        number_of_peers = self.peers_manager.unchoked_peers_count()
        percentage_completed = float((float(new_progression) / self.torrent.total_length) * 100)

        print "Number of peers: {} - Completed : {}%".format(number_of_peers, percentage_completed)

        self.percentage_completed = new_progression

    def _exit_threads(self):
        self.peers_manager.is_active = False
        os._exit(0)
