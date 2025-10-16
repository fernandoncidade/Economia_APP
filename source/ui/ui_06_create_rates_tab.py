from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSizePolicy
from PySide6.QtCore import Qt
from .ui_17_history_container import HistoryContainer

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

    self.rate_equiv_result = HistoryContainer(self)
    self.rate_equiv_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    layout.addRow("Taxa Atual (%):", self.rate_equiv_i)
    layout.addRow("Período da Taxa Atual (em unidades de tempo):", self.rate_equiv_current_n)
    layout.addRow("Período da Taxa Desejada (em unidades de tempo):", self.rate_equiv_target_n)
    layout.addRow(calc_equiv_button)

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
    btn_edit_equiv = QPushButton("Editar Cálculo")
    btn_delete_equiv = QPushButton("Excluir Seleção")
    btn_export_equiv = QPushButton("Exportar PDF")
    bottom_layout.addWidget(btn_edit_equiv)
    bottom_layout.addWidget(btn_delete_equiv)
    bottom_layout.addWidget(btn_export_equiv)
    btn_vlayout.addWidget(bottom_row)

    btn_export_equiv.clicked.connect(lambda: self.export_to_pdf(self.rate_equiv_result, "equivalencia_taxa.pdf"))
    btn_delete_equiv.clicked.connect(lambda: self.rate_equiv_result.delete_selected())
    def toggle_edit_equiv():
        if self.rate_equiv_result.is_editing():
            self.rate_equiv_result.commit_edit()
            btn_edit_equiv.setText("Editar Cálculo")

        else:
            ok = self.rate_equiv_result.edit_selected()
            if ok:
                btn_edit_equiv.setText("Salvar Edição")

    btn_edit_equiv.clicked.connect(toggle_edit_equiv)
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

    self.rate_real_result = HistoryContainer(self)
    self.rate_real_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    layout.addRow(self.rate_real_calc_type)
    layout.addRow("Taxa Real (r %):", self.rate_real_r)
    layout.addRow("Taxa Aparente (i %):", self.rate_real_i)
    layout.addRow("Taxa de Inflação (θ %):", self.rate_real_inflation)
    layout.addRow(calc_real_button)

    btn_widget_real = QWidget()
    btn_widget_real.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    btn_vlayout_real = QVBoxLayout(btn_widget_real)
    btn_vlayout_real.setContentsMargins(0,0,0,0)
    btn_vlayout_real.setAlignment(Qt.AlignLeft)

    top_row_r = QWidget()
    top_layout_r = QHBoxLayout(top_row_r)
    top_layout_r.setContentsMargins(0,0,0,0)
    top_layout_r.setAlignment(Qt.AlignLeft)
    top_layout_r.setSpacing(6)
    btn_clear_inputs_r = QPushButton("Limpar Entrada")
    btn_clear_output_r = QPushButton("Limpar Saída")
    btn_clear_all_r = QPushButton("Limpar Tudo")
    top_layout_r.addWidget(btn_clear_inputs_r)
    top_layout_r.addWidget(btn_clear_output_r)
    top_layout_r.addWidget(btn_clear_all_r)
    btn_vlayout_real.addWidget(top_row_r)

    bottom_row_r = QWidget()
    bottom_layout_r = QHBoxLayout(bottom_row_r)
    bottom_layout_r.setContentsMargins(0,0,0,0)
    bottom_layout_r.setAlignment(Qt.AlignLeft)
    bottom_layout_r.setSpacing(6)
    btn_edit_real = QPushButton("Editar Cálculo")
    btn_delete_real = QPushButton("Excluir Seleção")
    btn_export_real = QPushButton("Exportar PDF")
    bottom_layout_r.addWidget(btn_edit_real)
    bottom_layout_r.addWidget(btn_delete_real)
    bottom_layout_r.addWidget(btn_export_real)
    btn_vlayout_real.addWidget(bottom_row_r)

    btn_export_real.clicked.connect(lambda: self.export_to_pdf(self.rate_real_result, "taxa_real_aparente.pdf"))
    btn_delete_real.clicked.connect(lambda: self.rate_real_result.delete_selected())
    def toggle_edit_real():
        if self.rate_real_result.is_editing():
            self.rate_real_result.commit_edit()
            btn_edit_real.setText("Editar Cálculo")

        else:
            ok = self.rate_real_result.edit_selected()
            if ok:
                btn_edit_real.setText("Salvar Edição")

    btn_edit_real.clicked.connect(toggle_edit_real)

    layout.addRow(btn_widget_real)
    right_layout.addWidget(self.rate_real_result)
