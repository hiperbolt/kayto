from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog
import background_rc
import sys
import ethernetprotocolapi
import json
import subprocess
import time

def handleExit():
    print("Exiting!")
    try:
        p.terminate()
    except AttributeError:
        pass
    subprocess.Popen(["python", "exithandler.py", ip, port])

def handleErr(err):
    outputToUi("ERROR: " + err)

def convertToSeconds(timecode): ## WARNING: HOURS NOT IMPLEMENTED. TIMELINE CLIPS OVER AN HOUR LONG WILL NOT WORK. shit will happen
    convertedTime = 0
    minutes = int(timecode[:2])
    seconds = int(timecode[-2:])
    for i in range(0, minutes):
        convertedTime += 60
    convertedTime += seconds
    return convertedTime

def FileDialogExport():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)

    dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setAcceptMode(QFileDialog.AcceptSave)
    dialog.setDefaultSuffix("ktmf")
    dialog.setNameFilters([f'{"Kayto Timeline File"} (*.{"ktmf"})'])
    if dialog.exec_() == QDialog.Accepted:
        return dialog.selectedFiles()[0]

def FileDialog():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)

    dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setAcceptMode(QFileDialog.AcceptOpen)
    dialog.setDefaultSuffix("ktmf")
    dialog.setNameFilters([f'{"Kayto Timeline File"} (*.{"ktmf"})'])
    if dialog.exec_() == QDialog.Accepted:
        path = dialog.selectedFiles()[0]
        return path
    else:
        return ''

def addToCustomTimeline(self):
    if clips != '':
        global customTimeline
        if customTimeline == None:
            if timelineContent != '':
                customTimeline = timelineContent
            else:
                customTimeline = []
        try:
            customTimeline.append(clips[self.spinBox.value()])
            self.textBrowser_2.append(clips[self.spinBox.value()])
        except IndexError:
            handleErr("Out of range!")
    else:
        handleErr("No Clips loaded!")

def removeFromCustomTimeline(self):
    global customTimeline
    if customTimeline == None:
        if timelineContent != '':
            customTimeline = timelineContent
        else:
            handleErr("No timeline!")
            return
    try:
        del customTimeline[-self.spinBox_2.value()]
    except IndexError:
        handleErr("Out of range!")

def exportTimeline():
    global customTimeline
    global path
    if customTimeline == [] or customTimeline == None:
        handleErr("No timeline to export!")
        return
    exportFile = FileDialogExport()
    try:
        with open(exportFile, "w+") as f:
            f.write(str(customTimeline))
    except TypeError:
        return
    path = exportFile
    customTimeline = None

def importTimeline():
    global customTimeline
    global path
    path = FileDialog()
    if path == '':
        return
    if set(eval(open(path, "r").read())).issubset(clips) == True: #DANGEROUS!! TRUSTING INPUT TO BE CORRECT!! IF THE .KTMF FILE IS CORRUPTED SHIT WILL HAPPEN.
        customTimeline = None
    else:
        path = ''
        handleErr("TIMELINE CLIPS NOT ALL PRESENT ON DISK!")

def outputToUi(output): #WIP, get a custom error / sucess message for each code. Ex "Started recording!" for record.
    global outputBuffer
    try:
        outputBuffer = output.decode("utf-8")
    except:
        outputBuffer = output

def actions(self, action):
    if action == "ping":
        if ethernetprotocolapi.ping(ip, port) != "err":
            self.label_2.setText("Sucessfull")
        else:
            self.label_2.setText("Unsucessfull :(")

    if self.label_2.text() == "Sucessfull": # IF SUCCESFULL CONNECTION:
        if action == "toggleSlot":
            outputToUi(ethernetprotocolapi.toggleSlot(ip, port))

        if self.radioButton.isChecked() == True: # TIMELINE MODE ACTIONS:

            if path == '':
                handleErr("No timeline imported!")
                return

            if customTimeline != None:
                handleErr("You must first save your custom timeline!")
                return

            global toPlayClip
            if action == "play":
                if self.checkBox.isChecked() == True: #IF SINGLE CLIP PLAYBACK:
                    if toPlayClip < len(timelineContent):
                        ethernetprotocolapi.playRange(ip, port, "set", clipId=int(timelineContent[toPlayClip][:1]))
                        time.sleep(0.2)
                        ethernetprotocolapi.play(ip, port)
                        toPlayClip += 1
                    else:
                        handleErr("End of Timeline! Resetting!")
                        ethernetprotocolapi.stop(ip, port) #Failsafe in case there was playback when reset was reached, prevents the whole disklist from playing
                        ethernetprotocolapi.playRange(ip, port, "clear")
                        toPlayClip = 0
                else: # IF NOT SINGLE CLIP PLAYBACK:
                    global p
                    p = subprocess.Popen(["python", "timeline_watchdog.py", path, ip, port])
                    outputToUi("Started Timeline Watchdog")

            if action == "stop":
                if self.checkBox.isChecked() == True: # IF SINGLE CLIP:
                    ethernetprotocolapi.stop(ip, port)
                    toPlayClip -= 1
                else: # IF NOT SINGLE CLIP:
                    p.terminate()
                    ethernetprotocolapi.stop(ip, port)


        else: # NON-TIMELINE MODE ACTIONS:
            if action == "play":
                ethernetprotocolapi.play(ip, port)
            elif action == "stop":
                ethernetprotocolapi.stop(ip, port)
            elif action == "record":
                ethernetprotocolapi.record(ip, port)
            elif action == "backLogic":
                backLogic()
            elif action == "frontLogic":
                frontLogic()
    else:
        handleErr("NO CONNECTION. TRY TO PING!")

def updateCustomTimeline(self):
    self.textBrowser_2.clear()
    for customclip in customTimeline:
        self.textBrowser_2.append(customclip)

def updateTimeline(self):
    global timelineContent
    global path
    if set(eval(open(path, "r").read())).issubset(clips) == False:
        path = ''
        self.textBrowser_2.clear()
        handleErr("TIMELINE CLIPS NOT ALL PRESENT ON DISK!")
        return

    if timelineContent != eval(open(path, "r").read()):
        self.textBrowser_2.clear()
        for tlclip in eval(open(path, "r").read()):
            self.textBrowser_2.append(tlclip)
            timelineContent = eval(open(path, "r").read())

def updateClips(self):
    global clips
    if ethernetprotocolapi.diskList(ip, port).decode("utf-8").splitlines() != clips:
        clips = ethernetprotocolapi.diskList(ip, port).decode("utf-8").splitlines()[6:][:-1]
        self.textBrowser.clear()
        for clip in clips:
            self.textBrowser.append(clip)

def jogLogic(self, state):
    if state == "pressed":
        while True:
            print("pressed loop")
    elif state == "released":
        print("released")


def backLogic():
    if str(ethernetprotocolapi.transportInfo(ip, port).split(b"timecode: ",1)[1][:11].decode("utf-8")) == "00:00:00:00": #Go to previous clip because we're at the start of one alredy
            response = ethernetprotocolapi.gotoClip(ip, port, "prev")
            outputToUi(response) #Handle response
    else: #We're mid clip, go to the beggining
        ethernetprotocolapi.clip(ip, port, "start")

def frontLogic():
    ethernetprotocolapi.gotoClip(ip, port, "next")


def fileRetrive(arg):
    with open("configFile.json", "r") as f:
        return json.load(f)[arg]

def fileSet(arg, setting):
    with open("configFile.json", "r+") as f:
                data = json.load(f)
                data[arg] = setting
                f.seek(0)
                json.dump(data, f)
                f.truncate()

ip = fileRetrive("IP")
port = fileRetrive("PORT")
timerInterval = 500
outputBuffer = ''
clips = ''
timeline = ''
p = ''
path = ''
timelineContent = ''
customTimeline = None
toPlayClip = 0

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(90, 20, 201, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(90, 50, 201, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(90, 90, 51, 31))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(300, 250, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        self.actionsUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Kayto - Connection Settings"))
        self.comboBox.setItemText(0, _translate("Dialog", "Blackmagic Hyperdeck Studio Mini "))
        self.label.setText(_translate("Dialog", "Device Type:"))
        self.label_2.setText(_translate("Dialog", "IP Address:"))
        self.plainTextEdit.setPlainText(_translate("Dialog", str(fileRetrive("IP"))))
        self.label_3.setText(_translate("Dialog", "TCP Port:"))
        self.plainTextEdit_2.setPlainText(_translate("Dialog", str(fileRetrive("PORT"))))
        self.pushButton.setText(_translate("Dialog", "Apply"))

    def actionsUi(self, Dialog):
        self.pushButton.clicked.connect(lambda: self.updateFile(Dialog))

    def updateFile(self, Dialog):
        fileSet("IP", self.plainTextEdit.toPlainText())
        fileSet("PORT", self.plainTextEdit_2.toPlainText())
        global ip
        global port
        ip = fileRetrive("IP")
        port = fileRetrive("PORT")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1917, 936)
        MainWindow.setMinimumSize(QtCore.QSize(1917, 936))
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet("")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background: url(:/resources/img.jpeg)")
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 340, 161, 71))
        self.pushButton.setStyleSheet("background: transparent")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 150, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setStyleSheet("background: transparent")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 150, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background: transparent")
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 190, 151, 41))
        self.pushButton_2.setStyleSheet("background:rgb(255, 255, 255)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 190, 121, 41))
        self.pushButton_3.setStyleSheet("background:rgb(255, 255, 255)")
        self.pushButton_3.setObjectName("pushButton_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(590, 410, 381, 331))
        self.textBrowser.setStyleSheet("background:rgb(255, 255, 255)")
        self.textBrowser.setObjectName("textBrowser")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(590, 380, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background: transparent")
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setObjectName("label_3")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(1090, 410, 371, 331))
        self.textBrowser_2.setStyleSheet("background:rgb(255, 255, 255)")
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1090, 380, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background: transparent")
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setObjectName("label_4")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(830, 750, 131, 21))
        self.pushButton_4.setStyleSheet("background:rgb(255, 255, 255)")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(1340, 380, 121, 21))
        self.pushButton_5.setStyleSheet("background:rgb(255, 255, 255)")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(1200, 380, 121, 21))
        self.pushButton_6.setStyleSheet("background:rgb(255, 255, 255)")
        self.pushButton_6.setObjectName("pushButton_6")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(560, 160, 441, 71))
        self.textBrowser_3.setStyleSheet("background:rgb(255, 255, 255)")
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(440, 180, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background: transparent")
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setObjectName("label_5")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(1330, 750, 131, 21))
        self.pushButton_7.setStyleSheet("background:rgb(255, 255, 255)")
        self.pushButton_7.setObjectName("pushButton_7")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(1150, 750, 101, 21))
        self.checkBox.setStyleSheet("background: transparent")
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(1100, 750, 51, 21))
        self.checkBox_2.setStyleSheet("background: transparent")
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(1600, 690, 221, 41))
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setProperty("value", 50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(310, 340, 161, 71))
        self.pushButton_8.setStyleSheet("background: transparent")
        self.pushButton_8.setText("")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(110, 460, 161, 71))
        self.pushButton_9.setStyleSheet("background: transparent")
        self.pushButton_9.setText("")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(110, 590, 161, 71))
        self.pushButton_10.setStyleSheet("background: transparent")
        self.pushButton_10.setText("")
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(310, 590, 161, 71))
        self.pushButton_11.setStyleSheet("background: transparent")
        self.pushButton_11.setText("")
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(310, 460, 161, 71))
        self.pushButton_12.setStyleSheet("background: transparent")
        self.pushButton_12.setText("")
        self.pushButton_12.setObjectName("pushButton_12")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(240, 290, 91, 31))
        self.radioButton.setStyleSheet("background:rgb(255, 255, 255)")
        self.radioButton.setObjectName("radioButton")
        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(780, 750, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(1280, 750, 42, 22))
        self.spinBox_2.setObjectName("spinBox_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1917, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuTimeline = QtWidgets.QMenu(self.menubar)
        self.menuTimeline.setObjectName("menuTimeline")
        self.menuSlots = QtWidgets.QMenu(self.menubar)
        self.menuSlots.setObjectName("menuSlots")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport_Different_Timeline = QtWidgets.QAction(MainWindow)
        self.actionImport_Different_Timeline.setObjectName("actionImport_Different_Timeline")
        self.actionExport_Current_Timeline = QtWidgets.QAction(MainWindow)
        self.actionExport_Current_Timeline.setObjectName("actionExport_Current_Timeline")
        self.actionToggle_Slot = QtWidgets.QAction(MainWindow)
        self.actionToggle_Slot.setObjectName("actionToggle_Slot")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menuTimeline.addAction(self.actionImport_Different_Timeline)
        self.menuTimeline.addAction(self.actionExport_Current_Timeline)
        self.menuSlots.addAction(self.actionToggle_Slot)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTimeline.menuAction())
        self.menubar.addAction(self.menuSlots.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.actionsUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.timer = QtCore.QTimer()
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Last ping:</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">?</span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Connectivity Settings"))
        self.pushButton_3.setText(_translate("MainWindow", "Try Ping"))
        self.label_3.setText(_translate("MainWindow", "Clips:"))
        self.label_4.setText(_translate("MainWindow", "Timeline:"))
        self.pushButton_4.setText(_translate("MainWindow", "Add to Timeline"))
        self.pushButton_5.setText(_translate("MainWindow", "Export Timeline"))
        self.pushButton_6.setText(_translate("MainWindow", "Import Timeline"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Output:</span></p></body></html>"))
        self.pushButton_7.setText(_translate("MainWindow", "Remove from Timeline"))
        self.checkBox.setText(_translate("MainWindow", "Stop at each clip"))
        self.checkBox_2.setText(_translate("MainWindow", "Loop"))
        self.radioButton.setText(_translate("MainWindow", "Timeline Mode"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTimeline.setTitle(_translate("MainWindow", "Timeline"))
        self.menuSlots.setTitle(_translate("MainWindow", "Slots"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionImport_Different_Timeline.setText(_translate("MainWindow", "Import Different Timeline"))
        self.actionExport_Current_Timeline.setText(_translate("MainWindow", "Export Current Timeline"))
        self.actionToggle_Slot.setText(_translate("MainWindow", "Toggle Slot"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    def actionsUi(self, MainWindow):
        self.pushButton.clicked.connect(lambda: actions(self, "play"))
        self.pushButton_2.clicked.connect(lambda: Dialog.show())
        self.pushButton_3.clicked.connect(lambda: actions(self, "ping"))
        self.pushButton_4.clicked.connect(lambda: addToCustomTimeline(self))
        self.pushButton_5.clicked.connect(lambda: exportTimeline())
        self.pushButton_6.clicked.connect(lambda: importTimeline())
        self.pushButton_7.clicked.connect(lambda: removeFromCustomTimeline(self))
        self.pushButton_8.clicked.connect(lambda: actions(self, "stop"))
        self.pushButton_9.clicked.connect(lambda: actions(self, "record"))
        self.pushButton_10.clicked.connect(lambda: actions(self, "backLogic"))
        self.pushButton_11.clicked.connect(lambda: actions(self, "frontLogic"))
        #self.horizontalSlider.sliderPressed.connect(lambda: jogLogic(self, "pressed"))  NOT IMPLEMENTED
        #self.horizontalSlider.sliderReleased.connect(lambda: jogLogic(self, "released")) NOT IMPLEMENTED
        self.actionToggle_Slot.triggered.connect(lambda: actions(self, "toggleSlot"))
        self.actionQuit.toggled.connect(lambda: sys.exit(0))
        self.timer.timeout.connect(lambda: self.updateWindow(MainWindow))
        self.timer.start(timerInterval)

    def updateWindow(self, MainWindow):
        global ip
        global port
        global outputBuffer
        ip = fileRetrive("IP")
        port = fileRetrive("PORT")
        if outputBuffer != "":
            self.textBrowser_3.append(outputBuffer)
            outputBuffer = ""
        if self.label_2.text() == "Sucessfull":
            updateClips(self)
        if path != "":
            if customTimeline == None:
                updateTimeline(self)
            else:
                updateCustomTimeline(self)
        else:
            if customTimeline != None:
                updateCustomTimeline(self)

if __name__ == "__main__":
    print("Starting Kayto...")
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(lambda: handleExit())
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
