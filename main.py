# !!________________________________________________Libraries Imports_________________________________________________!!

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox, QSlider, QVBoxLayout, QWidget, QTextEdit, QSpinBox, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QFont
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
import sys
# ____________________________________________________________________________________________________________________!!

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        loadUi('main.ui', self)
        
        
# !!________________________________________________Manipulates________________________________________________________!!        
        self.setWindowTitle("untitled")
        self.setWindowIcon(QIcon("Icons/MainWindowIcon.png"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(8)
        self.slider.setMaximum(72)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self.changeFontSize)    
        layout2 = QHBoxLayout()
        self.font_size_label = QLabel(str(self.slider.value()), self)
        self.font_size_label.setGeometry(130, 85, 50, 20)
        self.font_size_label.setFont(QFont("sanserif",15))
        layout2.addWidget(self.slider)
        layout2.addWidget(self.font_size_label)
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addLayout(layout2)
        widget = QWidget()
        widget.setLayout(layout2)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
# ________________________________________________Global Variables____________________________________________________!!     
        self.current_path = None
        self.currentFontSize = int(self.font_size_label.text())
        self.unsavedChanges = False
# _________________________________________________++Connections++____________________________________________________!!

        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.save_asFile)
        self.actionUndo.triggered.connect(self.undoEdit)
        self.actionRedo.triggered.connect(self.redoEditFile)
        self.actionCut.triggered.connect(self.cutEdit)
        self.actionCopy.triggered.connect(self.copyEdit)
        self.actionPaste.triggered.connect(self.pasteEdit)
        self.actionDark_Mode.triggered.connect(self.dark_modeApperance)
        self.actionLight_Mode.triggered.connect(self.light_modeApperance)
        # self.actionChange_Font_Size.triggered.connect(self.font_sizeApperance_Increase)
        # self.actionDecrease_Font_Size.triggered.connect(self.font_sizeApperance_decrease)
        self.actionExit.triggered.connect(self.exitApp)

        
# _____________________________________________________++Functions++__________________________________________________!!
# __________________________________________________________File______________________________________________________
    def newFile(self):
        self.textEdit.clear()
        self.setWindowTitle("untitled")
        self.current_path = None


    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open', 'Desktop', 'Text documents (*.txt)')
        self.setWindowTitle(fname[0])
        with open(fname[0], 'r') as f:
            fileText = f.read()
            self.textEdit.setText(fileText)
        self.current_path = fname[0]
        
    def saveFile(self):
        if self.current_path is not None:
            #save without opening file dialog
            fileText = self.textEdit.toPlainText()
            with open(self.current_path, 'w') as f:
                f.write(fileText)
                            
        else:
            self.save_asFile()
            

    def save_asFile(self):
        pathname = QFileDialog.getSaveFileName(self, 'Save file',  'Desktop', 'Text documents (*.txt)')
        filetext = self.textEdit.toPlainText()
        with open(pathname[0], 'w' ) as f:
            f.write(filetext)
        self.current_path = pathname[0]
        self.setWindowTitle(pathname[0])
        
    
    def exitApp(self):
        # create a message box asking the user to save or discard changes
        reply = QMessageBox.question(self, 'Save Changes?',
                                    'Do you want to save changes?',
                                    QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                                    QMessageBox.StandardButton.Save)
        if reply == QMessageBox.StandardButton.Save:
            # save changes and quit the application
            self.saveFile()
            QApplication.quit()
        elif reply == QMessageBox.StandardButton.Discard:
            # discard changes and quit the application
            QApplication.quit()
        else:
            # user clicked cancel, do not quit the application
            pass

        
# __________________________________________________________Edit______________________________________________________

    def undoEdit(self):
        self.textEdit.undo()
            
    def redoEditFile(self):
        self.textEdit.redo()
            
    def cutEdit(self):
        self.textEdit.cut()
        
    def copyEdit(self):
        self.textEdit.copy()
        
    def pasteEdit(self):
        self.textEdit.paste()
# _________________________________________________________Apperance__________________________________________________
    def light_modeApperance(self):
        self.setStyleSheet("")

    def dark_modeApperance(self):
        self.setStyleSheet('''
                            QWidget{
                                background-color: rgb(33,33,33);
                                color: #FFFFFF;
                            }
                            QTextEdit{
                                bacckground-color: rgb(46,46,46);}
                            QMenuBar::item:selected{
                                color: #000000;}
                            ''')
            
     
    def changeFontSize(self, value):
        self.font_size_label.setText(str(self.slider.value()))
        self.textEdit.setFontPointSize(value)
        
              
    # def font_sizeApperance_Increase(self):
    #     self.currentFontSize+=5
    #     self.textEdit.setFontPointSize(self.currentFontSize)
    #     self.font_size_label.setText(str(self.currentFontSize))
        
        
    # def font_sizeApperance_decrease(self):
    #     self.currentFontSize-=5
    #     self.textEdit.setFontPointSize(self.currentFontSize)
    #     self.font_size_label.setText(str(self.currentFontSize))
        
        
        
     
# __________________________________________________________Exec______________________________________________________!!

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
