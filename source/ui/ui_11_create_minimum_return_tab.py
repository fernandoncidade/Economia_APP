from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QSizePolicy, QLabel
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication, Qt
from .ui_23_history_container import HistoryContainer
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_minimum_return_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "Retorno Mínimo (TMA)"))

        # Campos de entrada
        self.min_return_investment = QLineEdit()
        self.min_return_tma = QLineEdit()
        self.min_return_periods = QLineEdit()

        self.min_return_investment.setValidator(QDoubleValidator())
        self.min_return_tma.setValidator(QDoubleValidator())
        self.min_return_periods.setValidator(QDoubleValidator())

        # Área de resultado
        self.min_return_result = HistoryContainer(self)
        self.min_return_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.min_return_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular Retorno Mínimo"))
        calc_button.clicked.connect(self.calculate_minimum_return)

        # Botões de controle
        btn_widget = QWidget()
        btn_vlayout = QVBoxLayout(btn_widget)
        btn_vlayout.setContentsMargins(0, 0, 0, 0)

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        btn_clear_inputs = QPushButton(tr("App", "Limpar Entrada"))
        btn_clear_output = QPushButton(tr("App", "Limpar Saída"))
        btn_clear_all = QPushButton(tr("App", "Limpar Tudo"))
        top_layout.addWidget(btn_clear_inputs)
        top_layout.addWidget(btn_clear_output)
        top_layout.addWidget(btn_clear_all)
        btn_vlayout.addWidget(top_row)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        btn_edit = QPushButton(tr("App", "Editar Cálculo"))
        btn_delete = QPushButton(tr("App", "Excluir Seleção"))
        btn_export = QPushButton(tr("App", "Exportar PDF"))
        bottom_layout.addWidget(btn_edit)
        bottom_layout.addWidget(btn_delete)
        bottom_layout.addWidget(btn_export)
        btn_vlayout.addWidget(bottom_row)

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.min_return_result, "retorno_minimo_tma.pdf"))
        btn_delete.clicked.connect(lambda: self.min_return_result.delete_selected())

        def toggle_edit():
            if self.min_return_result.is_editing():
                self.min_return_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.min_return_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit)

        # Adicionar campos ao layout
        layout.addRow(QLabel(tr("App", "<b>Cálculo de Retorno Mínimo baseado em TMA</b>")))
        layout.addRow(tr("App", "Aporte (Investimento):"), self.min_return_investment)
        layout.addRow(tr("App", "TMA Anual (%):"), self.min_return_tma)
        layout.addRow(tr("App", "Períodos por Ano:"), self.min_return_periods)
        layout.addRow(calc_button)
        layout.addRow(btn_widget)

        def clear_inputs():
            self.min_return_investment.clear()
            self.min_return_tma.clear()
            self.min_return_periods.clear()

        def clear_output():
            self.min_return_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

        right_layout.addWidget(self.min_return_result)

    except Exception as e:
        logger.error(f"Erro ao criar aba de retorno mínimo: {e}", exc_info=True)
        raise
