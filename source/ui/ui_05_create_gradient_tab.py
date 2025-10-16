from PySide6.QtWidgets import QLineEdit, QPushButton, QComboBox, QTextEdit, QSizePolicy

def create_gradient_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Gradientes")

    self.grad_type = QComboBox()
    self.grad_type.addItems(["Gradiente Aritmético (G)", "Gradiente Geométrico (g)"])

    self.grad_p = QLineEdit()
    self.grad_g = QLineEdit()
    self.grad_i = QLineEdit()
    self.grad_n = QLineEdit()

    self.grad_result = QTextEdit()
    self.grad_result.setReadOnly(True)
    self.grad_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    calc_button = QPushButton("Calcular Valor Presente (P)")
    calc_button.clicked.connect(self.calculate_gradient)

    layout.addRow("Tipo de Gradiente:", self.grad_type)
    layout.addRow("Valor Presente (P):", self.grad_p)
    layout.addRow("Gradiente (G ou g %):", self.grad_g)
    layout.addRow("Taxa de Juros (i % ao período):", self.grad_i)
    layout.addRow("Número de Períodos (n):", self.grad_n)
    layout.addRow(calc_button)
    right_layout.addWidget(self.grad_result)
    self.grad_p.setEnabled(False)
