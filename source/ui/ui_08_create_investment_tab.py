from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QSizePolicy
from PySide6.QtCore import Qt
from .ui_17_history_container import HistoryContainer

def create_investment_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Análise de Investimentos")

    self.invest_initial = QLineEdit()
    self.invest_cashflow = QLineEdit()
    self.invest_n = QLineEdit()
    self.invest_tma = QLineEdit()

    self.invest_result = HistoryContainer(self)
    self.invest_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    calc_button = QPushButton("Calcular VPL e VAUE")
    calc_button.clicked.connect(self.calculate_investment)

    layout.addRow("Investimento Inicial:", self.invest_initial)
    layout.addRow("Fluxo de Caixa Líquido Periódico (Benefícios - Custos):", self.invest_cashflow)
    layout.addRow("Número de Períodos (n):", self.invest_n)
    layout.addRow("Taxa Mínima de Atratividade (TMA %):", self.invest_tma)
    layout.addRow(calc_button)

    btn_widget = QWidget()
    btn_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    btn_vlayout = QVBoxLayout(btn_widget)
    btn_vlayout.setContentsMargins(0,0,0,0)
    btn_vlayout.setAlignment(Qt.AlignLeft)

    top_row = QWidget()
    top_layout = QHBoxLayout(top_row)
    top_layout.setContentsMargins(0,0,0,0)
    top_layout.setAlignment(Qt.AlignLeft)
    top_layout.setSpacing(6)
    btn_clear_inputs = QPushButton("Limpar Entrada")
    btn_clear_output = QPushButton("Limpar Saída")
    btn_clear_all = QPushButton("Limpar Tudo")
    top_layout.addWidget(btn_clear_inputs)
    top_layout.addWidget(btn_clear_output)
    top_layout.addWidget(btn_clear_all)
    btn_vlayout.addWidget(top_row)

    bottom_row = QWidget()
    bottom_layout = QHBoxLayout(bottom_row)
    bottom_layout.setContentsMargins(0,0,0,0)
    bottom_layout.setAlignment(Qt.AlignLeft)
    bottom_layout.setSpacing(6)
    btn_edit = QPushButton("Editar Cálculo")
    btn_delete = QPushButton("Excluir Seleção")
    btn_export = QPushButton("Exportar PDF")
    bottom_layout.addWidget(btn_edit)
    bottom_layout.addWidget(btn_delete)
    bottom_layout.addWidget(btn_export)
    btn_vlayout.addWidget(bottom_row)

    btn_export.clicked.connect(lambda: self.export_to_pdf(self.invest_result, "investimento.pdf"))
    btn_delete.clicked.connect(lambda: self.invest_result.delete_selected())
    def toggle_edit_invest():
        if self.invest_result.is_editing():
            self.invest_result.commit_edit()
            btn_edit.setText("Editar Cálculo")

        else:
            ok = self.invest_result.edit_selected()
            if ok:
                btn_edit.setText("Salvar Edição")

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
