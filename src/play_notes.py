import pygame
import os

class SoundPlayer:
    def __init__(self, notes):
        pygame.mixer.init()
        self.notes = notes
        self.sounds = {}
        for note in self.notes:
            sound_path = os.path.join("resources", "sounds", f"{note}.mp3")
            if os.path.exists(sound_path):
                self.sounds[note] = pygame.mixer.Sound(sound_path)
            else:
                print(f"Warning: {sound_path} not found.")

    def play_note_by_index(self, i):
        if 0 <= i < len(self.notes):
            note = self.notes[i]
            if note in self.sounds:
                self.sounds[note].play()
