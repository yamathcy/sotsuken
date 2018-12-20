import librosa
from librosa import display
from librosa import core

import madmom
import numpy as np
import scipy as sp
from matplotlib import pylab as plt
import os,sys
import pandas as pd
import seaborn as sns


class audio_obj:

    def __init__(self):
        self.audio = None   #ファイル
        self.wav = None     #波形
        self.is_read = False    #ファイルを読み込んだか
        self.spectrogram = None #STFTした後のリスト
        self.note = []

    def read(self,file):
        self.audio = file
        if not os.path.isfile("./" + self.audio):
            print("ファイルがありません")
        else:
            try:
                self.wav, fs = librosa.load("./" + self.audio, sr=44100)
                self.is_read = True
            except OSError:
                print("オーディオファイルではありません")


    def show_wave_spectrogram(self):
        if self.is_read == True:
            try:
                self.spectrogram = librosa.stft(self.wav)
                print("spectrogram;{}".format(type(self.spectrogram)))
                librosa.display.specshow(np.log(np.abs(self.spectrogram) ** 2), y_axis="log", x_axis="time")
                plt.title('Power spectrogram')
                plt.colorbar(format='%+2.0f dB')
                plt.tight_layout()
                plt.show()
            except librosa.util.exceptions.ParameterError:
                print("ParameterErrorOccured")
                print(type(self.spectrogram))


    def wave_to_midi(self):
        a = librosa.stft(self.wav)
        #self.note.append(np.floor(12 * np.log2(/440) + 69.5))

"""
class pitch_rating:

    def __init__(self):
        self.score = 0.0



class rhythm_rating:

    def __init__(self):
        self.score = 0.0

class volume_rating:

    def __init__(self):
        self.score = 0.0

def overall_score_ranker(s1,s2,s3,w1,w2,w3):
    # 重みづけ和を返す
    return w1*s1 + w2*s2 + w3*s3
"""

def main():
    print("hoge")
    file = input("オーディオファイルを入力してください")
    analyze = audio_obj()
    analyze.read(file)
    analyze.show_wave_spectrogram()


if __name__ == "__main__":
    main()