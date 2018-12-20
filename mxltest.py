import music21 as m21
from music21 import *
import os

piece = None

print("Musicxmlのファイル名を入力してください")
sheet = input("ファイル名")
if os.path.isfile("./" +sheet):
    try:
        piece = m21.converter.parse("./" + sheet)
        piece.





    except OSError:
        print("MusicXMLではありません")
else:
    print("ファイルがありません")
