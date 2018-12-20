import os,sys,re
import mido
import numpy as np
import pandas as pd
import ngram
import nltk
from matplotlib.pylab import plot as plt
from collections import defaultdict,Counter


class midi_music_sheet():

    def __init__(self,midifilename):

        # 読み込むMIDIファイルの名前
        self.midifile = mido.MidiFile(midifilename)

        # デルタタイム
        self.delta = 240

        # スケール
        self.scale = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}

        # その楽譜の音のシーケンス
        self.sequence = []

        # スケールの集計
        self.scale_count = {"C":0,"C#":0,"D":0,"D#":0,"E":0,"F":0,"F#":0,"G":0,"G#":0,"A":0,"A#":0,"B":0}

        #　音価のカウント
        self.dur_count = {}

        #　音高のbi-gram
        self.pitch_bi_gram = None

        #  音価のbi-gram
        self.dur_bi_gram= None

        # すでに楽譜を読み込んでインスタンス化したか
        self.is_read = False

        # 音高差
        self.jumps = None

    def show_status(self):
        print(vars(self))


    def counting(self):
        if self.is_read == False:
            self.is_read = True
            #読み込んだMIDIファイルの全パートの音符を集計
            on_notes = dict()
            tmp_score = []

            for track in self.midifile.tracks:
                e_time = 0
                for msg in track:
                    print(msg)
                    e_time += msg.time
                    try:
                        if msg.velocity != 0:
                            on_notes[msg.note] = e_time
                        else:
                            on_time = on_notes.pop(msg.note)
                            dur = (e_time - on_time)/self.delta
                            tmp_score.append([
                                msg.note,
                                self.scale[msg.note%12],
                                dur,
                                msg.velocity,
                                msg.channel,
                                on_time / self.delta
                            ])

                            self.scale_count[self.scale[msg.note%12]] += 1
                            if dur not in self.dur_count:
                                self.dur_count[dur] = 1
                            else:
                                self.dur_count[dur] += 1
                    except AttributeError:
                        print("metamessage")
                        pass

            self.sequence = tmp_score
            #print(tmp_score)
            #scorecount = pd.DataFrame(tmp_score, columns=["NoteID","Note","Octabve","Duration","Velocity","Channel","time"])
            #print(scorecount)

            #duration  = pd.DataFrame(self.dur_count,columns=["numbers"])


    def make_bigram(self):
        corpus = []
        #print(self.sequence)

        print("hoge")
        #self.dur_bi_gram = nltk.bigrams(self.sequence[2])
        print(type(self.sequence))
        print(type(self.sequence[0]))
        for track in self.sequence:
            for x in track:
                corpus.append(x)


        self.pitch_bi_gram = nltk.bigrams(corpus)


        #self.pitch_bi_gram = nltk.bigrams(self.sequence[:, 0])


    def count_jump (self):
        #big = nltk.bigrams(self.sequence[k for k in range(len(self.sequence))][0])
        jumps = nltk.FreqDist(self.pitch_bi_gram)
        print(jumps.items())
        return jumps


    def show_counter(self):
        print()


def main ():
    msheet = input("MIDIファイルの名前を入力")
    if not os.path.isfile("./" + msheet):
        print("ファイルがありません")
    else:
        try:
            mus = midi_music_sheet(msheet)
            mus.counting()
            mus.show_status()
            mus.make_bigram()
            jump_hist = mus.count_jump()
            count = Counter()
            print("jumphist {}").format(jump_hist)
            for item in jump_hist.items():
                print(item)
                for n in range(item[1]):
                    div = item[0][0] - item[0][1]
                    count[div] += 1

            print(count.items())


        except OSError:
            print("MIDIファイルではありません")




if __name__ == "__main__":
    main()






