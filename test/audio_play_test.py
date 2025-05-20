import sys,os
import time
import pygame as pg
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gameObject.audio_manager import AudioManager

def on_bgm_playing(sender, **kwargs):
    print(f"开始播放背景音乐: {kwargs.get('name')}")

def on_bgm_stopped(sender):
    print("背景音乐停止了")

def on_effect_playing(sender, **kwargs):
    print(f"开始播放音效: {kwargs.get('name')}")


def main():
    pg.init()
    #pg.display.set_mode((700, 500))

    audio = AudioManager()

    audio.signals["bgm_playing"].connect(on_bgm_playing)
    audio.signals["effect_playing"].connect(on_effect_playing)

    # 播放 testBgm.flac
    audio.playMusic("testBgm")

    time.sleep(5)  # 播放 5 秒

    # 停止播放音乐，播放 testPianoEffect.mp3
    print("停止播放音乐")
    audio.stop_music()
    audio.playEffect("testPianoEffect")

    time.sleep(5)

    # 重复播放音效以及bgm
    audio.playEffect("testPianoEffect")
    time.sleep(5)
    
    # 减小音效音量
    print("减小音效音量:0.1")
    audio.set_effect_volume("testPianoEffect",0.1)
    time.sleep(5)

    # 重复播放背景音乐
    audio.playMusic("testBgm")
    audio.playMusic("testBgm")
    time.sleep(5)
    
    # 调整音乐音量
    audio.set_music_volume(0.6)
    print("减小音乐音量:0.6")

    time.sleep(10)
    print("停止播放音乐")
    audio.stop_music()
    pg.quit()

if __name__ == "__main__":
    main()
