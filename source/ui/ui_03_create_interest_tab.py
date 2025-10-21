from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QSizePolicy
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_17_history_container import HistoryContainer

def create_interest_tab(self):
    tr = QCoreApplication.translate
    widget, layout, right_layout = self.create_layout()
    self.tabs.addTab(widget, tr("App", "Juros Simples e Compostos"))

    self.interest_calc_type = QComboBox()
    self.interest_calc_type.addItems([tr("App", "Calcular Montante (F)"), tr("App", "Calcular Principal (P)")])

    self.interest_regime = QComboBox()
    self.interest_regime.addItems([tr("App", "Juros Compostos"), tr("App", "Juros Simples")])

    self.interest_p = QLineEdit()
    self.interest_f = QLineEdit()
    self.interest_i = QLineEdit()
    self.interest_n = QLineEdit()
    
    self.interest_p.setValidator(QDoubleValidator())
    self.interest_f.setValidator(QDoubleValidator())
    self.interest_i.setValidator(QDoubleValidator())
    self.interest_n.setValidator(QDoubleValidator())

    self.interest_result = HistoryContainer(self)
    self.interest_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
    self.interest_result.setFont(fixed_font)

    calc_button = QPushButton(tr("App", "Calcular"))
    calc_button.clicked.connect(self.calculate_interest)

    layout.addRow(self.interest_calc_type)
    layout.addRow(self.interest_regime)
    layout.addRow(tr("App", "Valor Principal (P):"), self.interest_p)
    layout.addRow(tr("App", "Valor do Montante (F):"), self.interest_f)
    layout.addRow(tr("App", "Taxa de Juros (i % ao período):"), self.interest_i)
    layout.addRow(tr("App", "Número de Períodos (n):"), self.interest_n)
    layout.addRow(calc_button)

    btn_widget = QWidget()
    btn_vlayout = QVBoxLayout(btn_widget)
    btn_vlayout.setContentsMargins(0, 0, 0, 0)

    top_row = QWidget()
    top_layout = QHBoxLayout(top_row)
    top_layout.setContentsMargins(0, 0, 0, 0)
    btn_clear_inputs = QPushButton(tr("App", "Limpar Entrada"))
    btn_clear_output = QPushButton(tr("App", "Limpar Saída"))
    btn_clear_all = QPushButton(tr("App", "Limpar Tudo"))
    top_layout.addWidget(btn_clear_inputs)
    top_layout.addWidget(btn_clear_output)
    top_layout.addWidget(btn_clear_all)
    btn_vlayout.addWidget(top_row)

    bottom_row = QWidget()
    bottom_layout = QHBoxLayout(bottom_row)
    bottom_layout.setContentsMargins(0, 0, 0, 0)
    btn_edit = QPushButton(tr("App", "Editar Cálculo"))
    btn_delete = QPushButton(tr("App", "Excluir Seleção"))
    btn_export = QPushButton(tr("App", "Exportar PDF"))
    bottom_layout.addWidget(btn_edit)
    bottom_layout.addWidget(btn_delete)
    bottom_layout.addWidget(btn_export)
    btn_vlayout.addWidget(bottom_row)

    btn_export.clicked.connect(lambda: self.export_to_pdf(self.interest_result, "juros.pdf"))
    btn_delete.clicked.connect(lambda: self.interest_result.delete_selected())

    def toggle_edit():
        if self.interest_result.is_editing():
            self.interest_result.commit_edit()
            btn_edit.setText(tr("App", "Editar Cálculo"))
            self.interest_p.setFocus()

        else:
            ok = self.interest_result.edit_selected()
            if ok:
                btn_edit.setText(tr("App", "Salvar Edição"))

            else:
                pass

    btn_edit.clicked.connect(toggle_edit)

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
    btn_clear_all.clicked.connect(lambda: (clear_inputs(), clear_output()))

    right_layout.addWidget(self.interest_result)

    def toggle_fields():
        if self.interest_calc_type.currentText() == tr("App", "Calcular Montante (F)"):
            self.interest_p.setEnabled(True)
            self.interest_f.setEnabled(False)
            self.interest_f.clear()

        else:
            self.interest_p.setEnabled(False)
            self.interest_f.setEnabled(True)
            self.interest_p.clear()

    self.interest_calc_type.currentIndexChanged.connect(toggle_fields)
    toggle_fields()
