import openai
import sys
import webbrowser
import random
from PyQt5 import QtCore, QtGui, QtWidgets

class ConversationWindow(QtWidgets.QWidget):
    def __init__(self, api_key):
        super().__init__()

        # Set window flags to remove window frame
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Set background color to a dark shade
        self.setStyleSheet("background-color: #1E1E1E; color: white;")

        self.api_key = api_key
        self.chat_history = ""

        # Add label with window title
        title_label = QtWidgets.QLabel("GPTChatter")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")

        self.input_text = QtWidgets.QLineEdit()
        self.input_text.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; border: 2px solid #ccc; background-color: #2F2F2F; color: white;")
        self.chat_output = QtWidgets.QTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_output.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; border: 2px solid #ccc; background-color: #2F2F2F; color: white;")
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; border: 2px solid #ccc; background-color: #E6F0FF; color: white;")
        self.quit_button = QtWidgets.QPushButton("Quit")
        self.quit_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; border: 2px solid #ccc; background-color: #FFCCCC; color: white;")
        self.github_button = QtWidgets.QPushButton("GitHub")
        self.github_button.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 10px; border: 2px solid #ccc; background-color: #333333; color: white;")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(title_label)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.github_button)
        button_layout.addWidget(self.quit_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.chat_output, stretch=1)
        layout.addWidget(self.input_text)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)
        self.input_text.returnPressed.connect(self.send_message)
        self.quit_button.clicked.connect(self.quit)
        self.github_button.clicked.connect(self.open_github)

        # Apply stylesheet to all child widgets recursively
        self.apply_stylesheet(self)

        # Set window title to empty string
        self.setWindowTitle("")



    def open_github(self):
        """
        Open the GitHub repository URL in a web browser
        """
        url = "https://github.com/ItZFerret/GPTChatter"
        webbrowser.open(url)

    # Rest of the code unchanged



    def mousePressEvent(self, event):
        """
        Handle mouse press events to move the window
        """
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        Handle mouse move events to move the window
        """
        if hasattr(self, 'dragPos'):
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def quit(self):
        """
        Quit the application
        """
        QtWidgets.QApplication.quit()



    def apply_stylesheet(self, widget):
        """
        Recursively apply the stylesheet to all child widgets
        """
        widget.setStyleSheet(self.styleSheet())
        for child in widget.children():
            if isinstance(child, QtWidgets.QWidget):
                self.apply_stylesheet(child)


    def send_message(self):
        message = self.input_text.text().strip()
        if message:
            self.input_text.clear()
            self.chat_output.append("<b>You:</b> " + message)
            response = self.get_response(message)
            self.chat_output.append("<b>ChatGPT:</b> " + response)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Message cannot be empty.")

    def get_response(self, message):
        openai.api_key = self.api_key

        prompt = f"Conversation with ChatGPT:\n{self.chat_history}<b>User:</b> {message}\n<b>ChatGPT:</b>"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        if response and response.choices and response.choices[0].text:
            self.chat_history += f"<b>User:</b> {message}\n<b>ChatGPT:</b> {response.choices[0].text}<br>"
            return response.choices[0].text
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid API key, please enter key into apikey.txt.")
            return ""

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationName("GPTChatter")

    # Read API key from apikey.txt
    with open('apikey.txt', 'r') as f:
        api_key = f.read().strip()

    # Check validity of API key
    openai.api_key = api_key
    try:
        openai.Engine.retrieve("text-davinci-002")
    except Exception as e:
        QtWidgets.QMessageBox.warning(None, "Error", "Invalid API key, please enter key into apikey.txt.")
        sys.exit()

    window = ConversationWindow(api_key=api_key)
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())