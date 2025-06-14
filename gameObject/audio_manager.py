import pygame as pg
from pathlib import Path
from blinker import Signal
from typing import Dict,List
import time
import threading

effectPath = Path("assets/effect")
musicPath = Path("assets/music")

class AudioManager:
    _instance = None
    # TODO: implement playList/Group, Function : makeConnection?
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        pg.mixer.init()

        self.effects = load_effects(effectPath, "mp3")
        self.bgms = load_bgms(musicPath, "ogg")
        # load_playList

        self.signals = {
            "bgm_playing": Signal(), # back name
            "effect_playing": Signal() # back name
            }
        self.bgm_switching_lock = threading.Lock()

    def playMusic(self, name : str):
        threading.Thread(target=self.onPlayMusic, args=(name,)).start()
    def onPlayMusic(self, name: str):
        with self.bgm_switching_lock:
            path = self.bgms.get(name)
            if path:
                pg.mixer.music.fadeout(2000)
                time.sleep(2.1)
                pg.mixer.music.load(str(path))
                self.signals["bgm_playing"].send(self, name = name)
                pg.mixer.music.play(-1, fade_ms=1500)
                time.sleep(1.6)

    def playEffect(self, name : str):
        threading.Thread(target=self.onPlayEffect, args=(name,)).start()
    def onPlayEffect(self, name : str):
        sound = self.effects.get(name)
        if sound: 
            self.signals["effect_playing"].send(self, name = name)
            sound.play()
         
    def set_music_volume(self, vol : float):
        pg.mixer.music.set_volume(vol)
    
    def set_effect_volume(self, name :str, vol : float):
        for sound in self.effects.values():
            sound.set_volume(vol)
    
    def stop_music(self, fade_ms=1500):
        pg.mixer.music.fadeout(fade_ms)


# Helper Functions
def load_effects(path: Path, ext: str) -> Dict[str, pg.mixer.Sound]:
      effects = {}
      pattern = f"*.{ext}" 
      for file in path.glob(pattern):
           filebasename = file.stem
           effects[filebasename] = pg.mixer.Sound(str(file))
      return effects

def load_bgms(path: Path, ext: str) -> Dict[str, Path]:
    bgms = {}
    pattern = f"*.{ext}" 
    for file in path.glob(pattern):
        filebasename = file.stem
        bgms[filebasename] = file
    return bgms

# def load_playList(self,path) -> List[str]