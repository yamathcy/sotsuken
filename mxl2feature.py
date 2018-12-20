import music21 as m21
import mido
import numpy as np
import nltk
from collections import Counter
import matplotlib.pylab as plt
import os,sys
import copy
import matplotlib.pylab as plt


class gakuhu:

    def __init__(self,notes):
        #歌詞
        self.lylic =[]
        #音列
        self.notes = notes
        #音高列
        self.pitch_unigram = self.notes.
        #音価列
        self.duration_unigram = []
        #音高/音価列
        self.p_d_unigram = []

    def add_lylic(self,lylic):
        self.lylic = lylic


    """
    def make_bi_gram(self):
        # 音列のbi-gramを作成して返す
        return tuple((self.notes[i:i+2]) for i in range(len(self.notes)-3))
    """

    def
"""
集計する特徴
A.局所特徴
１．音符のbi-gram →音高、音長ともにとる
２．音符のbi-gram→音高のみ（2音の音程）
３．音符のbi-gram→音長のみ
４．特殊記号の音
５．音価
６．歌詞の音韻（＊）

B.大局的特徴（観測可能）
１．音域（最高音、最低音）
２．ピッチエントロピー
３．音価のエントロピー


C.大局的特徴（人間の感性を考慮すべきもの）
１．メロディのなじみやすさ→暗意実現モデル？
２．リズムの複雑さ
３．息継ぎのしにくさ

D.その他個人性にかかわるもの
１．喚声点をまたぐ回数（局所）
２．音域
３．聴いた回数
４．その人が好きな楽曲との類似性


モデル１
a-1,a-2,a-3,a-4,a-5,b-1,b-2,b-3

"""

def extract_feature(piece):
    piece.show()

def main():
    file =[]
    models = []
    ok = False
    while ok == False:
        print("Musicxmlのファイル名を入力してください")
        music_file = input("ファイル名")
        if os.path.isfile("./" +music_file):
            try:
               file.append(music_file)
            except OSError:
                print("MusicXMLではありません")
        else:
            print("ファイルがありません")
        is_continue = input("続けますか？終了するなら0と入力")
        if is_continue == "0":
            ok = True

        for sheet in file:
            model = gakuhu()

            #楽譜の読み込み
            piece  = m21.converter.parse("./"+ sheet)
            #特徴集計
            #piece.show()
            vocal = piece.parts[0]

            #音の集計
            vocal.plot('pianoroll')

            #plt.show(plot_result)

            #歌詞の読み込み
            lylic = m21.search.lyrics.LyricSearcher(vocal)
            gakuhu.add_lylic(lylic)

            #音価の集計
            gakuhu.notes = vocal.flat.notesAndRests.stream()



if __name__ == "__main__":
    main()