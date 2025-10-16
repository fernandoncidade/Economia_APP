from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QSizePolicy
from .ui_17_history_container import HistoryContainer

def create_annuity_tab(self):
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, "Anuidades")

    self.annuity_calc_type = QComboBox()
    self.annuity_calc_type.addItems(["Calcular Prestação (A)", "Calcular Valor Presente (P)"])

    self.annuity_type = QComboBox()
    self.annuity_type.addItems(["Postecipada", "Antecipada"])

    self.annuity_p = QLineEdit()
    self.annuity_a = QLineEdit()
    self.annuity_i = QLineEdit()
    self.annuity_n = QLineEdit()

    self.annuity_result = HistoryContainer(self)
    self.annuity_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    calc_button = QPushButton("Calcular")
    calc_button.clicked.connect(self.calculate_annuity)

    layout.addRow(self.annuity_calc_type)
    layout.addRow("Tipo de Série:", self.annuity_type)
    layout.addRow("Valor Presente (P):", self.annuity_p)
    layout.addRow("Valor da Prestação (A):", self.annuity_a)
    layout.addRow("Taxa de Juros (i % ao período):", self.annuity_i)
    layout.addRow("Número de Períodos (n):", self.annuity_n)
    layout.addRow(calc_button)

    btn_widget = QWidget()
    btn_vlayout = QVBoxLayout(btn_widget)
    btn_vlayout.setContentsMargins(0, 0, 0, 0)

    top_row = QWidget()
    top_layout = QHBoxLayout(top_row)
    top_layout.setContentsMargins(0,0,0,0)
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
    btn_edit = QPushButton("Editar Cálculo")
    btn_delete = QPushButton("Excluir Seleção")
    btn_export = QPushButton("Exportar PDF")
    bottom_layout.addWidget(btn_edit)
    bottom_layout.addWidget(btn_delete)
    bottom_layout.addWidget(btn_export)
    btn_vlayout.addWidget(bottom_row)

    btn_export.clicked.connect(lambda: self.export_to_pdf(self.annuity_result, "anuidades.pdf"))
    btn_delete.clicked.connect(lambda: self.annuity_result.delete_selected())

    def toggle_edit_annuity():
        if self.annuity_result.is_editing():
            self.annuity_result.commit_edit()
            btn_edit.setText("Editar Cálculo")
            self.annuity_p.setFocus()

        else:
            ok = self.annuity_result.edit_selected()
            if ok:
                btn_edit.setText("Salvar Edição")

    btn_edit.clicked.connect(toggle_edit_annuity)
    layout.addRow(btn_widget)

    def clear_inputs():
        self.annuity_p.clear()
        self.annuity_a.clear()
        self.annuity_i.clear()
        self.annuity_n.clear()
        self.annuity_calc_type.setCurrentIndex(0)
        self.annuity_type.setCurrentIndex(0)

    def clear_output():
        self.annuity_result.clear()

    def clear_all():
        clear_inputs()
        clear_output()

    btn_clear_inputs.clicked.connect(clear_inputs)
    btn_clear_output.clicked.connect(clear_output)
    btn_clear_all.clicked.connect(clear_all)

    right_layout.addWidget(self.annuity_result)

    def toggle_fields():
        if self.annuity_calc_type.currentText() == "Calcular Prestação (A)":
            self.annuity_p.setEnabled(True)
            self.annuity_a.setEnabled(False)
            self.annuity_a.clear()

        else:
            self.annuity_p.setEnabled(False)
            self.annuity_a.setEnabled(True)
            self.annuity_p.clear()

    self.annuity_calc_type.currentIndexChanged.connect(toggle_fields)
    toggle_fields()
