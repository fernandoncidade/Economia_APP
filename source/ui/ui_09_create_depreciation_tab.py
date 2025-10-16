from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QSizePolicy
from PySide6.QtCore import Qt
from .ui_17_history_container import HistoryContainer

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
    self.deprec_result = HistoryContainer(self)

    calc_button = QPushButton("Calcular")
    calc_button.clicked.connect(self.calculate_depreciation)

    layout.addRow("Método de Depreciação:", self.deprec_method)
    layout.addRow("Valor de Aquisição do Ativo (P):", self.deprec_p)
    layout.addRow("Valor Residual Estimado (VRE):", self.deprec_vre)
    layout.addRow("Vida Útil (N anos):", self.deprec_n)
    layout.addRow("Analisar ano específico (k):", self.deprec_k)
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

    btn_export.clicked.connect(lambda: self.export_to_pdf(self.deprec_result, "depreciacao.pdf"))
    btn_delete.clicked.connect(lambda: self.deprec_result.delete_selected())
    def toggle_edit_deprec():
        if self.deprec_result.is_editing():
            self.deprec_result.commit_edit()
            btn_edit.setText("Editar Cálculo")

        else:
            ok = self.deprec_result.edit_selected()
            if ok:
                btn_edit.setText("Salvar Edição")

    btn_edit.clicked.connect(toggle_edit_deprec)
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
