from PyQt5 import QtCore, QtGui, QtWidgets
import pickle
import cv2
import face_recognition
from glob import glob
import os, sqlite3, shutil
import random
import sqlite3 as sql

from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 320)
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color:#4f545c;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 110, 381, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("background-color:#72767d;\n"
                                    "color: #fff;\n"
                                    "")
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(100, 20, 180, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.textEdit_2.setFont(font)
        self.textEdit_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.textEdit_2.setStyleSheet("background-color:#72767d;\n"
                                      "color: #fff;")
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 280, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setMouseTracking(True)
        self.pushButton.setStyleSheet("border-radius: 8px;\n"
                                      "background-color: #72767d;\n"
                                      "color: white;\n"
                                      "\n"
                                      "")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 60, 70, 30))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setMouseTracking(True)
        self.pushButton_2.setTabletTracking(False)
        self.pushButton_2.setStyleSheet("\n"
                                        "border-radius: 8px;\n"
                                        "background-color: #72767d;\n"
                                        "color: white;\n"
                                        "")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(65, 60, 250, 30))
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium Cond")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setMouseTracking(True)
        self.pushButton_3.setTabletTracking(False)
        self.pushButton_3.setStyleSheet("\n"
                                        "border-radius: 8px;\n"
                                        "background-color: #72767d;\n"
                                        "color: white;\n"
                                        "")
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Распознавание лиц"))
        MainWindow.setWindowIcon(QtGui.QIcon('icon2.png'))
        self.textEdit.setPlaceholderText(
            _translate("MainWindow", "Нажмите на кнопку 'Открыть' и добавьте 5 и более фотографий в папку."))
        self.textEdit_2.setPlaceholderText(_translate("MainWindow", "Введите имя"))
        self.pushButton.setText(_translate("MainWindow", "Запустить"))
        self.pushButton.clicked.connect(self.detect)
        self.pushButton_2.setText(_translate("MainWindow", "Открыть"))
        self.pushButton_2.setToolTip("Добавить фото")
        self.pushButton_2.clicked.connect(self.openDataset)
        self.pushButton_3.setText(_translate("MainWindow", "Сохранить пользователя в базу данных"))
        self.pushButton_3.clicked.connect(self.train_model)

    def openDataset(self):
        os.system("explorer.exe c:\\dataset")

    def detect(self):
        sp = []
        j = 0
        for i in glob('pickle/*.pickle'):
            print(i)
            sp.append(i)
        data = pickle.loads(open(sp[0], "rb").read())
        cap = cv2.VideoCapture(0)
        while True:

            d = {"name": "unknown"}
            ret, image = cap.read()
            location = face_recognition.face_locations(image, model='hog')
            encoding = face_recognition.face_encodings(image, location)

            for face_encoding, face_location in zip(encoding, location):
                result = face_recognition.compare_faces(data['enc'], face_encoding)
                match = None
                print(result)

                if True in result:
                    match = data['name']
                    # print(f'Добро пожаловать {match}')
                else:
                    match = d['name']
                    if j + 1 < len(sp):
                        data = pickle.loads(open(sp[j + 1], "rb").read())
                        j += 1
                    else:
                        j = -1
                    print(j)
                    # print(f'Пользователь не распознан')
                left_top = (face_location[3], face_location[0])
                right_bottom = (face_location[1], face_location[2])
                color = [255, 255, 255]
                cv2.rectangle(image, left_top, right_bottom, color, 3)
                left_bottom = (face_location[3], face_location[2])
                right_bottom = (face_location[1], face_location[2] + 20)
                cv2.rectangle(image, left_bottom, right_bottom, color, cv2.FILLED)
                cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 0), 2)

            cv2.imshow('Esc-close', image)

            k = cv2.waitKeyEx(20)
            if k == 27:
                self.textEdit.appendHtml('Нажата ESC распознавание закрыто.')
                cv2.destroyAllWindows()
                break

    def train_model(self):
        name = self.textEdit_2.toPlainText()
        names = []
        id_user = random.randint(100000, 999999)
        for l in glob('pickle/*.pickle'):
            names.append(l.split('\\')[1].split('_')[0])
        if any(e in name for e in names):  # проверка на имя
            self.textEdit.appendHtml('Имя занято.')
        elif name == '':
            self.textEdit.appendHtml('Поле пустое.')
        elif any(e in name for e in names) == False:

            self.textEdit.appendHtml(f'Идентификатор: {name}.{id_user}')
            self.textEdit.appendHtml(f'Файл {name}_enc.pickle')
            known_encodings = []
            images = os.listdir("C:/dataset")

            # print(images)
            for (i, image) in enumerate(images):
                self.textEdit.appendHtml(f"[+] создание по фото {i + 1}/{len(images)}")

                face_img = face_recognition.load_image_file(f"C:\dataset\{image}")
                face_enc = face_recognition.face_encodings(face_img)[0]

                if len(known_encodings) == 0:
                    known_encodings.append(face_enc)

                else:
                    for item in range(0, len(known_encodings)):
                        result = face_recognition.compare_faces([face_enc], known_encodings[item])
                        if result[0]:
                            known_encodings.append(face_enc)
                            break
                        else:
                            break
            if len(known_encodings) == 0:
                self.textEdit.appendHtml(f'Загрузите фотографии, колличество: {len(known_encodings)}')
            else:
                self.textEdit.appendHtml(f'Обработано фотографий: {len(known_encodings)}')
                data = {
                    "name": name,
                    "enc": known_encodings
                }

                with open(f"pickle/{name}_enc.pickle", "wb") as file:
                    file.write(pickle.dumps(data))

                con = sql.connect('data.sqlite3')  # добавление в бд
                cur = con.cursor()
                self.textEdit.appendHtml(f"подключение к бд")
                with open(f'pickle/{name}_enc.pickle', 'rb') as file:
                    photo = file.read()
                    cur.execute('''INSERT INTO photos(id, name, photo) VALUES(?, ?, ?)''', [id_user, name, photo])
                con.commit()
                cur.close()
                con.close()
                # return self.textEdit.append(f"Данные сохранены.")
                return self.textEdit.appendHtml(f"Данные сохранены.{id_user},{name}")





def createDataset():
    if not os.path.exists('C:/dataset'):  # проверка на папку с фотографиями
        os.mkdir('C:/dataset')  # папка dataset создана


def exportDb():
    con = sqlite3.connect('data.sqlite3')
    cur = con.cursor()
    query = 'SELECT name, photo FROM photos'
    cur.execute(query)
    photos = cur.fetchall()
    if not os.path.exists('pickle'):  # проверка на папку с фотографиями
        os.mkdir('pickle')
        print('Папка pickle создана.')
        for row in photos:
            print(f'{row[0]}_enc.pickle')
            with open(f'pickle/{row[0]}_enc.pickle', 'wb') as f:
                f.write(row[1])
    con.commit()
    cur.close()
    con.close()


def close():
    path_p = 'pickle'
    path_d = 'C:/dataset'
    shutil.rmtree(path_p)
    shutil.rmtree(path_d)
    print('папки удалены')
# def button(self):
#     self.pushButton_2.clicked.connect(self.savePhoto)
#     self.pushButton_4.clicked.connect(self.getFileNames)


if __name__ == "__main__":
    import sys
createDataset()
exportDb()
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
status = app.exec_()
close()
sys.exit(status)
