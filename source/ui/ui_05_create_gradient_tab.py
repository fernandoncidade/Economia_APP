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

        # Modo de cálculo
        self.grad_calc_mode = QComboBox()
        self.grad_calc_mode.addItems([
            tr("App", "Calcular Valor Presente (P)"),
            tr("App", "Calcular k-ésimo Termo (X_k)"),
            tr("App", "Renda Perpétua")
        ])

        self.grad_type = QComboBox()
        self.grad_type.addItems([tr("App", "Gradiente Aritmético (G)"), tr("App", "Gradiente Geométrico (g)")])

        self.grad_p = QLineEdit()
        self.grad_a = QLineEdit()
        self.grad_g = QLineEdit()
        self.grad_i = QLineEdit()
        self.grad_n = QLineEdit()
        self.grad_k = QLineEdit()

        self.grad_p.setValidator(QDoubleValidator())
        self.grad_a.setValidator(QDoubleValidator())
        self.grad_g.setValidator(QDoubleValidator())
        self.grad_i.setValidator(QDoubleValidator())
        self.grad_n.setValidator(QDoubleValidator())
        self.grad_k.setValidator(QDoubleValidator())

        self.grad_result = HistoryContainer(self)
        self.grad_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.grad_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular"))
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

        layout.addRow(tr("App", "Modo de Cálculo:"), self.grad_calc_mode)
        layout.addRow(tr("App", "Tipo de Gradiente:"), self.grad_type)
        layout.addRow(tr("App", "Valor Presente (P):"), self.grad_p)
        layout.addRow(tr("App", "Renda Periódica (A):"), self.grad_a)
        layout.addRow(tr("App", "Gradiente (G ou g %):"), self.grad_g)
        layout.addRow(tr("App", "Taxa de Juros (i % ao período):"), self.grad_i)
        layout.addRow(tr("App", "Número de Períodos (n):"), self.grad_n)
        layout.addRow(tr("App", "Termo desejado (k):"), self.grad_k)
        layout.addRow(calc_button)
        layout.addRow(btn_widget)
        right_layout.addWidget(self.grad_result)

        def toggle_fields():
            calc_mode = self.grad_calc_mode.currentIndex()
            is_geometric = self.grad_type.currentIndex() == 1

            # Renda Perpétua
            if calc_mode == 2:
                self.grad_p.setEnabled(False)
                self.grad_a.setEnabled(True)
                self.grad_g.setEnabled(False)
                self.grad_n.setEnabled(False)
                self.grad_k.setEnabled(False)
                self.grad_type.setEnabled(False)

            # Calcular X_k (só para geométrico)
            elif calc_mode == 1:
                self.grad_p.setEnabled(True)
                self.grad_a.setEnabled(False)
                self.grad_g.setEnabled(True)
                self.grad_n.setEnabled(True)
                self.grad_k.setEnabled(True)
                self.grad_type.setEnabled(True)

            # Calcular P
            else:
                self.grad_p.setEnabled(False)
                self.grad_a.setEnabled(False)
                self.grad_g.setEnabled(True)
                self.grad_n.setEnabled(True)
                self.grad_k.setEnabled(False)
                self.grad_type.setEnabled(True)

        self.grad_calc_mode.currentIndexChanged.connect(toggle_fields)
        self.grad_type.currentIndexChanged.connect(toggle_fields)
        toggle_fields()

        def clear_inputs():
            self.grad_p.clear()
            self.grad_a.clear()
            self.grad_g.clear()
            self.grad_i.clear()
            self.grad_n.clear()
            self.grad_k.clear()

        def clear_output():
            self.grad_result.clear()

        def clear_all():
            clear_inputs()
            clear_output()

        btn_clear_inputs.clicked.connect(clear_inputs)
        btn_clear_output.clicked.connect(clear_output)
        btn_clear_all.clicked.connect(clear_all)

    except Exception as e:
        logger.error(f"Erro ao criar aba de gradientes: {e}", exc_info=True)
        raise
