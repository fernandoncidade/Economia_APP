from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
from PySide6.QtCore import Qt
from .ui_17_history_container import HistoryContainer

def create_amortization_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Amortização")

    self.amort_system = QComboBox()
    self.amort_system.addItems(["Sistema Francês (Price)", "Sistema de Amortização Constante (SAC)", "Sistema de Amortização Misto (SAM)"])

    self.amort_p = QLineEdit()
    self.amort_i = QLineEdit()
    self.amort_n = QLineEdit()

    calc_button = QPushButton("Gerar Tabela de Amortização")
    calc_button.clicked.connect(self.calculate_amortization)

    self.amort_table = QTableWidget()
    self.amort_table.setColumnCount(5)
    self.amort_table.setHorizontalHeaderLabels(["Período (k)", "Prestação", "Juros", "Amortização", "Saldo Devedor"])
    self.amort_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    self.amort_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    self.amort_result = HistoryContainer(self)
    self.amort_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    layout.addRow("Sistema de Amortização:", self.amort_system)
    layout.addRow("Valor do Financiamento (P):", self.amort_p)
    layout.addRow("Taxa de Juros (i % ao período):", self.amort_i)
    layout.addRow("Prazo (n períodos):", self.amort_n)
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

    btn_export.clicked.connect(lambda: self.export_amortization_pdf("amortizacao.pdf"))
    btn_delete.clicked.connect(lambda: self.amort_result.delete_selected())
    def toggle_edit_amort():
        if self.amort_result.is_editing():
            self.amort_result.commit_edit()
            btn_edit.setText("Editar Cálculo")

        else:
            ok = self.amort_result.edit_selected()
            if ok:
                btn_edit.setText("Salvar Edição")

    btn_edit.clicked.connect(toggle_edit_amort)

    layout.addRow(btn_widget)

    def clear_inputs():
        self.amort_p.clear()
        self.amort_i.clear()
        self.amort_n.clear()
        self.amort_system.setCurrentIndex(0)

    def clear_output():
        self.amort_table.clearContents()
        self.amort_table.setRowCount(1)
        for c in range(self.amort_table.columnCount()):
            self.amort_table.setItem(0, c, QTableWidgetItem(""))

        self.amort_result.clear()

    def clear_all():
        clear_inputs()
        clear_output()

    btn_clear_inputs.clicked.connect(clear_inputs)
    btn_clear_output.clicked.connect(clear_output)
    btn_clear_all.clicked.connect(clear_all)

    right_layout.addWidget(self.amort_result)
    right_layout.addWidget(self.amort_table)
