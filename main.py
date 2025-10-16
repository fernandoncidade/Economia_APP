import sys
from PySide6.QtWidgets import QApplication
from source import FinancialCalculatorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinancialCalculatorApp()
    window.show()
    sys.exit(app.exec())
