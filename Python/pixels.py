import sys,os
sys.path.append("api")
import api.CommandStream as CS
import api.CommandGetter as CG
import threading
import collections


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QSizePolicy, QHeaderView, QHBoxLayout, QVBoxLayout, QLayout, QGraphicsDropShadowEffect

BACKGROUND_COLOR = "#fafbff"

TITLE_COLOR = "#3090f0"
GRID_COLOR = "#e1eaf7"

INDEX_SIZE = 13

CANVAS_X = 64
CANVAS_Y = 96

TOTAL = 0

commands = {
        "SET_PIXEL": r"set \d{1,2} \d{1,2} [a-zA-Z0-9#]+",
    }
stream = CG.listen("kZFLnAGUflM", commands)

players = {}

# Create a PyQt5 application
app = QApplication(sys.argv)


widget = QWidget()
widget.setStyleSheet(f"background-color: {BACKGROUND_COLOR}")
layout = QHBoxLayout()
widget.setLayout(layout)


left_layout = QVBoxLayout()
left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

#title_layout = QVBoxLayout()

mov = QLabel()
mov.setFixedSize(424, 280)
mov.setAttribute(Qt.WA_TranslucentBackground)

movie = QMovie("C:/LiveGames/GIFBUN.gif")
movie.setCacheMode(QMovie.CacheAll)
movie.setSpeed(100)
movie.setScaledSize(mov.size())

mov.setMovie(movie)
movie.start()

mov.show()

#mov.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
left_layout.addWidget(mov)

#title_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
#left_layout.addLayout(title_layout)




#instr_layout = QVBoxLayout()

wdg = QLabel("Interactive Pixel Art!")
wdg.setFont(QFont('Segoe Print', 26))
wdg.setStyleSheet(f"font-size: 26px; font-weight: bold; margin-bottom: 10px; margin-top: 60px; color: {TITLE_COLOR}; opacity: 0.5; font-style: italic; font-weight: bold;")
wdg.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
left_layout.addWidget(wdg)

wdg = QLabel("Viewers can control the pixel art\non the right by typing in the stream chat:")
wdg.setFont(QFont('Segoe Print', 20))
wdg.setWordWrap(True)
wdg.setStyleSheet(f"font-size: 20px; margin: 0px;")
wdg.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
left_layout.addWidget(wdg)

wdg = QLabel("set <y> <x> <color>")
wdg.setFont(QFont('Consolas', 35))
wdg.setStyleSheet(f"font-size: 35px; font-weight: bold; margin: 0px; font-style: italic; color: #8f0707;")
wdg.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
left_layout.addWidget(wdg)

#instr_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
#left_layout.addLayout(instr_layout)



#top_layout = QVBoxLayout()

wdg = QLabel("Top Painters")
wdg.setFont(QFont('Segoe Print', 26))
wdg.setStyleSheet(f"font-size: 26px; font-weight: bold; margin-bottom: 10px; margin-top: 60px; color: {TITLE_COLOR}; opacity: 0.5; font-style: italic; font-weight: bold;")
wdg.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
left_layout.addWidget(wdg)

wdg_total = QLabel(f"Total Pixels Placed: {TOTAL}")
wdg_total.setFont(QFont('Segoe Print', 18))
wdg_total.setWordWrap(True)
wdg_total.setStyleSheet(f"font-size: 18px; margin: 0px; color: orange;")
wdg_total.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
left_layout.addWidget(wdg_total)


wdg = QLabel("Viewers who placed the most pixels:")
wdg.setFont(QFont('Segoe Print', 20))
wdg.setWordWrap(True)
wdg.setStyleSheet(f"font-size: 20px; margin: 0px;")
wdg.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
left_layout.addWidget(wdg)

top = QLabel("")
top.setStyleSheet(f"font-size: 20px; margin: 0px; font-style: italic; color: #3373b5;")
top.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
left_layout.addWidget(top)

left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
#left_layout.addLayout(top_layout)




layout.addLayout(left_layout)


grid_layout = QGridLayout()
grid_layout.setSpacing(0)
grid_layout.setSizeConstraint(QGridLayout.SetFixedSize)
layout.addLayout(grid_layout)


for i in range(1, CANVAS_X+1):
    pixel = QLabel(str(i))
    pixel.setStyleSheet(f"font-size:{INDEX_SIZE}px; margin: 0px; padding: 0px; width: 10px; height:10px; color: grey;")
    pixel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    pixel.setMinimumSize(15, 15)
    pixel.setAlignment(Qt.AlignCenter)
    grid_layout.addWidget(pixel, i, 0)

for j in range(1, CANVAS_Y+1):
    pixel = QLabel(str(j))
    pixel.setStyleSheet(f"font-size:{INDEX_SIZE-2}px; margin: 0px; padding: 0px; width: 10px; height:10px; color: grey;")
    pixel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    pixel.setMinimumSize(15, 15)
    pixel.setAlignment(Qt.AlignCenter)
    grid_layout.addWidget(pixel, 0, j)


rows = [None]
# Add widgets to the grid grid_layout
for i in range(1, CANVAS_X+1):
    row = [None]


    for j in range(1,CANVAS_Y+1):

        pixel = QLabel("")
        pixel.setStyleSheet(f"background-color: white; font-size:0.01px; margin: 0px; padding: 0px; width: 10px; height:10px; border-left: 1px solid {GRID_COLOR}; border-top: 1px solid {GRID_COLOR};")
        pixel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        pixel.setMinimumSize(15, 15)
        grid_layout.addWidget(pixel, i, j)
        row.append(pixel)
        

    rows.append(row)


def handle():
    global TOTAL
    global players
    while True:
        com = stream.read()
        print(f"[{com.t}] - {com.d} ({com.p})")
        data = com.d.split(" ")
        i = int(data[1])
        j = int(data[2])
        if i == 0 or j == 0 or i > CANVAS_X or j > CANVAS_Y:
            continue
        color = data[3]
        TOTAL += 1
        rows[i][j].setStyleSheet(f"background-color: {color}; border-left: 1px solid {GRID_COLOR}; border-top: 1px solid {GRID_COLOR};")

        if com.p not in players:
            players[com.p] = 1
        else:
            players[com.p] += 1

        s = ""

        lst = sorted(players.items(), key=lambda item: item[1], reverse=True)

        cnt = 0
        for key, value in lst:
            cnt += 1
            s += f"{cnt}. {key} - {value}\n"
            if cnt == 5:
                break

        players = dict(lst)

        wdg_total.setText(f"Total Pixels Placed: {TOTAL}")
        top.setText(s)



hdl = threading.Thread(target=handle)
hdl.daemon = True
hdl.start()

# Show the widget and run the PyQt5 event loop
widget.show()
sys.exit(app.exec_())

