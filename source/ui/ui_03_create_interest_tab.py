from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QTextEdit, QSizePolicy
from PySide6.QtGui import QDoubleValidator

def create_interest_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Juros Simples e Compostos")

    self.interest_calc_type = QComboBox()
    self.interest_calc_type.addItems(["Calcular Montante (F)", "Calcular Principal (P)"])

    self.interest_regime = QComboBox()
    self.interest_regime.addItems(["Juros Compostos", "Juros Simples"])

    self.interest_p = QLineEdit()
    self.interest_f = QLineEdit()
    self.interest_i = QLineEdit()
    self.interest_n = QLineEdit()
    
    self.interest_p.setValidator(QDoubleValidator())
    self.interest_f.setValidator(QDoubleValidator())
    self.interest_i.setValidator(QDoubleValidator())
    self.interest_n.setValidator(QDoubleValidator())

    self.interest_result = QTextEdit()
    self.interest_result.setReadOnly(True)
    self.interest_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    calc_button = QPushButton("Calcular")
    calc_button.clicked.connect(self.calculate_interest)

    layout.addRow(self.interest_calc_type)
    layout.addRow(self.interest_regime)
    layout.addRow("Valor Principal (P):", self.interest_p)
    layout.addRow("Valor do Montante (F):", self.interest_f)
    layout.addRow("Taxa de Juros (i % ao período):", self.interest_i)
    layout.addRow("Número de Períodos (n):", self.interest_n)
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
        self.interest_p.clear()
        self.interest_f.clear()
        self.interest_i.clear()
        self.interest_n.clear()
        self.interest_calc_type.setCurrentIndex(0)
        self.interest_regime.setCurrentIndex(0)

    def clear_output():
        self.interest_result.clear()

    def clear_all():
        clear_inputs()
        clear_output()

    btn_clear_inputs.clicked.connect(clear_inputs)
    btn_clear_output.clicked.connect(clear_output)
    btn_clear_all.clicked.connect(clear_all)

    right_layout.addWidget(self.interest_result)

    def toggle_fields():
        if self.interest_calc_type.currentText() == "Calcular Montante (F)":
            self.interest_p.setEnabled(True)
            self.interest_f.setEnabled(False)
            self.interest_f.clear()

        else:
            self.interest_p.setEnabled(False)
            self.interest_f.setEnabled(True)
            self.interest_p.clear()

    self.interest_calc_type.currentIndexChanged.connect(toggle_fields)
    toggle_fields()
