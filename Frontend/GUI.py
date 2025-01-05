from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit , QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter,QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
AssistantName = env_vars.get("AssistantName")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = f"{current_dir}/Frontend/Files"
GraphicsDirPath = f"{current_dir}/Frontend/Graphics"

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def QueryModifier (Query):
    new_query= Query.lower().strip()
    query_words = new_query.split()
    question_words = ["what", "when", "where", "why", "how","whose" ,"who", "which","how's", "what's", "when's", "where's", "why's", "who's", "which's", "whose's", "can you" , "could you", "would you", "will you", "may you", "might you", "should you", "do you", "did you", "have you", "had you", "has you", "is it", "was it", "are you", "were you", "am i", "am i not", "is it not", "are you not", "were you not", "was it not", "do you not", "did you not", "does it not", "have you not", "has it not", "had you not", "will you not", "would you not", "can you not", "could you not", "may you not", "might you not", "should you not", "can you", "could you", "would you", "will you", "may you", "might you", "should you", "do you", "did you", "does it", "have you", "has it", "had you", "will you", "would you", "can you", "could you", "would you", "will you", "may you", "might you", "should you", "do you", "did you", "does it", "have you", "has it", "had you", "will you", "would you", "can you", "could you", "would you", "will you", "may you", "might you", "should you", "do you", "did you", "does it", "have you", "has it", "had you", "will you", "would you", "can you", "could you", "would you", "will you", "may you", "might you", "should you", "do you", "did you", "does it", "have you"]



    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] == [" . " , " ? " , " ! "]:
            new_query = new_query[:-1] + " ?"
        else:
            new_query += " ?"
    else :
        if query_words[-1][-1] == [" . " , " ? " , " ! "]:
            new_query = new_query[:-1] + " ."
        else:
            new_query += " ."

    return new_query.capitalize()

def SetMicropohoneStatus(Command):
    with open(f"{TempDirPath}/Mic.data", "w", encoding="utf-8") as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(f"{TempDirPath}/Mic.data", "r",encoding="utf-8") as file:
        status=  file.read()
    return status

def SetAssistantStatus(Command):
    with open(f"{TempDirPath}/Status.data", "w",encoding="utf-8") as file:
        file.write(Command)

def GetAssistantStatus():
    with open(f"{TempDirPath}/Status.data", "r", encoding="utf-8") as file:
        status=  file.read()
    return status

def MicButtonInitialized():
    SetMicropohoneStatus("False")

def MicButtonClosed():
    SetMicropohoneStatus("True")

def GraphicDirectoryPath(FileName):
    path = f"{GraphicsDirPath}/{FileName}"
    return path

def TempDirectoryPath(FileName):
    path = f"{TempDirPath}/{FileName}"
    return path

def ShowTextToScreen(Text):
    with open(f"{TempDirPath}/Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

class ChatSection(QWidget):

    def __init__(self):
        super(ChatSection, self).__init__()
        self.toggled = False  # Initialize toggled
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10,40,40,100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border :none;")
        movie = QMovie(GraphicDirectoryPath("Jarvis.gif"))
        max_gif_size_W = 480
        max_gif_size_H = 270
        movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 20px; margin-right: 195px; border:none; margin-top:-30px")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
                     QScrollBar:vertical {
                           border: none;
                           background: black;
                           width: 10px;
                           margin: 0px 0px 0px 0px;
                           }

                           QScrollBar::handle:vertical {
                           background: white;
                           min-height: 20px;
                           }

                            QScrollBar::add-line:vertical {
                           background: black;
                           subcontrol-position: bottom;
                            subcontrol-origin: margin;
                           height: 10px;
                           }

                            QScrollBar::up-arrow:vertical , QScrollBar::down-arrow:vertical {
                           border: none;
                           background: none;
                           color : none;
                           }

                           QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                            background: none;
                            }

                           """)
        
    def loadMessages(self):

        global old_chat_message

        with open(TempDirectoryPath("Responses.data"), "r", encoding="utf-8") as file:
            messages = file.read()

            if None == messages:
                pass
            elif len(messages) < 1:
                pass
            elif str(old_chat_message) == str(messages):
                pass
            else:
                self.addMessage(messages=messages, color="white")
                old_chat_message = messages

    def SpeechRecogText(self):
        with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self , path ,width = 60, height = 60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self ,event=None):
        if self.toggled:
            self.load_icon(GraphicDirectoryPath("voice.png"), 60, 60)
            MicButtonInitialized()
        else:
            self.load_icon(GraphicDirectoryPath("mic.png"), 60, 60)
            MicButtonClosed()

        self.toggled = not self.toggled

    def addMessage(self, messages, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(messages + "\n")
        self.chat_text_edit.setTextCursor(cursor)

class InitialScreen(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0,0,0,0)
        gif_label = QLabel()
        movie = QMovie(GraphicDirectoryPath("Jarvis.gif"))
        gif_label.setMovie(movie)
        max_gif_size_h = int(screen_width / 16 * 9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_h))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicDirectoryPath("Mic_on.png"))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150,150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = False  # Initialize toggled
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        self.label = QLabel()
        self.label.setStyleSheet("color: white; font-size: 16px ; margin-bottom :0px;")
        content_layout.addWidget(gif_label,alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0,0,0,150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self , path ,width = 60, height = 60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self ,event=None):
        if self.toggled:
            self.load_icon(GraphicDirectoryPath("Mic_on.png"), 60, 60)
            MicButtonInitialized()
        else:
            self.load_icon(GraphicDirectoryPath("Mic_off.png"), 60, 60)
            MicButtonClosed()

        self.toggled = not self.toggled


class MessageScreen(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.initUi()
        self.current_screen = None
        self.stacked_widget = stacked_widget

    def initUi(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft)
        home_button = QPushButton()
        home_icon = QIcon(GraphicDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("Home")
        home_button.setStyleSheet("height : 40px ; line-height:40px ;background-color: white; color:black; border: none; font-size: 16px;")
        message_button = QPushButton()
        message_icon = QIcon(GraphicDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("Chat")
        message_button.setStyleSheet("height : 40px ; line-height:40px ;background-color: white; color:black; border: none; font-size: 16px;")
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicDirectoryPath("Minimize2.png"))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color: white; color:black; border: none; font-size: 16px;")
        minimize_button.clicked.connect(self.minimize)
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicDirectoryPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicDirectoryPath("Minimize.png"))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color: white; color:black; border: none; font-size: 16px;")
        self.maximize_button.clicked.connect(self.maximize)
        close_button = QPushButton()
        close_icon = QIcon(GraphicDirectoryPath("Close.png"))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color: white; color:black; border: none; font-size: 16px;")
        close_button.clicked.connect(self.close)
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("background-color: black;")
        title_label = QLabel(f"{AssistantName.capitalize()}AI")
        title_label.setStyleSheet("color: white; font-size: 20px; background-color: black;")
        home_button.clicked.connect(lambda:self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda:self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True
        self.oldPos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimize(self):
        self.parent().showMinimized()

    def maximize(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def close(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable :
            self.offset = event.pos()
    
    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        
        message_screen = MessageScreen(self)
        layout = self.parent().layout()

        if layout is not None:
            layout.addWidget(message_screen)

        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        
        initial_screen = InitialScreen(self)
        layout = self.parent().layout()

        if layout is not None:
            layout.addWidget(initial_screen)

        self.current_screen = initial_screen

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUi()

    def initUi(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()
