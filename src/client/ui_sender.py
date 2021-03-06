import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QScrollArea, QPushButton, QLabel, QWidget, QVBoxLayout

import sender

class FileButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_src = ''

    def setFileSource(self, e):
        self.file_src = e

    def getFileSource(self):
        return self.file_src


class ScrollFrame(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.form = QtWidgets.QFormLayout()
        self.setFixedHeight(121)
        self.container = parent
        self.groupBox = QtWidgets.QGroupBox('')
        self.files = []

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            print('Accepted')
        else:
            e.ignore()
            print('Ignored')
        self.setStyleSheet("background: rgb(30, 136, 229);\n"
                           "border: 1px solid rgb(25, 118, 210);\n"
                           "color: white")

    def dragLeaveEvent(self, e):
        self.setStyleSheet("background: rgb(150, 150, 150);\n"
                           "border: 1px solid rgb(150, 150, 150);\n"
                           "color: white")

    def dropEvent(self, e):
        self.setStyleSheet("QScrollArea{\n"
                            "    color: white;\n"
                            "}\n"
                            "QLabel{\n"
                            "    color: white;\n"
                            "}\n"
                            "QPushButton {\n"
                            "    background: rgb(232, 232, 232);\n"
                            "    color: white;\n"
                            "    border: 1px solid rgb(227, 227, 227);\n"
                            "}\n"
                            "\n"
                            "QPushButton:hover {\n"
                            "    background: rgb(255,0,0);\n"
                            "    border: 1px solid rgb(255,0,0);\n"
                            "}\n"
                            "\n"
                            "QPushButton:pressed {\n"
                            "    background: rgb(182,0,0);\n"
                            "    border: 1px solid rgb(182,0,0);\n"
                            "}\n"
                            "\n"
                            "QWidget {\n"
                            "    background: rgb(120, 120, 120);\n"
                            "}\n"
                            "\n"
                            "")
        if (self.form.rowCount() == 0):
            self.container.switchLabel(False)

        for url in e.mimeData().urls():
            f, file_src = str(url.toString()).split('///')
            file_dir, file_name = os.path.split(file_src)

            print(file_src)
            label = QLabel(file_name)
            btn = FileButton('Remove')

            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)

            label.setFont(font)
            label.setFixedWidth(270)
            btn.setFont(font)
            btn.setFixedWidth(50)
            btn.setFixedHeight(20)

            btn.setFileSource(str(file_src))

            btn.clicked.connect(self.clickedRemove)

            self.form.addRow(label, btn)

        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)

    def clickedRemove(self):
        self.form.removeRow(self.sender())

        if (self.form.rowCount() == 0):
            self.container.switchLabel(True)

    def uploadFiles(self):
        for i in range(self.form.rowCount() * 2):
            if (i % 2):
                self.files.append(self.form.itemAt(i).widget().getFileSource())

        for f in self.files:
            print(f'File: {f}')
            self.container.sender.sendToServer(f)
        data = ''
        with open('received_output.txt') as f:
            for i, l in enumerate(f):
                self.container.outputFrame.addLine(l)

        self.container.loadingWindow.hide()
        self.container.outputFrame.show()
        self.container.outputDetailsLabel.show()


class OutputFrame(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.form = QtWidgets.QFormLayout()
        self.setFixedHeight(121)
        self.container = parent
        self.groupBox = QtWidgets.QGroupBox('')
        self.files = []

    def addLine(self, e):
        label = QLabel(e)
        label.setStyleSheet('color: white')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        label.setFont(font)
        label.setFixedHeight(14)
        label.adjustSize()

        self.form.addRow(label)
        self.groupBox.setLayout(self.form)
        self.setWidget(self.groupBox)


class LoadingWindow(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(LoadingWindow, self).__init__(parent)
        self.loadingLabel = QtWidgets.QLabel(self)
        self.loadingLabel.setStyleSheet('color: white')
        self.loadingLabel.setGeometry(QtCore.QRect(135, 100, 144, 17))
        self.loadingLabel.setText('Loading...')
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.loadingLabel.setFont(font)
        self.loadingLabel.setObjectName("loadingLabel")
        self.loadingLabel.adjustSize()

class DDWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Rendt Sender Demo')
        self.setWindowIcon(QtGui.QIcon('../../assets/img/rendt_new_logo_square.png'))
        self.resize(421, 283)
        self.setStyleSheet("QPushButton {\n"
                                "    background: rgb(232, 232, 232);\n"
                                "    border: 1px solid rgb(227, 227, 227);\n"
                                "}\n"
                                "\n"
                                "QPushButton:hover {\n"
                                "    background: rgb(200, 200, 200);\n"
                                "}\n"
                                "\n"
                                "QPushButton:pressed {\n"
                                "    background: rgb(150, 150, 150);\n"
                                "}\n"
                                "\n"
                                "QWidget {\n"
                                "    background: rgb(120, 120, 120);\n"
                                "}\n"
                                "\n"
                                "")

        # Setting up the layout
        self.layout = QVBoxLayout()

        # Setting up the label and configuring it
        self.label = QLabel(self)
        self.label.setText('Drag & Drop')
        self.label.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")

        # Adding Scroll Frame where the Dragging and Dropping will happen
        self.scroll = ScrollFrame(self)
        self.scroll.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.scroll.setStyleSheet("background: rgb(150, 150, 150);\n"
                                  "border: 1px solid rgb(150, 150, 150);\n")
        self.scroll.setWidgetResizable(True)

        # Setting up the label inside the frame and configuring it
        self.uploadLabel = QLabel(self.scroll)
        self.uploadLabel.setStyleSheet('color: white')
        self.uploadLabel.setGeometry(QtCore.QRect(100, 50, 144, 17))
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)

        self.uploadLabel.setFont(font)
        self.uploadLabel.setObjectName("uploadLabel")
        self.uploadLabel.setText('Drag & Drop files here')
        self.uploadLabel.adjustSize()

        # Adding the 'Upload' button and configuring it
        self.uploadBtn = QPushButton(self)
        self.uploadBtn.setGeometry(QtCore.QRect(320, 200, 71, 31))
        self.uploadBtn.setText('Upload')

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        self.uploadBtn.setFont(font)
        self.uploadBtn.setStyleSheet("color: white;")
        self.uploadBtn.setObjectName("uploadBtn")
        self.uploadBtn.clicked.connect(self.startLoadingWindow)

        # Setting up Loading Screen
        self.loadingWindow = LoadingWindow(self)
        self.loadingWindow.hide()

        # Adding Output Details Label
        self.outputDetailsLabel = QLabel(self)
        self.outputDetailsLabel.setText('Received Output')
        self.outputDetailsLabel.setGeometry(QtCore.QRect(30, 20, 210, 43))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)

        self.outputDetailsLabel.setFont(font)
        self.outputDetailsLabel.setStyleSheet("color: white;")
        self.outputDetailsLabel.adjustSize()
        self.outputDetailsLabel.hide()

        # Adding Ouput Frame
        self.outputFrame = OutputFrame(self)
        self.outputFrame.setGeometry(QtCore.QRect(30, 70, 361, 121))
        self.outputFrame.setStyleSheet("background: rgb(150, 150, 150);\n"
                                  "border: 1px solid rgb(150, 150, 150);\n")
        self.outputFrame.setWidgetResizable(True)
        self.outputFrame.hide()

        # Adding everything into the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.uploadLabel)
        self.layout.addWidget(self.uploadBtn)
        self.layout.addWidget(self.loadingWindow)
        self.layout.addWidget(self.outputDetailsLabel)
        self.layout.addWidget(self.outputFrame)

        # Creating Sender class instance
        self.sender = sender.Sender()
    
    def startLoadingWindow(self):
        self.label.hide()
        self.scroll.hide()
        self.uploadLabel.hide()
        self.uploadBtn.hide()
        self.loadingWindow.show()
        
        self.scroll.uploadFiles()
    
    def switchLabel(self, flag):
        if (flag):
            self.uploadLabel.show()
        else:
            self.uploadLabel.hide()
        

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)

    window = DDWindow()
    window.show()

    sys.exit(app.exec_())
