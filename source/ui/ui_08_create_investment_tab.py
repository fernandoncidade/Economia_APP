from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QSizePolicy
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_17_history_container import HistoryContainer
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_investment_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "Análise de Investimentos"))

        self.invest_initial = QLineEdit()
        self.invest_cashflow = QLineEdit()
        self.invest_n = QLineEdit()
        self.invest_tma = QLineEdit()

        self.invest_initial.setValidator(QDoubleValidator())
        self.invest_cashflow.setValidator(QDoubleValidator())
        self.invest_n.setValidator(QDoubleValidator())
        self.invest_tma.setValidator(QDoubleValidator())

        self.invest_result = HistoryContainer(self)
        self.invest_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.invest_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular VPL e VAUE"))
        calc_button.clicked.connect(self.calculate_investment)

        layout.addRow(tr("App", "Investimento Inicial:"), self.invest_initial)
        layout.addRow(tr("App", "Fluxo de Caixa Líquido Periódico (Benefícios - Custos):"), self.invest_cashflow)
        layout.addRow(tr("App", "Número de Períodos (n):"), self.invest_n)
        layout.addRow(tr("App", "Taxa Mínima de Atratividade (TMA %):"), self.invest_tma)
        layout.addRow(calc_button)

        btn_widget = QWidget()
        btn_vlayout = QVBoxLayout(btn_widget)
        btn_vlayout.setContentsMargins(0,0,0,0)

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0,0,0,0)
        btn_clear_inputs = QPushButton(tr("App", "Limpar Entrada"))
        btn_clear_output = QPushButton(tr("App", "Limpar Saída"))
        btn_clear_all = QPushButton(tr("App", "Limpar Tudo"))
        top_layout.addWidget(btn_clear_inputs)
        top_layout.addWidget(btn_clear_output)
        top_layout.addWidget(btn_clear_all)
        btn_vlayout.addWidget(top_row)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0,0,0,0)
        btn_edit = QPushButton(tr("App", "Editar Cálculo"))
        btn_delete = QPushButton(tr("App", "Excluir Seleção"))
        btn_export = QPushButton(tr("App", "Exportar PDF"))
        bottom_layout.addWidget(btn_edit)
        bottom_layout.addWidget(btn_delete)
        bottom_layout.addWidget(btn_export)
        btn_vlayout.addWidget(bottom_row)

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.invest_result, "investimento.pdf"))
        btn_delete.clicked.connect(lambda: self.invest_result.delete_selected())
        def toggle_edit_invest():
            if self.invest_result.is_editing():
                self.invest_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.invest_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit_invest)
        layout.addRow(btn_widget)

        def clear_inputs():
            self.invest_initial.clear()
            self.invest_cashflow.clear()
            self.invest_n.clear()
            self.invest_tma.clear()

        def clear_output():
            self.invest_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

        right_layout.addWidget(self.invest_result)

    except Exception as e:
        logger.error(f"Erro ao criar aba de investimento: {e}", exc_info=True)
        raise
