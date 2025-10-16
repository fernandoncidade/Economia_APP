from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QSizePolicy

def create_investment_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Análise de Investimentos")

    self.invest_initial = QLineEdit()
    self.invest_cashflow = QLineEdit()
    self.invest_n = QLineEdit()
    self.invest_tma = QLineEdit()

    self.invest_result = QTextEdit()
    self.invest_result.setReadOnly(True)
    self.invest_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    calc_button = QPushButton("Calcular VPL e VAUE")
    calc_button.clicked.connect(self.calculate_investment)

    layout.addRow("Investimento Inicial:", self.invest_initial)
    layout.addRow("Fluxo de Caixa Líquido Periódico (Benefícios - Custos):", self.invest_cashflow)
    layout.addRow("Número de Períodos (n):", self.invest_n)
    layout.addRow("Taxa Mínima de Atratividade (TMA %):", self.invest_tma)
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
