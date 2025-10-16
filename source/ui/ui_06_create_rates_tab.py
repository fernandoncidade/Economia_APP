from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QSizePolicy
from PySide6.QtCore import Qt

def create_rates_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Conversão de Taxas")

    layout.addRow(QLabel("<b>Equivalência de Taxas Efetivas</b>"))
    self.rate_equiv_i = QLineEdit()
    self.rate_equiv_current_n = QLineEdit("1")
    self.rate_equiv_target_n = QLineEdit("12")

    calc_equiv_button = QPushButton("Calcular Taxa Equivalente")
    calc_equiv_button.clicked.connect(self.calculate_rate_equivalence)

    self.rate_equiv_label = QLabel("<b>Resultado — Equivalência de Taxas</b>")
    self.rate_equiv_label.setAlignment(Qt.AlignLeft)
    self.rate_equiv_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    right_layout.addWidget(self.rate_equiv_label)

    self.rate_equiv_result = QTextEdit()
    self.rate_equiv_result.setReadOnly(True)
    self.rate_equiv_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.rate_equiv_result.setWordWrapMode(self.rate_equiv_result.wordWrapMode())

    layout.addRow("Taxa Atual (%):", self.rate_equiv_i)
    layout.addRow("Período da Taxa Atual (em unidades de tempo):", self.rate_equiv_current_n)
    layout.addRow("Período da Taxa Desejada (em unidades de tempo):", self.rate_equiv_target_n)
    layout.addRow(calc_equiv_button)

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
        self.rate_equiv_i.clear()
        self.rate_equiv_current_n.setText("1")
        self.rate_equiv_target_n.setText("12")
        self.rate_real_calc_type.setCurrentIndex(0)
        self.rate_real_r.clear()
        self.rate_real_i.clear()
        self.rate_real_inflation.clear()

    def clear_output():
        self.rate_equiv_result.clear()
        self.rate_real_result.clear()

    def clear_all():
        clear_inputs()
        clear_output()

    btn_clear_inputs.clicked.connect(clear_inputs)
    btn_clear_output.clicked.connect(clear_output)
    btn_clear_all.clicked.connect(clear_all)

    right_layout.addWidget(self.rate_equiv_result)

    layout.addRow(QLabel("<b>Taxa Real e Aparente (Inflação)</b>"))
    self.rate_real_calc_type = QComboBox()
    self.rate_real_calc_type.addItems(["Calcular Taxa Aparente (i)", "Calcular Taxa Real (r)"])
    self.rate_real_r = QLineEdit()
    self.rate_real_i = QLineEdit()
    self.rate_real_inflation = QLineEdit()

    calc_real_button = QPushButton("Calcular")
    calc_real_button.clicked.connect(self.calculate_real_rate)

    self.rate_real_label = QLabel("<b>Resultado — Taxa Real / Aparente</b>")
    self.rate_real_label.setAlignment(Qt.AlignLeft)
    self.rate_real_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
    right_layout.addWidget(self.rate_real_label)

    self.rate_real_result = QTextEdit()
    self.rate_real_result.setReadOnly(True)
    self.rate_real_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.rate_real_result.setWordWrapMode(self.rate_real_result.wordWrapMode())

    layout.addRow(self.rate_real_calc_type)
    layout.addRow("Taxa Real (r %):", self.rate_real_r)
    layout.addRow("Taxa Aparente (i %):", self.rate_real_i)
    layout.addRow("Taxa de Inflação (θ %):", self.rate_real_inflation)
    layout.addRow(calc_real_button)
    right_layout.addWidget(self.rate_real_result)
