from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QTextEdit

def create_depreciation_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Depreciação")

    self.deprec_method = QComboBox()
    self.deprec_method.addItems(["Método Linear", "Método da Soma dos Dígitos dos Anos"])

    self.deprec_p = QLineEdit()
    self.deprec_vre = QLineEdit()
    self.deprec_n = QLineEdit()
    self.deprec_k = QLineEdit()

    self.deprec_k.setPlaceholderText("Opcional: para cálculo específico do ano k")
    self.deprec_result = QTextEdit()
    self.deprec_result.setReadOnly(True)

    calc_button = QPushButton("Calcular")
    calc_button.clicked.connect(self.calculate_depreciation)

    layout.addRow("Método de Depreciação:", self.deprec_method)
    layout.addRow("Valor de Aquisição do Ativo (P):", self.deprec_p)
    layout.addRow("Valor Residual Estimado (VRE):", self.deprec_vre)
    layout.addRow("Vida Útil (N anos):", self.deprec_n)
    layout.addRow("Analisar ano específico (k):", self.deprec_k)
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
        self.deprec_p.clear()
        self.deprec_vre.clear()
        self.deprec_n.clear()
        self.deprec_k.clear()

    def clear_output():
        self.deprec_result.clear()

    def clear_all():
        clear_inputs()
        clear_output()

    btn_clear_inputs.clicked.connect(clear_inputs)
    btn_clear_output.clicked.connect(clear_output)
    btn_clear_all.clicked.connect(clear_all)

    right_layout.addWidget(self.deprec_result)
