import pygame
import os


class MusicPlayer:
    """Simple playlist player using pygame.mixer."""

    def __init__(self, music_dir):
        pygame.mixer.init()
        self.tracks = []
        if os.path.isdir(music_dir):
            for f in sorted(os.listdir(music_dir)):
                if f.lower().endswith((".mp3", ".wav", ".ogg")):
                    self.tracks.append(os.path.join(music_dir, f))
        self.index = 0
        self.playing = False

    def _load_current(self):
        if not self.tracks:
            return
        pygame.mixer.music.load(self.tracks[self.index])

    def play(self):
        if not self.tracks:
            return
        if self.playing:
            return
        if pygame.mixer.music.get_busy() and not self.playing:
            pygame.mixer.music.unpause()
        else:
            self._load_current()
            pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next(self):
        if not self.tracks:
            return
        self.index = (self.index + 1) % len(self.tracks)
        was_playing = self.playing
        pygame.mixer.music.stop()
        self.playing = False
        if was_playing:
            self.play()

    def previous(self):
        if not self.tracks:
            return
        self.index = (self.index - 1) % len(self.tracks)
        was_playing = self.playing
        pygame.mixer.music.stop()
        self.playing = False
        if was_playing:
            self.play()

    def current_track_name(self):
        if not self.tracks:
            return "(no tracks)"
        return os.path.basename(self.tracks[self.index])

    def progress(self):
        """Return (pos_sec, length_sec) if available."""
        if not self.tracks or not self.playing:
            return 0, 0
        pos = pygame.mixer.music.get_pos() / 1000.0
        if pos < 0:
            pos = 0
        return pos, 0  # length unknown without mutagen; show elapsed only