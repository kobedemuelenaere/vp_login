import csv
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QSizePolicy, QScrollArea, QCheckBox    
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import vp_bot
from functools import partial

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        with open('sites.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header
            for row in reader:
                name, path, website = row
                path_input = QLineEdit(path)
                website_input = QLineEdit(website)
                
                restart_driver_checkbox = QCheckBox("Restart Browser")
                
                run_button = QPushButton('Run')
                run_button.setStyleSheet("""
                    QPushButton {
                        background-color: green;
                        color: white;
                        border-radius: 10px;
                        font-weight: bold;
                    }
                    """)
                run_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                run_button.setFixedWidth(200)
                run_button.clicked.connect(partial(self.run, path_input, website_input, restart_driver_checkbox))

                
                name_label = QLabel(str(name))
                font = QFont()
                font.setBold(True)
                font.setUnderline(True)
                name_label.setFont(font)

                path_layout = QVBoxLayout()
                path_layout.addWidget(path_input)

                website_layout = QVBoxLayout()
                website_layout.addWidget(website_input)

                input_layout = QVBoxLayout()
                input_layout.addWidget(name_label)
                input_layout.addLayout(path_layout)
                input_layout.addLayout(website_layout)
                
                button_layout = QVBoxLayout()
                button_layout.addWidget(restart_driver_checkbox)
                button_layout.addWidget(run_button)
                hbox = QHBoxLayout()
                hbox.addLayout(input_layout)
                hbox.addLayout(button_layout)
                
                widget = QWidget()
                widget.setLayout(hbox)
                widget.setStyleSheet("""
                    QWidget {
                        border: 1px solid black;
                        padding: 20px;
                        border-radius: 10px;
                    }
                """)
                layout.addWidget(widget)
                layout.addSpacing(50)

            scroll = QScrollArea()  # Create a QScrollArea
            scroll.setWidgetResizable(True)  # Allow the scroll area to resize its contents

            widget = QWidget()  # Create a QWidget
            widget.setLayout(layout)  # Set the QVBoxLayout as the layout of the QWidget

            scroll.setWidget(widget)  # Set the QWidget as the widget of the QScrollArea

            self.setLayout(QVBoxLayout())
            self.layout().addWidget(scroll)  # Add the QScrollArea to the main layout of the window

            self.setWindowTitle('My App')
            self.setMinimumWidth(800)# Set a minimum width
            self.setMinimumHeight(600)# Set a minimum height
            self.show()

    def run(self, path_input, website_input, restart_driver):
        path = path_input.text().split(',')
        website = website_input.text()
        print(restart_driver.isChecked())
        try:
            vp_bot.access_site_loop(path, website, restart_driver.isChecked())
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Set the style to "Fusion"
    app.setStyleSheet("""
    QWidget {
        background-color: #ffffff;
        color: #000000;
    }
    QPushButton {
        background-color: #eeeeee;
    }
    QLineEdit {
        background-color: #dddddd;
    }
    """
    )
    ex = MyApp()
    sys.exit(app.exec_())
