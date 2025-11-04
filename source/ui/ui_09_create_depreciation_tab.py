from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QSizePolicy
from PySide6.QtGui import QDoubleValidator, QFontDatabase
from PySide6.QtCore import QCoreApplication
from .ui_17_history_container import HistoryContainer
from utils.LogManager import LogManager

logger = LogManager.get_logger()

def create_depreciation_tab(self):
    tr = QCoreApplication.translate
    try:
        widget, layout, right_layout = self.create_layout()
        self.tabs.addTab(widget, tr("App", "Depreciação"))

        self.deprec_method = QComboBox()
        self.deprec_method.addItems([tr("App", "Método Linear"), tr("App", "Método da Soma dos Dígitos dos Anos")])

        self.deprec_p = QLineEdit()
        self.deprec_vre = QLineEdit()
        self.deprec_n = QLineEdit()
        self.deprec_k = QLineEdit()

        self.deprec_p.setValidator(QDoubleValidator())
        self.deprec_vre.setValidator(QDoubleValidator())
        self.deprec_n.setValidator(QDoubleValidator())
        self.deprec_k.setValidator(QDoubleValidator())

        self.deprec_k.setPlaceholderText(tr("App", "Opcional: para cálculo específico do ano k"))
        self.deprec_result = HistoryContainer(self)
        self.deprec_result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.deprec_result.setFont(fixed_font)

        calc_button = QPushButton(tr("App", "Calcular"))
        calc_button.clicked.connect(self.calculate_depreciation)

        layout.addRow(tr("App", "Método de Depreciação:"), self.deprec_method)
        layout.addRow(tr("App", "Valor de Aquisição do Ativo (P):"), self.deprec_p)
        layout.addRow(tr("App", "Valor Residual Estimado (VRE):"), self.deprec_vre)
        layout.addRow(tr("App", "Vida Útil (N anos):"), self.deprec_n)
        layout.addRow(tr("App", "Analisar ano específico (k):"), self.deprec_k)
        layout.addRow(calc_button)

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

        btn_export.clicked.connect(lambda: self.export_to_pdf(self.deprec_result, "depreciacao.pdf"))
        btn_delete.clicked.connect(lambda: self.deprec_result.delete_selected())
        def toggle_edit_deprec():
            if self.deprec_result.is_editing():
                self.deprec_result.commit_edit()
                btn_edit.setText(tr("App", "Editar Cálculo"))

            else:
                ok = self.deprec_result.edit_selected()
                if ok:
                    btn_edit.setText(tr("App", "Salvar Edição"))

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

    except Exception as e:
        logger.error(f"Erro ao criar aba de depreciação: {e}", exc_info=True)
        raise
