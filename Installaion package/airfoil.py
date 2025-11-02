from PySide6.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
import sys

def get_xfoil_inputs():
    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    class XfoilInputWindow(QDialog):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Xfoil Input Parameters")
            self.layout = QVBoxLayout()
            self.inputs = None 
            
            self.layout.addWidget(QLabel("Enter Xfoil Path"))
            self.xfoilpath= QLineEdit()
            self.layout.addWidget(self.xfoilpath)
            
            # AOA Inputs
            self.layout.addWidget(QLabel("Enter Initial AOA (degrees):"))
            self.aoa_initial_input = QLineEdit()
            self.layout.addWidget(self.aoa_initial_input)

            self.layout.addWidget(QLabel("Enter Final AOA (degrees):"))
            self.aoa_final_input = QLineEdit()
            self.layout.addWidget(self.aoa_final_input)

            # Airfoil Type Selector
            self.layout.addWidget(QLabel("Select Airfoil Type:"))
            self.airfoil_type_combo = QComboBox()
            self.airfoil_type_combo.addItems(["NACA", "Custom"])
            self.layout.addWidget(self.airfoil_type_combo)

            # Airfoil Detail Input
            self.airfoil_label = QLabel("Enter NACA Series Number (e.g. 0012):")
            self.airfoil_input = QLineEdit()
            self.layout.addWidget(self.airfoil_label)
            self.layout.addWidget(self.airfoil_input)

            self.airfoil_type_combo.currentTextChanged.connect(self.update_airfoil_prompt)

            self.submit_button = QPushButton("Submit")
            self.submit_button.clicked.connect(self.submit)
            self.layout.addWidget(self.submit_button)

            self.setLayout(self.layout)

        def update_airfoil_prompt(self, text):
            if text == "NACA":
                self.airfoil_label.setText("Enter NACA Series Number (e.g. 0012):")
                self.airfoil_input.setPlaceholderText("0012")
            else:
                self.airfoil_label.setText("Enter Coordinate File Name (e.g. airfoil.txt):")
                self.airfoil_input.setPlaceholderText("airfoil.txt")
                self.airfoil_input.clear()

        def submit(self):
            try:
                aoa_initial = float(self.aoa_initial_input.text())
                aoa_final = float(self.aoa_final_input.text())
                airfoil_type = self.airfoil_type_combo.currentText()
                airfoil_value = self.airfoil_input.text().strip()
                xfoil_path = self.xfoilpath.text().strip().strip('"')
                
                if not airfoil_value:
                    raise ValueError("Please provide airfoil details.")

                self.inputs = {
                    "aoa_initial": aoa_initial,
                    "aoa_final": aoa_final,
                    "airfoil_type": airfoil_type,
                    "airfoil_value": airfoil_value,
                    "xfoil_path": xfoil_path
                }
                self.accept() 
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", str(e))

    window = XfoilInputWindow()
    window.exec() 
    return window.inputs
