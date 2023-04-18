# !!________________________________________________Libraries Imports_________________________________________________!!

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox, QSlider, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QFontDialog, QColorDialog
from PyQt6.QtGui import QIcon, QFont, QColor
from PyQt6.QtCore import Qt, QFileInfo
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.uic import loadUi
import webbrowser
import docx
import sys


# ____________________________________________________________________________________________________________________!!

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        loadUi("NotePadET.ui", self)
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
        self.font = QFont()
        self.bold_on = False
        self.italic_on = False
        self.underline_on = False
        self.saved = False
# _________________________________________________++Connections++____________________________________________________!!

        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.save_asFile)
        self.actionPrint.triggered.connect(self.print)
        self.actionPrint_Preview.triggered.connect(self.preview_dialog)
        self.actionPDF.triggered.connect(self.exportAsPDF)
        self.actionExit_2.triggered.connect(self.exitApp)
        self.actionUndo.triggered.connect(self.undoEdit)
        self.actionRedo.triggered.connect(self.redoEditFile)
        self.actionCut.triggered.connect(self.cutEdit)
        self.actionCopy.triggered.connect(self.copyEdit)
        self.actionPaste.triggered.connect(self.pasteEdit)
        self.actionBold.triggered.connect(self.toggle_Bold)
        self.actionItalic.triggered.connect(self.toggle_Italic)
        self.actionUnderline.triggered.connect(self.toggle_underLine)
        self.actionLeft_2.triggered.connect(self.align_left)
        self.actionRight.triggered.connect(self.align_right)
        self.actionCenter.triggered.connect(self.align_center)
        self.actionJustify.triggered.connect(self.align_justify)
        self.actionFont.triggered.connect(self.font_dialog)
        self.actionColor.triggered.connect(self.color_dialog)       
        self.actionDark_Mode.triggered.connect(self.dark_modeApperance)
        self.actionLight_Mode.triggered.connect(self.light_modeApperance)
        self.actionToggle.triggered.connect(self.toggle)
        # self.actionZoom_in.triggered.connect(self.font_sizeApperance_Increase)
        # self.actionZoom_Out.triggered.connect(self.font_sizeApperance_decrease)
        self.actionGitHub.triggered.connect(self.github)
        self.actionGmail.triggered.connect(self.gmail)
        self.actionAbout_Me.triggered.connect(self.about)     
# _____________________________________________________++Functions++__________________________________________________!!
# __________________________________________________________File______________________________________________________
   
    def newFile(self):
        if self.maybe_save():
            self.textEdit.clear()
            self.setWindowTitle("untitled")
            self.current_path = None


    def maybe_save(self):
        if not self.textEdit.document().isModified():
            return True
        ret = QMessageBox.warning(self,"Application", "The document has been modified.\n Do you want to save changes?", QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |QMessageBox.StandardButton.Cancel)
        if ret == QMessageBox.StandardButton.Save:
            return self.saveFile()
        if ret == QMessageBox.StandardButton.Cancel:
            return False
        if ret == QMessageBox.StandardButton.Discard:
            return True
    
    
    
    # def openFile(self):
    #     fname = QFileDialog.getOpenFileName(self, 'Open', 'Desktop', 'Text documents (*.txt)')
    #     self.setWindowTitle(fname[0])
    #     with open(fname[0], 'r') as f:
    #         fileText = f.read()
    #         self.textEdit.setText(fileText)
    #     self.current_path = fname[0]
    
    
    

    def openFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open', 'Desktop', 'Text documents (*.txt);;Word documents (*.docx)')
        self.setWindowTitle(fname)
        with open(fname, 'r') as f:
            if fname.endswith('.txt'):
                fileText = f.read()
                self.textEdit.setText(fileText)
            elif fname.endswith('.docx'):
                doc = docx.Document(fname)
                fileText = '\n'.join([para.text for para in doc.paragraphs])
                self.textEdit.setText(fileText)
        self.current_path = fname







        
    def saveFile(self):
        if self.current_path is not None:
            #save without opening file dialog
            fileText = self.textEdit.toPlainText()
            with open(self.current_path, 'w') as f:
                f.write(fileText)
                QMessageBox.about(self, "Save File", " Your changes have been saved")
                
                            
        else:
            self.save_asFile()
            


    def save_asFile(self):
        pathname = QFileDialog.getSaveFileName(self, 'Save file',  'Desktop', 'Text documents (*.txt)')
        filetext = self.textEdit.toPlainText()
        with open(pathname[0], 'w' ) as f:
            f.write(filetext)
            QMessageBox.about(self, "Save File As", " Congratulations, File has been saved sucessfully!!")
        self.current_path = pathname[0]
        self.setWindowTitle(pathname[0])
        
    
    def print(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)
          
          
          
    def preview_dialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.print_preview)
        previewDialog.exec()
         
    def print_preview(self, printer):
        self.textEdit.print(printer)
        
        
        
        
                
    def exportAsPDF(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF', "write your PDF name here")
        if fn != "":
            if QFileInfo(fn).suffix() == "": 
                fn += '.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print(printer)
         

    
    
    
    def wheelEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.textEdit.zoomIn(1)
            else:
                self.textEdit.zoomOut(1)
        else:
            super().wheelEvent(event)
    
    
    def closeEvent(self, event):
        if not self.saved:
            reply = QMessageBox.question(self, 'Save', 'Do you want to save your changes?', 
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Save:
                # The user clicked the "Save" button
                self.saveFile()
            elif reply == QMessageBox.StandardButton.Discard:
                # The user clicked the "Discard" button
                self.textEdit.clear()
            elif reply == QMessageBox.StandardButton.Cancel:
                # The user clicked the "Cancel" button
                return


         
            
    

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
# __________________________________________________________Format______________________________________________________
        
    def Bold(self):
        self.font.setBold(True)
        self.textEdit.setFont(self.font)
        self.bold_on = True

    def deBold(self):
        self.font.setBold(False)
        self.textEdit.setFont(self.font)
        self.bold_on = False

    def toggle_Bold(self):
        if self.bold_on:
            self.deBold()
        else:
            self.Bold()





    def Italic(self):
        self.font.setItalic(True)
        self.textEdit.setFont(self.font)
        self.italic_on = True

    def deItalic(self):
        self.font.setItalic(False)
        self.textEdit.setFont(self.font)
        self.italic_on = False

    def toggle_Italic(self):
        if self.italic_on:
            self.deItalic()
        else:
            self.Italic()





    def underLine(self):
        self.font.setUnderline(True)
        self.textEdit.setFont(self.font)
        self.underline_on = True

    def deunderLine(self):
        self.font.setUnderline(False)
        self.textEdit.setFont(self.font)
        self.underline_on = False

    def toggle_underLine(self):
        if self.underline_on:
            self.deunderLine()
        else:
            self.underLine()
            
    
    
    
    
    def align_left(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def align_right(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def align_center(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def align_justify(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)
    
        
        
        
    def font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)
            
    
    def color_dialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)
        

# _________________________________________________________View__________________________________________________
    def light_modeApperance(self):
        self.setStyleSheet("")

    def dark_modeApperance(self):
        title_bar_color = QColor(26, 33, 49)  # Define a QColor object with the desired color
        self.setStyleSheet(f'''
            QMainWindow::title {{
                background-color: {title_bar_color.name()};
            }}
            QWidget {{
                background-color: rgb(70,70,70);
                color: #FFFFFF;
            }}
            QTextEdit {{
                background-color: rgb(38, 38, 38);
            }}
            QMenuBar {{
                background-color: rgb(70,70,70);
            }}
            QToolBar {{
                background-color: rgb(70,70,70);
            }}
            QMenuBar::item:selected {{
                color: #000000;
            }}
            QAction::item:selected {{
                color: #000000;
            }}
            
        ''')
    
     
    def toggle(self):
        # Check which mode the application is currently in
        current_color = self.textEdit.palette().color(self.textEdit.backgroundRole())
        if current_color == QColor(38, 38, 38):
            # If in dark mode, switch to light mode
            self.light_modeApperance()
        else:
            # If in light mode, switch to dark mode
            self.dark_modeApperance()
        self.textEdit.setStyleSheet("")  # Clear any custom styles on the QTextEdit widget
    





            
    def changeFontSize(self, value):
        self.font_size_label.setText(str(self.slider.value()))
        self.textEdit.setFontPointSize(value)
        
              
    # def font_sizeApperance_Increase(self):
    #     # self.current = self.currentFontSize
    #     if (self.currentFontSize < 250):
    #         self.currentFontSize+=2
    #         self.textEdit.setFontPointSize(self.currentFontSize)
    #         # self.font_size_label.setText(str(self.currentFontSize))
    #     else:
    #         self.currentFontSize=250
    #         self.textEdit.setFontPointSize(self.currentFontSize)
    #         pass
        

        
        
    # def font_sizeApperance_decrease(self):
        
    #     # self.current = self.currentFontSize
    #     if (self.currentFontSize > 8):
    #         self.currentFontSize-=2
    #         self.textEdit.setFontPointSize(self.currentFontSize)
    #         # self.font_size_label.setText(str(self.currentFontSize))
    #     else:
    #         self.currentFontSize= 8
    #         self.textEdit.setFontPointSize(self.currentFontSize)
    #         pass

# _________________________________________________________About__________________________________________________

    def github(self):
        url = 'https://github.com/MohammadSayed02/MohammadSayed'
        webbrowser.open(url)

        
    def gmail(self):
        url = 'mailto:Mohammadeltayeb554@gmail.com'
        webbrowser.open(url)
   
    def about(self):
        QMessageBox.about(self, "About App", "ETSTORE,inc \n Thank You for using my App\n For Any Bugs or Suggestions please contact me at once")
        
# __________________________________________________________Exec______________________________________________________!!

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
