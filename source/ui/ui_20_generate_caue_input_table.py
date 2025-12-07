from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QCoreApplication, Qt
from .ui_02_get_float_from_line_edit import get_float_from_line_edit
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def generate_caue_input_table(self, *_):
    tr = QCoreApplication.translate
    try:
        if not self.caue_max_years.text().strip():
            self.caue_result.append(f"{tr('App', 'Erro')}: {tr('App', 'Por favor, informe o número máximo de anos.')}")
            return

        max_years = int(get_float_from_line_edit(self, self.caue_max_years))

        if max_years <= 0:
            self.caue_result.append(f"{tr('App', 'Erro')}: {tr('App', 'O número de anos deve ser maior que zero.')}")
            return

        self.caue_input_table.setRowCount(max_years)

        # Valores padrão do exercício (quando n=5)
        default_vr = [40000.0, 32000.0, 25000.0, 22000.0, 20000.0]
        default_com = [10000.0, 10500.0, 11000.0, 11500.0, 12000.0]

        def fmt_brl(v: float) -> str:
            return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        for n in range(1, max_years + 1):
            item_year = QTableWidgetItem(str(n))
            item_year.setFlags(item_year.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.caue_input_table.setItem(n-1, 0, item_year)

            if max_years == 5:
                vr_text = fmt_brl(default_vr[n-1])
                com_text = fmt_brl(default_com[n-1])

            else:
                vr_text = ""
                com_text = ""

            self.caue_input_table.setItem(n-1, 1, QTableWidgetItem(vr_text))
            self.caue_input_table.setItem(n-1, 2, QTableWidgetItem(com_text))

    except ValueError as ve:
        logger.error(f"Erro de valor ao gerar tabela de entrada CAUE: {ve}", exc_info=True)
        self.caue_result.append(f"{tr('App', 'Erro')}: {tr('App', 'Por favor, informe um número válido de anos.')}")

    except Exception as e:
        logger.error(f"Erro ao gerar tabela de entrada CAUE: {e}", exc_info=True)
        self.caue_result.append(f"{tr('App', 'Erro')}: {e}")
