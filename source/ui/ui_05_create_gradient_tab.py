from PySide6.QtWidgets import QLineEdit, QPushButton, QComboBox, QSizePolicy, QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_17_history_container import HistoryContainer
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_gradient_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "Gradientes"))

        self.grad_type = QComboBox()
        self.grad_type.addItems([tr("App", "Gradiente Aritmético (G)"), tr("App", "Gradiente Geométrico (g)")])

        self.grad_p = QLineEdit()
        self.grad_g = QLineEdit()
        self.grad_i = QLineEdit()
        self.grad_n = QLineEdit()

        self.grad_p.setValidator(QDoubleValidator())
        self.grad_g.setValidator(QDoubleValidator())
        self.grad_i.setValidator(QDoubleValidator())
        self.grad_n.setValidator(QDoubleValidator())

        self.grad_result = HistoryContainer(self)
        self.grad_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.grad_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular Valor Presente (P)"))
        calc_button.clicked.connect(self.calculate_gradient)

        btn_widget = QWidget()
        btn_vlayout = QVBoxLayout(btn_widget)
        btn_vlayout.setContentsMargins(0,0,0,0)

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0,0,0,0)
        btn_clear_inputs = QPushButton(tr("App", "Limpar Entrada"))
        btn_clear_output = QPushButton(tr("App", "Limpar Saída"))
        btn_clear_all = QPushButton(tr("App", "Limpar Tudo"))
        top_layout.addWidget(btn_clear_inputs)
        top_layout.addWidget(btn_clear_output)
        top_layout.addWidget(btn_clear_all)
        btn_vlayout.addWidget(top_row)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0,0,0,0)
        btn_edit = QPushButton(tr("App", "Editar Cálculo"))
        btn_delete = QPushButton(tr("App", "Excluir Seleção"))
        btn_export = QPushButton(tr("App", "Exportar PDF"))
        bottom_layout.addWidget(btn_edit)
        bottom_layout.addWidget(btn_delete)
        bottom_layout.addWidget(btn_export)
        btn_vlayout.addWidget(bottom_row)

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.grad_result, "gradiente.pdf"))
        btn_delete.clicked.connect(lambda: self.grad_result.delete_selected())

        def toggle_edit_grad():
            if self.grad_result.is_editing():
                self.grad_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))
                self.grad_p.setFocus()

            else:
                ok = self.grad_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

        btn_edit.clicked.connect(toggle_edit_grad)

        layout.addRow(tr("App", "Tipo de Gradiente:"), self.grad_type)
        layout.addRow(tr("App", "Valor Presente (P):"), self.grad_p)
        layout.addRow(tr("App", "Gradiente (G ou g %):"), self.grad_g)
        layout.addRow(tr("App", "Taxa de Juros (i % ao período):"), self.grad_i)
        layout.addRow(tr("App", "Número de Períodos (n):"), self.grad_n)
        layout.addRow(calc_button)
        layout.addRow(btn_widget)
        right_layout.addWidget(self.grad_result)
        self.grad_p.setEnabled(False)

    except Exception as e:
        logger.error(f"Erro ao criar aba de gradientes: {e}", exc_info=True)
        raise
