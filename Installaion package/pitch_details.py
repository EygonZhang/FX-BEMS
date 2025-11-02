
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sys

def get_pitch_inputs():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    
    class PitchInputWindow(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Linear Pitch Details, of the form a - b * r")
            self.resize(450, 300)
            self.layout = QVBoxLayout()

            self.layout.addWidget(QLabel("Enter a in Degrees:"))
            self.a_input = QLineEdit()
            self.layout.addWidget(self.a_input)

            self.layout.addWidget(QLabel("Enter b in Degrees/m:"))
            self.b_input = QLineEdit()
            self.layout.addWidget(self.b_input)

            self.submit_button = QPushButton("Submit")
            self.submit_button.clicked.connect(self.submit)
            self.layout.addWidget(self.submit_button)

            self.setLayout(self.layout)
            self.inputs = None

        def submit(self):
            try:
                a = float(self.a_input.text())
                b = float(self.b_input.text())
                self.inputs = {
                    "pitch_intercept": a,
                    "pitch_slope": b,
                }
                
                self.accept()
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", str(e))

    window = PitchInputWindow()


    window.exec()

  
    return window.inputs
