from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy

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

    self.amort_result = QTextEdit()
    self.amort_result.setReadOnly(True)
    self.amort_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    layout.addRow("Sistema de Amortização:", self.amort_system)
    layout.addRow("Valor do Financiamento (P):", self.amort_p)
    layout.addRow("Taxa de Juros (i % ao período):", self.amort_i)
    layout.addRow("Prazo (n períodos):", self.amort_n)
    layout.addRow(calc_button)

    btn_widget = QWidget()
    btn_layout = QHBoxLayout(btn_widget)
    btn_layout.setContentsMargins(0, 0, 0, 0)
    btn_clear_inputs = QPushButton("Limpar Entrada")
    btn_clear_output = QPushButton("Limpar Saída")
    btn_clear_all = QPushButton("Limpar Tudo")
    btn_layout.addWidget(btn_clear_inputs)
    btn_layout.addWidget(btn_clear_output)
    btn_layout.addWidget(btn_clear_all)
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
