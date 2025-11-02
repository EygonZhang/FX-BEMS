
import sys
import os

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,QFormLayout, QFileDialog, QStackedWidget, QMessageBox,QGroupBox, QHBoxLayout, QRadioButton)

from bemt_solver import BEMT_Solver  
from llt_solver import LLT_Solver


class GeometryPage(QWidget):
    def __init__(self, stacked):
        super().__init__()
        self.stacked = stacked

        form = QFormLayout()
        self.R = QLineEdit("")
        self.Nb = QLineEdit("")
        self.r1 = QLineEdit("")
        self.N = QLineEdit("")
        self.rpm = QLineEdit("")

        form.addRow("Radius (m):", self.R)
        form.addRow("No. of Blades:", self.Nb)
        form.addRow("Radius at Root (m):", self.r1)
        form.addRow("No. of Blade Elements:", self.N)
        form.addRow("Rotations per Min (rpm):", self.rpm)

        next_btn = QPushButton("Next →")
        next_btn.clicked.connect(self.goto_next)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>Geometrical Properties</b>"))
        layout.addLayout(form)
        layout.addWidget(next_btn)
        self.setLayout(layout)

    def goto_next(self):
        data = {"R": float(self.R.text()),"Nb": int(self.Nb.text()), "r1": float(self.r1.text()), "N": int(self.N.text()), "rpm": float(self.rpm.text()) }
        self.stacked.geometry_data = data
        self.stacked.setCurrentIndex(1)



class SurroundingsPage(QWidget):
    def __init__(self, stacked):
        super().__init__()
        self.stacked = stacked

        form = QFormLayout()
        self.rho = QLineEdit("1025")
        self.mu = QLineEdit("0.0013155")
        self.U = QLineEdit("2")
        self.SOS = QLineEdit("1500")

        form.addRow("Density (kg/m³):", self.rho)
        form.addRow("Dynamic Viscosity (Pa·s):", self.mu)
        form.addRow("Inlet Velocity (m/s):", self.U)
        form.addRow("Speed of Sound (m/s):", self.SOS)
        
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        
        next_btn = QPushButton("Next →")
        next_btn.clicked.connect(self.goto_next)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>Surrounding Flow Conditions</b>"))
        layout.addLayout(form)
        layout.addWidget(back_btn)
        layout.addWidget(next_btn)
        self.setLayout(layout)

    def goto_next(self):
        data = {"rho": float(self.rho.text()),"mu": float(self.mu.text()), "U": float(self.U.text()),"SOS": float(self.SOS.text())}
        self.stacked.surround_data = data
        self.stacked.setCurrentIndex(2)



class GeneralSettingsPage(QWidget):
    def __init__(self, stacked):
        super().__init__()
        self.stacked = stacked

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>General Settings</b>"))

        
        self.tip_group = self.make_yes_no("Apply Tip Loss?")
        self.hub_group = self.make_yes_no("Apply Hub Loss?")
        self.linear_pitch = self.make_yes_no("Linear Twist Distribution?")
        self.linear_chord = self.make_yes_no("Linear Chord Distribution?")
        self.xfoil = self.make_yes_no("Use XFOIL?")
        self.c18 = self.make_yes_no("Use C18 Table?")
        self.airfoil075 = self.make_yes_no("Use 0.75R Airfoil Properties?")
        self.LLT = self.make_yes_no("Use LLT Solver?")

        for g in [self.tip_group, self.hub_group, self.linear_pitch, self.linear_chord, self.xfoil, self.c18, self.airfoil075, self.LLT]:
            layout.addWidget(g["box"])
            
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        layout.addWidget(back_btn)
        
        next_btn = QPushButton("Next →")
        next_btn.clicked.connect(self.goto_next)
        layout.addWidget(next_btn)

        self.setLayout(layout)

    def make_yes_no(self, label):
        box = QGroupBox(label)
        yes = QRadioButton("Yes")
        no = QRadioButton("No")
        no.setChecked(True)
        hbox = QHBoxLayout()
        hbox.addWidget(yes)
        hbox.addWidget(no)
        box.setLayout(hbox)
        return {"box": box, "yes": yes, "no": no}

    def goto_next(self):
        data = {"Tip_Loss": self.tip_group["yes"].isChecked(),"Hub_Loss": self.hub_group["yes"].isChecked(),"Linear_Pitch": self.linear_pitch["yes"].isChecked(),"Linear_Chord": self.linear_chord["yes"].isChecked(),"Xfoil": self.xfoil["yes"].isChecked(),"C18": self.c18["yes"].isChecked(),"Section": self.airfoil075["yes"].isChecked(),"LLT": self.LLT["yes"].isChecked()}
        self.stacked.settings_data = data
        self.stacked.setCurrentIndex(3)



class ResultsPage(QWidget):
    def __init__(self, stacked):
        super().__init__()
        self.stacked = stacked

        self.run_btn = QPushButton("Run BEMT Solver")
        self.run_btn.clicked.connect(self.run_solver)

        self.save_btn = QPushButton("Download Results")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.download_results)
        
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(2))
        
        
        self.figure, self.ax = plt.subplots(1, 2, figsize=(9, 4))
        self.canvas = FigureCanvas(self.figure)
        self.output_label = QLabel("")
        self.output_label.setStyleSheet("font-size: 14px; font-weight: bold; color: darkblue;")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<b>BEMT Output</b>"))
        layout.addWidget(self.run_btn)
        layout.addWidget(back_btn)
        layout.addWidget(self.canvas)
        layout.addWidget(self.output_label) 
        layout.addWidget(self.save_btn)
        self.setLayout(layout)
    
    def run_solver(self):
        try:
            geom = self.stacked.geometry_data
            env = self.stacked.surround_data
            sett = self.stacked.settings_data
            
            results = BEMT_Solver(
                geom["R"], geom["Nb"], geom["rpm"], geom["r1"], geom["N"], env["mu"], env["rho"], env["SOS"], env["U"], sett["Linear_Pitch"], sett["Linear_Chord"], sett["Tip_Loss"], sett["Hub_Loss"], sett["Xfoil"], sett["C18"], sett["Section"])
            
            if results is None:
             QMessageBox.critical(self, "Solver Error", "Solver returned no results.")
             return
            self.results = results
            
            if sett["LLT"]:
             LLT_results= LLT_Solver( geom["R"], geom["Nb"], geom["rpm"], geom["r1"], geom["N"], env["mu"], env["rho"], env["SOS"],env["U"], sett["Linear_Pitch"], sett["Linear_Chord"])
             self.LLT_results = LLT_results
            
            thrust = results.get("Thrust (kN)", None)
            torque = results.get("Torque (kNm)", None)
            power =  results.get("Power (kW)", None)
            
            if sett["LLT"]:
             LLT_thrust = LLT_results.get("Thrust (kN)", None)
             LLT_torque = LLT_results.get("Torque (kNm)", None)
             LLT_power =  LLT_results.get("Power (kW)", None)
            
            output_text = ""

            if thrust is not None and torque is not None:
                output_text += f"Main Solver →  Thrust: {thrust:.2f} kN | Torque: {torque:.2f} kNm | Power: {power:.2f} kW\n"
            else:
                output_text += "Main solver did not return thrust/torque.\n"

            if sett["LLT"]:
                output_text += f"LLT Solver  →  Thrust: {LLT_thrust:.2f} kN | Torque: {LLT_torque:.2f} kNm | Power: {LLT_power:.2f} kW"

            self.output_label.setText(output_text)
            
            
            self.ax[0].clear()
            self.ax[1].clear()

            if "radius_values" in results:
                r = results["radius_values"]
                if "dFn Normal Force (kN)" in results:
                    self.ax[0].plot(r, results["dFn Normal Force (kN)"], label="dFn Normal Force (kN)")
                if "dFt Tangential Force (kN)" in results:
                    self.ax[0].plot(r, results["dFt Tangential Force (kN)"], label="dFt Tangential Force (kN)")
                self.ax[0].set_title("Force Distribution")
                self.ax[0].set_xlabel("Radius (m)")
                self.ax[0].set_ylabel("Force (kN/m)")
                self.ax[0].legend()

                if "AOA_values (Degrees)" in results:
                    self.ax[1].plot(r, results["AOA_values (Degrees)"], label="AOA (deg)")
                self.ax[1].set_title("Angle of Attack")
                self.ax[1].set_xlabel("Radius (m)")
                self.ax[1].set_ylabel("Angle (°)")
                self.ax[1].legend()

            self.figure.tight_layout()
            self.canvas.draw()
            self.save_btn.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Solver failed:\n{e}")

    def download_results(self):
     folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
     if not folder:
        return

     sett = self.stacked.settings_data

     excel_path = os.path.join(folder, "BEMT_Results.xlsx")
     plot_path = os.path.join(folder, "BEMT_plots.png")

     with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
       
        df_main = pd.DataFrame({"Radius (m)": self.results["radius_values"]})
        exclude_keys = ["radius_values", "Power (kW)", "Thrust (kN)", "Torque (kNm)"]

        for key, val in self.results.items():
            if key not in exclude_keys:
                df_main[key] = val

        df_main.to_excel(writer, sheet_name="BEMT_Results", index=False)

        df_total = pd.DataFrame({"Thrust (kN)": [self.results.get("Thrust (kN)", None)],"Power (kW)": [self.results.get("Power (kW)", None)],"Torque (kNm)": [self.results.get("Torque (kNm)", None)]})
        df_total.to_excel(writer, sheet_name="Total BEMT Results", index=False)

    
        if sett["LLT"]:
            df_llt = pd.DataFrame({"Radius (m)": self.LLT_results["xi"]})
            exclude_keys = ["xi", "Power (kW)", "Thrust (kN)", "Torque (kNm)"]

            for key, val in self.LLT_results.items():
                if key not in exclude_keys:
                    df_llt[key] = val

            df_llt.to_excel(writer, sheet_name="LLT_Results", index=False)

       
            df_llttotal = pd.DataFrame({"Thrust (kN)": [self.LLT_results.get("Thrust (kN)", None)], "Power (kW)": [self.LLT_results.get("Power (kW)", None)], "Torque (kNm)": [self.LLT_results.get("Torque (kNm)", None)]})
            df_llttotal.to_excel(writer, sheet_name="Total LLT Results", index=False)

   
                

              
        self.figure.savefig(plot_path, dpi=300)
        excel_filename = os.path.basename(excel_path)
        plot_filename = os.path.basename(plot_path)



class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.geometry_data = {}
        self.surround_data = {}
        self.settings_data = {}

        self.page1 = GeometryPage(self)
        self.page2 = SurroundingsPage(self)
        self.page3 = GeneralSettingsPage(self)
        self.page4 = ResultsPage(self)

        self.addWidget(self.page1)
        self.addWidget(self.page2)
        self.addWidget(self.page3)
        self.addWidget(self.page4)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("BEMT Analysis GUI")
    window.resize(950, 600)
    window.show()
    sys.exit(app.exec())
