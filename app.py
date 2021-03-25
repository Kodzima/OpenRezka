from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import requests
from bs4 import BeautifulSoup as bs4
import time
import os
from panel import Ui_Form
from choose import Ui_choose
import json


class Ui_MainWindow(object):
   
    def get_url(url):
        url = url.replace('\/', '/')
        return url

    def start_film(url):
        try:
                response = requests.post(url)
                html = response.text
                all_quality = ['[1080p]','[720p]','[480p]','[360p]','[240p]','[144p]']
                for quality in all_quality:
                        videoIndex = html.find(f'{quality}https:\/\/')
                        if videoIndex > 0:
                                endUrlindex = html.find(':hls', videoIndex)
                                url = html[videoIndex + len(quality) : endUrlindex]
                                url = Ui_MainWindow.get_url(url)
                                os.system(f'vlc {url}')
                                break
        except:
                html = str(url)
                all_quality = ['[1080p]','[720p]','[480p]','[360p]','[240p]','[144p]']
                for quality in all_quality:
                        videoIndex = html.rfind(f'{quality}https://')
                        if videoIndex > 0:
                                endUrlindex = html.find(':hls', videoIndex)
                                url = html[videoIndex + len(quality) : endUrlindex]
                                os.system(f'vlc {url}')
                                break

    def panelFunc(self):
        global nameOfFilm
        self.Form = QtWidgets.QWidget()
        panel = Ui_Form()
        panel.setupUi(self.Form)
        panel.label.setText(ui.listWidget.currentItem().text())
        nameOfFilm = panel.label.text()
        type = types[names.index(ui.listWidget.currentItem().text())]

        if type == 'Сериал' or type == 'Аниме':
                panel.pushButton_2.setText('Выбрать серию')
        url_photo = photo_url[names.index(ui.listWidget.currentItem().text())]
        image = QtGui.QImage()
        image.loadFromData(requests.get(url_photo).content)
        panel.filmPoster.setPixmap(QtGui.QPixmap(image))
        self.Form.show()

        def get_url(url):
                url = url.replace('\/', '/')
                return url



        def get_type():
                type = types[names.index(panel.label.text())]
                if type == 'Сериал' or type == 'Аниме':
                        Ui_MainWindow.choose(self)
                else:
                        currentFilm = panel.label.text()
                        start_film(urls[names.index(currentFilm)])

        def start_film(url):
                response = requests.post(url)
                time.sleep(2)
                html = response.text
                all_quality = ['[1080p]','[720p]','[480p]','[360p]','[240p]','[144p]']
                for quality in all_quality:
                        videoIndex = html.find(f'{quality}https:\/\/')
                        if videoIndex > 0:
                                endUrlindex = html.find(':hls', videoIndex)
                                url = html[videoIndex + len(quality) : endUrlindex]
                                url = get_url(url)
                                os.system(f'vlc {url}')
                                break


        panel.pushButton_2.clicked.connect(get_type)




    def choose(self):
        def get_season():
                global dataId
                global altTranslateId
                series.listWidget.clear()
                series.listWidget_2.clear()
                index = series.comboBox.currentIndex()
                response = requests.get(urls[names.index(nameOfFilm)])
                html = response.text
                startIndex = html.find('initCDNSeriesEvents')
                endIndex = html.find('{',startIndex)
                html = html[startIndex : endIndex]
                html = html.split(',')
                dataId = str(html[0])
                endIndex = dataId.find('(')
                dataId = dataId[endIndex + 1:]

                if translatorsId != []:
                        payload = {
                                'id'  :	str(dataId),
                                'translator_id'	: str(translatorsId[index]),
                                'action' : "get_episodes"
                                }         
                else:
                        altTranslateId = html[1]
                        payload = {
                                'id'  :	str(dataId),
                                'translator_id'	: altTranslateId,
                                'action' : "get_episodes"
                                }                   

                response = requests.post(f'https://rezka.ag/ajax/get_cdn_series/?t={int(time.time()*1000)}', data = payload)
                jsonResponse = json.loads(response.content)
                response = jsonResponse['seasons']
                soup = bs4(response, 'lxml')
                items = soup.findAll('li',class_ = "b-simple_season__item")

                for item in items:
                        series.listWidget.addItem(item.get_text())
                
        def get_serias():
                series.listWidget_2.clear()
                index = series.comboBox.currentIndex()
                currentSeason = series.listWidget.currentItem().text()
                currentSeason = int(currentSeason.split()[1])
                if translatorsId != []:
                        payload = {
                                'id'  :	str(dataId),
                                'translator_id'	: str(translatorsId[index]),
                                'action' : "get_episodes"
                                }         
                else:
                        payload = {
                                'id'  :	str(dataId),
                                'translator_id'	: altTranslateId,
                                'action' : "get_episodes"
                                }           

                response = requests.post(f'https://rezka.ag/ajax/get_cdn_series/?t={int(time.time()*1000)}', data = payload)
                jsonResponse = json.loads(response.content)
                response = jsonResponse['episodes']
                soup = bs4(response, 'lxml')
                items = soup.find('ul',{'id' : f'simple-episodes-list-{currentSeason}'})

                for item in items:
                        series.listWidget_2.addItem(item.get_text())

        def start_serial():
                currentSeason = series.listWidget.currentItem().text()
                currentSeason = int(currentSeason.split()[1])
                currentEpisode = series.listWidget_2.currentItem().text()
                currentEpisode = int(currentEpisode.split()[1])
                index = series.comboBox.currentIndex()
                if translatorsId != []:
                        payload = {
                                'id'  :	str(dataId),
                                'translator_id'	: str(translatorsId[index]),
                                'season' : str(currentSeason),
                                'episode' : str(currentEpisode),
                                'action' : "get_stream"
                                }        
                else:
                        payload = {
                                'id'  :	str(dataId),
                                'translator_id'	: altTranslateId,
                                'season' : str(currentSeason),
                                'episode' : str(currentEpisode),
                                'action' : "get_stream"
                                }           

                response = requests.post(f'https://rezka.ag/ajax/get_cdn_series/?t={int(time.time()*1000)}', data = payload)
                jsonResponse = json.loads(response.content)
                response = jsonResponse['url']
                Ui_MainWindow.start_film(response)



        global translatorsId
        self.choose = QtWidgets.QWidget()
        series = Ui_choose()
        series.setupUi(self.choose)
        response = requests.post(urls[names.index(nameOfFilm)])
        soup = bs4(response.content, 'lxml')
        items = soup.findAll('li', class_ ='b-translator__item')
        translatorsId = []
        for item in items:
                translatorsId.append(item.get('data-translator_id'))
                series.comboBox.addItem(item.get('title'))
        
        series.comboBox.setCurrentIndex(0)
        get_season()
        
        self.choose.show()

        series.listWidget.clicked.connect(get_serias)
        series.pushButton.clicked.connect(start_serial)
        series.comboBox.currentIndexChanged.connect(get_season)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(773, 600)
        MainWindow.setStyleSheet("background-color: rgb(29, 45, 44);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalFrame.sizePolicy().hasHeightForWidth())
        self.horizontalFrame.setSizePolicy(sizePolicy)
        self.horizontalFrame.setStyleSheet("color: rgb(150, 150, 150);\n"
"")
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setStyleSheet("border:1px;\n"
"border-radius:5px;\n"
"background-color: rgb(42, 49, 47);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setStyleSheet("border:1px;\n"
"border-radius:5px;\n"
"background-color: rgb(42, 49, 47);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.label = QtWidgets.QLabel(self.horizontalFrame)
        font = QtGui.QFont()
        font.setFamily("Noto Sans Gurmukhi Thin")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setStyleSheet("border:1px;\n"
"border-radius:5px;\n"
"background-color: rgb(42, 49, 47);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setStyleSheet("border:1px;\n"
"border-radius:5px;\n"
"background-color: rgb(42, 49, 47);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addWidget(self.horizontalFrame)
        self.gridFrame_2 = QtWidgets.QFrame(self.centralwidget)
        self.gridFrame_2.setStyleSheet("background-color: rgb(37, 45, 50);")
        self.gridFrame_2.setObjectName("gridFrame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridFrame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.gridFrame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setStyleSheet("background-color: rgb(28, 42, 61);\n"
"color: rgb(53, 126, 165);\n"
"border:5px solid;\n"
"border-radius: 10px;\n"
"border-color: rgb(60, 72, 83);")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.listWidget = QtWidgets.QListWidget(self.gridFrame_2)
        self.listWidget.setStyleSheet("background-color: rgb(28, 42, 61);\n"
"color: rgb(53, 126, 165);\n"
"border:5px solid;\n"
"border-radius: 10px;\n"
"border-color: rgb(60, 72, 83);")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.listWidget.doubleClicked.connect(self.panelFunc)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.gridFrame_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def choose_film():
                for name in names:
                        ui.listWidget.addItem(name)

        

        def search():
                global names
                global urls
                global photo_url
                global types
                ui.listWidget.clear()
                name = ui.lineEdit.text()
                name = name.replace(' ', '+')
                response = requests.get(f'https://rezka.ag/search/?do=search&subaction=search&q={name}')
                soup = bs4(response.content, "lxml")
                items = soup.findAll('div', class_ = 'b-content__inline_item')
                names = []
                urls = []
                photo_url = []
                types = []
                for item in items:
                        names.append(item.find('div', class_ = 'b-content__inline_item-link').get_text())
                        urls.append(item.find('div', class_ = 'b-content__inline_item-link').find('a').get('href'))
                        photo_url.append(item.find('div', class_ ='b-content__inline_item-cover').find('img').get('src'))
                        types.append(item.find('i', class_='entity').get_text())
                choose_film()

        self.lineEdit.returnPressed.connect(search)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OpenRezka"))
        self.pushButton_5.setText(_translate("MainWindow", "О программе"))
        self.pushButton_4.setText(_translate("MainWindow", "Тестовая кнопка 2"))
        self.label.setText(_translate("MainWindow", "OpenRezka"))
        self.pushButton_3.setText(_translate("MainWindow", "Избранное"))
        self.pushButton_2.setText(_translate("MainWindow", "Тестовая кнопка"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Введите сюда ваш запрос"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    

    sys.exit(app.exec_())
