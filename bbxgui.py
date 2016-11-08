import sys
import os
import bbdb
import bbxfunc
import trainjson
from contconv import *
try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    input('PyQt4 is missing u need to instal this ')


FORM_WIDTH, FORM_HEIGHT = 582, 420
FORM_START_X, FORM_START_Y = 0, 0  # compute when QtGui.Qapplication is create (main())
ICON_WIDTH, ICON_HEIGHT = 70, 70
WINDOW_ICON = os.path.join('resources', 'icons', 'ne.ico')
CHANGE_ICON_A = os.path.join('resources', 'icons', 'ne.ico')
CHANGE_ICON_B = os.path.join('resources', 'icons', 'sound.png')
METRO_ICON = os.path.join('resources', 'icons', 'metro.png')
URL_ICON = os.path.join('resources', 'icons', 'url.png')
TRAIN_ICON = os.path.join('resources', 'icons', 'train.png')
WRITE_ICON = os.path.join('resources', 'icons', 'write.png')
LABELS_FONT = 'Levenim MT'                  #'Impact'

# Manage visibility of elements and switch souds/beats mode
change_state, metro_state, url_state = False, False, False



class Window(QtGui.QMainWindow):
    """Main window"""

    def __init__(self):

        # Set Window parameters
        super(Window, self).__init__()
        self.setGeometry(FORM_START_X, FORM_START_Y, FORM_WIDTH, FORM_HEIGHT)
        self.setWindowTitle('0.0.1 Beta')
        self.setWindowIcon(QtGui.QIcon(WINDOW_ICON))
        self.setFixedSize(FORM_WIDTH, FORM_HEIGHT)

        # directly set allowed windows buttons (up right)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint
                            | QtCore.Qt.WindowTitleHint)

        #set style
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))

        # list of currents urls
        self._curr_query = []

        # Add elements

        #    actionButton   (search button)
        self.actionButton = QtGui.QPushButton('search', self)
        self.actionButton.setGeometry(QtCore.QRect(325, 370, 86, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setFamily(LABELS_FONT)
        self.actionButton.setFont(font)
        self.actionButton.clicked.connect(lambda: bbxfunc.search_action(
                                        self.resultBox, self._curr_query, change_state,
                                        array=array_conv(self.arrayEdit, change_state),
                                        diff=diff_conv(self.diffEdit, change_state),
                                        bpm=bpm_conv(self.bpmEdit, change_state)
                                         )
                                         )

        #    searchLabel
        self.searchLabel = QtGui.QLabel(' Search \n Beat', self)
        self.searchLabel.setGeometry(QtCore.QRect(20, 315, 120, 100))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setFamily(LABELS_FONT)
        self.searchLabel.setAlignment(QtCore.Qt.AlignCenter)
        font.setKerning(True)
        self.searchLabel.setFont(font)
        self.searchLabel.setWordWrap(False)

        #    arrayLabel
        self.arrayLabel = QtGui.QLabel('used sounds', self)
        self.arrayLabel.setGeometry(QtCore.QRect(220, 348, 71, 46))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(LABELS_FONT)
        self.arrayLabel.setWordWrap(True)
        self.arrayLabel.setFont(font)
        self.arrayLabel.setAlignment(QtCore.Qt.AlignCenter)

        #    arrayEdit
        self.arrayEdit = QtGui.QLineEdit(self)
        self.arrayEdit.setGeometry(QtCore.QRect(160, 360, 51, 20))

        #    metroLabel
        self.metroLabel = QtGui.QLabel('30 BPM', self)
        self.metroLabel.setGeometry(QtCore.QRect(371, 50, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setFamily(LABELS_FONT)
        self.metroLabel.setFont(font)
        self.metroLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.metroLabel.setVisible(metro_state)

        #    dial
        self.dial = QtGui.QDial(self)
        self.dial.setGeometry(QtCore.QRect(381, 80, 100, 100))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.dial.setFont(font)
        self.dial.setMinimum(30)
        self.dial.setMaximum(220)
        self.dial.valueChanged.connect(lambda: bbxfunc.dial_func(self.metroLabel, self.dial.value()))
        self.dial.setVisible(change_state)

        #    displayLabel    (main label to display the current beat or sound)
        self.displayLabel = QtGui.QLabel(
            'with any wishes and suggestions please email me: RakitinAndreiRakitin @gmail.com', self)
        self.displayLabel.setGeometry(QtCore.QRect(20, -20, 350, 301))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setFamily(LABELS_FONT)
        self.displayLabel.setFont(font)
        self.displayLabel.setAutoFillBackground(False)
        self.displayLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.displayLabel.setScaledContents(False)
        self.displayLabel.setWordWrap(True)

        #    bpmLabel
        self.bpmLabel = QtGui.QLabel('bpm', self)
        self.bpmLabel.setGeometry(QtCore.QRect(240, 390, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(LABELS_FONT)
        self.bpmLabel.setFont(font)

        #    diffEdit
        self.diffEdit = QtGui.QLineEdit(self)
        self.diffEdit.setGeometry(QtCore.QRect(170, 330, 31, 20))

        #    diffLabel
        self.diffLabel = QtGui.QLabel('difficulty', self)
        self.diffLabel.setGeometry(QtCore.QRect(220, 330, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(LABELS_FONT)
        self.diffLabel.setFont(font)
        self.diffLabel.setAlignment(QtCore.Qt.AlignCenter)

        #    resultBox   (comboBox of current query result)
        self.resultBox = QtGui.QComboBox(self)
        self.resultBox.setGeometry(QtCore.QRect(310, 340, 121, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setFamily(LABELS_FONT)
        self.resultBox.setFont(font)
        self.resultBox.currentIndexChanged.connect(lambda: bbxfunc.rb_change(
                                                        self.resultBox, self.displayLabel,
                                                        self._curr_query, self.urlEdit
                                                                            )
                                                   )
        #    urlEdit
        self.urlEdit = QtGui.QLineEdit(self)
        self.urlEdit.setGeometry(QtCore.QRect(375, 220, 113, 20))
        self.urlEdit.setVisible(url_state)

        #    urlButton      (open URL)
        self.urlButton = QtGui.QPushButton('open url', self)
        self.urlButton.setGeometry(QtCore.QRect(390, 250, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setFamily(LABELS_FONT)
        self.urlButton.setFont(font)
        self.urlButton.clicked.connect(lambda: bbxfunc.url_open(url_conv(self.urlEdit)))
        self.urlButton.setVisible(url_state)

        #    bpmEdit
        self.bpmEdit = QtGui.QLineEdit(self)
        self.bpmEdit.setGeometry(QtCore.QRect(170, 390, 31, 20))

        #    bottomLine     (split  area line)
        self.bottomLine = QtGui.QFrame(self)
        self.bottomLine.setGeometry(QtCore.QRect(0, 300, FORM_WIDTH-ICON_WIDTH-12, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bottomLine.setFont(font)
        self.bottomLine.setFrameShape(QtGui.QFrame.HLine)
        self.bottomLine.setFrameShadow(QtGui.QFrame.Sunken)




        # Toolbar actions, icons etc
        # Change mode tool
        self.changeAction = QtGui.QAction(QtGui.QIcon(CHANGE_ICON_A), 'Change to sounds', self)
        self.changeAction.triggered.connect(switch_change_state)
        self.changeAction.triggered.connect(lambda: bbxfunc.change_func(self.changeAction,
                                            self.diffLabel, self.bpmLabel, self.arrayLabel,
                                            self.searchLabel,
                                            change_state))
        # Flip metro tool
        self.metroAction = QtGui.QAction(QtGui.QIcon(METRO_ICON), 'Flip metronom', self)
        self.metroAction.triggered.connect(switch_metro_state)
        self.metroAction.triggered.connect(lambda: bbxfunc.metro_func(self.metroLabel, self.dial, metro_state))

        # Flip url tool
        self.urlAction = QtGui.QAction(QtGui.QIcon(URL_ICON), 'Flip URL', self)
        self.urlAction.triggered.connect(switch_url_state)
        self.urlAction.triggered.connect(lambda: bbxfunc.url_func(self.urlEdit, self.urlButton, url_state))

        # Show train tool
        self.trainAction = QtGui.QAction(QtGui.QIcon(TRAIN_ICON), 'show random exercise', self)
        self.trainAction.triggered.connect\
            (
            lambda: bbxfunc.exer_func(self,                                      # create obj from json and
            trainjson.Exercise.from_json(trainjson.TRAIN_FILE).random_exercise() # invoke random_exercise()
                                     )                                           # which return rand exer list
            )


        # Write to db subwindow
        self.writeAction = QtGui.QAction(QtGui.QIcon(WRITE_ICON), 'write into DB', self)
        self.writeAction.triggered.connect(lambda: bbxfunc.create_sub_window(change_state, self))

        # Init toolbar

        self.toolBar = self.addToolBar('')

        self.addToolBar(QtCore.Qt.RightToolBarArea, self.toolBar)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(ICON_WIDTH,ICON_HEIGHT))
        self.toolBar.addAction(self.changeAction)
        self.toolBar.addAction(self.metroAction)
        self.toolBar.addAction(self.urlAction)
        self.toolBar.addAction(self.trainAction)
        self.toolBar.addAction(self.writeAction)


        # tuple of all active elements
        self.elements = (self.writeAction, self.trainAction, self.urlAction, self.metroAction, self.changeAction,
                         self.dial, self.bpmEdit, self.urlEdit, self.arrayEdit, self.diffEdit,
                         self.bpmLabel, self.arrayLabel, self.diffLabel, self.displayLabel,
                         self.metroLabel, self.searchLabel, self.resultBox, self.actionButton,
                         self.urlButton
                         )



        # Finaly draw objs
        self.show()


class BeatsSubWindow(QtGui.QMdiSubWindow):
    """Subwindow for write beats into DB"""

    def __init__(self, parent):

        # disable parent
        self.parent = parent
        for i in self.parent.elements:
            i.setDisabled(True)

        # Set sub window parameters
        super(BeatsSubWindow, self).__init__(parent)

        self.setGeometry(50, 50, 0, 0)
        self.setWindowTitle('Write new beat')
        self.setWindowIcon(QtGui.QIcon(CHANGE_ICON_A))
        self.setFixedSize(FORM_WIDTH // 1.3, FORM_HEIGHT // 1.3)
        self.setSystemMenu(None)

        # set style
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))

        # Add elements
        self.arrayEdit = QtGui.QLineEdit(self)
        self.arrayEdit.setGeometry(QtCore.QRect(90, 190, 140, 20))

        self.arrayLabel = QtGui.QLabel('beat*', self)
        self.arrayLabel.setGeometry(QtCore.QRect(220, 190, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.arrayLabel.setFont(font)
        self.arrayLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.actionButton = QtGui.QPushButton('write', self)
        self.actionButton.setGeometry(QtCore.QRect(320, 150, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.actionButton.setFont(font)
        self.actionButton.clicked.connect(lambda: bbxfunc.write_beat_to_db(
                                        array=array_conv(self.arrayEdit, change_state),
                                        diff=diff_conv(self.diffEdit, change_state),
                                        bpm=bpm_conv(self.bpmEdit, change_state)
                                                                  )
                                          )

        self.bpmEdit = QtGui.QLineEdit(self)
        self.bpmEdit.setGeometry(QtCore.QRect(140, 160, 31, 20))

        self.bpmLabel = QtGui.QLabel('bpm', self)
        self.bpmLabel.setGeometry(QtCore.QRect(210, 160, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bpmLabel.setFont(font)

        self.diffEdit = QtGui.QLineEdit(self)
        self.diffEdit.setGeometry(QtCore.QRect(140, 140, 31, 20))

        self.diffLabel = QtGui.QLabel('difficulty', self)
        self.diffLabel.setGeometry(QtCore.QRect(190, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.diffLabel.setFont(font)
        self.diffLabel.setAlignment(QtCore.Qt.AlignCenter)

        # customize windows hint button
        self.setWindowFlags(QtCore.Qt.WindowTitleHint)

        self.actionButton = QtGui.QPushButton('X', self)
        self.actionButton.setGeometry(QtCore.QRect(200, 230, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.actionButton.setFont(font)
        self.actionButton.clicked.connect(lambda: self.close())

        self.show()


    def closeEvent(self, QCloseEvent):
        '''enable all elements of parent'''

        for i in self.parent.elements:
            i.setDisabled(False)


class SoundsSubWindow(QtGui.QMdiSubWindow):
    """Subwindow for write sounds into DB"""

    def __init__(self, parent):
        # disable parent
        self.parent = parent
        for i in self.parent.elements:
            i.setDisabled(True)

        # Set sub window parameters
        super(SoundsSubWindow, self).__init__(parent)

        self.setGeometry(50, 50, 0, 0)
        self.setWindowTitle('Write new sound')
        self.setWindowIcon(QtGui.QIcon(CHANGE_ICON_B))
        self.setFixedSize(FORM_WIDTH // 1.3, FORM_HEIGHT // 1.3)
        self.setSystemMenu(None)
        # set style
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))

        # Add elements
        self.nameEdit = QtGui.QLineEdit(self)
        self.nameEdit.setGeometry(QtCore.QRect(113, 220, 81, 20))

        self.nameLabel = QtGui.QLabel('full sound name*', self)
        self.nameLabel.setGeometry(QtCore.QRect(213, 220, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nameLabel.setFont(font)
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.arrayEdit = QtGui.QLineEdit(self)
        self.arrayEdit.setGeometry(QtCore.QRect(140, 200, 31, 20))

        self.arrayLabel = QtGui.QLabel('literal*', self)
        self.arrayLabel.setGeometry(QtCore.QRect(190, 200, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.arrayLabel.setFont(font)
        self.arrayLabel.setAlignment(QtCore.Qt.AlignCenter)



        self.actionButton = QtGui.QPushButton('write', self)
        self.actionButton.setGeometry(QtCore.QRect(320, 150, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.actionButton.setFont(font)
        self.actionButton.clicked.connect(lambda: bbxfunc.write_sound_to_db(
                                        array=array_conv(self.arrayEdit, change_state),
                                        diff=diff_conv(self.diffEdit, change_state),
                                        type_=self.typeEdit.text(),
                                        sample=sample_conv(self.sampleEdit),
                                        url=url_conv(self.urlEdit),
                                        name=name_conv(self.nameEdit)
                                                                  )
                                          )

        self.typeEdit = QtGui.QLineEdit(self)
        self.typeEdit.setGeometry(QtCore.QRect(140, 180, 31, 20))

        self.typeLabel = QtGui.QLabel('type', self)
        self.typeLabel.setGeometry(QtCore.QRect(210, 180, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.typeLabel.setFont(font)
        self.typeLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.diffEdit = QtGui.QLineEdit(self)
        self.diffEdit.setGeometry(QtCore.QRect(140, 160, 31, 20))

        self.diffLabel = QtGui.QLabel('difficulty', self)
        self.diffLabel.setGeometry(QtCore.QRect(190, 160, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.diffLabel.setFont(font)
        self.diffLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.urlEdit = QtGui.QLineEdit(self)
        self.urlEdit.setGeometry(QtCore.QRect(140, 140, 31, 20))

        self.urlLabel = QtGui.QLabel('url', self)
        self.urlLabel.setGeometry(QtCore.QRect(190, 140, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.urlLabel.setFont(font)
        self.urlLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.sampleEdit = QtGui.QLineEdit(self)
        self.sampleEdit.setGeometry(QtCore.QRect(140, 120, 31, 20))

        self.sampleLabel = QtGui.QLabel('sample', self)
        self.sampleLabel.setGeometry(QtCore.QRect(190, 120, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sampleLabel.setFont(font)
        self.sampleLabel.setAlignment(QtCore.Qt.AlignCenter)

        # customize windows hint button
        self.setWindowFlags(QtCore.Qt.WindowTitleHint)

        self.actionButton = QtGui.QPushButton('X', self)
        self.actionButton.setGeometry(QtCore.QRect(200, 250, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.actionButton.setFont(font)
        self.actionButton.clicked.connect(lambda: self.close())

        self.show()


    def closeEvent(self, QCloseEvent):
        '''enable all elements of parent'''

        for i in self.parent.elements:
            i.setDisabled(False)


class ExerciseSubWindow(QtGui.QMdiSubWindow):
    """Subwindow for show random exercise from json file"""

    def __init__(self, parent, exer):
        # disable parent
        self.parent = parent
        for i in self.parent.elements:
            i.setDisabled(True)

        # Set sub window parameters
        super(ExerciseSubWindow, self).__init__(parent)

        self.setGeometry(50, 50, 0, 0)
        self.setWindowTitle(exer[0])
        self.setWindowIcon(QtGui.QIcon(TRAIN_ICON))
        self.setFixedSize(FORM_WIDTH // 1.3, FORM_HEIGHT // 1.3)
        self.setSystemMenu(None)
        # set style
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('cleanlooks'))

        # Add elements

        self.displayLabel = QtGui.QLabel(exer[1], self)
        self.displayLabel.setGeometry(QtCore.QRect(20, -20, 400, 301))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setFamily(LABELS_FONT)
        self.displayLabel.setFont(font)
        self.displayLabel.setAutoFillBackground(False)
        self.displayLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.displayLabel.setScaledContents(False)
        self.displayLabel.setWordWrap(True)
        self.displayLabel.setAlignment(QtCore.Qt.AlignCenter)

        # customize windows hint button
        self.setWindowFlags(QtCore.Qt.WindowTitleHint)

        self.actionButton = QtGui.QPushButton('X', self)
        self.actionButton.setGeometry(QtCore.QRect(200, 230, 61, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.actionButton.setFont(font)
        self.actionButton.clicked.connect(lambda: self.close())

        self.show()


    def closeEvent(self, QCloseEvent):
        '''enable all elements of parent'''

        for i in self.parent.elements:
            i.setDisabled(False)


# golbal state switchers
def switch_change_state():
    global change_state
    change_state = not change_state


def switch_metro_state():
    global metro_state
    metro_state = not metro_state


def switch_url_state():
    global url_state
    url_state = not url_state



if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    # set cenral place for Window
    FORM_START_Y = app.desktop().screenGeometry().height() // 2 - FORM_HEIGHT // 2
    FORM_START_X = app.desktop().screenGeometry().width() // 2 - FORM_WIDTH // 2

    bbxForm = Window()

    # initialize Database
    bbdb.init_db()

    sys.exit(app.exec_())


