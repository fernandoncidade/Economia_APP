from PySide6.QtWidgets import QTableWidgetItem

def set_amort_table_row(self, k, prestacao, juros, amortizacao, saldo_devedor):
    self.amort_table.setItem(k, 0, QTableWidgetItem(str(k)))
    self.amort_table.setItem(k, 1, QTableWidgetItem(f"{prestacao:.2f}"))
    self.amort_table.setItem(k, 2, QTableWidgetItem(f"{juros:.2f}"))
    self.amort_table.setItem(k, 3, QTableWidgetItem(f"{amortizacao:.2f}"))
    self.amort_table.setItem(k, 4, QTableWidgetItem(f"{abs(saldo_devedor):.2f}"))
