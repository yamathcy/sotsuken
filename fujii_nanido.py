import mido
import music21 as m21
import numpy as np
import matplotlib.pylab as plt
import os,sys
from collections import Counter,defaultdict


class f_difficulty:

    def __init__(self,music_file):
        # 音楽ファイル
        self.music_file = music_file
        # 音長の集計
        self.duration_list = Counter()
        # 音聴ごとの難易度
        self.duration_difficulty = {}
        # 楽曲テンポ
        self.tempo = 0
        # 重みパラメータ
        self.omomi = np.array[0.5,0.4,0.1]


    def midi_difficulty(self):
        try:
            mid = mido.MidiFile("./"+self.music_file)
            deltaTime = 480
            on_notes = dict()
            score = []

        except OSError:
            print("MIDIファイルではありません")

    def mxl_difficulty(self):
        try:
            m21.corpus.parse("./"+ self.music_file)
        except OSError:
            print("MusicXMLではありません")

def main():
    #ファイルの読み込み
    print("ファイルを読み込みます")
    print("MIDI:0 MusicXml:1")
    mode = input("読み込むファイルの種類を選んでください")
    file = input("読み込むファイル名を入力してください")
    if os.path.isfile("./"+file):
       difficulty = f_difficulty(file)
       if mode == 0:
           difficulty.midi_difficulty()
       elif mode == 1:
           difficulty.mxl_difficulty()

    else:
        print("ファイルがありません")



if __name__ == "__main__":
    main()