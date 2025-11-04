from PySide6.QtWidgets import QTableWidgetItem
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def set_amort_table_row(self, k, prestacao, juros, amortizacao, saldo_devedor):
    try:
        self.amort_table.setItem(k, 0, QTableWidgetItem(str(k)))
        self.amort_table.setItem(k, 1, QTableWidgetItem(f"{prestacao:.2f}"))
        self.amort_table.setItem(k, 2, QTableWidgetItem(f"{juros:.2f}"))
        self.amort_table.setItem(k, 3, QTableWidgetItem(f"{amortizacao:.2f}"))
        self.amort_table.setItem(k, 4, QTableWidgetItem(f"{abs(saldo_devedor):.2f}"))

    except Exception as e:
        logger.error(f"Erro ao definir linha da tabela de amortização: {e}", exc_info=True)
        raise
