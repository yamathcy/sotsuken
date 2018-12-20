import music21 as m21
from music21 import *
import matplotlib.pylab as plt
from collections import Counter
import pandas as pd
import numpy as np

analysis_corpus = []
analysis_section = {0: "A melody", 1: "B melody", 2: "Sabi"}

def shuukei(vocalpart):
    """
    音価・音高のペアのオブジェクトを楽譜から作る
    タイの部分→連結

    """
    record = []
    checker = False
    # タイがついた場合の途中記録用
    pitch_tmp = 0.0
    duration_tmp = 0.0
    for i in vocalpart.flat.notesAndRests.stream():

        # タイがついている
        if i.tie:
            # タイのはじめの音ならまず音高を記録する
            if checker == False:
                if i.isNote == True:
                    # record.append([i.pitch.ps,i.duration.quarterLength])
                    # 音符はノート番号
                    pitch_tmp = i.pitch.ps
                    duration_tmp += i.duration.quarterLength
                elif i.isRest == True:
                    # record.append(["rest",i.duration.quarterLength])
                    # 休符は無限にする
                    pitch_tmp = np.inf
                    duration_tmp += i.duration.quarterLength

            # タイの途中の音なら音長を足していく
            else:
                duration_tmp += i.duration.quarterLength

            # タイはついている
            checker = True

        # タイがついてない
        else:
            checker = False
            # 直前がタイの最後の音ならタイでつながって一音になった音を追加
            if not duration_tmp == 0.0:
                record.append([pitch_tmp, duration_tmp])
                duration_tmp = 0.0

            # そうでなければ普通に追加
            if i.isNote == True:
                record.append([i.pitch.ps, i.duration.quarterLength])
            elif i.isRest == True:
                record.append([np.inf, i.duration.quarterLength])

    return record


def count_duration(song):
    # [音高,音価]が要素になったリストから音価を集計する
    lis = []
    for n in range(len(song)):
        lis.append(song[n][1])
    duration_count = Counter(lis)
    # 集計結果のカウンターを返す
    # sorted_count = sorted(duration_count.items(),key=lambda x:x[0])
    # return sorted_count

    return duration_count

def count_pitch(song):
    #[音高,音価]が要素になったリストから音高を集計する
    lis = []
    for n in range(len(song)):
        lis.append(song[n][0])
    pitch_count = Counter(lis)
    #集計結果のカウンターを返す
    return pitch_count

def make_pitch_bigram(shuukei_obj):
    #[音高,音価]が要素になったリストから音高のBigramのリストを作成する
    pitch_diff = []
    for i in range(len(shuukei_obj)-1):
        if shuukei_obj[i+1][0] > 10000 and shuukei_obj[i][0] > 10000:
        	pass
        else:
            pitch_diff.append(shuukei_obj[i+1][0] - shuukei_obj[i][0])
    return pitch_diff

def make_duration_bigram(shuukei_obj):
    #[音高,音価]が要素になったリストから音価のBigramのリストを作成する
    duration_diff = []
    for i in range(len(shuukei_obj)-1):
        duration_diff.append(shuukei_obj[i+1][1] - shuukei_obj[i][1])
    return duration_diff


def jump_rate(bigram_status):
    # バイグラム列から跳躍、下降跳躍、上向跳躍の割合を返す
    up_jump = 0
    down_jump = 0
    slope = 0
    for key in bigram_status.keys():
        if np.abs(key) <= 2:
            slope += bigram_status[key]
        elif np.abs(key) <= 10000:
            if key > 0:
                up_jump += bigram_status[key]
            else:
                down_jump += bigram_status[key]
    all_of_notes = up_jump + down_jump + slope

    return [(up_jump + down_jump) / all_of_notes, up_jump / all_of_notes, down_jump / all_of_notes]

def delete_inf(bigram_status):
    #休符を含むBigramから休符を削除
    del bigram_status[np.inf]
    del bigram_status[-np.inf]
    del bigram_status[None]
    return bigram_status


def separate_section(piece, a_start, a_end, b_start, b_end, s_start, s_end):
    # Aメロ,Bメロ,サビに分割
    # 各セクションの始点と終点の小節番号を引数に与える
    sections = []
    amero = piece.measures(a_start, a_end)
    bmero = piece.measures(b_start, b_end)
    sabi = piece.measures(s_start, s_end)

    print(sabi)
    sections.append(amero)
    sections.append(bmero)
    sections.append(sabi)

    return sections

def counter_plot(counter,song,section,analysee_name,bar_color):
    # カウンターオブジェクトのプロット
    left = counter.keys()
    height = counter.values()
    plt.title("song: {} ({}'s {})".format(song,section,analysee_name))
    plt.bar(left,height,color=bar_color)
    for x, y in zip(left, height):
        try:
            plt.text(x, y, y, ha='center', va='bottom')
        except ValueError:
            pass
    plt.grid()
    plt.show()

#音高、音価のペアのリストをセクションごとに作成
def make_note(sections):
    notes = []
    for item in sections:
        note_obj = shuukei(item)
        notes.append(note_obj)
    return notes

#セクションごとに音高、音価のペア列から音程列を作成
def make_pitch_diff(notes):
    ontei = []
    for item in notes:
        bigram = make_pitch_bigram(item)
        onteiobj = delete_inf(Counter(bigram))
        ontei.append(onteiobj)
    return ontei


class gakuhu_object:
    """
    ボーカルパートのあらゆる情報を保持するクラス

    __init__(self,file)　
    初期化、読み込む楽譜ファイルを与える

    separate_section(self,a_start,a_end,b_start,b_end,s_start,s_end)
    A,B,サビに楽譜を分割、それぞれのセクションの始めの小節と終わりの小節の番号を与える
    """

    # コンストラクタ
    def __init__(self, name, file, separate_info):
        # 楽曲名
        self.name = name
        # ボーカルパートを読み込み（一つ目のパートがボーカルである前提・・・）
        self.piece = m21.converter.parse("./" + file).parts[0]
        # Aメロ、Bメロ、サビのオブジェクトを保持する
        self.sections = separate_section(self.piece, separate_info[0], separate_info[1], separate_info[2],
                                         separate_info[3], separate_info[4], separate_info[5])
        # 音高、音列のペア
        self.notes = make_note(self.sections)
        # 音程列
        self.ontei = make_pitch_diff(self.notes)

        analysis_corpus.append(self)

    # 調の表示
    def show_key(self):
        print("------------" + self.name + "-------------")
        for num, section in enumerate(self.sections):
            print("-------{}の統計情報---------".format(analysis_section[num]))
            print("調:{}".format(analysis.discrete.analyzeStream(section, "Krumhansl")))

    """
    #音高、音価のペアのリストをセクションごとに作成
    def make_note(self):
        for item in self.sections:
            note_obj = shuukei(item) 
            self.notes.append(note_obj)

    #音程列の作成
    def make_pitch_diff(self):
        for item in self.notes:
            bigram = make_pitch_bigram(item)
            onteiobj = delete_inf(Counter(bigram))
            self.notes.append(onteiobj)
    """

    # 音高のカウント
    def counting_pitch(self):
        for item in self.sections:
            pitch_space = graph.plot.HistogramPitchSpace(item, xHideUnused=False)
            pitch_space.colors = "magenta"
            pitch_space.run()
            pitch_class = graph.plot.HistogramPitchClass(item, xHideUnused=False)
            pitch_class.colors = "cyan"
            pitch_class.run()
            # item.plot("histogram","pitch",xHideUnused=False)
            # item.plot("histogram","pitchclass",xHideUnused=False)

    # 音価のカウント
    def counting_duration(self):
        for num, item in enumerate(self.notes):
            dcount = count_duration(item)
            # print(dcount)
            duras = {}
            for i in sorted(dcount.keys()):
                new_key = str(i)
                duras[new_key] = dcount[i]
            counter_plot(duras, self.name, str(analysis_section[num]), "duration by Quarter Length", "g")

    # 音高差の集計をプロット
    def plot_pitch_diff(self):
        for num, item in enumerate(self.ontei):
            counter_plot(item, self.name, str(analysis_section[num]), "pitch_diff", "r")

    # 跳躍進行の割合を表示
    def calucurate_jump(self):
        for num, sect in enumerate(self.ontei):
            a = delete_inf(Counter(sect))
            jump_status = jump_rate(a)
            print("{}の跳躍情報　跳躍の割合:{:.2},上向跳躍の割合:{:.2},下降跳躍の割合:{:.2}".format(analysis_section[num], jump_status[0],
                                                                           jump_status[1], jump_status[2]))

    # 音域（何半音ぶんか）を表示
    def caluculate_pitch_range(self):
        print("hoge")


"""青野モデル算出のためのプログラム群"""
def make_d_timeline(vocal):




def aono_model(vocal):

    m = [[3.0,1.0,2.0,1.0] * vocal.notesAndRests.streamLength]
    """
    M→拍頭アクセントメロディの有無にかかわらず休符であっても全ての計算点に与えられる
    1/4拍ごとに（3,1,2,1）で与えられる
    """
    d = make_d_timeline(vocal)
    """
    D→音長アクセント
    
    """
    f =
    l =
    h =
    v =
    w =
    p =




def main():

    """
    （楽譜の読み込み）
    cherry = gakuhu_object("Cherry", "cherry.xml", [1, 8, 9, 15, 16, 24])
    tsunami = gakuhu_object("TSUNAMI", "TSUNAMI.xml", [1, 16, 17, 25, 25, 42])
    roman = gakuhu_object("Roman Hikou", "roman.xml", [1, 8, 9, 16, 16, 29])
    aporo = gakuhu_object("Aporo", "aporo3.xml", [20, 34, 35, 43, 44, 59])
    guren = gakuhu_object("Guren No Yumiya", "guren.mxl", [12, 27, 28, 35, 36, 51])
    konayuki = gakuhu_object("Konayuki", "konayuki.mxl", [5, 26, 27, 37, 37, 45])
    """

    for sheets in analysis_corpus:
        sheets.show_key()
        sheets.counting_pitch()
        plt.figure()
        sheets.counting_duration()
        plt.figure()
        sheets.plot_pitch_diff()
        sheets.calucurate_jump()