from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sys

def get_chord_inputs():
    app = QApplication.instance()  
    if not app:
        app = QApplication(sys.argv)

    class ChordInputWindow(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Linear Chord Details, of the form a - b * r")
            self.resize(450, 300)
            self.layout = QVBoxLayout()
            self.inputs = None 

            self.layout.addWidget(QLabel("Enter a in m:"))
            self.a_input = QLineEdit()
            self.layout.addWidget(self.a_input)

            self.layout.addWidget(QLabel("Enter b:"))
            self.b_input = QLineEdit()
            self.layout.addWidget(self.b_input)

            self.submit_button = QPushButton("Submit")
            self.submit_button.clicked.connect(self.submit)
            self.layout.addWidget(self.submit_button)

            self.setLayout(self.layout)

        def submit(self):
            try:
                a = float(self.a_input.text())
                b = float(self.b_input.text())
                self.inputs = {
                    "chord_intercept": a,
                    "chord_slope": b,
                }
                self.accept()
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", str(e))

    window = ChordInputWindow()
    window.exec() 
    return window.inputs
