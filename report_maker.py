import os
import sys
import csv
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

path = ""
if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
elif __file__:
    path = os.path.dirname(__file__)

status = ""

def time_to_ms(time):
    fields = time.split(":")
    return ((int(fields[0]) * 60) + int(fields[1])) * 1000 + int(fields[2])

def time_diff(start_s, end_s):
    start = time_to_ms(start_s)
    end = time_to_ms(end_s)
    return end - start

def run(filename, savedir):
    global path, status
    new_path = path + '/' + filename
    file = ""
    try:
        file = open(new_path, 'r')
    except:
        try:
            file = open(new_path + ".txt", 'r')
        except:
            status = "plik o nazwie '" + filename + "' nie istnieje"
            return
    lines = file.readlines()
    lines = lines[7:]

    e_time = lines[-1].split(' ')
    e_time = e_time[0]
    total_time = time_to_ms(e_time)
    obstacle_crash = 0
    other_crash = 0
    speeding = 0

    current_ad = '-'

    fields = []
    log = [["czas reakcji [ms]","rodzaj przeszkody","grupa reklam", "rodzaj reakcji", "kolizja z przeszkodą"]]
    for i in range(len(lines)):
        fields.append(lines[i].replace("    ", " ").split(" "))

        #reklama
        if fields[-1][1] == "LED":
            if fields[-1][2] == "ON" and fields[-1][5] != "F\n" and fields[-1][5] != "E\n":
                current_ad = fields[-1][5][0]
            else:
                current_ad = '-'
                
        #czas reakcji
        if i > 0 and fields[-2][1] == "Przeszkoda":
            obstacle = ' '.join(fields[-2][1:])
            reaction = ' '.join(fields[-1][1:]) 
            obstacle = obstacle[0:-1]
            reaction = reaction[0:-1]
            log.append([time_diff(fields[-2][0], fields[-1][0]), obstacle, current_ad, reaction, "nie"])

        #liczba kolizji
        if fields[-1][1] == "Kolizja":
            if fields[-1][3] == "przeszkoda\n":
                obstacle_crash += 1
                log[-1][4] = "tak"
            else:
                other_crash += 1

        if fields[-1][1] == "Przekroczona":
            speeding += 1

    log = [l for l in log if 'Przeszkoda' not in l[3] and 'LED' not in l[3]]


    log.insert(0,["PODSUMOWANIE WYNIKÓW SYMULACJI"])
    log.insert(1,[])
    log.append([])
    log.append(["czas przejazdu [ms]:", total_time])
    log.append(["liczba kolizji z przeszkodą:", obstacle_crash])
    log.append(["liczba kolizji z otoczeniem:", obstacle_crash])
    log.append(["liczba przekroczeń prędkości:", speeding])

    if filename.endswith('.txt'):
        filename = filename[:-4]
    with open(os.path.join(savedir, filename + '_wyniki.csv'),'w',newline='') as file2:
        writer = csv.writer(file2)
        writer.writerows(log)
    print(os.path.join(savedir, filename, '_wyniki.csv'))
    status = "utworzono plik '" + filename + "_wyniki.csv'"
    file.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        margin = 106
        self.w = 400 + 2 * margin
        self.h = 270
        self.setGeometry(200, 200, self.w, self.h)
        self.setWindowTitle("wyniki symulacji")
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        # File selection
        file_layout = QtWidgets.QVBoxLayout()
        self.fileBtn = QtWidgets.QPushButton("Wybierz plik")
        self.fileBtn.clicked.connect(self.chooseFile)
        self.filePathLabel = QtWidgets.QLabel("")
        self.filePathLabel.setWordWrap(True)
        file_layout.addWidget(self.fileBtn)
        file_layout.addWidget(self.filePathLabel)
        layout.addLayout(file_layout)

        # Directory selection
        dir_layout = QtWidgets.QVBoxLayout()
        self.dirBtn = QtWidgets.QPushButton("Wybierz miejsce zapisu")
        self.dirBtn.clicked.connect(self.chooseOutputDir)
        self.dirPathLabel = QtWidgets.QLabel("")
        self.dirPathLabel.setWordWrap(True)
        dir_layout.addWidget(self.dirBtn)
        dir_layout.addWidget(self.dirPathLabel)
        layout.addLayout(dir_layout)

        # Calculate button
        self.btn = QtWidgets.QPushButton("Stwórz raport")
        self.btn.clicked.connect(self.clicked)
        layout.addWidget(self.btn, alignment=QtCore.Qt.AlignCenter)

        # Info label
        self.info = QtWidgets.QLabel("")
        self.info.setStyleSheet("QLabel { color : red; }")
        self.info.setWordWrap(True)
        layout.addWidget(self.info)

        # Initialize variables
        self.selectedFile = ""
        self.outputDir = ""

    def chooseFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "Text Files (*.txt)")
        if filename.endswith('.txt'):
            self.selectedFile = filename
            self.filePathLabel.setText(f"Wybrany plik: {filename}")
            self.filePathLabel.adjustSize()
        else:
            self.filePathLabel.setText("Wybrano nieprawidłowy plik. Proszę wybrać plik .txt")
            self.filePathLabel.adjustSize()

    def chooseOutputDir(self):
        directory = QFileDialog.getExistingDirectory(self, "Wybierz folder zapisu")
        if directory:
            self.outputDir = directory
            self.dirPathLabel.setText(f"Folder zapisu: {directory}")
            self.dirPathLabel.adjustSize()

    def clicked(self):
        global status
        if self.selectedFile and self.outputDir:
            # wyodrębnianie nazwy pliku bez ścieżki
            local_name = os.path.splitext(os.path.basename(self.selectedFile))[0]
            # ustawienie ścieżki pliku jako globalnej zmiennej path
            global path
            path = os.path.dirname(self.selectedFile)
            run(local_name, self.outputDir)
            # przenoszenie wygenerowanego pliku do wybranego folderu
            src = os.path.join(path, local_name + "_wyniki.csv")
            dst = os.path.join(self.outputDir, local_name + "_wyniki.csv")
            if os.path.exists(src):
                os.rename(src, dst)
            self.info.setText(status)
            self.info.adjustSize()
        else:
            self.info.setText("Nie wybrano pliku lub miejsca zapisu.")
            self.info.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

window()
