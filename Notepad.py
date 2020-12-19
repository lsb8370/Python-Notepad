#QTPY

#참조
#https://www.youtube.com/watch?v=Ss7dDDS-DhU&list=PLnIaYcDMsScwsKo1rQ18cLHvBdjou-kb5&ab_channel=%EC%9E%AC%EC%A6%90%EB%B3%B4%ED%94%84
#https://wikidocs.net/35478
#https://appia.tistory.com/298


import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QFileDialog, QTextEdit, QHBoxLayout, QVBoxLayout, QDialog, QDialogButtonBox, QLineEdit, QLabel

class ReplaceDialog(QDialog):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.setWindowTitle('바꾸기')

        self.findLabel = QLabel('찾을 내용', self)
        self.findInput = QLineEdit(self)

        self.replaceLabel = QLabel('바꿀 내용', self)
        self.replaceInput = QLineEdit(self)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setText('모두 바꾸기')
        self.buttonBox.button(QDialogButtonBox.Cancel).setText('취소')
        self.buttonBox.accepted.connect(self.replace)
        self.buttonBox.rejected.connect(self.cancel)

        self.layout = QVBoxLayout()

        self.findLayout = QHBoxLayout()
        self.findLayout.addWidget(self.findLabel)
        self.findLayout.addWidget(self.findInput)
        self.layout.addLayout(self.findLayout)

        self.replaceLayout = QHBoxLayout()
        self.replaceLayout.addWidget(self.replaceLabel)
        self.replaceLayout.addWidget(self.replaceInput)
        self.layout.addLayout(self.replaceLayout)

        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def replace(self):
        self.text = self.text.replace(self.findInput.text(), self.replaceInput.text())
        self.accept()

    def cancel(self):
        self.reject()

    def get_text(self):
        return self.text

class QtGUI(QMainWindow):
    contextLength = 0
    timer = 0.0

    undoStack = ""

    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("메모장")
        menubar = self.menuBar()

        Filemenu = menubar.addMenu("파일")
        Filemenu1 = menubar.addMenu("편집")
        Filemenu2 = menubar.addMenu("서식")

        # 파일 메뉴 Action 정의
        # newfile = QAction('새로 만들기', self)
        loadfile = QAction('열기', self)
        savefile = QAction('저장', self)
        exit = QAction('끝내기', self)
        
        # 수정 메뉴 Action 정의
        undotext = QAction('실행 취소', self)
        replacetext = QAction('바꾸기', self)

        # 서식 메뉴 Action 정의
        # changefont = QAction('Font', self)

        # 메뉴들 선택 시 실행될 함수 정의
        loadfile.triggered.connect(self.add_open)
        savefile.triggered.connect(self.add_save)
        exit.triggered.connect(qApp.quit)

        undotext.triggered.connect(self.undo)
        replacetext.triggered.connect(self.replace)

        # 메뉴에 하위 메뉴 생성
        Filemenu.addAction(loadfile)
        Filemenu.addAction(savefile)
        Filemenu.addAction(exit)

        Filemenu1.addAction(undotext)
        Filemenu1.addAction(replacetext)

        self.text1 = QTextEdit(self)
        self.text1.setAcceptRichText(True)
        self.text1.textChanged.connect(self.save_inputText)

        self.setCentralWidget(self.text1)
        self.show()

    def save_inputText(self):
        if len(self.text1.toPlainText()) == 0:
            self.undoStack = ""

        # 글상자에 있는 글자보다 저장된 글자가 짧다면
        elif len(self.undoStack) < len(self.text1.toPlainText()):
            self.undoStack += self.text1.toPlainText()[-1]
            print(self.undoStack)
        # 저장된 글자보다 글상자에 있는 글자가 길다면
        elif len(self.undoStack) > len(self.text1.toPlainText()):
            self.undoStack = self.undoStack[:-1]
            print(self.undoStack)
        # 저장된 글자보다 글상자에 있는 글자가 같다면
        elif len(self.undoStack) == len(self.text1.toPlainText()):
            self.undoStack = self.undoStack[:-1] + self.text1.toPlainText()[-1]
            print(self.undoStack)

    def undo(self):
        self.undoStack = self.undoStack[:-1]
        self.text1.setText(self.undoStack)

    def replace(self):
        replace = ReplaceDialog(self.text1.toPlainText())
        replace.exec_()
        self.text1.setText(replace.get_text())

    def add_open(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './')
        fileName = FileOpen[0]
        f = open(FileOpen[0], 'r', encoding='utf-8') #encoding이 잘못 인식되는 오류 해결
        textcontenct = f.read()
        self.text1.setText(textcontenct)
        f.close()

    def add_save(self):
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './')
        textcontent = self.text1.toPlainText()
        f = open(FileSave[0] + '.txt', 'w') # 자동으로 .txt 파일로 저장함
        f.write(textcontent)
        f.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()
