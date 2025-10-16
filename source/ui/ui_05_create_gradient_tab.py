from PySide6.QtWidgets import QLineEdit, QPushButton, QComboBox, QSizePolicy, QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from .ui_17_history_container import HistoryContainer

def create_gradient_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Gradientes")

    self.grad_type = QComboBox()
    self.grad_type.addItems(["Gradiente Aritmético (G)", "Gradiente Geométrico (g)"])

    self.grad_p = QLineEdit()
    self.grad_g = QLineEdit()
    self.grad_i = QLineEdit()
    self.grad_n = QLineEdit()

    self.grad_result = HistoryContainer(self)
    self.grad_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    calc_button = QPushButton("Calcular Valor Presente (P)")
    calc_button.clicked.connect(self.calculate_gradient)

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

    btn_export.clicked.connect(lambda: self.export_to_pdf(self.grad_result, "gradiente.pdf"))
    btn_delete.clicked.connect(lambda: self.grad_result.delete_selected())

    def toggle_edit_grad():
        if self.grad_result.is_editing():
            self.grad_result.commit_edit()
            btn_edit.setText("Editar Cálculo")
            self.grad_p.setFocus()

        else:
            ok = self.grad_result.edit_selected()
            if ok:
                btn_edit.setText("Salvar Edição")

    btn_edit.clicked.connect(toggle_edit_grad)

    layout.addRow("Tipo de Gradiente:", self.grad_type)
    layout.addRow("Valor Presente (P):", self.grad_p)
    layout.addRow("Gradiente (G ou g %):", self.grad_g)
    layout.addRow("Taxa de Juros (i % ao período):", self.grad_i)
    layout.addRow("Número de Períodos (n):", self.grad_n)
    layout.addRow(calc_button)
    layout.addRow(btn_widget)
    right_layout.addWidget(self.grad_result)
    self.grad_p.setEnabled(False)
