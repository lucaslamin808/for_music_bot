import random
from collections import deque

from config import config


class Playlist:
    # Armazenamento de todas as músicas e opções fila

    def __init__(self):
        # Armazena os links das músicas que foram e a serem reproduzidas
        self.playque = deque()
        self.playhistory = deque()

        # Armazena separadamente o nome das músicas que já foram reproduzidas
        self.trackname_history = deque()
        self.loop = False

    def __len__(self):
        return len(self.playque)

    def add_name(self, trackname):
        self.trackname_history.append(trackname)
        if len(self.trackname_history) > config.MAX_TRACKNAME_HISTORY_LENGTH:
            self.trackname_history.popleft()

    def add(self, track):
        self.playque.append(track)

    def next(self, song_played):

        if self.loop == True:
            self.playque.appendleft(self.playhistory[-1])

        if len(self.playque) == 0:
            return None

        if len(self.playque) == 0:
            return None

        if song_played != "Dummy":
            if len(self.playhistory) > config.MAX_HISTORY_LENGTH:
                self.playhistory.popleft()

        return self.playque[0]

    def prev(self, current_song):

        if current_song is None:
            self.playque.appendleft(self.playhistory[-1])
            return self.playque[0]

        ind = self.playhistory.index(current_song)
        self.playque.appendleft(self.playhistory[ind - 1])
        if current_song != None:
            self.playque.insert(1, current_song)

    def shuffle(self):
        random.shuffle(self.playque)

    def empty(self):
        self.playque.clear()
        self.playhistory.clear()
