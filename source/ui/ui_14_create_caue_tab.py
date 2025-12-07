from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, 
                                QSizePolicy, QLabel, QTableWidget, QHeaderView)
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_20_generate_caue_input_table import generate_caue_input_table
from .ui_23_history_container import HistoryContainer
from source.utils.LogManager import LogManager
from source.utils.TextFormat import to_html_subscripts

logger = LogManager.get_logger()

def create_caue_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "CAUE - Vida Econômica"))

        # Campos de entrada
        self.caue_initial_cost = QLineEdit()
        self.caue_tma = QLineEdit()
        self.caue_max_years = QLineEdit()

        self.caue_initial_cost.setValidator(QDoubleValidator())
        self.caue_tma.setValidator(QDoubleValidator())
        self.caue_max_years.setValidator(QDoubleValidator())

        # Valores padrão
        self.caue_initial_cost.setText("50000")
        self.caue_tma.setText("12")
        self.caue_max_years.setText("5")

        # Tabela de entrada de dados
        self.caue_input_table = QTableWidget()
        self.caue_input_table.setColumnCount(3)
        headers = [tr("App", "Ano (n)"), tr("App", "VR_n (R$)"), tr("App", "Com_n (R$)")]
        self.caue_input_table.setHorizontalHeaderLabels(headers)
        self.caue_input_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.caue_input_table.setMinimumHeight(200)

        # Tabela de saída (Resultados)
        self.caue_output_table = QTableWidget()
        self.caue_output_table.setColumnCount(4)
        out_headers = [
            tr("App", "Ano (n)"),
            tr("App", "VR_n (R$)"),
            tr("App", "Com_n (R$)"),
            tr("App", "CAUE_n (R$)"),
        ]
        self.caue_output_table.setHorizontalHeaderLabels(out_headers)
        self.caue_output_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.caue_output_table.setMinimumHeight(200)

        # Área de resultado
        self.caue_result = HistoryContainer(self)
        self.caue_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.caue_result.setFont(fixed_font)
        self.caue_result.setMinimumSize(0, 0)

        # Botões
        btn_generate_table = QPushButton(tr("App", "Gerar Tabela de Entrada"))
        btn_generate_table.clicked.connect(lambda: generate_caue_input_table(self))

        calc_button = QPushButton(tr("App", "Calcular CAUE e Vida Econômica"))
        calc_button.clicked.connect(self.calculate_caue)

        # Layout
        layout.addRow(QLabel(to_html_subscripts(tr("App", "<b>Dados do Ativo</b>"))))
        layout.addRow(tr("App", "Custo de Aquisição (P) R$:"), self.caue_initial_cost)
        layout.addRow(tr("App", "TMA (% ao ano):"), self.caue_tma)
        layout.addRow(tr("App", "Número Máximo de Anos:"), self.caue_max_years)
        layout.addRow(btn_generate_table)

        layout.addRow(QLabel(to_html_subscripts(tr("App", "<b>Valores de Revenda e Custos</b>"))))
        layout.addRow(self.caue_input_table)

        layout.addRow(QLabel(to_html_subscripts(tr("App", "<b>Tabela de Resultados (CAUE)</b>"))))

        layout.addRow(calc_button)

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

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.caue_result, "caue_vida_economica.pdf"))
        btn_delete.clicked.connect(lambda: self.caue_result.delete_selected())

        def toggle_edit():
            if self.caue_result.is_editing():
                self.caue_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.caue_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit)

        def clear_inputs():
            self.caue_initial_cost.clear()
            self.caue_tma.clear()
            self.caue_max_years.setText("5")
            self.caue_input_table.clearContents()
            self.caue_input_table.setRowCount(0)
            self.caue_output_table.clearContents()
            self.caue_output_table.setRowCount(0)

        def clear_output():
            self.caue_result.clear()
            self.caue_output_table.clearContents()
            self.caue_output_table.setRowCount(0)

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

        layout.addRow(btn_widget)
        right_layout.addWidget(self.caue_result)

    except Exception as e:
        logger.error(f"Erro ao criar aba CAUE: {e}", exc_info=True)
        raise
